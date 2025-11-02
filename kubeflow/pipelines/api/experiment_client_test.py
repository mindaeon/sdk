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

from unittest import mock

from kubeflow.pipelines.api.experiment_client import ExperimentClient


@mock.patch("kubeflow.core.base_client.client")
@mock.patch("kubeflow.core.base_client.KubeconfigAuthProvider")
def test_create_experiment(mock_auth_provider, mock_k8s_client):
    """Tests creating an experiment."""
    client = ExperimentClient()
    client.api_client.call_api.return_value = {
        "experiment_id": "test-experiment",
        "display_name": "test-experiment",
        "created_at": "2025-01-01T00:00:00Z",
    }
    client.create_experiment("test-experiment")
    client.api_client.call_api.assert_called_with(
        "/apis/v2beta1/experiments",
        "POST",
        body={"display_name": "test-experiment", "description": None},
        query_params={},
    )


@mock.patch("kubeflow.core.base_client.client")
@mock.patch("kubeflow.core.base_client.KubeconfigAuthProvider")
def test_get_experiment(mock_auth_provider, mock_k8s_client):
    """Tests getting an experiment."""
    client = ExperimentClient()
    client.api_client.call_api.return_value = {
        "experiment_id": "test-experiment",
        "display_name": "test-experiment",
        "created_at": "2025-01-01T00:00:00Z",
    }
    client.get_experiment("test-experiment")
    client.api_client.call_api.assert_called_with(
        "/apis/v2beta1/experiments/test-experiment", "GET"
    )


@mock.patch("kubeflow.core.base_client.client")
@mock.patch("kubeflow.core.base_client.KubeconfigAuthProvider")
def test_list_experiments(mock_auth_provider, mock_k8s_client):
    """Tests listing experiments."""
    client = ExperimentClient()
    client.api_client.call_api.return_value = {"experiments": []}
    client.list_experiments()
    client.api_client.call_api.assert_called_with(
        "/apis/v2beta1/experiments", "GET"
    )


@mock.patch("kubeflow.core.base_client.client")
@mock.patch("kubeflow.core.base_client.KubeconfigAuthProvider")
def test_delete_experiment(mock_auth_provider, mock_k8s_client):
    """Tests deleting an experiment."""
    client = ExperimentClient()
    client.delete_experiment("test-experiment")
    client.api_client.call_api.assert_called_with(
        "/apis/v2beta1/experiments/test-experiment", "DELETE"
    )


@mock.patch("kubeflow.core.base_client.client")
@mock.patch("kubeflow.core.base_client.KubeconfigAuthProvider")
def test_archive_experiment(mock_auth_provider, mock_k8s_client):
    """Tests archiving an experiment."""
    client = ExperimentClient()
    client.archive_experiment("test-experiment")
    client.api_client.call_api.assert_called_with(
        "/apis/v2beta1/experiments/test-experiment:archive", "POST"
    )


@mock.patch("kubeflow.core.base_client.client")
@mock.patch("kubeflow.core.base_client.KubeconfigAuthProvider")
def test_unarchive_experiment(mock_auth_provider, mock_k8s_client):
    """Tests unarchiving an experiment."""
    client = ExperimentClient()
    client.unarchive_experiment("test-experiment")
    client.api_client.call_api.assert_called_with(
        "/apis/v2beta1/experiments/test-experiment:unarchive", "POST"
    )
