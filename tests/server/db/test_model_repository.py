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

from waterdip.server.db.models.models import BaseModelDB, ModelVersionDB
from waterdip.server.db.mongodb import (
    MONGO_COLLECTION_MODEL_VERSION,
    MONGO_COLLECTION_MODELS,
    MongodbBackend,
)
from waterdip.server.db.repositories.model_repository import (
    ModelRepository,
    ModelVersionRepository,
)


@pytest.mark.usefixtures("mock_mongo_backend")
class TestModelsRepository:
    def test_should_create_model(self, mock_mongo_backend: MongodbBackend):
        model_repo = ModelRepository(mongodb=mock_mongo_backend)
        model_uuid = uuid.uuid4()
        inserted_model = model_repo.register_model(
            BaseModelDB(model_id=model_uuid, model_name="test_model")
        )
        assert model_uuid == inserted_model.model_id


@pytest.mark.usefixtures("mock_mongo_backend")
class TestModelVersionsRepository:
    def test_should_create_model_version(self, mock_mongo_backend: MongodbBackend):
        model_repo = ModelVersionRepository(mongodb=mock_mongo_backend)
        model_uuid, model_version_uuid = uuid.uuid4(), uuid.uuid4()

        inserted_model = model_repo.register_model_version(
            ModelVersionDB(
                model_version_id=model_version_uuid,
                model_version="v1",
                model_id=model_uuid,
            )
        )
        assert model_version_uuid == inserted_model.model_version_id

    def test_should_return_model_version_by_id(
        self, mock_mongo_backend: MongodbBackend
    ):
        model_repo = ModelVersionRepository(mongodb=mock_mongo_backend)
        model_uuid, model_version_uuid, model_version_name = (
            uuid.uuid4(),
            uuid.uuid4(),
            "v1",
        )

        mock_mongo_backend.database[MONGO_COLLECTION_MODEL_VERSION].insert_one(
            ModelVersionDB(
                model_version_id=model_version_uuid,
                model_version=model_version_name,
                model_id=model_uuid,
            ).dict()
        )

        response_version = model_repo.find_by_id(model_version_id=model_version_uuid)
        assert model_uuid == response_version.model_id
        assert model_version_name == response_version.model_version

    def test_should_return_none_if_not_found_by_id(
        self, mock_mongo_backend: MongodbBackend
    ):
        model_repo = ModelVersionRepository(mongodb=mock_mongo_backend)
        model_uuid, model_version_uuid, model_version_name = (
            uuid.uuid4(),
            uuid.uuid4(),
            "v1",
        )

        mock_mongo_backend.database[MONGO_COLLECTION_MODEL_VERSION].insert_one(
            ModelVersionDB(
                model_version_id=model_version_uuid,
                model_version=model_version_name,
                model_id=model_uuid,
            ).dict()
        )

        response_version = model_repo.find_by_id(model_version_id=uuid.uuid4())
        assert response_version is None
