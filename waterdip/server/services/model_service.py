#  Copyright 2022-present, the Waterdip Labs Pvt. Ltd.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import uuid
from datetime import datetime
from typing import Dict, List, Optional, Union

from waterdip.server.apis.models.params import RequestPagination, RequestSort
from waterdip.server.db.models.datasets import DatasetDB

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

from uuid import UUID

from fastapi import Depends

from waterdip.server.apis.models.models import (
    ModelListRow,
    ModelOverviewAlerts,
    ModelOverviewPredictions,
    ModelOverviewResponse,
    ModelPredictionHistogram,
    ModelVersionSchema,
)
from waterdip.server.db.models.models import (
    BaseModelDB,
    BaseModelVersionDB,
    ModelDB,
    ModelVersionDB,
    ModelVersionSchemaFieldDetails,
    ModelVersionSchemaInDB,
)
from waterdip.server.db.repositories.model_repository import (
    ModelRepository,
    ModelVersionRepository,
)
from waterdip.server.errors.base_errors import EntityNotFoundError
from waterdip.server.services.alert_service import AlertService
from waterdip.server.services.dataset_service import DatasetService, ServiceEventDataset
from waterdip.server.services.row_service import EventDatasetRowService


class ModelVersionService:
    _INSTANCE: "ModelVersionService" = None

    @classmethod
    def get_instance(
        cls,
        repository: ModelVersionRepository = Depends(
            ModelVersionRepository.get_instance
        ),
        dataset_service: DatasetService = Depends(DatasetService.get_instance),
    ):
        if not cls._INSTANCE:
            cls._INSTANCE = cls(repository=repository, dataset_service=dataset_service)
        return cls._INSTANCE

    def __init__(
        self, repository: ModelVersionRepository, dataset_service: DatasetService
    ):
        self._repository = repository
        self._dataset_service = dataset_service

    def find_by_id(self, model_version_id: uuid.UUID) -> Optional[ModelVersionDB]:
        found_model_version = self._repository.find_by_id(
            model_version_id=model_version_id
        )

        if not found_model_version:
            raise EntityNotFoundError(name=str(model_version_id), type="Model Version")

        return found_model_version

    def get_all_datasets(self, model_version_id: uuid.UUID) -> List[DatasetDB]:
        list_dataset: tuple[List[DatasetDB], int] = self._dataset_service.list_dataset(
            model_version_id=model_version_id
        )
        return list_dataset[0]

    @staticmethod
    def _schema_conversion(
        version_schema: ModelVersionSchema,
        schema_type: Literal["features", "predictions"] = "features",
    ):
        """
        Converts API provided model schema to DB compatible data structure.
        In case of predictions, it generates index value for the prediction column.
        This index value would be useful for linking prediction value and prediction score in different list
        """
        schema, index = {}, 0
        schema_value_dict = (
            version_schema.features
            if schema_type == "features"
            else version_schema.predictions
        )
        for k, v in schema_value_dict.items():
            if schema_type == "features":
                schema[k] = ModelVersionSchemaFieldDetails(data_type=v.value)
            elif schema_type == "predictions":
                schema[k] = ModelVersionSchemaFieldDetails(
                    data_type=v.value, list_index=index
                )
                index = index + 1
        return schema

    def register_model_version(
        self,
        model_id: uuid.UUID,
        model_version: str,
        version_schema: ModelVersionSchema,
    ) -> ModelVersionDB:

        model_version_id, serving_dataset_id = uuid.uuid4(), uuid.uuid4()

        event_dataset = ServiceEventDataset(
            dataset_id=serving_dataset_id,
            dataset_name=f"{model_version}_serving",
            created_at=datetime.utcnow(),
            model_id=model_id,
            model_version_id=model_version_id,
            environment="PRODUCTION",
        )

        model_version_db = BaseModelVersionDB(
            model_id=model_id,
            model_version_id=model_version_id,
            model_version=model_version,
            created_at=datetime.utcnow(),
            version_schema=ModelVersionSchemaInDB(
                features=self._schema_conversion(version_schema, "features"),
                predictions=self._schema_conversion(version_schema, "predictions"),
            ),
        )
        model_version = self._repository.register_model_version(model_version_db)
        self._dataset_service.create_event_dataset(event_dataset)

        return model_version

    def agg_model_versions_per_model(
        self, model_ids: List[str]
    ) -> Dict[str, List[str]]:
        return self._repository.agg_model_versions_per_model(
            model_ids=model_ids, top_n=1
        )

    def find_all_versions_for_model(self, model_id: UUID) -> List[ModelVersionDB]:
        """
        Returns all associated model versions of the provided model

        Parameters:
            model_id(UUID): model unique ID

        Returns:
            List[ModelVersionDB]: list of all model versions associated with the model ID
        """
        filters = {"model_id": str(model_id)}
        return self._repository.find_versions(version_filters=filters)


class ModelService:
    _INSTANCE: "ModelService" = None

    @classmethod
    def get_instance(
        cls,
        repository: ModelRepository = Depends(ModelRepository.get_instance),
        model_version_service: ModelVersionService = Depends(
            ModelVersionService.get_instance
        ),
        row_service: EventDatasetRowService = Depends(
            EventDatasetRowService.get_instance
        ),
        alert_service: AlertService = Depends(AlertService.get_instance),
    ):
        if not cls._INSTANCE:
            cls._INSTANCE = cls(
                repository=repository,
                model_version_service=model_version_service,
                row_service=row_service,
                alert_service=alert_service,
            )
        return cls._INSTANCE

    def __init__(
        self,
        repository: ModelRepository,
        model_version_service: ModelVersionService,
        row_service: EventDatasetRowService,
        alert_service: AlertService,
    ):
        self._repository = repository
        self._model_version_service = model_version_service
        self._row_service = row_service
        self._alert_service = alert_service

    def register_model(
        self, model_name: str, model_id: Optional[UUID] = None
    ) -> ModelDB:
        generated_model_id = uuid.uuid4() if model_id is None else model_id
        model_db = BaseModelDB(
            model_id=generated_model_id,
            model_name=model_name,
            created_at=datetime.utcnow(),
        )

        return self._repository.register_model(model_db)

    def find_by_id(self, model_id: uuid.UUID) -> Optional[ModelDB]:
        found_model = self._repository.find_by_id(model_id=model_id)

        if not found_model:
            raise EntityNotFoundError(name=str(model_id), type="Model")

        return found_model

    def list_models(
        self,
        sort_request: Optional[RequestSort] = None,
        pagination: Optional[RequestPagination] = None,
        get_all_versions_flag: Optional[bool] = False,
    ) -> List[ModelListRow]:
        list_models: [ModelDB] = self._repository.find_models(
            filters={},
            sort=[(sort_request.get_sort_field, sort_request.get_sort_order)]
            if sort_request and sort_request.sort
            else [("created_at", -1)],
            skip=(pagination.page - 1) * pagination.limit if pagination else 0,
            limit=pagination.limit if pagination else 10,
        )

        agg_model_versions = self._model_version_service.agg_model_versions_per_model(
            model_ids=[str(model.model_id) for model in list_models]
        )

        def get_all_versions(model_id: UUID) -> Union[None, List[UUID]]:
            """
            Get all versions of a model
               if the model has no versions or the version data is not requested, return None
            """
            if str(model_id) in agg_model_versions and get_all_versions_flag:
                return [UUID(version) for version in agg_model_versions[str(model_id)]]
            else:
                return None

        alerts = self._alert_service.get_alerts(
            model_ids=[str(model.model_id) for model in list_models]
        )

        def get_latest_version(model_id: UUID) -> Union[UUID, None]:

            """
            Get the latest version of a model
            if the model has no versions, return None
            """
            if str(model_id) in agg_model_versions:
                """
                agg_model_versions[str(model_id)] returns list of all model versions.
                Below, we query 0th index to get the latest version,and then
                again query 0th index to get its version id, which we want to return, hence [0][0]
                """
                return UUID(agg_model_versions[str(model_id)][0][0])
            else:
                return None

        model_rows = [
            ModelListRow(
                model_id=model.model_id,
                model_name=model.model_name,
                model_version_id=get_latest_version(model.model_id),
                model_versions=get_all_versions(model.model_id),
                total_predictions=self._row_service.count_prediction_by_model_id(
                    str(model.model_id)
                ),
                last_prediction=self._row_service.find_last_prediction_date(
                    str(model.model_id)
                ),
                num_alert_perf=alerts.get(str(model.model_id), {}).get(
                    "MODEL_PERFORMANCE", 0
                ),
                num_alert_drift=alerts.get(str(model.model_id), {}).get("DRIFT", 0),
                num_alert_data_quality=alerts.get(str(model.model_id), {}).get(
                    "DATA_QUALITY", 0
                ),
            )
            for model in list_models
        ]

        return model_rows

    def count_models(self) -> int:
        return self._repository.count_models(filters={})

    def model_overview(self, model_id: UUID):
        model_id = str(model_id)

        prediction_average = self._row_service.prediction_average(model_id)
        week_prediction_stats = self._row_service.week_prediction_stats(model_id)
        prediction_histogram = self._row_service.prediction_histogram(model_id)
        prediction_histogram_version = self._row_service.prediction_histogram_version(
            model_id
        )

        alerts_count = self._alert_service.count_alert_by_filter(
            {"model_id": str(model_id)}
        )
        alert_week_stats = self._alert_service.alert_week_stats(model_id)
        latest_alerts = self._alert_service.find_alerts(model_id)

        return ModelOverviewResponse(
            model_id=model_id,
            model_prediction_overview=ModelOverviewPredictions(
                pred_yesterday=week_prediction_stats["pred_yesterday"],
                pred_percentage_change=week_prediction_stats["pred_percentage_change"],
                pred_trend_data=week_prediction_stats["pred_trend_data"],
                pred_average=prediction_average["pred_average"],
                pred_average_window_days=prediction_average["pred_average_window_days"],
            ),
            model_alert_overview=ModelOverviewAlerts(
                alerts_count=alerts_count,
                alert_trend_data=alert_week_stats["alert_trend_data"],
                alert_percentage_change=alert_week_stats["alert_percentage_change"],
            ),
            model_alert_list=latest_alerts,
            model_prediction_hist=ModelPredictionHistogram(
                predictions=prediction_histogram,
                predictions_versions=prediction_histogram_version,
            ),
        )
