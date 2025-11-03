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

from typing import Optional

from kubeflow.core.base_client import BaseClient
from kubeflow.core.config import KubeflowConfig


class NotebookClient(BaseClient):
    """A client for interacting with Kubeflow Notebooks."""

    def __init__(self, config: Optional[KubeflowConfig] = None):
        """Initializes the NotebookClient."""
        super().__init__(config=config)
