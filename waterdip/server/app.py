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

import json
import time
import traceback

from fastapi import FastAPI
from loguru import logger
from pydantic import ConfigError
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from waterdip import __version__ as wd_version
from waterdip.server.apis.router import api_router
from waterdip.server.commons.config import settings
from waterdip.server.db.mongodb import MongodbBackend
from waterdip.utils.logging import configure_logging


def configure_api_router(app: FastAPI):
    """Configures the api router"""
    app.include_router(api_router)


def configure_database(app: FastAPI):
    """
    Configures database for the server.
    On Startup, it will create mongodb backend instance

    """

    @app.on_event("startup")
    async def configure_mongo():
        try:
            print(settings.obfuscated_mongodb())
            MongodbBackend.get_instance()

        except BaseException as error:
            logger.error(
                f"failed to connect to mongo instance [{settings.obfuscated_mongodb()}]"
            )
            raise ConfigError(
                f"Mongodb endpoint at {settings.obfuscated_mongodb()} "
                "is not available or not responding.\n"
                "Please make sure your Mongodb instance is launched and correctly running and\n"
                "you have the necessary access permissions. "
                "Once you have verified this, restart the Waterdip server.\n"
            ) from error


def configure_middleware(app: FastAPI):
    """
    Configures fastapi middleware
    """

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        """
        Middleware to add response time HEADER to the response.
        Every response will have total time taken in millisecond for the API.
        """
        try:
            start_time = time.time()
            response = await call_next(request)
            process_time = round(round((time.time() - start_time) * 1000, 2))
            response.headers["X-Process-Time"] = str(process_time) + " ms"
            logger.info("{0} took time {1} ms", request.url.path, process_time)
            return response
        except Exception:
            logger.error(traceback.print_exc())
            return Response(
                json.dumps(
                    {
                        "loc": [],
                        "msg": "Internal Server Error",
                        "type": "unexpected_error",
                    }
                ),
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            )


def configure_app_logging(app: FastAPI):
    """Configure app logging using"""
    app.on_event("startup")(configure_logging)


app = FastAPI(
    title="Waterdip",
    description="Waterdip API",
    version=str(wd_version),
    docs_url="/api/docs" if settings.docs_enabled else None,
    openapi_url="/api/docs/spec.json",
)

for app_configure in [configure_api_router, configure_middleware, configure_database]:
    app_configure(app)
