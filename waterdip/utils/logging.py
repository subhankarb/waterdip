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

import logging

from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        logger_opt = logger.opt(depth=7, exception=record.exc_info)
        logger_opt.log(record.levelname, record.getMessage())


class Formatter:
    def __init__(self):
        self.padding = 0
        self.fmt = "{level: <8} | {time} |  {name}:{function}:{line}{extra[padding]} | {message}\n{exception}"

    def format(self, record):
        length = len("{name}:{function}:{line}".format(**record))
        self.padding = max(self.padding, length)
        record["extra"]["padding"] = " " * (self.padding - length)
        return self.fmt


def configure_logging():
    """Logging configuration"""
    intercept_handler = InterceptHandler()

    for name in [
        "uvicorn",
        "uvicorn.lifespan",
        "uvicorn.error",
        "uvicorn.access",
        "fastapi",
        "waterdip",
        "waterdip.server",
    ]:
        logger_ = logging.getLogger(name)
        logger_.propagate = False
        logger_.handlers = [intercept_handler]
