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
from kubeflow.pipelines.types.pipeline_types import Pipeline, PipelineVersion


class PipelineClient(BaseClient):
    """A client for interacting with Kubeflow Pipelines."""

    def __init__(self, config: Optional[KubeflowConfig] = None):
        """Initializes the PipelineClient."""
        super().__init__(config)
        self.api_version = "v2beta1"

    def create_pipeline(
        self,
        pipeline_name: str,
        description: Optional[str] = None,
        namespace: Optional[str] = None,
    ) -> Pipeline:
        """Creates a pipeline."""
        body = {"display_name": pipeline_name, "description": description}
        params = {}
        if namespace:
            params["namespace"] = namespace
        response = self.api_client.call_api(
            f"/apis/{self.api_version}/pipelines", "POST", body=body, query_params=params
        )
        return Pipeline(**response)

    def create_pipeline_version(
        self,
        pipeline_id: str,
        pipeline_version_name: str,
        package_url: str,
        description: Optional[str] = None,
    ) -> PipelineVersion:
        """Creates a pipeline version."""
        body = {
            "display_name": pipeline_version_name,
            "package_url": {"pipeline_url": package_url},
            "description": description,
        }
        response = self.api_client.call_api(
            f"/apis/{self.api_version}/pipelines/{pipeline_id}/versions",
            "POST",
            body=body,
        )
        return PipelineVersion(**response)

    def get_pipeline(self, pipeline_id: str) -> Pipeline:
        """Gets a pipeline."""
        response = self.api_client.call_api(
            f"/apis/{self.api_version}/pipelines/{pipeline_id}", "GET"
        )
        return Pipeline(**response)

    def get_pipeline_by_name(self, pipeline_name: str) -> Optional[Pipeline]:
        """Gets a pipeline by name."""
        pipelines = self.list_pipelines()
        for pipeline in pipelines:
            if pipeline.display_name == pipeline_name:
                return self.get_pipeline(pipeline.pipeline_id)
        return None

    def list_pipelines(self) -> list[Pipeline]:
        """Lists pipelines."""
        response = self.api_client.call_api(
            f"/apis/{self.api_version}/pipelines", "GET"
        )
        return [Pipeline(**p) for p in response.get("pipelines", [])]

    def delete_pipeline(self, pipeline_id: str):
        """Deletes a pipeline."""
        return self.api_client.call_api(
            f"/apis/{self.api_version}/pipelines/{pipeline_id}", "DELETE"
        )

    def get_pipeline_version(
        self, pipeline_id: str, pipeline_version_id: str
    ) -> PipelineVersion:
        """Gets a pipeline version."""
        response = self.api_client.call_api(
            f"/apis/{self.api_version}/pipelines/{pipeline_id}/versions/{pipeline_version_id}",
            "GET",
        )
        return PipelineVersion(**response)

    def list_pipeline_versions(self, pipeline_id: str) -> list[PipelineVersion]:
        """Lists pipeline versions."""
        response = self.api_client.call_api(
            f"/apis/{self.api_version}/pipelines/{pipeline_id}/versions", "GET"
        )
        return [
            PipelineVersion(**pv) for pv in response.get("pipeline_versions", [])
        ]
