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

from uuid import UUID

from fastapi import Depends
from pydantic import Field

from waterdip.server.commons.models import MonitorType
from waterdip.server.db.models.monitors import (
    BaseMonitorDB,
    DataQualityBaseMonitorCondition,
    DriftBaseMonitorCondition,
    MonitorIdentification,
    PerformanceBaseMonitorCondition,
)
from waterdip.server.db.repositories.monitor_repository import MonitorRepository
from waterdip.server.services.model_service import ModelService, ModelVersionService


class ServiceBaseMonitor(BaseMonitorDB):
    pass


class ServiceDataQualityMonitor(ServiceBaseMonitor):
    monitor_type: MonitorType = Field(default=MonitorType.DATA_QUALITY, const=True)
    monitor_condition: DataQualityBaseMonitorCondition = Field(...)


class ServicePerformanceMonitor(ServiceBaseMonitor):
    monitor_type: MonitorType = Field(default=MonitorType.PERFORMANCE, const=True)
    monitor_condition: PerformanceBaseMonitorCondition = Field(...)


class ServiceDriftMonitor(ServiceBaseMonitor):
    monitor_type: MonitorType = Field(default=MonitorType.DRIFT, const=True)
    monitor_condition: DriftBaseMonitorCondition = Field(...)


class MonitorService:
    _INSTANCE: "MonitorService" = None

    @classmethod
    def get_instance(
        cls,
        repository: MonitorRepository = Depends(MonitorRepository.get_instance),
        model_service: ModelService = Depends(ModelService.get_instance),
        model_version_service: ModelVersionService = Depends(
            ModelVersionService.get_instance
        ),
    ):
        if not cls._INSTANCE:
            cls._INSTANCE = cls(
                repository=repository,
                model_service=model_service,
                model_version_service=model_version_service,
            )
        return cls._INSTANCE

    def __init__(
        self,
        repository: MonitorRepository,
        model_service: ModelService,
        model_version_service: ModelVersionService,
    ):
        self._repository = repository
        self.model_service = model_service
        self.model_version_service = model_version_service

    def _check_monitor_identification(
        self, monitor_identification: MonitorIdentification
    ):
        """
        Constrain check for model creation. This will check the
        existence of model_id and model_version_id associated with the monitor
        """
        self.model_version_service.find_by_id(
            model_version_id=monitor_identification.model_version_id
        )
        self.model_service.find_by_id(model_id=monitor_identification.model_id)

    def create_data_quality_monitor(
        self, data_quality_monitor: ServiceDataQualityMonitor
    ):
        self._check_monitor_identification(data_quality_monitor.monitor_identification)
        self._repository.insert_monitor(monitor=data_quality_monitor)

    def create_model_performance_monitor(self, perf_monitor: ServicePerformanceMonitor):
        self._check_monitor_identification(perf_monitor.monitor_identification)
        self._repository.insert_monitor(monitor=perf_monitor)

    def create_drift_monitor(self, drift_monitor: ServiceDriftMonitor):
        self._check_monitor_identification(drift_monitor.monitor_identification)
        self._repository.insert_monitor(monitor=drift_monitor)
