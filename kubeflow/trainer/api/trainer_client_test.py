# Copyright 2023 The Kubeflow Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may not use this file except in compliance with the License.
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

import pytest

from kubeflow.trainer import TrainingClient, types

# TODO(Bobgy): test the real API server instead of mocking the client.

fake_conf = MagicMock()


def test_list_jobs():
    with (
        patch("kubeflow.core.base_client.KubeconfigAuthProvider") as mock_auth_provider,
        patch("kubeflow.core.base_client.client.ApiClient") as _mock_api_client,
        patch("kubeflow.core.base_client.client.CustomObjectsApi") as mock_custom_api,
    ):
        mock_auth_provider.return_value.get_api_client_configuration.return_value = fake_conf
        mock_custom_api.return_value.list_namespaced_custom_object.return_value = {
            "items": [
                {
                    "metadata": {"name": "test-job"},
                    "spec": {},
                    "status": {"phase": "Running"},
                }
            ]
        }
        client = TrainingClient()
        jobs = client.list_jobs(namespace="my-namespace")
        mock_custom_api.return_value.list_namespaced_custom_object.assert_called_with(
            group="kubeflow.org",
            namespace="my-namespace",
            plural="trainingjobs",
            version="v1alpha1",
        )
        assert jobs == [
            types.TrainJob(
                name="test-job",
                spec=types.TrainJobSpec(),
                status=types.TrainJobStatus(phase="Running"),
            )
        ]


def test_get_job():
    with (
        patch("kubeflow.core.base_client.KubeconfigAuthProvider") as mock_auth_provider,
        patch("kubeflow.core.base_client.client.ApiClient") as _mock_api_client,
        patch("kubeflow.core.base_client.client.CustomObjectsApi") as mock_custom_api,
    ):
        mock_auth_provider.return_value.get_api_client_configuration.return_value = fake_conf
        mock_custom_api.return_value.get_namespaced_custom_object.return_value = {
            "metadata": {"name": "test-job"},
            "spec": {},
            "status": {"phase": "Running"},
        }
        client = TrainingClient()
        job = client.get_job(name="test-job", namespace="my-namespace")
        mock_custom_api.return_value.get_namespaced_custom_object.assert_called_with(
            group="kubeflow.org",
            name="test-job",
            namespace="my-namespace",
            plural="trainingjobs",
            version="v1alpha1",
        )
        assert job == types.TrainJob(
            name="test-job",
            spec=types.TrainJobSpec(),
            status=types.TrainJobStatus(phase="Running"),
        )


def test_delete_job():
    with (
        patch("kubeflow.core.base_client.KubeconfigAuthProvider") as mock_auth_provider,
        patch("kubeflow.core.base_client.client.ApiClient") as _mock_api_client,
        patch("kubeflow.core.base_client.client.CustomObjectsApi") as mock_custom_api,
    ):
        mock_auth_provider.return_value.get_api_client_configuration.return_value = fake_conf
        client = TrainingClient()
        result = client.delete_job(name="test-job", namespace="my-namespace")
        mock_custom_api.return_value.delete_namespaced_custom_object.assert_called_with(
            group="kubeflow.org",
            name="test-job",
            namespace="my-namespace",
            plural="trainingjobs",
            version="v1alpha1",
        )
        assert result is None


def test_update_job():
    with (
        patch("kubeflow.core.base_client.KubeconfigAuthProvider") as mock_auth_provider,
        patch("kubeflow.core.base_client.client.ApiClient") as _mock_api_client,
        patch("kubeflow.core.base_client.client.CustomObjectsApi") as mock_custom_api,
    ):
        mock_auth_provider.return_value.get_api_client_configuration.return_value = fake_conf
        client = TrainingClient()
        job = types.TrainJob(
            name="test-job",
            spec=types.TrainJobSpec(),
            status=types.TrainJobStatus(phase="Running"),
        )
        client.update_job(job=job, namespace="my-namespace")
        mock_custom_api.return_value.patch_namespaced_custom_object.assert_called_with(
            group="kubeflow.org",
            name="test-job",
            namespace="my-namespace",
            plural="trainingjobs",
            version="v1alpha1",
            body=job.to_dict(),
        )


def test_list_runtimes():
    with (
        patch("kubeflow.core.base_client.KubeconfigAuthProvider") as mock_auth_provider,
        patch("kubeflow.core.base_client.client.ApiClient") as _mock_api_client,
        patch("kubeflow.core.base_client.client.CustomObjectsApi") as mock_custom_api,
    ):
        mock_auth_provider.return_value.get_api_client_configuration.return_value = fake_conf
        mock_custom_api.return_value.list_namespaced_custom_object.return_value = {
            "items": [
                {
                    "metadata": {"name": "test-runtime"},
                    "spec": {"template": "test-template"},
                }
            ]
        }
        client = TrainingClient()
        runtimes = client.list_runtimes(namespace="my-namespace")
        mock_custom_api.return_value.list_namespaced_custom_object.assert_called_with(
            group="kubeflow.org",
            namespace="my-namespace",
            plural="trainingruntimes",
            version="v1alpha1",
        )
        assert runtimes == [
            types.Runtime(name="test-runtime", spec=types.RuntimeSpec(template="test-template"))
        ]


def test_create_job_with_runtime_config():
    with (
        patch("kubeflow.core.base_client.KubeconfigAuthProvider") as mock_auth_provider,
        patch("kubeflow.core.base_client.client.ApiClient") as _mock_api_client,
        patch("kubeflow.core.base_client.client.CustomObjectsApi") as mock_custom_api,
    ):
        mock_auth_provider.return_value.get_api_client_configuration.return_value = fake_conf
        mock_custom_api.return_value.get_namespaced_custom_object.return_value = {
            "metadata": {"name": "test-runtime"},
            "spec": {
                "template": {
                    "spec": {
                        "containers": [
                            {
                                "name": "main",
                                "image": "test-image",
                            }
                        ]
                    }
                }
            },
        }

        client = TrainingClient()
        job_name = client.create_job(namespace="my-namespace", runtime="test-runtime")
        assert job_name.startswith("job-")
        mock_custom_api.return_value.create_namespaced_custom_object.assert_called_with(
            group="kubeflow.org",
            namespace="my-namespace",
            plural="trainingjobs",
            version="v1alpha1",
            body={
                "apiVersion": "kubeflow.org/v1alpha1",
                "kind": "TrainingJob",
                "metadata": {
                    "name": job_name,
                    "namespace": "my-namespace",
                },
                "spec": {
                    "runtimeId": "test-runtime",
                    "template": {
                        "spec": {
                            "containers": [
                                {
                                    "name": "main",
                                    "image": "test-image",
                                }
                            ]
                        }
                    },
                },
            },
        )


def test_get_job_logs():
    with (
        patch("kubeflow.core.base_client.KubeconfigAuthProvider") as mock_auth_provider,
        patch("kubeflow.core.base_client.client.ApiClient") as _mock_api_client,
        patch("kubeflow.core.base_client.client.CoreV1Api") as mock_core_api,
    ):
        mock_auth_provider.return_value.get_api_client_configuration.return_value = fake_conf
        mock_core_api.return_value.list_namespaced_pod.return_value = {
            "items": [{"metadata": {"name": "test-pod"}}]
        }
        mock_core_api.return_value.read_namespaced_pod_log.return_value = "test log content"
        client = TrainingClient()
        logs = client.get_job_logs(name="test-job", namespace="my-namespace")
        assert logs == "test log content"
        mock_core_api.return_value.read_namespaced_pod_log.assert_called_with(
            name="test-pod", namespace="my-namespace"
        )


@pytest.mark.parametrize(
    "phase, expected",
    [
        ("Pending", True),
        ("Running", True),
        ("Succeeded", False),
        ("Failed", False),
        ("Unknown", True),
    ],
)
def test_is_job_running(phase, expected):
    job = types.TrainJob(
        name="test-job",
        spec=types.TrainJobSpec(),
        status=types.TrainJobStatus(phase=phase),
    )
    assert job.is_running() == expected
