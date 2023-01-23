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

from waterdip.core.commons.models import DatasetType, Environment
from waterdip.server.db.models.datasets import BaseDatasetDB
from waterdip.server.db.mongodb import MONGO_COLLECTION_DATASETS, MongodbBackend
from waterdip.server.db.repositories.dataset_repository import DatasetRepository


@pytest.mark.usefixtures("mock_mongo_backend")
class TestDatasetsRepository:
    def test_should_create_dataset(self, mock_mongo_backend: MongodbBackend):
        dataset_repo = DatasetRepository(mongodb=mock_mongo_backend)
        dataset_id, model_id, model_version_id = (
            uuid.uuid4(),
            uuid.uuid4(),
            uuid.uuid4(),
        )
        dataset = BaseDatasetDB(
            dataset_id=dataset_id,
            dataset_name="dataset",
            environment=Environment.TRAINING,
            model_id=model_id,
            model_version_id=model_version_id,
            dataset_type=DatasetType.BATCH,
        )
        inserted_dataset = dataset_repo.create_dataset(dataset=dataset)
        assert dataset_id == inserted_dataset.dataset_id

    def test_should_delete_alerts_by_model_id(self, mock_mongo_backend: MongodbBackend):
        dataset_repo = DatasetRepository(mongodb=mock_mongo_backend)
        dataset_id, model_id, model_version_id = (
            uuid.uuid4(),
            uuid.uuid4(),
            uuid.uuid4(),
        )
        dataset = BaseDatasetDB(
            dataset_id=dataset_id,
            dataset_name="dataset",
            model_id=model_id,
            model_version_id=model_version_id,
            dataset_type=DatasetType.BATCH,
        )
        mock_mongo_backend.database[MONGO_COLLECTION_DATASETS].insert_one(
            dataset.dict()
        )
        dataset_repo.delete_datasets_by_model_id(str(model_id))
        dataset_repo.delete_datasets_by_model_id({"model_id": str(model_id)})
        count = mock_mongo_backend.database[MONGO_COLLECTION_DATASETS].count_documents(
            {"model_id": str(model_id)}
        )
        assert count == 0
