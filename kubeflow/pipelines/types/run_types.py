# Copyright 2025 The Kubeflow Authors.
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
from enum import Enum
from typing import Dict, Any, Optional

from pydantic import BaseModel


class RunState(str, Enum):
    """The state of a pipeline run."""

    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"
    CANCELED = "CANCELED"
    PENDING = "PENDING"
    RUNNING = "RUNNING"


class Run(BaseModel):
    """A Kubeflow Pipeline Run."""

    run_id: str
    display_name: str
    created_at: datetime
    state: RunState
    error: Optional[Dict[str, Any]] = None
    pipeline_version_reference: Optional[Dict[str, Any]] = None


class RunDetails(Run):
    """Detailed information about a Kubeflow Pipeline Run."""

    run_details: Dict[str, Any]
