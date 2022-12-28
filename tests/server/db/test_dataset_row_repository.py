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
import datetime
import uuid
from typing import List

import pytest
from fastapi import Depends

from waterdip.server.commons.models import ColumnDataType, ColumnMappingType
from waterdip.server.db.models.dataset_rows import (
    BaseDatasetBatchRowDB,
    BaseEventRowDB,
    EventDataColumnDB,
)
from waterdip.server.db.mongodb import (
    MONGO_COLLECTION_BATCH_ROWS,
    MONGO_COLLECTION_EVENT_ROWS,
    MongodbBackend,
)
from waterdip.server.db.repositories.dataset_row_repository import (
    EventDatasetRowRepository,
)


@pytest.mark.usefixtures("mock_mongo_backend")
class TestEventDatasetRowRepository:
    def test_should_insert_rows(self, mock_mongo_backend: MongodbBackend):
        event_repo = EventDatasetRowRepository(mongodb=mock_mongo_backend)
        rows = [
            BaseEventRowDB(
                row_id=uuid.uuid4(),
                dataset_id=uuid.uuid4(),
                model_id=uuid.uuid4(),
                model_version_id=uuid.uuid4(),
                event_id="event_id",
                columns=[
                    EventDataColumnDB(
                        name="column_name",
                        value_numeric=1,
                        value_categorical="column_value",
                        data_type=ColumnDataType.CATEGORICAL,
                        mapping_type=ColumnMappingType.FEATURE,
                        column_list_index=1,
                    )
                ],
                created_at=datetime.datetime.now(),
                meta={"meta_key": "meta_value"},
            )
            for _ in range(10)
        ]

        created_rows = event_repo.inset_rows(rows=rows)
        assert len(created_rows) == len(rows)

    def test_count_prediction_by_model_id(self, mock_mongo_backend: MongodbBackend):
        event_repo = EventDatasetRowRepository(mongodb=mock_mongo_backend)
        mongo_db = mock_mongo_backend.database[MONGO_COLLECTION_EVENT_ROWS]
        model_id = uuid.uuid4()
        rows = [
            BaseEventRowDB(
                row_id=uuid.uuid4(),
                dataset_id=uuid.uuid4(),
                model_id=model_id,
                model_version_id=uuid.uuid4(),
                event_id="event_id",
                columns=[
                    EventDataColumnDB(
                        name="column_name",
                        value_numeric=1,
                        value_categorical="column_value",
                        data_type=ColumnDataType.CATEGORICAL,
                        mapping_type=ColumnMappingType.PREDICTION,
                        column_list_index=1,
                    )
                ],
                created_at=datetime.datetime.now(),
                meta={"meta_key": "meta_value"},
            )
            for _ in range(10)
        ]
        mongo_db.insert_many([row.dict() for row in rows])
        count = event_repo.count_prediction_by_model_id(model_id=str(model_id))
        assert count == len(rows)

    def test_find_last_prediction_date(self, mock_mongo_backend: MongodbBackend):
        event_repo = EventDatasetRowRepository(mongodb=mock_mongo_backend)
        mongo_db = mock_mongo_backend.database[MONGO_COLLECTION_EVENT_ROWS]
        model_id = uuid.uuid4()
        created_at = datetime.datetime(2022, 12, 16, 18, 17, 43, 470000)
        rows = [
            BaseEventRowDB(
                row_id=uuid.uuid4(),
                dataset_id=uuid.uuid4(),
                model_id=model_id,
                model_version_id=uuid.uuid4(),
                event_id="event_id",
                columns=[
                    EventDataColumnDB(
                        name="column_name",
                        value_numeric=1,
                        value_categorical="column_value",
                        data_type=ColumnDataType.CATEGORICAL,
                        mapping_type=ColumnMappingType.PREDICTION,
                        column_list_index=1,
                    )
                ],
                created_at=created_at,
                meta={"meta_key": "meta_value"},
            )
            for _ in range(1)
        ]
        mongo_db.insert_many([row.dict() for row in rows])
        last_prediction_date = event_repo.find_last_prediction_date(
            model_id=str(model_id)
        )
        assert last_prediction_date == rows[-1].created_at
