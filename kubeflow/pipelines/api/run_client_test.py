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

from kubeflow.pipelines.api.run_client import RunClient
from kubeflow.pipelines.types.run_types import PipelineVersionReference


@mock.patch("kubeflow.core.base_client.client")
@mock.patch("kubeflow.core.base_client.KubeconfigAuthProvider")
def test_create_run(mock_auth_provider, mock_k8s_client):
    """Tests creating a run."""
    client = RunClient()
    client.api_client.call_api.return_value = {
        "run_id": "test-run",
        "display_name": "test-run",
        "created_at": "2025-01-01T00:00:00Z",
        "state": "PENDING",
    }
    client.create_run(
        "test-run",
        PipelineVersionReference(
            pipeline_id="test-pipeline", pipeline_version_id="test-version"
        ),
    )
    client.api_client.call_api.assert_called_with(
        "/apis/v2beta1/runs",
        "POST",
        body={
            "display_name": "test-run",
            "pipeline_version_reference": {
                "pipeline_id": "test-pipeline",
                "pipeline_version_id": "test-version",
            },
            "runtime_config": {},
        },
        query_params={},
    )


@mock.patch("kubeflow.core.base_client.client")
@mock.patch("kubeflow.core.base_client.KubeconfigAuthProvider")
def test_get_run(mock_auth_provider, mock_k8s_client):
    """Tests getting a run."""
    client = RunClient()
    client.api_client.call_api.return_value = {
        "run_id": "test-run",
        "display_name": "test-run",
        "created_at": "2025-01-01T00:00:00Z",
        "state": "SUCCEEDED",
    }
    client.get_run("test-run")
    client.api_client.call_api.assert_called_with(
        "/apis/v2beta1/runs/test-run", "GET"
    )


@mock.patch("kubeflow.core.base_client.client")
@mock.patch("kubeflow.core.base_client.KubeconfigAuthProvider")
def test_list_runs(mock_auth_provider, mock_k8s_client):
    """Tests listing runs."""
    client = RunClient()
    client.api_client.call_api.return_value = {"runs": []}
    client.list_runs()
    client.api_client.call_api.assert_called_with("/apis/v2beta1/runs", "GET")


@mock.patch("kubeflow.core.base_client.client")
@mock.patch("kubeflow.core.base_client.KubeconfigAuthProvider")
def test_delete_run(mock_auth_provider, mock_k8s_client):
    """Tests deleting a run."""
    client = RunClient()
    client.delete_run("test-run")
    client.api_client.call_api.assert_called_with(
        "/apis/v2beta1/runs/test-run", "DELETE"
    )


@mock.patch("kubeflow.core.base_client.client")
@mock.patch("kubeflow.core.base_client.KubeconfigAuthProvider")
def test_archive_run(mock_auth_provider, mock_k8s_client):
    """Tests archiving a run."""
    client = RunClient()
    client.archive_run("test-run")
    client.api_client.call_api.assert_called_with(
        "/apis/v2beta1/runs/test-run:archive", "POST"
    )


@mock.patch("kubeflow.core.base_client.client")
@mock.patch("kubeflow.core.base_client.KubeconfigAuthProvider")
def test_unarchive_run(mock_auth_provider, mock_k8s_client):
    """Tests unarchiving a run."""
    client = RunClient()
    client.unarchive_run("test-run")
    client.api_client.call_api.assert_called_with(
        "/apis/v2beta1/runs/test-run:unarchive", "POST"
    )


@mock.patch("kubeflow.core.base_client.client")
@mock.patch("kubeflow.core.base_client.KubeconfigAuthProvider")
def test_retry_run(mock_auth_provider, mock_k8s_client):
    """Tests retrying a run."""
    client = RunClient()
    client.retry_run("test-run")
    client.api_client.call_api.assert_called_with(
        "/apis/v2beta1/runs/test-run:retry", "POST"
    )


@mock.patch("kubeflow.core.base_client.client")
@mock.patch("kubeflow.core.base_client.KubeconfigAuthProvider")
def test_terminate_run(mock_auth_provider, mock_k8s_client):
    """Tests terminating a run."""
    client = RunClient()
    client.terminate_run("test-run")
    client.api_client.call_api.assert_called_with(
        "/apis/v2beta1/runs/test-run:terminate", "POST"
    )
