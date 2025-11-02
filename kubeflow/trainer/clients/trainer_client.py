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

import random
import string
from typing import Optional

from kubeflow.core.base_client import BaseClient
from kubeflow.core.config import KubeflowConfig


class TrainerClient(BaseClient):
    """TrainerClient is a client for managing Kubeflow training jobs."""

    def __init__(self, config: Optional[KubeflowConfig] = None):
        """Initializes a TrainerClient.

        Args:
            config: The KubeflowConfig object to use for authentication.
        """
        super().__init__(config=config)

    def list_runtimes(self):
        """List available runtimes."""
        from kubeflow.trainer.types import Runtime

        resources = self.list_custom_resources(
            group="kubeflow.org",
            version="v1alpha1",
            namespace=self.config.client.namespace,
            plural="trainingruntimes",
        )
        return [
            Runtime(name=item.metadata["name"], trainer=None, spec=item.spec)
            for item in resources
        ]

    def create_job(
        self,
        name: Optional[str] = None,
        namespace: Optional[str] = None,
        runtime: Optional[str] = None,
        spec=None,
    ) -> str:
        """Create a training job.

        Args:
            name: The name of the training job.
            namespace: The namespace to create the training job in.
            runtime: The runtime to use for the training job.
            spec: The specification of the training job.
        """
        if runtime and spec:
            raise ValueError("Cannot specify both runtime and spec.")
        if not runtime and not spec:
            raise ValueError("Must specify either runtime or spec.")
        if runtime:
            runtime_obj = self.get_runtime(name=runtime, namespace=namespace)
            spec = runtime_obj.spec
        namespace = namespace or self.config.client.namespace
        train_job_name = name or self._generate_job_name()
        self.create_custom_resource(
            group="kubeflow.org",
            version="v1alpha1",
            namespace=namespace,
            plural="trainingjobs",
            body={
                "apiVersion": "kubeflow.org/v1alpha1",
                "kind": "TrainingJob",
                "metadata": {
                    "name": train_job_name,
                    "namespace": namespace,
                },
                "spec": spec,
            },
        )
        return train_job_name

    def list_jobs(self):
        """List created TrainJobs."""
        from kubeflow.trainer.types import TrainJob

        resources = self.list_custom_resources(
            group="kubeflow.org",
            version="v1alpha1",
            namespace=self.config.client.namespace,
            plural="trainingjobs",
        )
        return [
            TrainJob(
                name=item.metadata["name"],
                runtime=None,
                status=item.status,
                creation_timestamp=item.metadata.get("creationTimestamp"),
            )
            for item in resources
        ]

    def get_job(self, name: str, namespace: Optional[str] = None):
        """Get a training job.

        Args:
            name: The name of the training job.
            namespace: The namespace to get the training job from.
        """
        from kubeflow.trainer.types import TrainJob

        namespace = namespace or self.config.client.namespace
        resource = self.get_custom_resource(
            group="kubeflow.org",
            version="v1alpha1",
            namespace=namespace,
            plural="trainingjobs",
            name=name,
        )
        return TrainJob(
            name=resource.metadata["name"],
            runtime=None,
            status=resource.status,
            creation_timestamp=resource.metadata.get("creationTimestamp"),
        )

    def get_job_logs(self, name: str, namespace: Optional[str] = None) -> str:
        """Get the logs of a training job.

        Args:
            name: The name of the training job.
            namespace: The namespace to get the training job logs from.
        """
        namespace = namespace or self.config.client.namespace
        trainjob = self.get_job(name=name, namespace=namespace)
        if trainjob.status and trainjob.status.get("pod_names"):
            # TODO(Bobgy): how to select which pod's log to show?
            pod_name = trainjob.status["pod_names"][0]
            return self.core_v1_api.read_namespaced_pod_log(
                name=pod_name, namespace=namespace
            )
        return ""

    def update_job(self, job, namespace: Optional[str] = None):
        """Update a training job.

        Args:
            job: The training job to update.
            namespace: The namespace to update the training job in.
        """
        namespace = namespace or self.config.client.namespace
        self.patch_custom_resource(
            group="kubeflow.org",
            version="v1alpha1",
            namespace=namespace,
            plural="trainingjobs",
            name=job.name,
            body=job.to_dict(),
        )

    def delete_job(self, name: str, namespace: Optional[str] = None):
        """Delete a training job.

        Args:
            name: The name of the training job to delete.
            namespace: The namespace to delete the training job from.
        """
        namespace = namespace or self.config.client.namespace
        self.delete_custom_resource(
            group="kubeflow.org",
            version="v1alpha1",
            namespace=namespace,
            plural="trainingjobs",
            name=name,
        )

    def get_runtime(self, name: str, namespace: Optional[str] = None):
        """Get a runtime.

        Args:
            name: The name of the runtime.
            namespace: The namespace to get the runtime from.
        """
        from kubeflow.trainer.types import Runtime

        namespace = namespace or self.config.client.namespace
        resource = self.get_custom_resource(
            group="kubeflow.org",
            version="v1alpha1",
            namespace=namespace,
            plural="trainingruntimes",
            name=name,
        )
        return Runtime(
            name=resource.metadata["name"], trainer=None, spec=resource.spec
        )

    def _get_steps(self, job_name: str, runtime) -> list:
        """Get steps for a TrainJob."""
        from kubeflow.trainer.types import Step

        pods = self.core_v1_api.list_namespaced_pod(
            namespace=self.config.client.namespace,
            label_selector=f"training.kubeflow.org/job-name={job_name}",
        )
        return [
            Step(
                name=pod.metadata.name,
                status=pod.status.phase,
                runtime=runtime,
                entrypoint=self._get_entrypoint(runtime=runtime, pod=pod),
            )
            for pod in pods.items
        ]

    def _get_entrypoint(self, runtime, pod) -> Optional:
        """Get entrypoint for a pod."""
        from kubeflow.trainer.types import Entrypoint

        # TODO(Bobgy): support more types of entrypoints
        if runtime.spec and runtime.spec.tensorboard and runtime.spec.tensorboard.port:
            for port in pod.spec.containers[0].ports:
                if port.container_port == runtime.spec.tensorboard.port:
                    # TODO(Bobgy): how to get the correct host IP and port?
                    return Entrypoint(
                        name="Tensorboard",
                        url=(
                            f"http://{pod.status.host_ip}:{port.host_port}/?pod={pod.metadata.name}"
                        ),
                    )
        return None

    def _generate_job_name(self, prefix: str = "job-", length: int = 5) -> str:
        """Generate a random job name."""
        # TODO(Bobgy): ensure the generated name is unique.
        chars = string.ascii_lowercase + string.digits
        suffix = "".join(random.choice(chars) for _ in range(length))
        return f"{prefix}{suffix}"
