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

from typing import Optional

from kubeflow.core.base_client import BaseClient
from kubeflow.core.config import KubeflowConfig


class RunClient(BaseClient):
    """A client for interacting with Kubeflow Pipeline Runs."""

    def __init__(self, config: Optional[KubeflowConfig] = None):
        """Initializes the RunClient."""
        super().__init__(config)
        self.api_version = "v2beta1"

    def create_run(self, pipeline_id: str, run_name: str):
        """Creates a pipeline run."""
        body = {"display_name": run_name, "pipeline_version_reference": {"pipeline_id": pipeline_id}}
        return self.api_client.call_api(
            f"/apis/{self.api_version}/runs", "POST", body=body
        )

    def get_run(self, run_id: str):
        """Gets a pipeline run."""
        return self.api_client.call_api(
            f"/apis/{self.api_version}/runs/{run_id}", "GET"
        )

    def list_runs(self):
        """Lists pipeline runs."""
        return self.api_client.call_api(f"/apis/{self.api_version}/runs", "GET")

    def delete_run(self, run_id: str):
        """Deletes a pipeline run."""
        return self.api_client.call_api(
            f"/apis/{self.api_version}/runs/{run_id}", "DELETE"
        )
