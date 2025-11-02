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

from typing import Optional

from kubeflow.core.base_client import BaseClient
from kubeflow.core.config import KubeflowConfig
from kubeflow.notebooks.models import Notebook


class NotebookClient(BaseClient):
    """A client for managing Kubeflow Notebooks."""

    def __init__(self, config: Optional[KubeflowConfig] = None):
        """Initializes a NotebookClient.

        Args:
            config: The KubeflowConfig object to use for authentication.
        """
        super().__init__(config=config)
        self.group = "kubeflow.org"
        self.version = "v1"
        self.plural = "notebooks"

    def create(self, notebook: Notebook, namespace: Optional[str] = None):
        """Creates a notebook."""
        return self.create_custom_resource(
            group=self.group,
            version=self.version,
            plural=self.plural,
            body=notebook.model_dump(),
            namespace=namespace,
        )

    def get(self, name: str, namespace: Optional[str] = None) -> Notebook:
        """Gets a notebook."""
        resource = self.get_custom_resource(
            group=self.group,
            version=self.version,
            plural=self.plural,
            name=name,
            namespace=namespace,
        )
        return Notebook(**resource.to_dict())

    def list(self, namespace: Optional[str] = None) -> list[Notebook]:
        """Lists notebooks."""
        resources = self.list_custom_resources(
            group=self.group,
            version=self.version,
            plural=self.plural,
            namespace=namespace,
        )
        return [Notebook(**item.to_dict()) for item in resources]

    def delete(self, name: str, namespace: Optional[str] = None):
        """Deletes a notebook."""
        return self.delete_custom_resource(
            group=self.group,
            version=self.version,
            plural=self.plural,
            name=name,
            namespace=namespace,
        )
