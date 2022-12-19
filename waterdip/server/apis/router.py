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

from fastapi import APIRouter

from waterdip.server.apis.routes.dataset_routers import router as dataset_routers
from waterdip.server.apis.routes.logging_routes import router as logging_routes
from waterdip.server.apis.routes.model_routes import router as model_routes
from waterdip.server.apis.routes.monitor_routes import router as monitor_routes

api_router = APIRouter()

api_router.include_router(dataset_routers, tags=["datasets"], prefix="/v1")
api_router.include_router(logging_routes, tags=["logging"], prefix="/v1")
api_router.include_router(model_routes, tags=["models"], prefix="/v1")
api_router.include_router(monitor_routes, tags=["monitors"], prefix="/v1")
