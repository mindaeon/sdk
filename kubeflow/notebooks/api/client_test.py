# Copyright 2024 The Kubeflow Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from unittest import mock

from kubeflow.core.k8s_resource import K8sResource
from kubeflow.notebooks.api.client import NotebookClient
from kubeflow.notebooks.models import Notebook


@mock.patch("kubeflow.core.base_client.client.ApiClient")
@mock.patch("kubeflow.core.base_client.KubeconfigAuthProvider")
@mock.patch("kubeflow.notebooks.api.client.NotebookClient.create_custom_resource")
def test_create_notebook(mock_create_custom_resource, mock_auth_provider, _mock_api_client):
    """Tests creating a notebook."""
    # Arrange
    client = NotebookClient()
    notebook = Notebook(name="test-notebook")
    mock_create_custom_resource.return_value = K8sResource(
        apiVersion="kubeflow.org/v1",
        kind="Notebook",
        metadata={"name": "test-notebook"},
    )

    # Act
    client.create(notebook)

    # Assert
    mock_create_custom_resource.assert_called_with(
        group="kubeflow.org",
        version="v1",
        plural="notebooks",
        body=notebook.model_dump(),
        namespace=None,
    )


@mock.patch("kubeflow.core.base_client.client.ApiClient")
@mock.patch("kubeflow.core.base_client.KubeconfigAuthProvider")
@mock.patch("kubeflow.notebooks.api.client.NotebookClient.get_custom_resource")
def test_get_notebook(mock_get_custom_resource, mock_auth_provider, _mock_api_client):
    """Tests getting a notebook."""
    # Arrange
    client = NotebookClient()
    mock_get_custom_resource.return_value = K8sResource(
        apiVersion="kubeflow.org/v1",
        kind="Notebook",
        metadata={"name": "test-notebook"},
    )

    # Act
    client.ge("test-notebook")

    # Assert
    mock_get_custom_resource.assert_called_with(
        group="kubeflow.org",
        version="v1",
        plural="notebooks",
        name="test-notebook",
        namespace=None,
    )


@mock.patch("kubeflow.core.base_client.client.ApiClient")
@mock.patch("kubeflow.core.base_client.KubeconfigAuthProvider")
@mock.patch("kubeflow.notebooks.api.client.NotebookClient.list_custom_resources")
def test_list_notebooks(mock_list_custom_resources, mock_auth_provider, _mock_api_client):
    """Tests listing notebooks."""
    # Arrange
    client = NotebookClient()
    mock_list_custom_resources.return_value = {"items": []}

    # Act
    client.list()

    # Assert
    mock_list_custom_resources.assert_called_with(
        group="kubeflow.org",
        version="v1",
        plural="notebooks",
        namespace=None,
    )


@mock.patch("kubeflow.core.base_client.client.ApiClient")
@mock.patch("kubeflow.core.base_client.KubeconfigAuthProvider")
@mock.patch("kubeflow.notebooks.api.client.NotebookClient.delete_custom_resource")
def test_delete_notebook(mock_delete_custom_resource, mock_auth_provider, _mock_api_client):
    """Tests deleting a notebook."""
    # Arrange
    client = NotebookClient()

    # Act
    client.delete("test-notebook")

    # Assert
    mock_delete_custom_resource.assert_called_with(
        group="kubeflow.org",
        version="v1",
        plural="notebooks",
        name="test-notebook",
        namespace=None,
    )
