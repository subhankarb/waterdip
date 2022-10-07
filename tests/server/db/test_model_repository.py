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

from waterdip.server.db.models.models import ModelInDB
from waterdip.server.db.mongodb import MongodbBackend
from waterdip.server.db.repositories.model_repository import ModelRepository


@pytest.mark.usefixtures("mock_mongo_backend")
class TestModelsRepository:
    def test_should_create_model(self, mock_mongo_backend: MongodbBackend):
        model_repo = ModelRepository(mongodb=mock_mongo_backend)
        model_uuid = uuid.uuid4()
        inserted_model_id = model_repo.register_model(
            ModelInDB(model_id=model_uuid, model_name="test_model")
        )
        assert model_uuid == uuid.UUID(inserted_model_id)
