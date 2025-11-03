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

"""Pydantic models for the Profile custom resource."""

from typing import Dict, Optional

from pydantic import BaseModel, Field

from kubeflow.core.k8s_resource import K8sResource


class Owner(BaseModel):
    """Pydantic model for the Owner of a Profile."""

    kind: str
    name: str


class ResourceQuota(BaseModel):
    """Pydantic model for the ResourceQuotaSpec of a Profile."""

    hard: Optional[Dict[str, str]] = None


class ProfileSpec(BaseModel):
    """Pydantic model for the Spec of a Profile."""

    owner: Owner
    resource_quota_spec: Optional[ResourceQuota] = Field(
        alias="resourceQuotaSpec", default=None
    )


class Profile(K8sResource):
    """Pydantic model for the Profile custom resource."""

    spec: ProfileSpec
