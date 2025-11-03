# Copyright 2024 The Kubeflow Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field


class K8sResource(BaseModel):
    """
    A Pydantic-based wrapper for Kubernetes resource dictionaries.
    Provides convenient access to common metadata fields.
    """

    api_version: str = Field(..., alias="apiVersion")
    kind: str
    metadata: Dict[str, Any]
    spec: Optional[Dict[str, Any]] = None
    status: Optional[Dict[str, Any]] = None
    raw: Dict[str, Any] = Field(..., alias="_raw")

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra="allow",
    )

    def __init__(self, **data):
        init_data = data.copy()
        init_data["_raw"] = data
        super().__init__(**init_data)

    @property
    def name(self) -> str:
        return self.metadata.get("name", "")

    @property
    def namespace(self) -> Optional[str]:
        return self.metadata.get("namespace")

    @property
    def uid(self) -> Optional[str]:
        return self.metadata.get("uid")

    @property
    def creation_timestamp(self) -> Optional[str]:
        return self.metadata.get("creationTimestamp")

    @property
    def labels(self) -> Dict[str, str]:
        return self.metadata.get("labels", {})

    @property
    def annotations(self) -> Dict[str, str]:
        return self.metadata.get("annotations", {})
