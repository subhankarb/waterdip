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

import mongomock
import pytest

from waterdip.server.db.mongodb import MongodbBackend


@pytest.fixture(autouse=True)
def mock_mongo_backend(monkeypatch) -> MongodbBackend:
    mock_mongo_client = mongomock.MongoClient()
    mock_mongo_database = mock_mongo_client.db
    mongo_backend = MongodbBackend(mock_mongo_client, "")
    # monkeypatch.setattr(mongo_backend, "client", mock_mongo_client)
    # monkeypatch.setattr(mongo_backend, "database", mock_mongo_database)
    return mongo_backend
