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

from unittest import mock

from kubeflow.pipelines.api.pipeline_client import PipelineClient


@mock.patch("kubeflow.core.base_client.client")
@mock.patch("kubeflow.core.base_client.KubeconfigAuthProvider")
def test_create_pipeline(mock_auth_provider, mock_k8s_client):
    """Tests creating a pipeline."""
    client = PipelineClient()
    client.api_client.call_api.return_value = {
        "pipeline_id": "test-pipeline",
        "display_name": "test-pipeline",
        "name": "test-pipeline",
        "created_at": "2025-01-01T00:00:00Z",
    }
    client.create_pipeline("test-pipeline")
    client.api_client.call_api.assert_called_with(
        "/apis/v2beta1/pipelines",
        "POST",
        body={"display_name": "test-pipeline", "description": None},
        query_params={},
    )


@mock.patch("kubeflow.core.base_client.client")
@mock.patch("kubeflow.core.base_client.KubeconfigAuthProvider")
def test_create_pipeline_version(mock_auth_provider, mock_k8s_client):
    """Tests creating a pipeline version."""
    client = PipelineClient()
    client.api_client.call_api.return_value = {
        "pipeline_id": "test-pipeline",
        "pipeline_version_id": "test-version",
        "display_name": "test-version",
        "created_at": "2025-01-01T00:00:00Z",
    }
    client.create_pipeline_version(
        "test-pipeline", "test-version", "http://example.com"
    )
    client.api_client.call_api.assert_called_with(
        "/apis/v2beta1/pipelines/test-pipeline/versions",
        "POST",
        body={
            "display_name": "test-version",
            "package_url": {"pipeline_url": "http://example.com"},
            "description": None,
        },
    )


@mock.patch("kubeflow.core.base_client.client")
@mock.patch("kubeflow.core.base_client.KubeconfigAuthProvider")
def test_get_pipeline(mock_auth_provider, mock_k8s_client):
    """Tests getting a pipeline."""
    client = PipelineClient()
    client.api_client.call_api.return_value = {
        "pipeline_id": "test-pipeline",
        "display_name": "test-pipeline",
        "name": "test-pipeline",
        "created_at": "2025-01-01T00:00:00Z",
    }
    client.get_pipeline("test-pipeline")
    client.api_client.call_api.assert_called_with(
        "/apis/v2beta1/pipelines/test-pipeline", "GET"
    )


@mock.patch("kubeflow.core.base_client.client")
@mock.patch("kubeflow.core.base_client.KubeconfigAuthProvider")
def test_list_pipelines(mock_auth_provider, mock_k8s_client):
    """Tests listing pipelines."""
    client = PipelineClient()
    client.api_client.call_api.return_value = {"pipelines": []}
    client.list_pipelines()
    client.api_client.call_api.assert_called_with(
        "/apis/v2beta1/pipelines", "GET"
    )


@mock.patch("kubeflow.core.base_client.client")
@mock.patch("kubeflow.core.base_client.KubeconfigAuthProvider")
def test_delete_pipeline(mock_auth_provider, mock_k8s_client):
    """Tests deleting a pipeline."""
    client = PipelineClient()
    client.delete_pipeline("test-pipeline")
    client.api_client.call_api.assert_called_with(
        "/apis/v2beta1/pipelines/test-pipeline", "DELETE"
    )


@mock.patch("kubeflow.core.base_client.client")
@mock.patch("kubeflow.core.base_client.KubeconfigAuthProvider")
def test_get_pipeline_version(mock_auth_provider, mock_k8s_client):
    """Tests getting a pipeline version."""
    client = PipelineClient()
    client.api_client.call_api.return_value = {
        "pipeline_id": "test-pipeline",
        "pipeline_version_id": "test-version",
        "display_name": "test-version",
        "created_at": "2025-01-01T00:00:00Z",
    }
    client.get_pipeline_version("test-pipeline", "test-version")
    client.api_client.call_api.assert_called_with(
        "/apis/v2beta1/pipelines/test-pipeline/versions/test-version", "GET"
    )


@mock.patch("kubeflow.core.base_client.client")
@mock.patch("kubeflow.core.base_client.KubeconfigAuthProvider")
def test_list_pipeline_versions(mock_auth_provider, mock_k8s_client):
    """Tests listing pipeline versions."""
    client = PipelineClient()
    client.api_client.call_api.return_value = {"pipeline_versions": []}
    client.list_pipeline_versions("test-pipeline")
    client.api_client.call_api.assert_called_with(
        "/apis/v2beta1/pipelines/test-pipeline/versions", "GET"
    )
