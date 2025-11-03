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

import logging
import random
import string
from typing import Any, List, Optional
import uuid

from kubeflow_katib_api import models

from kubeflow.core.base_client import BaseClient
from kubeflow.core.config import KubeflowConfig
from kubeflow.core.k8s_resource import K8sResource
from kubeflow.optimizer.constants import constants
from kubeflow.optimizer.types.algorithm_types import (
    BaseAlgorithm,
    GridSearch,
    Hyperband,
    RandomSearch,
)
from kubeflow.optimizer.types.optimization_types import (
    Metric,
    Objective,
    OptimizationJob,
    Search,
    Trial,
    TrialConfig,
)
from kubeflow.trainer.api.trainer_client import TrainerClient
import kubeflow.trainer.constants.constants as trainer_constants
from kubeflow.trainer.types.types import TrainJobTemplate

logger = logging.getLogger(__name__)


class OptimizerClient(BaseClient):
    def __init__(self, config: Optional[KubeflowConfig] = None):
        """Initialize a Kubeflow Optimizer client."""
        super().__init__(config=config)
        self.trainer_client = TrainerClient(config=self.config)

    def optimize(
        self,
        trial_template: TrainJobTemplate,
        *,
        trial_config: Optional[TrialConfig] = None,
        search_space: dict[str, Any],
        objectives: Optional[list[Objective]] = None,
        algorithm: Optional[BaseAlgorithm] = None,
    ) -> str:
        """Create an OptimizationJob for hyperparameter tuning."""
        job_name = random.choice(string.ascii_lowercase) + uuid.uuid4().hex[:11]
        objectives = objectives or [Objective()]
        algorithm = algorithm or RandomSearch()
        trial_config = trial_config or TrialConfig()

        parameters_spec = []
        trial_parameters = []
        if trial_template.trainer.func_args is None:
            trial_template.trainer.func_args = {}

        for param_name, param_spec in search_space.items():
            param_spec.name = param_name
            parameters_spec.append(param_spec)
            trial_parameters.append(
                models.V1beta1TrialParameterSpec(name=param_name, reference=param_name)
            )
            trial_template.trainer.func_args[param_name] = f"${{trialParameters.{param_name}}}"

        train_job_spec = self.trainer_client._get_trainjob_spec(
            runtime=trial_template.runtime,
            trainer=trial_template.trainer,
            initializer=trial_template.initializer,
        )

        experiment = models.V1beta1Experiment(
            apiVersion=constants.API_VERSION,
            kind=constants.EXPERIMENT_KIND,
            metadata={"name": job_name},
            spec=models.V1beta1ExperimentSpec(
                trialTemplate=models.V1beta1TrialTemplate(
                    retain=True,
                    primaryContainerName=trainer_constants.NODE,
                    trialParameters=trial_parameters,
                    trialSpec={
                        "apiVersion": trainer_constants.API_VERSION,
                        "kind": trainer_constants.TRAINJOB_KIND,
                        "spec": train_job_spec.to_dict(),
                    },
                ),
                parameters=parameters_spec,
                maxTrialCount=trial_config.num_trials,
                parallelTrialCount=trial_config.parallel_trials,
                maxFailedTrialCount=trial_config.max_failed_trials,
                objective=models.V1beta1ObjectiveSpec(
                    objectiveMetricName=objectives[0].metric,
                    type=objectives[0].direction.value,
                    additionalMetricNames=[obj.metric for obj in objectives[1:]]
                    if len(objectives) > 1
                    else None,
                ),
                algorithm=algorithm._to_katib_spec(),
            ),
        )

        self.create_custom_resource(
            group=constants.GROUP,
            version=constants.VERSION,
            plural=constants.EXPERIMENT_PLURAL,
            body=experiment.to_dict(),
        )
        return job_name

    def list_jobs(self) -> List[OptimizationJob]:
        """List created OptimizationJobs."""
        resources = self.list_custom_resources(
            group=constants.GROUP,
            version=constants.VERSION,
            plural=constants.EXPERIMENT_PLURAL,
        )
        return [self._from_k8s_resource(res) for res in resources]

    def get_job(self, name: str) -> OptimizationJob:
        """Get an OptimizationJob."""
        resource = self.get_custom_resource(
            group=constants.GROUP,
            version=constants.VERSION,
            plural=constants.EXPERIMENT_PLURAL,
            name=name,
        )
        return self._from_k8s_resource(resource)

    def delete_job(self, name: str):
        """Delete an OptimizationJob."""
        self.delete_custom_resource(
            group=constants.GROUP,
            version=constants.VERSION,
            plural=constants.EXPERIMENT_PLURAL,
            name=name,
        )

    def _from_k8s_resource(self, resource: K8sResource) -> OptimizationJob:
        """Convert a K8sResource to an OptimizationJob."""
        spec = resource.spec or {}
        status = resource.status or {}
        job = OptimizationJob(
            name=resource.name,
            search_space=self._get_search_space(spec.get("parameters", [])),
            objectives=self._get_objectives(spec.get("objective", {})),
            algorithm=self._get_algorithm(spec.get("algorithm", {})),
            trial_config=TrialConfig(
                num_trials=spec.get("maxTrialCount"),
                parallel_trials=spec.get("parallelTrialCount"),
                max_failed_trials=spec.get("maxFailedTrialCount"),
            ),
            trials=self._get_trials(resource.name),
            creation_timestamp=resource.creation_timestamp,
            status=self._get_status(status),
        )
        return job

    def _get_trials(self, job_name: str) -> List[Trial]:
        """Get Trials for an OptimizationJob."""
        resources = self.list_custom_resources(
            group=constants.GROUP,
            version=constants.VERSION,
            plural=constants.TRIAL_PLURAL,
            namespace=self.config.client.namespace,
        )
        trials = []
        for res in resources:
            if res.labels.get(constants.EXPERIMENT_LABEL) == job_name:
                spec = res.spec or {}
                status = res.status or {}
                trial = Trial(
                    name=res.name,
                    parameters={
                        p["name"]: p["value"]
                        for p in spec.get("parameterAssignments", [])
                    },
                    trainjob=self.trainer_client.get_job(name=res.name),
                    metrics=[
                        Metric(**m)
                        for m in status.get("observation", {}).get("metrics", [])
                    ],
                )
                trials.append(trial)
        return trials

    def _get_status(self, status: dict) -> str:
        """Get the status of an OptimizationJob."""
        conditions = status.get("conditions", [])
        for c in conditions:
            if (
                c.get("type") == constants.EXPERIMENT_SUCCEEDED
                and c.get("status") == "True"
            ):
                return constants.OPTIMIZATION_JOB_COMPLETE
            elif (
                c.get("type") == constants.OPTIMIZATION_JOB_FAILED
                and c.get("status") == "True"
            ):
                return constants.OPTIMIZATION_JOB_FAILED
        return constants.OPTIMIZATION_JOB_RUNNING

    def _get_search_space(self, params: list) -> dict:
        """Get search space from Katib spec."""
        search_space = {}
        for p in params:
            name = p["name"]
            param_type = p["parameterType"]
            space = p["feasibleSpace"]
            if param_type == "int":
                search_space[name] = Search.range(
                    min=int(space["min"]),
                    max=int(space["max"]),
                    step=int(space.get("step", 1)),
                )
            elif param_type == "double":
                search_space[name] = Search.uniform(
                    min=float(space["min"]), max=float(space["max"])
                )
            elif param_type == "categorical":
                search_space[name] = Search.choice(space["list"])
            elif param_type == "discrete":
                search_space[name] = Search.choice([int(v) for v in space["list"]])
        return search_space

    def _get_objectives(self, objective: dict) -> list:
        """Get objectives from Katib spec."""
        objectives = [
            Objective(
                metric=objective.get("objectiveMetricName"),
                direction=objective.get("type"),
            )
        ]
        for m in objective.get("additionalMetricNames", []):
            objectives.append(Objective(metric=m))
        return objectives

    def _get_algorithm(self, algorithm: dict) -> BaseAlgorithm:
        """Get algorithm from Katib spec."""
        name = algorithm.get("algorithmName")
        settings = {
            s["name"]: s["value"] for s in algorithm.get("algorithmSettings", [])
        }
        if name == "random":
            return RandomSearch()
        elif name == "grid":
            return GridSearch()
        elif name == "hyperband":
            return Hyperband(**settings)
        else:
            # Fallback for other algorithms.
            return BaseAlgorithm(name=name, settings=settings)
