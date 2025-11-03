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


class PipelineClient(BaseClient):
    """A client for interacting with Kubeflow Pipelines."""

    def __init__(self, config: Optional[KubeflowConfig] = None):
        """Initializes the PipelineClient."""
        super().__init__(config)
        self.api_version = "v2beta1"

    def create_pipeline(self, pipeline_name: str, pipeline_package_path: str):
        """Creates a pipeline."""
        with open(pipeline_package_path, "rb") as f:
            pipeline_package = f.read()

        response = self.api_client.call_api(
            f"/apis/{self.api_version}/pipelines/upload",
            "POST",
            query_params=[("name", pipeline_name)],
            body=pipeline_package,
            header_params={"Content-Type": "application/zip"},
            _preload_content=False,
        )
        return response

    def create_pipeline_version(self, pipeline_id: str, pipeline_package_path: str):
        """Creates a pipeline version."""
        with open(pipeline_package_path, "rb") as f:
            pipeline_package = f.read()

        response = self.api_client.call_api(
            f"/apis/{self.api_version}/pipelines/{pipeline_id}/versions/upload",
            "POST",
            body=pipeline_package,
            header_params={"Content-Type": "application/zip"},
            _preload_content=False,
        )
        return response

    def get_pipeline(self, pipeline_id: str):
        """Gets a pipeline."""
        return self.api_client.call_api(
            f"/apis/{self.api_version}/pipelines/{pipeline_id}", "GET"
        )

    def get_pipeline_by_name(self, pipeline_name: str):
        """Gets a pipeline by name."""
        pipelines = self.list_pipelines()
        for pipeline in pipelines["pipelines"]:
            if pipeline["display_name"] == pipeline_name:
                return self.get_pipeline(pipeline["pipeline_id"])
        return None

    def list_pipelines(self):
        """Lists pipelines."""
        return self.api_client.call_api(
            f"/apis/{self.api_version}/pipelines", "GET"
        )

    def delete_pipeline(self, pipeline_id: str):
        """Deletes a pipeline."""
        return self.api_client.call_api(
            f"/apis/{self.api_version}/pipelines/{pipeline_id}", "DELETE"
        )
