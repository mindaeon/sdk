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

from unittest.mock import patch

from kubernetes.client import Configuration

from kubeflow.model_registry.clients import ModelRegistryClient
from kubeflow.model_registry.types import (
    ModelArtifact,
    ModelArtifactCreate,
    ModelVersion,
    ModelVersionCreate,
    RegisteredModel,
    RegisteredModelCreate,
)

# Create a fake config for the client to use
fake_conf = Configuration()
fake_conf.host = "http://localhost:8080"


def test_model_registry_client_create_registered_model():
    """Tests the create_registered_model method of the ModelRegistryClient."""
    registered_model = RegisteredModelCreate(
        name="my-model",
    )

    with patch(
        "kubeflow.core.base_client.KubeconfigAuthProvider"
    ) as mock_auth_provider, patch(
        "kubeflow.core.base_client.client.ApiClient"
    ) as mock_api_client:
        mock_auth_provider.return_value.get_api_client_configuration.return_value = (
            fake_conf
        )
        mock_api_client.return_value.call_api.return_value = (
            RegisteredModel(
                id="my-model-id",
                createTimeSinceEpoch="0",
                lastUpdateTimeSinceEpoch="0",
                **registered_model.model_dump(by_alias=True, exclude_none=True),
            ),
            201,
            {},
        )
        client = ModelRegistryClient()
        client.create_registered_model(registered_model)
        mock_api_client.return_value.call_api.assert_called_with(
            "/api/model_registry/v1alpha3/registered_models",
            "POST",
            body=registered_model.model_dump(by_alias=True, exclude_none=True),
            response_type=RegisteredModel,
            _return_http_data_only=False,
        )


def test_model_registry_client_create_model_version():
    """Tests the create_model_version method of the ModelRegistryClient."""
    model_version = ModelVersionCreate(
        name="my-version",
        registeredModelId="my-model-id",
    )

    with patch(
        "kubeflow.core.base_client.KubeconfigAuthProvider"
    ) as mock_auth_provider, patch(
        "kubeflow.core.base_client.client.ApiClient"
    ) as mock_api_client:
        mock_auth_provider.return_value.get_api_client_configuration.return_value = (
            fake_conf
        )
        mock_api_client.return_value.call_api.return_value = (
            ModelVersion(
                id="my-version-id",
                createTimeSinceEpoch="0",
                lastUpdateTimeSinceEpoch="0",
                **model_version.model_dump(by_alias=True, exclude_none=True),
            ),
            201,
            {},
        )
        client = ModelRegistryClient()
        client.create_model_version(model_version)
        mock_api_client.return_value.call_api.assert_called_with(
            "/api/model_registry/v1alpha3/model_versions",
            "POST",
            body=model_version.model_dump(by_alias=True, exclude_none=True),
            response_type=ModelVersion,
            _return_http_data_only=False,
        )


def test_model_registry_client_create_model_artifact():
    """Tests the create_model_artifact method of the ModelRegistryClient."""
    model_artifact = ModelArtifactCreate(
        name="my-artifact",
    )

    with patch(
        "kubeflow.core.base_client.KubeconfigAuthProvider"
    ) as mock_auth_provider, patch(
        "kubeflow.core.base_client.client.ApiClient"
    ) as mock_api_client:
        mock_auth_provider.return_value.get_api_client_configuration.return_value = (
            fake_conf
        )
        mock_api_client.return_value.call_api.return_value = (
            ModelArtifact(
                id="my-artifact-id",
                createTimeSinceEpoch="0",
                lastUpdateTimeSinceEpoch="0",
                **model_artifact.model_dump(by_alias=True, exclude_none=True),
            ),
            201,
            {},
        )
        client = ModelRegistryClient()
        client.create_model_artifact(model_artifact)
        mock_api_client.return_value.call_api.assert_called_with(
            "/api/model_registry/v1alpha3/model_artifacts",
            "POST",
            body=model_artifact.model_dump(by_alias=True, exclude_none=True),
            response_type=ModelArtifact,
            _return_http_data_only=False,
        )
