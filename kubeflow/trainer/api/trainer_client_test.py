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

from kubeflow_trainer_api.models import (
    IoK8sApiBatchV1JobTemplateSpec as V1alpha2JobTemplate,
    JobsetV1alpha2ReplicatedJob as V1alpha2ReplicatedJob,
)
from kubernetes import client
import pytest

from kubeflow.core.config import KubeflowConfig
from kubeflow.trainer.api.trainer_client import TrainerClient
from kubeflow.trainer.types import types

SAMPLE_PYTORCHJOB = {
    "apiVersion": "kubeflow.org/v1",
    "kind": "PyTorchJob",
    "metadata": {"name": "test-job", "namespace": "default"},
    "spec": {
        "pytorchReplicaSpecs": {
            "Worker": {
                "replicas": 1,
                "template": {
                    "spec": {
                        "containers": [
                            {
                                "name": "pytorch",
                                "image": "pytorch/pytorch:1.11.0-cuda11.3-cudnn8-runtime",
                                "command": ["echo", "hello"],
                            }
                        ]
                    }
                },
            }
        }
    },
}

SAMPLE_RUNTIME = {
    "apiVersion": "trainer.kubeflow.org/v1alpha1",
    "kind": "ClusterTrainingRuntime",
    "metadata": {"name": "test-runtime", "namespace": "default"},
    "spec": {
        "template": {
            "spec": {
                "replicatedJobs": [
                    V1alpha2ReplicatedJob(
                        name="node",
                        template=V1alpha2JobTemplate(
                            metadata={
                                "labels": {"trainer.kubeflow.org/trainjob-ancestor-step": "node"}
                            },
                            spec={
                                "template": {
                                    "spec": {
                                        "containers": [
                                            {
                                                "name": "node",
                                                "image": "python:3.9",
                                            }
                                        ]
                                    }
                                }
                            },
                        ),
                    )
                ]
            }
        }
    },
}


@pytest.fixture
def fake_config():
    """Returns a fake KubeflowConfig object."""
    cfg = KubeflowConfig()
    cfg.auth.provider = "kubeconfig"
    return cfg


def test_get_job(fake_config):
    """Tests the get_job method."""
    with (
        patch("kubeflow.core.base_client.KubeconfigAuthProvider") as mock_auth_provider,
        patch("kubeflow.core.base_client.client.ApiClient"),
        patch("kubeflow.core.base_client.client.CustomObjectsApi") as mock_custom_api,
    ):
        mock_auth_provider.return_value.get_api_client_configuration.return_value = (
            client.Configuration()
        )
        mock_custom_api.return_value.get_namespaced_custom_object.return_value = SAMPLE_PYTORCHJOB
        trainer_client = TrainerClient(config=fake_config)
        trainer_client.custom_api = mock_custom_api.return_value
        trainer_client.get_runtime = MagicMock()
        trainer_client.get_job("test-job")

        mock_custom_api.return_value.get_namespaced_custom_object.assert_called_with(
            group="trainer.kubeflow.org",
            version="v1alpha1",
            namespace="default",
            plural="trainjobs",
            name="test-job",
        )


def test_list_jobs(fake_config):
    """Tests the list_jobs method."""
    with (
        patch("kubeflow.core.base_client.KubeconfigAuthProvider") as mock_auth_provider,
        patch("kubeflow.core.base_client.client.ApiClient"),
        patch("kubeflow.core.base_client.client.CustomObjectsApi") as mock_custom_api,
    ):
        mock_auth_provider.return_value.get_api_client_configuration.return_value = (
            client.Configuration()
        )
        mock_custom_api.return_value.list_namespaced_custom_object.return_value = {
            "items": [SAMPLE_PYTORCHJOB]
        }
        trainer_client = TrainerClient(config=fake_config)
        trainer_client.custom_api = mock_custom_api.return_value
        trainer_client.get_runtime = MagicMock()
        trainer_client.list_jobs()

        mock_custom_api.return_value.list_namespaced_custom_object.assert_called_with(
            group="trainer.kubeflow.org",
            version="v1alpha1",
            namespace="default",
            plural="trainjobs",
        )


def test_delete_job(fake_config):
    """Tests the delete_job method."""
    with (
        patch("kubeflow.core.base_client.KubeconfigAuthProvider") as mock_auth_provider,
        patch("kubeflow.core.base_client.client.ApiClient"),
        patch("kubeflow.core.base_client.client.CustomObjectsApi") as mock_custom_api,
    ):
        mock_auth_provider.return_value.get_api_client_configuration.return_value = (
            client.Configuration()
        )
        trainer_client = TrainerClient(config=fake_config)
        trainer_client.custom_api = mock_custom_api.return_value
        trainer_client.delete_job("test-job")

        mock_custom_api.return_value.delete_namespaced_custom_object.assert_called_with(
            group="trainer.kubeflow.org",
            version="v1alpha1",
            namespace="default",
            plural="trainjobs",
            name="test-job",
        )


def test_get_runtime(fake_config):
    """Tests the get_runtime method."""
    with (
        patch("kubeflow.core.base_client.KubeconfigAuthProvider") as mock_auth_provider,
        patch("kubeflow.core.base_client.client.ApiClient"),
        patch("kubeflow.core.base_client.client.CustomObjectsApi") as mock_custom_api,
    ):
        mock_auth_provider.return_value.get_api_client_configuration.return_value = (
            client.Configuration()
        )
        mock_custom_api.return_value.get_namespaced_custom_object.return_value = SAMPLE_RUNTIME
        trainer_client = TrainerClient(config=fake_config)
        trainer_client.custom_api = mock_custom_api.return_value
        trainer_client.get_runtime("test-runtime")

        mock_custom_api.return_value.get_namespaced_custom_object.assert_called_with(
            group="trainer.kubeflow.org",
            version="v1alpha1",
            namespace="default",
            plural="clustertrainingruntimes",
            name="test-runtime",
        )


def test_list_runtimes(fake_config):
    """Tests the list_runtimes method."""
    with (
        patch("kubeflow.core.base_client.KubeconfigAuthProvider") as mock_auth_provider,
        patch("kubeflow.core.base_client.client.ApiClient"),
        patch("kubeflow.core.base_client.client.CustomObjectsApi") as mock_custom_api,
    ):
        mock_auth_provider.return_value.get_api_client_configuration.return_value = (
            client.Configuration()
        )
        mock_custom_api.return_value.list_namespaced_custom_object.return_value = {
            "items": [SAMPLE_RUNTIME]
        }
        trainer_client = TrainerClient(config=fake_config)
        trainer_client.custom_api = mock_custom_api.return_value
        trainer_client.list_runtimes()

        mock_custom_api.return_value.list_namespaced_custom_object.assert_called_with(
            group="trainer.kubeflow.org",
            version="v1alpha1",
            namespace="default",
            plural="clustertrainingruntimes",
        )


def test_train(fake_config):
    """Tests the train method."""

    def dummy_func():
        pass

    with (
        patch("kubeflow.core.base_client.KubeconfigAuthProvider") as mock_auth_provider,
        patch("kubeflow.core.base_client.client.ApiClient"),
        patch("kubeflow.core.base_client.client.CustomObjectsApi") as mock_custom_api,
    ):
        mock_auth_provider.return_value.get_api_client_configuration.return_value = (
            client.Configuration()
        )
        mock_custom_api.return_value.create_namespaced_custom_object.return_value = (
            SAMPLE_PYTORCHJOB
        )
        trainer_client = TrainerClient(config=fake_config)
        trainer_client.custom_api = mock_custom_api.return_value
        mock_runtime = MagicMock()
        mock_runtime.name = "test-runtime"
        mock_runtime.trainer.trainer_type = types.TrainerType.CUSTOM_TRAINER
        trainer_client.get_runtime = MagicMock(return_value=mock_runtime)
        trainer = types.CustomTrainer(func=dummy_func)
        trainer_client.train(trainer=trainer)

        mock_custom_api.return_value.create_namespaced_custom_object.assert_called_once()


def test_get_job_logs(fake_config):
    """Tests the get_job_logs method."""
    with (
        patch("kubeflow.core.base_client.KubeconfigAuthProvider") as mock_auth_provider,
        patch("kubeflow.core.base_client.client.ApiClient"),
        patch("kubeflow.core.base_client.client.CoreV1Api") as mock_core_api,
    ):
        mock_auth_provider.return_value.get_api_client_configuration.return_value = (
            client.Configuration()
        )
        trainer_client = TrainerClient(config=fake_config)
        trainer_client.core_v1_api = mock_core_api.return_value
        trainer_client.get_job = MagicMock(
            return_value=types.TrainJob(
                name="test-job",
                runtime=MagicMock(),
                steps=[
                    types.Step(
                        name="node-0",
                        status="Running",
                        pod_name="test-pod",
                    )
                ],
                num_nodes=1,
                creation_timestamp=MagicMock(),
            )
        )
        trainer_client.get_job_logs("test-job")

        mock_core_api.return_value.read_namespaced_pod_log.assert_called_with(
            name="test-pod",
            namespace="default",
            container="node",
        )
