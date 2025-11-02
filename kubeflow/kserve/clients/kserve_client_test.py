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
from kubernetes.config import ConfigException

from kubeflow.kserve.clients import KServeClient
from kubeflow.kserve.types import (
    InferenceService,
    ModelFormat,
    ModelSpec,
    PredictorSpec,
)

# Create a fake config for the client to use
fake_conf = Configuration()
fake_conf.host = "http://localhost:8080"


def test_kserve_client_create():
    """Tests the create method of the KServeClient."""
    inferenceservice = InferenceService(
        name="my-inference-service",
        predictor=PredictorSpec(
            model=ModelSpec(
                modelFormat=ModelFormat(name="sklearn"),
                storageUri="gs://my-bucket/my-model",
            )
        ),
    )

    with patch(
        "kubeflow.core.base_client.KubeconfigAuthProvider"
    ) as mock_auth_provider, patch(
        "kubeflow.core.base_client.BaseClient.create_custom_resource"
    ) as mock_create:
        mock_auth_provider.return_value.get_api_client_configuration.return_value = (
            fake_conf
        )
        client = KServeClient()
        client.create(inferenceservice)
        mock_create.assert_called_with(
            group="serving.kserve.io",
            version="v1beta1",
            plural="inferenceservices",
            body=inferenceservice.model_dump(by_alias=True, exclude_none=True),
            namespace="default",
        )


def test_kserve_client_get():
    """Tests the get method of the KServeClient."""
    with patch(
        "kubeflow.core.base_client.KubeconfigAuthProvider"
    ) as mock_auth_provider, patch(
        "kubeflow.core.base_client.BaseClient.get_custom_resource"
    ) as mock_get:
        mock_auth_provider.return_value.get_api_client_configuration.return_value = (
            fake_conf
        )
        mock_get.return_value = {
            "apiVersion": "serving.kserve.io/v1beta1",
            "kind": "InferenceService",
            "metadata": {"name": "my-inference-service"},
            "spec": {
                "predictor": {
                    "model": {
                        "modelFormat": {"name": "sklearn"},
                        "storageUri": "gs://my-bucket/my-model",
                    }
                }
            },
        }
        client = KServeClient()
        inferenceservice = client.get("my-inference-service")
        mock_get.assert_called_with(
            group="serving.kserve.io",
            version="v1beta1",
            plural="inferenceservices",
            name="my-inference-service",
            namespace="default",
        )
        assert inferenceservice.metadata["name"] == "my-inference-service"
        assert inferenceservice.spec.predictor.model.model_format.name == "sklearn"


def test_kserve_client_list():
    """Tests the list method of the KServeClient."""
    with patch(
        "kubeflow.core.base_client.KubeconfigAuthProvider"
    ) as mock_auth_provider, patch(
        "kubeflow.core.base_client.BaseClient.list_custom_resources"
    ) as mock_list:
        mock_auth_provider.return_value.get_api_client_configuration.return_value = (
            fake_conf
        )
        mock_list.return_value = [
            {
                "apiVersion": "serving.kserve.io/v1beta1",
                "kind": "InferenceService",
                "metadata": {"name": "my-inference-service"},
                "spec": {
                    "predictor": {
                        "model": {
                            "modelFormat": {"name": "sklearn"},
                            "storageUri": "gs://my-bucket/my-model",
                        }
                    }
                },
            }
        ]
        client = KServeClient()
        inferenceservices = client.list()
        mock_list.assert_called_with(
            group="serving.kserve.io",
            version="v1beta1",
            plural="inferenceservices",
            namespace="default",
        )
        assert len(inferenceservices) == 1
        assert inferenceservices[0].metadata["name"] == "my-inference-service"


def test_kserve_client_update():
    """Tests the update method of the KServeClient."""
    inferenceservice = InferenceService(
        name="my-inference-service",
        predictor=PredictorSpec(
            model=ModelSpec(
                modelFormat=ModelFormat(name="sklearn"),
                storageUri="gs://my-bucket/my-model",
            )
        ),
    )

    with patch(
        "kubeflow.core.base_client.KubeconfigAuthProvider"
    ) as mock_auth_provider, patch(
        "kubeflow.core.base_client.BaseClient.patch_custom_resource"
    ) as mock_patch:
        mock_auth_provider.return_value.get_api_client_configuration.return_value = (
            fake_conf
        )
        client = KServeClient()
        client.update(inferenceservice)
        mock_patch.assert_called_with(
            group="serving.kserve.io",
            version="v1beta1",
            plural="inferenceservices",
            name="my-inference-service",
            body=inferenceservice.model_dump(by_alias=True, exclude_none=True),
            namespace="default",
        )


def test_kserve_client_delete():
    """Tests the delete method of the KServeClient."""
    with patch(
        "kubeflow.core.base_client.KubeconfigAuthProvider"
    ) as mock_auth_provider, patch(
        "kubeflow.core.base_client.BaseClient.delete_custom_resource"
    ) as mock_delete:
        mock_auth_provider.return_value.get_api_client_configuration.return_value = (
            fake_conf
        )
        client = KServeClient()
        client.delete("my-inference-service")
        mock_delete.assert_called_with(
            group="serving.kserve.io",
            version="v1beta1",
            plural="inferenceservices",
            name="my-inference-service",
            namespace="default",
        )
