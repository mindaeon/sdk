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


class ExperimentClient(BaseClient):
    """A client for interacting with Kubeflow Pipeline Experiments."""

    def __init__(self, config: Optional[KubeflowConfig] = None):
        """Initializes the ExperimentClient."""
        super().__init__(config)
        self.api_version = "v2beta1"

    def create_experiment(self, experiment_name: str):
        """Creates a pipeline experiment."""
        body = {"display_name": experiment_name}
        return self.api_client.call_api(
            f"/apis/{self.api_version}/experiments", "POST", body=body
        )

    def get_experiment(self, experiment_id: str):
        """Gets a pipeline experiment."""
        return self.api_client.call_api(
            f"/apis/{self.api_version}/experiments/{experiment_id}", "GET"
        )

    def list_experiments(self):
        """Lists pipeline experiments."""
        return self.api_client.call_api(
            f"/apis/{self.api_version}/experiments", "GET"
        )

    def delete_experiment(self, experiment_id: str):
        """Deletes a pipeline experiment."""
        return self.api_client.call_api(
            f"/apis/{self.api_version}/experiments/{experiment_id}", "DELETE"
        )
