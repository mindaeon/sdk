# Copyright 2025 The Kubeflow Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from kubeflow.core.base_client import BaseClient
from kubeflow.model_registry.types import (
    ModelArtifact,
    ModelVersion,
    ModelArtifactCreate,
    ModelVersion,
    ModelVersionCreate,
    RegisteredModel,
    RegisteredModelCreate,
)


class ModelRegistryClient(BaseClient):
    """Client for interacting with the Kubeflow Model Registry."""

    def __init__(self, **kwargs):
        """Initializes a ModelRegistryClient."""
        super().__init__(**kwargs)
        self.base_path = "/api/model_registry/v1alpha3"

    def create_registered_model(
        self, registered_model: RegisteredModelCreate
    ) -> RegisteredModel:
        """Creates a new registered model.

        Args:
            registered_model: The RegisteredModel to create.

        Returns:
            The created RegisteredModel.
        """
        response, _, _ = self.api_client.call_api(
            f"{self.base_path}/registered_models",
            "POST",
            body=registered_model.model_dump(by_alias=True, exclude_none=True),
            response_type=RegisteredModel,
            _return_http_data_only=False,
        )
        return response

    def create_model_version(self, model_version: ModelVersionCreate) -> ModelVersion:
        """Creates a new model version.

        Args:
            model_version: The ModelVersion to create.

        Returns:
            The created ModelVersion.
        """
        response, _, _ = self.api_client.call_api(
            f"{self.base_path}/model_versions",
            "POST",
            body=model_version.model_dump(by_alias=True, exclude_none=True),
            response_type=ModelVersion,
            _return_http_data_only=False,
        )
        return response

    def create_model_artifact(
        self, model_artifact: ModelArtifactCreate
    ) -> ModelArtifact:
        """Creates a new model artifact.

        Args:
            model_artifact: The ModelArtifact to create.

        Returns:
            The created ModelArtifact.
        """
        response, _, _ = self.api_client.call_api(
            f"{self.base_path}/model_artifacts",
            "POST",
            body=model_artifact.model_dump(by_alias=True, exclude_none=True),
            response_type=ModelArtifact,
            _return_http_data_only=False,
        )
        return response
