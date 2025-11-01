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

import logging
import random
import re
import string
from collections.abc import Iterator
from typing import List, Optional, Union
import uuid

from kubeflow_trainer_api import models

from kubeflow.core.base_client import BaseClient
from kubeflow.core.config import KubeflowConfig
from kubeflow.core.k8s_resource import K8sResource
from kubeflow.trainer.constants import constants
from kubeflow.trainer.types import types
import kubeflow.trainer.utils as utils

logger = logging.getLogger(__name__)


class TrainerClient(BaseClient):
    def __init__(self, config: Optional[KubeflowConfig] = None):
        """Initialize a Kubeflow Trainer client."""
        super().__init__(config=config)

    def list_runtimes(self) -> List[types.Runtime]:
        """List available runtimes."""
        resources = self.list_custom_resources(
            group=constants.GROUP,
            version=constants.VERSION,
            plural=constants.CLUSTER_TRAINING_RUNTIME_PLURAL,
        )
        return [self._runtime_from_k8s_resource(res) for res in resources]

    def get_runtime(self, name: str) -> types.Runtime:
        """Get a runtime."""
        resource = self.get_custom_resource(
            group=constants.GROUP,
            version=constants.VERSION,
            plural=constants.CLUSTER_TRAINING_RUNTIME_PLURAL,
            name=name,
        )
        return self._runtime_from_k8s_resource(resource)

    def train(
        self,
        runtime: Optional[types.Runtime] = None,
        initializer: Optional[types.Initializer] = None,
        trainer: Optional[
            Union[types.CustomTrainer, types.CustomTrainerContainer, types.BuiltinTrainer]
        ] = None,
    ) -> str:
        """Create a TrainJob."""
        train_job_name = random.choice(string.ascii_lowercase) + uuid.uuid4().hex[:11]
        train_job = models.TrainerV1alpha1TrainJob(
            apiVersion=constants.API_VERSION,
            kind=constants.TRAINJOB_KIND,
            metadata={"name": train_job_name},
            spec=self._get_trainjob_spec(runtime, initializer, trainer),
        )
        self.create_custom_resource(
            group=constants.GROUP,
            version=constants.VERSION,
            plural=constants.TRAINJOB_PLURAL,
            body=train_job.to_dict(),
        )
        return train_job_name

    def list_jobs(self) -> List[types.TrainJob]:
        """List created TrainJobs."""
        resources = self.list_custom_resources(
            group=constants.GROUP,
            version=constants.VERSION,
            plural=constants.TRAINJOB_PLURAL,
        )
        return [self._trainjob_from_k8s_resource(res) for res in resources]

    def get_job(self, name: str) -> types.TrainJob:
        """Get a TrainJob."""
        resource = self.get_custom_resource(
            group=constants.GROUP,
            version=constants.VERSION,
            plural=constants.TRAINJOB_PLURAL,
            name=name,
        )
        return self._trainjob_from_k8s_resource(resource)

    def get_job_logs(
        self,
        name: str,
        step: str = constants.NODE + "-0",
        follow: Optional[bool] = False,
    ) -> Iterator[str]:
        """Get logs from a specific step of a TrainJob."""
        pod_name = None
        for s in self.get_job(name).steps:
            if s.status != constants.POD_PENDING and s.name == step:
                pod_name = s.pod_name
                break
        if pod_name is None:
            return

        container_name = re.sub(r"-\d+$", "", step)
        if follow:
            return self.core_v1_api.read_namespaced_pod_log(
                name=pod_name,
                namespace=self.config.client.namespace,
                container=container_name,
                follow=True,
                _preload_content=False,
            ).stream()
        else:
            return self.core_v1_api.read_namespaced_pod_log(
                name=pod_name,
                namespace=self.config.client.namespace,
                container=container_name,
            ).splitlines()

    def delete_job(self, name: str):
        """Delete a TrainJob."""
        self.delete_custom_resource(
            group=constants.GROUP,
            version=constants.VERSION,
            plural=constants.TRAINJOB_PLURAL,
            name=name,
        )

    def _runtime_from_k8s_resource(self, resource: K8sResource) -> types.Runtime:
        """Convert a K8sResource to a Runtime."""
        spec = resource.spec or {}
        return types.Runtime(
            name=resource.name,
            trainer=utils.get_runtime_trainer(
                resource.labels.get(constants.RUNTIME_FRAMEWORK_LABEL, ""),
                spec.get("template", {}).get("spec", {}).get("replicatedJobs", []),
                spec.get("mlPolicy", {}),
            ),
        )

    def _trainjob_from_k8s_resource(self, resource: K8sResource) -> types.TrainJob:
        """Convert a K8sResource to a TrainJob."""
        spec = resource.spec or {}
        status = resource.status or {}
        runtime = self.get_runtime(spec.get("runtimeRef", {}).get("name", ""))
        trainjob = types.TrainJob(
            name=resource.name,
            creation_timestamp=resource.creation_timestamp,
            runtime=runtime,
            steps=self._get_steps(resource.name, runtime),
            num_nodes=spec.get("trainer", {}).get("numNodes") or runtime.trainer.num_nodes,
            status=self._get_status(status),
        )
        return trainjob

    def _get_steps(self, job_name: str, runtime: types.Runtime) -> List[types.Step]:
        """Get steps for a TrainJob."""
        pods = self.core_v1_api.list_namespaced_pod(
            namespace=self.config.client.namespace,
            label_selector=constants.POD_LABEL_SELECTOR.format(trainjob_name=job_name),
        )
        steps = []
        for pod in pods.items:
            pod_resource = K8sResource(**pod.to_dict())
            step_name = pod_resource.labels.get(constants.JOBSET_RJOB_NAME_LABEL, "")
            if step_name in {
                constants.DATASET_INITIALIZER,
                constants.MODEL_INITIALIZER,
            }:
                steps.append(
                    utils.get_trainjob_initializer_step(
                        pod_resource.name,
                        pod_resource.spec,
                        pod_resource.status,
                    )
                )
            elif step_name in {constants.LAUNCHER, constants.NODE}:
                steps.append(
                    utils.get_trainjob_node_step(
                        pod_resource.name,
                        pod_resource.spec,
                        pod_resource.status,
                        runtime,
                        step_name,
                        int(pod_resource.labels.get(constants.JOB_INDEX_LABEL, 0)),
                    )
                )
        return steps

    def _get_status(self, status: dict) -> str:
        """Get the status of a TrainJob."""
        conditions = status.get("conditions", [])
        for c in conditions:
            if c.get("type") in {
                constants.TRAINJOB_COMPLETE,
                constants.TRAINJOB_FAILED,
            } and c.get("status") == "True":
                return c.get("type")
        return constants.TRAINJOB_RUNNING

    def _get_trainjob_spec(
        self,
        runtime: Optional[types.Runtime] = None,
        initializer: Optional[types.Initializer] = None,
        trainer: Optional[
            Union[types.CustomTrainer, types.CustomTrainerContainer, types.BuiltinTrainer]
        ] = None,
    ) -> models.TrainerV1alpha1TrainJobSpec:
        """Get TrainJob spec from the given parameters"""
        if runtime is None:
            runtime = self.get_runtime(constants.TORCH_RUNTIME)

        trainer_cr = models.TrainerV1alpha1Trainer()
        if trainer:
            if isinstance(trainer, (types.CustomTrainer, types.CustomTrainerContainer)):
                if runtime.trainer.trainer_type != types.TrainerType.CUSTOM_TRAINER:
                    raise ValueError(f"CustomTrainer can't be used with {runtime} runtime")
                trainer_cr = utils.get_trainer_cr_from_custom_trainer(runtime, trainer)
            elif isinstance(trainer, types.BuiltinTrainer):
                if runtime.trainer.trainer_type != types.TrainerType.BUILTIN_TRAINER:
                    raise ValueError(f"BuiltinTrainer can't be used with {runtime} runtime")
                trainer_cr = utils.get_trainer_cr_from_builtin_trainer(
                    runtime, trainer, initializer
                )
            else:
                raise ValueError(
                    f"The trainer type {type(trainer)} is not supported."
                )

        return models.TrainerV1alpha1TrainJobSpec(
            runtimeRef=models.TrainerV1alpha1RuntimeRef(name=runtime.name),
            trainer=(trainer_cr if trainer_cr != models.TrainerV1alpha1Trainer() else None),
            initializer=(
                models.TrainerV1alpha1Initializer(
                    dataset=utils.get_dataset_initializer(initializer.dataset),
                    model=utils.get_model_initializer(initializer.model),
                )
                if isinstance(initializer, types.Initializer)
                else None
            ),
        )
