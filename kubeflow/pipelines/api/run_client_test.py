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
from kubeflow.pipelines.api.run_client import RunClient
from kubeflow.pipelines.types.run_types import Run, RunState


@pytest.fixture
def fake_config():
    """Returns a fake KubeflowConfig object."""
    cfg = KubeflowConfig()
    cfg.auth.provider = "kubeconfig"
    return cfg


def test_create_run(fake_config):
    """Tests the create_run method."""
    with (
        patch("kubeflow.core.base_client.KubeconfigAuthProvider") as mock_auth_provider,
        patch("kubeflow.core.base_client.client.ApiClient") as mock_api_client,
    ):
        mock_auth_provider.return_value.get_api_client_configuration.return_value = (
            client.Configuration()
        )
        mock_api_client.return_value.call_api = MagicMock()

        run_client = RunClient(config=fake_config)
        run_client.create_run("test-pipeline-id", "test-run")

        run_client.api_client.call_api.assert_called_with(
            "/apis/v2beta1/runs",
            "POST",
            body={
                "display_name": "test-run",
                "pipeline_version_reference": {"pipeline_id": "test-pipeline-id"},
            },
        )


def test_get_run(fake_config):
    """Tests the get_run method."""
    with (
        patch("kubeflow.core.base_client.KubeconfigAuthProvider") as mock_auth_provider,
        patch("kubeflow.core.base_client.client.ApiClient") as mock_api_client,
    ):
        mock_auth_provider.return_value.get_api_client_configuration.return_value = (
            client.Configuration()
        )
        mock_api_client.return_value.call_api = MagicMock(
            return_value={
                "run_id": "test-run-id",
                "name": "test-run",
                "display_name": "test-run",
                "created_at": "2025-01-01T00:00:00Z",
                "state": "RUNNING",
            }
        )
        run_client = RunClient(config=fake_config)
        run_client.get_run("test-run-id")

        run_client.api_client.call_api.assert_called_with("/apis/v2beta1/runs/test-run-id", "GET")


def test_list_runs(fake_config):
    """Tests the list_runs method."""
    with (
        patch("kubeflow.core.base_client.KubeconfigAuthProvider") as mock_auth_provider,
        patch("kubeflow.core.base_client.client.ApiClient") as mock_api_client,
    ):
        mock_auth_provider.return_value.get_api_client_configuration.return_value = (
            client.Configuration()
        )
        mock_api_client.return_value.call_api = MagicMock()
        run_client = RunClient(config=fake_config)
        run_client.list_runs()

        run_client.api_client.call_api.assert_called_with("/apis/v2beta1/runs", "GET")


def test_delete_run(fake_config):
    """Tests the delete_run method."""
    with (
        patch("kubeflow.core.base_client.KubeconfigAuthProvider") as mock_auth_provider,
        patch("kubeflow.core.base_client.client.ApiClient") as mock_api_client,
    ):
        mock_auth_provider.return_value.get_api_client_configuration.return_value = (
            client.Configuration()
        )
        mock_api_client.return_value.call_api = MagicMock()
        run_client = RunClient(config=fake_config)
        run_client.delete_run("test-run-id")

        run_client.api_client.call_api.assert_called_with(
            "/apis/v2beta1/runs/test-run-id", "DELETE"
        )


def test_wait_for_run_completion_success(fake_config):
    """Tests the wait_for_run_completion method for a successful run."""
    with (
        patch("kubeflow.core.base_client.KubeconfigAuthProvider") as mock_auth_provider,
        patch("kubeflow.core.base_client.client.ApiClient") as mock_api_client,
        patch("time.sleep"),
    ):
        mock_auth_provider.return_value.get_api_client_configuration.return_value = (
            client.Configuration()
        )
        mock_api_client.return_value.call_api = MagicMock()
        run_client = RunClient(config=fake_config)
        run_client.get_run = MagicMock(
            side_effect=[
                Run(
                    run_id="test-run-id",
                    name="test-run",
                    created_at="2025-01-01T00:00:00Z",
                    state=RunState.RUNNING,
                ),
                Run(
                    run_id="test-run-id",
                    name="test-run",
                    created_at="2025-01-01T00:00:00Z",
                    state=RunState.SUCCEEDED,
                ),
            ]
        )
        run = run_client.wait_for_run_completion("test-run-id")
        assert run.state == RunState.SUCCEEDED


def test_wait_for_run_completion_failure(fake_config):
    """Tests the wait_for_run_completion method for a failed run."""
    with (
        patch("kubeflow.core.base_client.KubeconfigAuthProvider") as mock_auth_provider,
        patch("kubeflow.core.base_client.client.ApiClient") as mock_api_client,
        patch("time.sleep"),
    ):
        mock_auth_provider.return_value.get_api_client_configuration.return_value = (
            client.Configuration()
        )
        mock_api_client.return_value.call_api = MagicMock()
        run_client = RunClient(config=fake_config)
        run_client.get_run = MagicMock(
            side_effect=[
                Run(
                    run_id="test-run-id",
                    name="test-run",
                    created_at="2025-01-01T00:00:00Z",
                    state=RunState.RUNNING,
                ),
                Run(
                    run_id="test-run-id",
                    name="test-run",
                    created_at="2025-01-01T00:00:00Z",
                    state=RunState.FAILED,
                ),
            ]
        )
        run = run_client.wait_for_run_completion("test-run-id")
        assert run.state == RunState.FAILED


def test_wait_for_run_completion_timeout(fake_config):
    """Tests the wait_for_run_completion method for a timeout."""
    with (
        patch("kubeflow.core.base_client.KubeconfigAuthProvider") as mock_auth_provider,
        patch("kubeflow.core.base_client.client.ApiClient") as mock_api_client,
        patch("time.sleep"),
    ):
        mock_auth_provider.return_value.get_api_client_configuration.return_value = (
            client.Configuration()
        )
        mock_api_client.return_value.call_api = MagicMock()
        run_client = RunClient(config=fake_config)
        run_client.get_run = MagicMock(
            return_value=Run(
                run_id="test-run-id",
                name="test-run",
                created_at="2025-01-01T00:00:00Z",
                state=RunState.RUNNING,
            )
        )
        with pytest.raises(TimeoutError):
            run_client.wait_for_run_completion("test-run-id", timeout=1)
