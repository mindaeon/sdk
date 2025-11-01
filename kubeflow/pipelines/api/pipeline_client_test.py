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

from unittest.mock import patch, mock_open, MagicMock

import pytest
from kubernetes import client
from kubeflow.core.config import KubeflowConfig
from kubeflow.pipelines.api.pipeline_client import PipelineClient


@pytest.fixture
def fake_config():
    """Returns a fake KubeflowConfig object."""
    cfg = KubeflowConfig()
    cfg.auth.provider = "kubeconfig"
    return cfg


def test_create_pipeline(fake_config):
    """Tests the create_pipeline method."""
    with patch(
        "kubeflow.core.base_client.KubeconfigAuthProvider"
    ) as mock_auth_provider, patch(
        "builtins.open", mock_open(read_data=b"test-data")
    ), patch(
        "kubeflow.core.base_client.client.ApiClient"
    ) as mock_api_client:
        mock_auth_provider.return_value.get_api_client_configuration.return_value = (
            client.Configuration()
        )
        mock_api_client.return_value.call_api = MagicMock()

        pipeline_client = PipelineClient(config=fake_config)
        pipeline_client.create_pipeline("test-pipeline", "test.zip")

        pipeline_client.api_client.call_api.assert_called_with(
            "/apis/v2beta1/pipelines/upload",
            "POST",
            query_params=[("name", "test-pipeline")],
            body=b"test-data",
            header_params={"Content-Type": "application/zip"},
            _preload_content=False,
        )


def test_get_pipeline(fake_config):
    """Tests the get_pipeline method."""
    with patch(
        "kubeflow.core.base_client.KubeconfigAuthProvider"
    ) as mock_auth_provider, patch(
        "kubeflow.core.base_client.client.ApiClient"
    ) as mock_api_client:
        mock_auth_provider.return_value.get_api_client_configuration.return_value = (
            client.Configuration()
        )
        mock_api_client.return_value.call_api = MagicMock()
        pipeline_client = PipelineClient(config=fake_config)
        pipeline_client.get_pipeline("test-pipeline-id")

        pipeline_client.api_client.call_api.assert_called_with(
            "/apis/v2beta1/pipelines/test-pipeline-id", "GET"
        )


def test_list_pipelines(fake_config):
    """Tests the list_pipelines method."""
    with patch(
        "kubeflow.core.base_client.KubeconfigAuthProvider"
    ) as mock_auth_provider, patch(
        "kubeflow.core.base_client.client.ApiClient"
    ) as mock_api_client:
        mock_auth_provider.return_value.get_api_client_configuration.return_value = (
            client.Configuration()
        )
        mock_api_client.return_value.call_api = MagicMock()
        pipeline_client = PipelineClient(config=fake_config)
        pipeline_client.list_pipelines()

        pipeline_client.api_client.call_api.assert_called_with(
            "/apis/v2beta1/pipelines", "GET"
        )


def test_delete_pipeline(fake_config):
    """Tests the delete_pipeline method."""
    with patch(
        "kubeflow.core.base_client.KubeconfigAuthProvider"
    ) as mock_auth_provider, patch(
        "kubeflow.core.base_client.client.ApiClient"
    ) as mock_api_client:
        mock_auth_provider.return_value.get_api_client_configuration.return_value = (
            client.Configuration()
        )
        mock_api_client.return_value.call_api = MagicMock()
        pipeline_client = PipelineClient(config=fake_config)
        pipeline_client.delete_pipeline("test-pipeline-id")

        pipeline_client.api_client.call_api.assert_called_with(
            "/apis/v2beta1/pipelines/test-pipeline-id", "DELETE"
        )


def test_get_pipeline_by_name(fake_config):
    """Tests the get_pipeline_by_name method."""
    with patch(
        "kubeflow.core.base_client.KubeconfigAuthProvider"
    ) as mock_auth_provider, patch(
        "kubeflow.core.base_client.client.ApiClient"
    ) as mock_api_client:
        mock_auth_provider.return_value.get_api_client_configuration.return_value = (
            client.Configuration()
        )
        mock_api_client.return_value.call_api = MagicMock(
            return_value={
                "pipelines": [
                    {"pipeline_id": "1", "display_name": "pipeline-1"},
                    {"pipeline_id": "2", "display_name": "pipeline-2"},
                ]
            }
        )
        pipeline_client = PipelineClient(config=fake_config)
        pipeline_client.get_pipeline_by_name("pipeline-2")

        pipeline_client.api_client.call_api.assert_any_call(
            "/apis/v2beta1/pipelines", "GET"
        )
        pipeline_client.api_client.call_api.assert_called_with(
            "/apis/v2beta1/pipelines/2", "GET"
        )
