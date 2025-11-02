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

from typing import Optional, List

from kubeflow.core.base_client import BaseClient
from kubeflow.core.config import KubeflowConfig
from kubeflow.katib.types import Trial


class TrialClient(BaseClient):
    """TrialClient is a client for managing Katib trials."""

    def __init__(self, config: Optional[KubeflowConfig] = None):
        """Initializes a TrialClient.

        Args:
            config: The KubeflowConfig object to use for authentication.
        """
        super().__init__(config=config)
        self.group = "kubeflow.org"
        self.version = "v1beta1"
        self.plural = "trials"

    def create(self, trial: Trial, namespace: Optional[str] = None):
        """Creates a trial.

        Args:
            trial: The trial to create.
            namespace: The namespace to create the trial in.
        """
        namespace = namespace or self.config.namespace
        self.create_custom_resource(
            group=self.group,
            version=self.version,
            plural=self.plural,
            body=trial.to_dict(),
            namespace=namespace,
        )

    def get(self, name: str, namespace: Optional[str] = None) -> Trial:
        """Gets a trial.

        Args:
            name: The name of the trial to get.
            namespace: The namespace to get the trial from.
        """
        namespace = namespace or self.config.namespace
        resource = self.get_custom_resource(
            group=self.group,
            version=self.version,
            plural=self.plural,
            name=name,
            namespace=namespace,
        )
        return Trial.from_dict(resource.to_dict())

    def list(self, namespace: Optional[str] = None) -> List[Trial]:
        """Lists trials.

        Args:
            namespace: The namespace to list trials from.
        """
        namespace = namespace or self.config.namespace
        resources = self.list_custom_resources(
            group=self.group,
            version=self.version,
            plural=self.plural,
            namespace=namespace,
        )
        return [Trial.from_dict(item.to_dict()) for item in resources]

    def delete(self, name: str, namespace: Optional[str] = None):
        """Deletes a trial.

        Args:
            name: The name of the trial to delete.
            namespace: The namespace to delete the trial from.
        """
        namespace = namespace or self.config.namespace
        self.delete_custom_resource(
            group=self.group,
            version=self.version,
            plural=self.plural,
            name=name,
            namespace=namespace,
        )

    def get_for_experiment(
        self, experiment_name: str, namespace: Optional[str] = None
    ) -> List[Trial]:
        """Gets the trials for an experiment.

        Args:
            experiment_name: The name of the experiment.
            namespace: The namespace of the experiment.
        """
        namespace = namespace or self.config.namespace
        trials = self.list(namespace=namespace)
        return [
            t
            for t in trials
            if t.metadata.labels.get("kubeflow.org/experiment") == experiment_name
        ]
