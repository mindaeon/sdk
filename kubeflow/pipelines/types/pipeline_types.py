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

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


class PipelineSpec(BaseModel):
    """The specification of a Kubeflow Pipeline."""

    pipeline_manifest: dict[str, Any]


class PipelineVersion(BaseModel):
    """A version of a Kubeflow Pipeline."""

    pipeline_version_id: str
    display_name: str
    created_at: datetime
    description: Optional[str] = None


class Pipeline(BaseModel):
    """A Kubeflow Pipeline."""

    pipeline_id: str
    display_name: str
    created_at: datetime
    description: Optional[str] = None
    pipeline_spec: Optional[PipelineSpec] = None
