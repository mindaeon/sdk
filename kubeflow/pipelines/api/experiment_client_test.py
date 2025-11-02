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

from unittest.mock import MagicMock, patch

from kubernetes import client
import pytest

from kubeflow.core.config import KubeflowConfig
from kubeflow.pipelines.api.experiment_client import ExperimentClient


@pytest.fixture
def fake_config():
    """Returns a fake KubeflowConfig object."""
    cfg = KubeflowConfig()
    cfg.auth.provider = "kubeconfig"
    return cfg


def test_create_experiment(fake_config):
    """Tests the create_experiment method."""
    with (
        patch("kubeflow.core.base_client.KubeconfigAuthProvider") as mock_auth_provider,
        patch("kubeflow.core.base_client.client.ApiClient") as mock_api_client,
    ):
        mock_auth_provider.return_value.get_api_client_configuration.return_value = (
            client.Configuration()
        )
        mock_api_client.return_value.call_api = MagicMock()

        experiment_client = ExperimentClient(config=fake_config)
        experiment_client.create_experiment("test-experiment")

        experiment_client.api_client.call_api.assert_called_with(
            "/apis/v2beta1/experiments",
            "POST",
            body={"display_name": "test-experiment"},
        )


def test_get_experiment(fake_config):
    """Tests the get_experiment method."""
    with (
        patch("kubeflow.core.base_client.KubeconfigAuthProvider") as mock_auth_provider,
        patch("kubeflow.core.base_client.client.ApiClient") as mock_api_client,
    ):
        mock_auth_provider.return_value.get_api_client_configuration.return_value = (
            client.Configuration()
        )
        mock_api_client.return_value.call_api = MagicMock()
        experiment_client = ExperimentClient(config=fake_config)
        experiment_client.get_experiment("test-experiment-id")

        experiment_client.api_client.call_api.assert_called_with(
            "/apis/v2beta1/experiments/test-experiment-id", "GET"
        )


def test_list_experiments(fake_config):
    """Tests the list_experiments method."""
    with (
        patch("kubeflow.core.base_client.KubeconfigAuthProvider") as mock_auth_provider,
        patch("kubeflow.core.base_client.client.ApiClient") as mock_api_client,
    ):
        mock_auth_provider.return_value.get_api_client_configuration.return_value = (
            client.Configuration()
        )
        mock_api_client.return_value.call_api = MagicMock()
        experiment_client = ExperimentClient(config=fake_config)
        experiment_client.list_experiments()

        experiment_client.api_client.call_api.assert_called_with("/apis/v2beta1/experiments", "GET")


def test_delete_experiment(fake_config):
    """Tests the delete_experiment method."""
    with (
        patch("kubeflow.core.base_client.KubeconfigAuthProvider") as mock_auth_provider,
        patch("kubeflow.core.base_client.client.ApiClient") as mock_api_client,
    ):
        mock_auth_provider.return_value.get_api_client_configuration.return_value = (
            client.Configuration()
        )
        mock_api_client.return_value.call_api = MagicMock()
        experiment_client = ExperimentClient(config=fake_config)
        experiment_client.delete_experiment("test-experiment-id")

        experiment_client.api_client.call_api.assert_called_with(
            "/apis/v2beta1/experiments/test-experiment-id", "DELETE"
        )
