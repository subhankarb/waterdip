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

from celery import Celery

from waterdip.server.commons.config import settings

celery_app = Celery(__name__, include=["waterdip.processor.tasks.monitors"])

celery_app.conf.broker_url = settings.redis_url
celery_app.conf.result_backend = settings.mongo_url
celery_app.conf.mongodb_backend_settings = {"database": settings.mongo_database}
celery_app.conf.result_extended = True

celery_app.autodiscover_tasks()

celery_app.conf.beat_schedule = {
    "generate_monitor_jobs_every_hour": {
        "task": "create_process_monitor_jobs",
        "schedule": 3600,
    }
}
