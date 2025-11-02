# Copyright 2025 The Kubeflow Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from kubeflow.core.base_client import BaseClient
from kubeflow.spark_operator.types import SparkApplication


class SparkClient(BaseClient):
    """Client for interacting with the Spark Operator."""

    def __init__(self, **kwargs):
        """Initializes a SparkClient."""
        super().__init__(**kwargs)
        self.group = "sparkoperator.k8s.io"
        self.version = "v1beta2"
        self.plural = "sparkapplications"

    def create(self, spark_application: SparkApplication):
        """Creates a SparkApplication.

        Args:
            spark_application: The SparkApplication to create.
        """
        return self.create_custom_resource(
            group=self.group,
            version=self.version,
            plural=self.plural,
            body=spark_application.model_dump(by_alias=True, exclude_none=True),
            namespace=spark_application.metadata.get("namespace")
            or self.config.client.namespace,
        )

    def get(self, name: str, namespace: str = None) -> SparkApplication:
        """Gets a SparkApplication.

        Args:
            name: The name of the SparkApplication.
            namespace: The namespace of the SparkApplication.

        Returns:
            The SparkApplication.
        """
        resource = self.get_custom_resource(
            group=self.group,
            version=self.version,
            plural=self.plural,
            name=name,
            namespace=namespace or self.config.client.namespace,
        )
        return SparkApplication(**resource)

    def list(self, namespace: str = None) -> list[SparkApplication]:
        """Lists SparkApplications.

        Args:
            namespace: The namespace to list SparkApplications in.

        Returns:
            A list of SparkApplications.
        """
        return [
            SparkApplication(**item)
            for item in self.list_custom_resources(
                group=self.group,
                version=self.version,
                plural=self.plural,
                namespace=namespace or self.config.client.namespace,
            )
        ]

    def update(self, spark_application: SparkApplication):
        """Updates a SparkApplication.

        Args:
            spark_application: The SparkApplication to update.
        """
        return self.patch_custom_resource(
            group=self.group,
            version=self.version,
            plural=self.plural,
            name=spark_application.metadata["name"],
            body=spark_application.model_dump(by_alias=True, exclude_none=True),
            namespace=spark_application.metadata.get("namespace")
            or self.config.client.namespace,
        )

    def delete(self, name: str, namespace: str = None):
        """Deletes a SparkApplication.

        Args:
            name: The name of the SparkApplication.
            namespace: The namespace of the SparkApplication.
        """
        return self.delete_custom_resource(
            group=self.group,
            version=self.version,
            plural=self.plural,
            name=name,
            namespace=namespace or self.config.client.namespace,
        )
