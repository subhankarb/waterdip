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

from pydantic import BaseModel
from pydantic.types import UUID4


class ModelInDB(BaseModel):
    model_id: UUID4
    model_name: str

    def dict(self, *args, **kwargs) -> "DictStrAny":
        model = super().dict(*args, **kwargs)
        model["model_id"] = str(model["model_id"])
        return model
