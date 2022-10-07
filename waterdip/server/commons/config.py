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

from typing import List

from pydantic import BaseSettings


class ServerSettings(BaseSettings):
    """ """

    mongo_url: str = "mongodb://dbuser:dbpass@127.0.0.1:27017/"
    mongo_database: str = "waterdip"
    mongo_collection_models: str = "wd_models"
    mongo_collection_model_version: str = "wd_model_versions"

    docs_enabled: bool = True

    cors_origins: List[str] = ["*"]

    class Config:
        env_prefix = "WD_"
        fields = {
            "mongo_url": {"env": ["MONGODB_URL", f"{env_prefix}MONGODB_URL"]},
            "mongo_database": {
                "env": ["MONGODB_DATABASE", f"{env_prefix}MONGODB_DATABASE"]
            },
            "docs_enabled": {"env": ["DOCS_ENABLED", f"{env_prefix}DOCS_ENABLED"]},
            "cors_origins": {"env": ["CORS_ORIGINS", f"{env_prefix}CORS_ORIGINS"]},
        }


settings = ServerSettings()
