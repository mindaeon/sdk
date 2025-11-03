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
from kubeflow.core.k8s_resource import K8sResource
from kubeflow.optimizer.api.optimizer_client import OptimizerClient
from kubeflow.optimizer.types.optimization_types import Search
from kubeflow.trainer.types.types import CustomTrainer, TrainJobTemplate

# A sample Katib Experiment for testing
SAMPLE_EXPERIMENT = {
    "apiVersion": "kubeflow.org/v1beta1",
    "kind": "Experiment",
    "metadata": {"name": "test-experiment", "namespace": "default"},
    "spec": {
        "parameters": [
            {
                "name": "learning_rate",
                "parameterType": "double",
                "feasibleSpace": {"min": "0.01", "max": "0.03"},
            }
        ],
        "objective": {
            "type": "maximize",
            "objectiveMetricName": "accuracy",
        },
        "algorithm": {"algorithmName": "random"},
    },
}


@pytest.fixture
def fake_config():
    cfg = KubeflowConfig()
    return cfg


def test_optimizer_client_optimize(fake_config):
    """Tests the optimize method."""
    fake_config.auth.provider = "kubeconfig"
    fake_conf = client.Configuration()

    def dummy_func():
        pass

    with (
        patch("kubeflow.core.base_client.KubeconfigAuthProvider") as mock_provider,
        patch("kubeflow.core.base_client.client.ApiClient"),
        patch("kubeflow.optimizer.api.optimizer_client.TrainerClient") as mock_trainer_client,
    ):
        mock_provider.return_value.get_api_client_configuration.return_value = fake_conf
        mock_trainer_client.return_value.get_runtime.return_value = MagicMock()
        optimizer_client = OptimizerClient(fake_config)
        optimizer_client.create_custom_resource = MagicMock()
        trainer = CustomTrainer(func=dummy_func)
        optimizer_client.optimize(
            trial_template=TrainJobTemplate(trainer=trainer),
            search_space={"learning_rate": Search.uniform(0.1, 0.2)},
        )
        optimizer_client.create_custom_resource.assert_called_once()


def test_optimizer_client_get_job(fake_config):
    """Tests the get_job method."""
    fake_config.auth.provider = "kubeconfig"
    fake_conf = client.Configuration()

    with (
        patch("kubeflow.core.base_client.KubeconfigAuthProvider") as mock_provider,
        patch("kubeflow.core.base_client.client.ApiClient"),
    ):
        mock_provider.return_value.get_api_client_configuration.return_value = fake_conf
        optimizer_client = OptimizerClient(fake_config)
        optimizer_client.get_custom_resource = MagicMock(
            return_value=K8sResource(**SAMPLE_EXPERIMENT)
        )
        job = optimizer_client.get_job("test-experiment")
        assert job.name == "test-experiment"
        assert "learning_rate" in job.search_space


def test_optimizer_client_list_jobs(fake_config):
    """Tests the list_jobs method."""
    fake_config.auth.provider = "kubeconfig"
    fake_conf = client.Configuration()

    with (
        patch("kubeflow.core.base_client.KubeconfigAuthProvider") as mock_provider,
        patch("kubeflow.core.base_client.client.ApiClient"),
    ):
        mock_provider.return_value.get_api_client_configuration.return_value = fake_conf
        optimizer_client = OptimizerClient(fake_config)
        optimizer_client.list_custom_resources = MagicMock(
            return_value=[K8sResource(**SAMPLE_EXPERIMENT)]
        )
        jobs = optimizer_client.list_jobs()
        assert len(jobs) == 1
        assert jobs[0].name == "test-experiment"


def test_optimizer_client_delete_job(fake_config):
    """Tests the delete_job method."""
    fake_config.auth.provider = "kubeconfig"
    fake_conf = client.Configuration()

    with (
        patch("kubeflow.core.base_client.KubeconfigAuthProvider") as mock_provider,
        patch("kubeflow.core.base_client.client.ApiClient"),
    ):
        mock_provider.return_value.get_api_client_configuration.return_value = fake_conf
        optimizer_client = OptimizerClient(fake_config)
        optimizer_client.delete_custom_resource = MagicMock()
        optimizer_client.delete_job("test-experiment")
        optimizer_client.delete_custom_resource.assert_called_once_with(
            group="kubeflow.org",
            version="v1beta1",
            plural="experiments",
            name="test-experiment",
        )
