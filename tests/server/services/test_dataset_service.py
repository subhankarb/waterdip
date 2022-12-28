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

import pytest
from pydantic import ValidationError

from waterdip.server.apis.models.params import RequestSort
from waterdip.server.commons.models import DatasetType
from waterdip.server.db.models.datasets import BaseDatasetDB
from waterdip.server.db.mongodb import MongodbBackend
from waterdip.server.db.repositories.dataset_repository import DatasetRepository
from waterdip.server.services.dataset_service import DatasetService


@pytest.mark.usefixtures("mock_mongo_backend")
class TestDatasetService:
    _model_id = uuid.uuid4()
    _model_version_id = uuid.uuid4()

    @pytest.mark.parametrize(
        "dataset_lists, dataset_count",
        [
            (
                [
                    BaseDatasetDB(
                        dataset_id=uuid.uuid4(),
                        dataset_name="d1",
                        dataset_type=DatasetType.BATCH,
                        model_id=_model_id,
                        model_version_id=_model_version_id,
                    )
                ],
                1,
            )
        ],
    )
    def test_list_dataset_should_return_datasets(
        self, mocker, dataset_lists, dataset_count, mock_mongo_backend: MongodbBackend
    ):
        mocker.patch(
            "waterdip.server.db.repositories.dataset_repository.DatasetRepository.find_datasets",
            return_value=dataset_lists,
        )
        mocker.patch(
            "waterdip.server.db.repositories.dataset_repository.DatasetRepository.count_dataset",
            return_value=dataset_count,
        )

        data_service = DatasetService.get_instance(
            DatasetRepository.get_instance(mongodb=mock_mongo_backend)
        )
        result = data_service.list_dataset(model_version_id=self._model_version_id)
        assert result[1] == 1
        assert len(result[0]) == 1

    @pytest.mark.parametrize("_sort", ["created_at_desc", "created-at_asc"])
    def test_should_return_result_if_sort_format_is_right(
        self, mocker, _sort, mock_mongo_backend: MongodbBackend
    ):
        mocker.patch(
            "waterdip.server.db.repositories.dataset_repository.DatasetRepository.find_datasets",
            return_value=[
                BaseDatasetDB(
                    dataset_id=uuid.uuid4(),
                    dataset_name="d1",
                    dataset_type=DatasetType.BATCH,
                    model_id=self._model_id,
                    model_version_id=self._model_version_id,
                )
            ],
        )
        mocker.patch(
            "waterdip.server.db.repositories.dataset_repository.DatasetRepository.count_dataset",
            return_value=1,
        )

        data_service = DatasetService.get_instance(
            DatasetRepository.get_instance(mongodb=mock_mongo_backend)
        )
        sort_order = RequestSort(sort=_sort)
        result = data_service.list_dataset(
            model_version_id=self._model_version_id, sort_request=sort_order
        )
        assert result[1] == 1
        assert len(result[0]) == 1
        assert sort_order.get_sort_order in [-1, 1]

    @pytest.mark.parametrize("sort", [("created_at_des",), ("created-at-des",)])
    def test_should_throw_error_if_sort_option_is_not_proper(
        self, mocker, sort, mock_mongo_backend: MongodbBackend
    ):
        mocker.patch(
            "waterdip.server.db.repositories.dataset_repository.DatasetRepository.find_datasets",
            return_value=[
                BaseDatasetDB(
                    dataset_id=uuid.uuid4(),
                    dataset_name="d1",
                    dataset_type=DatasetType.BATCH,
                    model_id=self._model_id,
                    model_version_id=self._model_version_id,
                )
            ],
        )
        mocker.patch(
            "waterdip.server.db.repositories.dataset_repository.DatasetRepository.count_dataset",
            return_value=1,
        )

        data_service = DatasetService.get_instance(
            DatasetRepository.get_instance(mongodb=mock_mongo_backend)
        )

        with pytest.raises(ValidationError):
            result = data_service.list_dataset(
                model_version_id=self._model_version_id,
                sort_request=RequestSort(sort=sort),
            )
