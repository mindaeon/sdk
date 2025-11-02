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

from typing import Any, Optional

from pydantic import BaseModel, Field


class K8sResource(BaseModel):
    """A wrapper for Kubernetes resources.

    This class provides a Pydantic model for Kubernetes resources. It includes
    methods for accessing common fields and converting the resource to a
    dictionary.
    """

    api_version: str = Field(..., alias="apiVersion")
    kind: str
    metadata: dict[str, Any]
    spec: Optional[dict[str, Any]] = None
    status: Optional[dict[str, Any]] = None
    raw: Optional[dict[str, Any]] = Field(None, alias="_raw")

    def __init__(self, **data):
        init_data = data.copy()
        init_data["_raw"] = data
        super().__init__(**init_data)

    @property
    def name(self) -> str:
        """Returns the name of the Kubernetes resource."""
        return self.metadata.get("name")

    @property
    def namespace(self) -> Optional[str]:
        """Returns the namespace of the Kubernetes resource."""
        return self.metadata.get("namespace")

    def to_dict(self) -> dict[str, Any]:
        """Returns the raw dictionary representation of the Kubernetes resource."""
        return self.raw

    def to_json(self, **kwargs) -> dict[str, Any]:
        """Returns the JSON representation of the Kubernetes resource."""
        return self.model_dump_json(**kwargs)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "K8sResource":
        """Creates a K8sResource object from a dictionary."""
        return cls(**data)
