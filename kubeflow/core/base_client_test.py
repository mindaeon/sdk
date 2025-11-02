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

"""Unit tests for kubeflow.core.base_client and helper methods."""

from unittest.mock import patch

from kubernetes import client
import pytest

from kubeflow.core.base_client import BaseClient
from kubeflow.core.config import KubeflowConfig
from kubeflow.core.k8s_resource import K8sResource

# A sample Kubernetes resource dictionary for testing
SAMPLE_RESOURCE = {
    "apiVersion": "v1",
    "kind": "Pod",
    "metadata": {"name": "test-pod"},
}


@pytest.fixture
def base_cfg():
    """Fixture to create a default KubeflowConfig."""
    cfg = KubeflowConfig()
    return cfg


def test_kubeconfig_auth_provider_selected(base_cfg):
    """Ensure BaseClient uses KubeconfigAuthProvider when configured."""
    base_cfg.auth.provider = "kubeconfig"
    fake_conf = client.Configuration()

    with (
        patch("kubeflow.core.base_client.KubeconfigAuthProvider") as mock_provider,
        patch("kubeflow.core.base_client.client.ApiClient") as mock_api_client,
    ):
        mock_provider.return_value.get_api_client_configuration.return_value = fake_conf
        base = BaseClient(base_cfg)
        mock_provider.assert_called_once()
        mock_api_client.assert_called_once_with(fake_conf)
        assert base.api_client == mock_api_client.return_value
        assert base.config.auth.provider == "kubeconfig"


def test_incluster_auth_provider_selected(base_cfg):
    """Ensure BaseClient uses InClusterAuthProvider when configured."""
    base_cfg.auth.provider = "incluster"
    fake_conf = client.Configuration()

    with (
        patch("kubeflow.core.base_client.InClusterAuthProvider") as mock_provider,
        patch("kubeflow.core.base_client.client.ApiClient") as mock_api_client,
    ):
        mock_provider.return_value.get_api_client_configuration.return_value = fake_conf
        base = BaseClient(base_cfg)
        mock_provider.assert_called_once()
        mock_api_client.assert_called_once_with(fake_conf)
        assert base.api_client == mock_api_client.return_value
        assert base.config.auth.provider == "incluster"


def test_invalid_provider_raises(base_cfg):
    """Ensure ValueError is raised for invalid auth provider."""
    base_cfg.auth.provider = "invalid"
    with pytest.raises(ValueError) as excinfo:
        BaseClient(base_cfg)
    assert "Invalid auth provider" in str(excinfo.value)


# ---------------------------------------------------------------------------
# Extended Tests for Custom Resource Helper Methods
# ---------------------------------------------------------------------------


@patch("kubeflow.core.base_client.client.CustomObjectsApi")
@patch("kubeflow.core.base_client.KubeconfigAuthProvider")
def test_get_custom_resource(mock_auth_provider, mock_custom_api_class):
    """Verify that get_custom_resource delegates correctly to CustomObjectsApi."""
    mock_auth_provider.return_value.get_api_client_configuration.return_value = (
        client.Configuration()
    )
    mock_custom_api_instance = mock_custom_api_class.return_value
    mock_custom_api_instance.get_namespaced_custom_object.return_value = SAMPLE_RESOURCE

    base = BaseClient()
    resource = base.get_custom_resource(
        group="testgroup", version="v1", plural="tests", name="test-resource"
    )

    mock_custom_api_instance.get_namespaced_custom_object.assert_called_once()
    assert isinstance(resource, K8sResource)
    assert resource.name == "test-pod"


@patch("kubeflow.core.base_client.client.CustomObjectsApi")
@patch("kubeflow.core.base_client.KubeconfigAuthProvider")
def test_list_custom_resources(mock_auth_provider, mock_custom_api_class):
    """Verify that list_custom_resources delegates correctly."""
    mock_auth_provider.return_value.get_api_client_configuration.return_value = (
        client.Configuration()
    )
    mock_custom_api_instance = mock_custom_api_class.return_value
    mock_custom_api_instance.list_namespaced_custom_object.return_value = {
        "items": [SAMPLE_RESOURCE]
    }

    base = BaseClient()
    resources = base.list_custom_resources(group="testgroup", version="v1", plural="tests")

    mock_custom_api_instance.list_namespaced_custom_object.assert_called_once()
    assert len(resources) == 1
    assert resources[0].name == "test-pod"


@patch("kubeflow.core.base_client.client.CustomObjectsApi")
@patch("kubeflow.core.base_client.KubeconfigAuthProvider")
def test_create_custom_resource(mock_auth_provider, mock_custom_api_class):
    """Verify create_custom_resource delegates correctly."""
    mock_auth_provider.return_value.get_api_client_configuration.return_value = (
        client.Configuration()
    )
    mock_custom_api_instance = mock_custom_api_class.return_value
    mock_custom_api_instance.create_namespaced_custom_object.return_value = SAMPLE_RESOURCE

    base = BaseClient()
    resource = base.create_custom_resource(
        group="testgroup",
        version="v1",
        plural="tests",
        body=SAMPLE_RESOURCE,
    )

    mock_custom_api_instance.create_namespaced_custom_object.assert_called_once()
    assert isinstance(resource, K8sResource)
    assert resource.name == "test-pod"


@patch("kubeflow.core.base_client.client.CustomObjectsApi")
@patch("kubeflow.core.base_client.KubeconfigAuthProvider")
def test_delete_custom_resource(mock_auth_provider, mock_custom_api_class):
    """Verify delete_custom_resource delegates correctly."""
    mock_auth_provider.return_value.get_api_client_configuration.return_value = (
        client.Configuration()
    )
    mock_custom_api_instance = mock_custom_api_class.return_value
    mock_custom_api_instance.delete_namespaced_custom_object.return_value = {"status": "Success"}

    base = BaseClient()
    response = base.delete_custom_resource(
        group="testgroup",
        version="v1",
        plural="tests",
        name="test-resource",
    )

    mock_custom_api_instance.delete_namespaced_custom_object.assert_called_once()
    assert response == {"status": "Success"}
