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

"""Test the Kubeflow SDK client."""

from unittest.mock import patch

from kubeflow.client.kubeflow_client import KubeflowClient, PipelinesClient
from kubeflow.core.config import KubeflowConfig
from kubeflow.notebooks.api.notebook_client import NotebookClient
from kubeflow.optimizer.api.optimizer_client import OptimizerClient
from kubeflow.trainer.api.trainer_client import TrainerClient


def test_kubeflow_client_trainer():
    """Tests the trainer property."""
    with patch("kubeflow.core.base_client.KubeconfigAuthProvider"), patch(
        "kubeflow.core.base_client.client.ApiClient"
    ):
        client = KubeflowClient(config=KubeflowConfig())
        assert isinstance(client.trainer, TrainerClient)


def test_kubeflow_client_optimizer():
    """Tests the optimizer property."""
    with patch("kubeflow.core.base_client.KubeconfigAuthProvider"), patch(
        "kubeflow.core.base_client.client.ApiClient"
    ):
        client = KubeflowClient(config=KubeflowConfig())
        assert isinstance(client.optimizer, OptimizerClient)


def test_kubeflow_client_notebooks():
    """Tests the notebooks property."""
    with patch("kubeflow.core.base_client.KubeconfigAuthProvider"), patch(
        "kubeflow.core.base_client.client.ApiClient"
    ):
        client = KubeflowClient(config=KubeflowConfig())
        assert isinstance(client.notebooks, NotebookClient)


def test_kubeflow_client_pipelines():
    """Tests the pipelines property."""
    with patch("kubeflow.core.base_client.KubeconfigAuthProvider"), patch(
        "kubeflow.core.base_client.client.ApiClient"
    ):
        client = KubeflowClient(config=KubeflowConfig())
        assert isinstance(client.pipelines, PipelinesClient)
