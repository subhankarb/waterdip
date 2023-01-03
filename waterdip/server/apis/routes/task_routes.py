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

from celery.result import AsyncResult
from fastapi import APIRouter
from starlette.responses import JSONResponse

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal
from waterdip.processor.tasks.monitors import generate_monitor_jobs

router = APIRouter()


@router.post("/task.run", name="task:run")
def run_task(
    task_name: Literal["generate_monitor_jobs"] = "generate_monitor_jobs",
):
    if task_name == "generate_monitor_jobs":
        task = generate_monitor_jobs.delay()
    else:
        raise NotImplementedError()
    return JSONResponse({"task_id": task.id})


@router.get("/task.status", name="task:status")
def get_status(job_id):
    task_result = AsyncResult(job_id)
    result = {
        "task_id": job_id,
        "task_status": task_result.status,
        "task_result": task_result.result,
    }
    return JSONResponse(result)
