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

from typing import Any, Optional

from kubeflow.core.base_client import BaseClient
from kubeflow.core.config import KubeflowConfig
from kubeflow.katib import (
    V1beta1AlgorithmSetting,
    V1beta1AlgorithmSpec,
    V1beta1ExperimentSpec,
    V1beta1FeasibleSpace,
    V1beta1ObjectiveSpec,
    V1beta1ParameterSpec,
)
from kubeflow.optimizer.types import Optimizer, SearchSpace


class OptimizerClient(BaseClient):
    """OptimizerClient is a client for managing Katib experiments as optimizers."""

    def __init__(self, config: Optional[KubeflowConfig] = None):
        """Initializes an OptimizerClient.

        Args:
            config: The KubeflowConfig object to use for authentication.
        """
        super().__init__(config=config)
        self.group = "kubeflow.org"
        self.version = "v1beta1"
        self.plural = "experiments"

    def create(self, optimizer: Optimizer, namespace: Optional[str] = None):
        """Creates an optimizer.

        Args:
            optimizer: The optimizer to create.
            namespace: The namespace to create the optimizer in.
        """
        namespace = namespace or self.config.namespace
        body = {
            "apiVersion": f"{self.group}/{self.version}",
            "kind": "Experiment",
            "metadata": {
                "name": optimizer.name,
                "namespace": namespace,
            },
            "spec": self._construct_experiment_spec(optimizer).to_dict(),
        }
        self.create_custom_resource(
            group=self.group,
            version=self.version,
            plural=self.plural,
            body=body,
            namespace=namespace,
        )

    def get(self, name: str, namespace: Optional[str] = None) -> Optimizer:
        """Gets an optimizer.

        Args:
            name: The name of the optimizer to get.
            namespace: The namespace to get the optimizer from.
        """
        namespace = namespace or self.config.namespace
        resource = self.get_custom_resource(
            group=self.group,
            version=self.version,
            plural=self.plural,
            name=name,
            namespace=namespace,
        )
        return Optimizer(
            name=resource.metadata["name"],
            search_space=SearchSpace(
                parameters=self._parse_parameter_specs(resource.spec["parameters"])
            ),
            objective=self._parse_objective_spec(resource.spec["objective"]),
            algorithm=self._parse_algorithm_spec(resource.spec["algorithm"]),
        )

    def list(self, namespace: Optional[str] = None) -> list[Optimizer]:
        """Lists optimizers.

        Args:
            namespace: The namespace to list optimizers from.
        """
        namespace = namespace or self.config.namespace
        resources = self.list_custom_resources(
            group=self.group,
            version=self.version,
            plural=self.plural,
            namespace=namespace,
        )
        return [
            Optimizer(
                name=item.metadata["name"],
                search_space=SearchSpace(
                    parameters=self._parse_parameter_specs(item.spec["parameters"])
                ),
                objective=self._parse_objective_spec(item.spec["objective"]),
                algorithm=self._parse_algorithm_spec(item.spec["algorithm"]),
            )
            for item in resources["items"]
        ]

    def delete(self, name: str, namespace: Optional[str] = None):
        """Deletes an optimizer.

        Args:
            name: The name of the optimizer to delete.
            namespace: The namespace to delete the optimizer from.
        """
        namespace = namespace or self.config.namespace
        self.delete_custom_resource(
            group=self.group,
            version=self.version,
            plural=self.plural,
            name=name,
            namespace=namespace,
        )

    def _construct_experiment_spec(self, optimizer: Optimizer) -> V1beta1ExperimentSpec:
        return V1beta1ExperimentSpec(
            objective=V1beta1ObjectiveSpec(
                type=optimizer.objective.type,
                goal=optimizer.objective.goal,
                objective_metric_name=optimizer.objective.objective_metric_name,
            ),
            algorithm=V1beta1AlgorithmSpec(
                algorithm_name=optimizer.algorithm.name,
                algorithm_settings=[
                    V1beta1AlgorithmSetting(name=k, value=str(v))
                    for k, v in optimizer.algorithm.settings.items()
                ],
            ),
            parameters=[
                V1beta1ParameterSpec(
                    name=p.name,
                    parameter_type=p.type,
                    feasible_space=V1beta1FeasibleSpace(
                        min=p.space.min,
                        max=p.space.max,
                        step=p.space.step,
                        list=p.space.values,
                    ),
                )
                for p in optimizer.search_space.parameters
            ],
        )

    def _parse_parameter_specs(self, params: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [
            {
                "name": p["name"],
                "type": p["parameterType"],
                "space": {
                    "min": p["feasibleSpace"].get("min"),
                    "max": p["feasibleSpace"].get("max"),
                    "step": p["feasibleSpace"].get("step"),
                    "values": p["feasibleSpace"].get("list"),
                },
            }
            for p in params
        ]

    def _parse_objective_spec(self, objective: dict[str, Any]) -> dict[str, Any]:
        return {
            "type": objective["type"],
            "goal": objective.get("goal"),
            "objective_metric_name": objective.get("objectiveMetricName"),
        }

    def _parse_algorithm_spec(self, algorithm: dict[str, Any]) -> dict[str, Any]:
        return {
            "name": algorithm["algorithmName"],
            "settings": {s["name"]: s["value"] for s in algorithm.get("algorithmSettings", [])},
        }
