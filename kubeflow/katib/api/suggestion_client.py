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
from kubeflow.katib.types import Suggestion


class SuggestionClient(BaseClient):
    """SuggestionClient is a client for managing Katib suggestions."""

    def __init__(self, config: Optional[KubeflowConfig] = None):
        """Initializes a SuggestionClient.

        Args:
            config: The KubeflowConfig object to use for authentication.
        """
        super().__init__(config=config)
        self.group = "kubeflow.org"
        self.version = "v1beta1"
        self.plural = "suggestions"

    def create(self, suggestion: Suggestion, namespace: Optional[str] = None):
        """Creates a suggestion.

        Args:
            suggestion: The suggestion to create.
            namespace: The namespace to create the suggestion in.
        """
        namespace = namespace or self.config.namespace
        self.create_custom_resource(
            group=self.group,
            version=self.version,
            plural=self.plural,
            body=suggestion.to_dict(),
            namespace=namespace,
        )

    def get(self, name: str, namespace: Optional[str] = None) -> Suggestion:
        """Gets a suggestion.

        Args:
            name: The name of the suggestion to get.
            namespace: The namespace to get the suggestion from.
        """
        namespace = namespace or self.config.namespace
        resource = self.get_custom_resource(
            group=self.group,
            version=self.version,
            plural=self.plural,
            name=name,
            namespace=namespace,
        )
        return Suggestion.from_dict(resource.to_dict())

    def list(self, namespace: Optional[str] = None) -> List[Suggestion]:
        """Lists suggestions.

        Args:
            namespace: The namespace to list suggestions from.
        """
        namespace = namespace or self.config.namespace
        resources = self.list_custom_resources(
            group=self.group,
            version=self.version,
            plural=self.plural,
            namespace=namespace,
        )
        return [Suggestion.from_dict(item.to_dict()) for item in resources]

    def delete(self, name: str, namespace: Optional[str] = None):
        """Deletes a suggestion.

        Args:
            name: The name of the suggestion to delete.
            namespace: The namespace to delete the suggestion from.
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
    ) -> List[Suggestion]:
        """Gets the suggestions for an experiment.

        Args:
            experiment_name: The name of the experiment.
            namespace: The namespace of the experiment.
        """
        namespace = namespace or self.config.namespace
        suggestions = self.list(namespace=namespace)
        return [
            s
            for s in suggestions
            if s.metadata.labels.get("kubeflow.org/experiment") == experiment_name
        ]
