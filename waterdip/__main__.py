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
import asyncio

import uvicorn

from waterdip import app, scheduler


class Server(uvicorn.Server):
    """Customized uvicorn.Server

    Uvicorn server overrides signals and we need to include
    Rocketry to the signals."""

    def handle_exit(self, sig: int, frame) -> None:
        scheduler.session.shut_down()
        return super().handle_exit(sig, frame)


async def main():
    """Run Rocketry and FastAPI"""

    uvicorn_config = uvicorn.Config(
        app, workers=1, loop="asyncio", port=4422, host="0.0.0.0"
    )

    server = Server(config=uvicorn_config)

    api = asyncio.create_task(server.serve())
    sched = asyncio.create_task(scheduler.serve())

    await asyncio.wait([api, sched])


if __name__ == "__main__":

    asyncio.run(main())
