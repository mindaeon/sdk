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

"""The Kubeflow SDK client."""

from typing import Optional

from kubeflow.core.config import KubeflowConfig
from kubeflow.optimizer.api.optimizer_client import OptimizerClient
from kubeflow.trainer.api.trainer_client import TrainerClient
from kubeflow.notebooks.api.notebook_client import NotebookClient
from kubeflow.pipelines.api.pipeline_client import PipelineClient
from kubeflow.pipelines.api.run_client import RunClient
from kubeflow.pipelines.api.experiment_client import ExperimentClient


class PipelinesClient:
    """A client for interacting with Kubeflow Pipelines."""

    def __init__(self, config: Optional[KubeflowConfig] = None):
        """Initializes the PipelinesClient."""
        if not config:
            config = KubeflowConfig()
        self.config = config
        self._pipeline_client = None
        self._run_client = None
        self._experiment_client = None

    @property
    def pipeline(self) -> PipelineClient:
        """Returns a PipelineClient."""
        if not self._pipeline_client:
            self._pipeline_client = PipelineClient(config=self.config)
        return self._pipeline_client

    @property
    def run(self) -> RunClient:
        """Returns a RunClient."""
        if not self._run_client:
            self._run_client = RunClient(config=self.config)
        return self._run_client

    @property
    def experiment(self) -> ExperimentClient:
        """Returns an ExperimentClient."""
        if not self._experiment_client:
            self._experiment_client = ExperimentClient(config=self.config)
        return self._experiment_client


class KubeflowClient:
    """A client for interacting with Kubeflow components."""

    def __init__(self, config: Optional[KubeflowConfig] = None):
        """Initializes the KubeflowClient."""
        if not config:
            config = KubeflowConfig()
        self.config = config
        self._trainer_client = None
        self._optimizer_client = None
        self._notebooks_client = None
        self._pipelines_client = None

    @property
    def trainer(self) -> TrainerClient:
        """Returns a TrainerClient."""
        if not self._trainer_client:
            self._trainer_client = TrainerClient(config=self.config)
        return self._trainer_client

    @property
    def optimizer(self) -> OptimizerClient:
        """Returns an OptimizerClient."""
        if not self._optimizer_client:
            self._optimizer_client = OptimizerClient(config=self.config)
        return self._optimizer_client

    @property
    def notebooks(self) -> NotebookClient:
        """Returns a NotebookClient."""
        if not self._notebooks_client:
            self._notebooks_client = NotebookClient(config=self.config)
        return self._notebooks_client

    @property
    def pipelines(self) -> PipelinesClient:
        """Returns a PipelinesClient."""
        if not self._pipelines_client:
            self._pipelines_client = PipelinesClient(config=self.config)
        return self._pipelines_client
