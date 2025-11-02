# Copyright 2023 The Kubeflow Authors.
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

from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest
from kubernetes.client import V1ObjectMeta, V1Pod
from kubeflow.core.k8s_resource import K8sResource
from kubeflow.trainer.clients import TrainerClient
from kubeflow.trainer.types import Runtime, TrainJob

# TODO(Bobgy): test the real API server instead of mocking the client.

fake_conf = MagicMock()


def test_list_jobs():
    with patch(
        "kubeflow.core.base_client.KubeconfigAuthProvider"
    ) as mock_auth_provider, patch(
        "kubeflow.core.base_client.client.ApiClient"
    ) as _mock_api_client, patch(
        "kubeflow.core.base_client.client.CustomObjectsApi"
    ) as mock_custom_api, patch(
        "kubeflow.trainer.clients.trainer_client.TrainJob"
    ) as mock_train_job:
        mock_auth_provider.return_value.get_api_client_configuration.return_value = (
            fake_conf
        )
        creation_timestamp = datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        mock_train_job.return_value = TrainJob(
            name="test-job",
            status={"phase": "Running"},
            creation_timestamp=creation_timestamp,
        )
        mock_custom_api.return_value.list_namespaced_custom_object.return_value = {
            "apiVersion": "kubeflow.org/v1alpha1",
            "kind": "TrainingJobList",
            "items": [
                {
                    "apiVersion": "kubeflow.org/v1alpha1",
                    "kind": "TrainingJob",
                    "metadata": {
                        "name": "test-job",
                        "creationTimestamp": creation_timestamp.isoformat(),
                    },
                    "spec": {},
                    "status": {"phase": "Running"},
                }
            ],
        }
        client = TrainerClient()
        jobs = client.list_jobs()
        mock_custom_api.return_value.list_namespaced_custom_object.assert_called_with(
            group="kubeflow.org",
            namespace="default",
            plural="trainingjobs",
            version="v1alpha1",
        )
        assert jobs == [
            TrainJob(
                name="test-job",
                status={"phase": "Running"},
                creation_timestamp=creation_timestamp,
            )
        ]


def test_get_job():
    with patch(
        "kubeflow.core.base_client.KubeconfigAuthProvider"
    ) as mock_auth_provider, patch(
        "kubeflow.core.base_client.client.ApiClient"
    ) as _mock_api_client, patch(
        "kubeflow.core.base_client.client.CustomObjectsApi"
    ) as mock_custom_api, patch(
        "kubeflow.trainer.clients.trainer_client.TrainJob"
    ) as mock_train_job:
        mock_auth_provider.return_value.get_api_client_configuration.return_value = (
            fake_conf
        )
        creation_timestamp = datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        mock_train_job.return_value = TrainJob(
            name="test-job",
            status={"phase": "Running"},
            creation_timestamp=creation_timestamp,
        )
        mock_custom_api.return_value.get_namespaced_custom_object.return_value = {
            "apiVersion": "kubeflow.org/v1alpha1",
            "kind": "TrainingJob",
            "metadata": {
                "name": "test-job",
                "creationTimestamp": creation_timestamp.isoformat(),
            },
            "spec": {},
            "status": {"phase": "Running"},
        }
        client = TrainerClient()
        job = client.get_job(name="test-job", namespace="my-namespace")
        mock_custom_api.return_value.get_namespaced_custom_object.assert_called_with(
            group="kubeflow.org",
            name="test-job",
            namespace="my-namespace",
            plural="trainingjobs",
            version="v1alpha1",
        )
        assert job == TrainJob(
            name="test-job",
            status={"phase": "Running"},
            creation_timestamp=creation_timestamp,
        )


def test_delete_job():
    with patch(
        "kubeflow.core.base_client.KubeconfigAuthProvider"
    ) as mock_auth_provider, patch(
        "kubeflow.core.base_client.client.ApiClient"
    ) as _mock_api_client, patch(
        "kubeflow.core.base_client.client.CustomObjectsApi"
    ) as mock_custom_api:
        mock_auth_provider.return_value.get_api_client_configuration.return_value = (
            fake_conf
        )
        client = TrainerClient()
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
    with patch(
        "kubeflow.core.base_client.KubeconfigAuthProvider"
    ) as mock_auth_provider, patch(
        "kubeflow.core.base_client.client.ApiClient"
    ) as _mock_api_client, patch(
        "kubeflow.core.base_client.client.CustomObjectsApi"
    ) as mock_custom_api:
        mock_auth_provider.return_value.get_api_client_configuration.return_value = (
            fake_conf
        )
        client = TrainerClient()
        job = TrainJob(
            name="test-job",
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
    with patch(
        "kubeflow.core.base_client.KubeconfigAuthProvider"
    ) as mock_auth_provider, patch(
        "kubeflow.core.base_client.client.ApiClient"
    ) as _mock_api_client, patch(
        "kubeflow.core.base_client.client.CustomObjectsApi"
    ) as mock_custom_api:
        mock_auth_provider.return_value.get_api_client_configuration.return_value = (
            fake_conf
        )
        mock_custom_api.return_value.list_namespaced_custom_object.return_value = {
            "apiVersion": "kubeflow.org/v1alpha1",
            "kind": "TrainingRuntimeList",
            "items": [
                {
                    "apiVersion": "kubeflow.org/v1alpha1",
                    "kind": "TrainingRuntime",
                    "metadata": {"name": "test-runtime"},
                    "spec": {"template": "test-template"},
                }
            ],
        }
        client = TrainerClient()
        runtimes = client.list_runtimes()
        mock_custom_api.return_value.list_namespaced_custom_object.assert_called_with(
            group="kubeflow.org",
            namespace="default",
            plural="trainingruntimes",
            version="v1alpha1",
        )
        assert runtimes == [
            Runtime(
                name="test-runtime",
                trainer=None,
                spec={"template": "test-template"},
            )
        ]


def test_create_job_with_runtime_config():
    with patch(
        "kubeflow.core.base_client.KubeconfigAuthProvider"
    ) as mock_auth_provider, patch(
        "kubeflow.core.base_client.client.ApiClient"
    ) as _mock_api_client, patch(
        "kubeflow.core.base_client.client.CustomObjectsApi"
    ) as mock_custom_api:
        mock_auth_provider.return_value.get_api_client_configuration.return_value = (
            fake_conf
        )
        mock_custom_api.return_value.get_namespaced_custom_object.return_value = {
            "apiVersion": "kubeflow.org/v1alpha1",
            "kind": "TrainingRuntime",
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

        def mock_create_job(group, namespace, plural, version, body):
            return body

        mock_custom_api.return_value.create_namespaced_custom_object.side_effect = (
            mock_create_job
        )

        client = TrainerClient()
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
            },
        )


def test_get_job_logs():
    with patch(
        "kubeflow.core.base_client.KubeconfigAuthProvider"
    ) as mock_auth_provider, patch(
        "kubeflow.core.base_client.client.ApiClient"
    ) as _mock_api_client, patch(
        "kubeflow.core.base_client.client.CustomObjectsApi"
    ) as mock_custom_api, patch(
        "kubeflow.core.base_client.client.CoreV1Api"
    ) as mock_core_api:
        mock_auth_provider.return_value.get_api_client_configuration.return_value = (
            fake_conf
        )
        mock_custom_api.return_value.get_namespaced_custom_object.return_value = {
            "apiVersion": "kubeflow.org/v1alpha1",
            "kind": "TrainingJob",
            "metadata": {"name": "test-job"},
            "spec": {},
            "status": {"pod_names": ["test-pod"]},
        }
        mock_core_api.return_value.list_namespaced_pod.return_value.items = [
            V1Pod(metadata=V1ObjectMeta(name="test-pod"))
        ]
        mock_core_api.return_value.read_namespaced_pod_log.return_value = (
            "test log content"
        )
        client = TrainerClient()
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
    job = TrainJob(
        name="test-job",
    )
    job.status = {"phase": phase}
    assert job.is_running() == expected
