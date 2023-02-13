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
from datetime import datetime, timedelta

import pytest

from tests.testing_helpers import MODEL_ID, MODEL_ID_2, MongodbBackendTesting
from waterdip.server.db.models.models import BaseModelDB
from waterdip.server.db.mongodb import MONGO_COLLECTION_MODELS
from waterdip.server.db.repositories.model_repository import ModelRepository
from waterdip.server.services.model_service import ModelService


@pytest.mark.usefixtures("mock_mongo_backend")
class TestModelService:
    @classmethod
    def setup_class(cls):
        cls.mock_mongo_backend = MongodbBackendTesting.get_instance()
        cls.models = [
            BaseModelDB(
                model_id=MODEL_ID, model_name="UPDATE TEST MODEL WHEN PREVIOUS IS NONE"
            ),
            BaseModelDB(
                model_id=MODEL_ID_2,
                model_name="UPDATE TEST MODEL WEHN PREVIOUS IS NOT NONE",
                prediction_classes=[
                    "TEST CLASS 1",
                    "TEST CLASS 2",
                ],
            ),
        ]
        cls.mock_mongo_backend.database[MONGO_COLLECTION_MODELS].insert_many(
            model.dict() for model in cls.models
        )
        cls.model_service = ModelService.get_instance(
            repository=ModelRepository.get_instance(
                mongodb=cls.mock_mongo_backend)
        )
        cls.prediction_classes_1 = [
            "TEST CLASS 1",
        ]
        cls.prediction_classes_input_2 = [
            "TEST CLASS 1",
            "TEST CLASS 3",
        ]
        cls.prediction_classes_output_2 = [
            "TEST CLASS 1",
            "TEST CLASS 2",
            "TEST CLASS 3",
        ]

    def test_should_update_prediction_classes_when_previous_is_none(self):
        self.model_service.update_prediction_classes(
            model_id=MODEL_ID, prediction_classes=self.prediction_classes_1
        )
        model = self.mock_mongo_backend.database[MONGO_COLLECTION_MODELS].find_one(
            {"model_id": MODEL_ID}
        )
        assert model["prediction_classes"] == self.prediction_classes_1

    def test_should_update_prediction_classes_when_previous_is_not_none(self):
        self.model_service.update_prediction_classes(
            model_id=MODEL_ID_2, prediction_classes=self.prediction_classes_input_2
        )
        model = self.mock_mongo_backend.database[MONGO_COLLECTION_MODELS].find_one(
            {"model_id": MODEL_ID_2}
        )
        assert self.prediction_classes_output_2[0] in model["prediction_classes"]
        assert self.prediction_classes_output_2[1] in model["prediction_classes"]
        assert self.prediction_classes_output_2[2] in model["prediction_classes"]

    @classmethod
    def teardown_class(cls):
        cls.mock_mongo_backend.database[MONGO_COLLECTION_MODELS].drop()
