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

import warnings

import mongomock
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from tests.testing_helpers import MongodbBackendTesting
from waterdip.server.db.mongodb import MongodbBackend


@pytest.fixture(scope="class")
def app() -> FastAPI:
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    from waterdip.server.app import app

    app.dependency_overrides[
        MongodbBackend.get_instance
    ] = MongodbBackendTesting.get_instance
    return app


@pytest.fixture(autouse=True)
def mock_mongo_backend(monkeypatch) -> MongodbBackend:
    mock_mongo_client = mongomock.MongoClient()
    return MongodbBackendTesting(mock_mongo_client)


@pytest.fixture(scope="class")
def test_client(app: FastAPI) -> TestClient:
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    client = TestClient(app)
    return client
