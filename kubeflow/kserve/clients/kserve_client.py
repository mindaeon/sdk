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
from kubeflow.kserve.types import InferenceService, PredictorSpec


class KServeClient(BaseClient):
    """KServeClient is a client for managing KServe InferenceServices."""

    def __init__(self, **kwargs):
        """Initializes a KServeClient."""
        super().__init__(**kwargs)
        self.group = "serving.kserve.io"
        self.version = "v1beta1"
        self.plural = "inferenceservices"

    def create(self, inferenceservice: InferenceService):
        """Creates an InferenceService.

        Args:
            inferenceservice: The InferenceService to create.
        """
        return self.create_custom_resource(
            group=self.group,
            version=self.version,
            plural=self.plural,
            body=inferenceservice.model_dump(by_alias=True, exclude_none=True),
            namespace=inferenceservice.metadata.get("namespace")
            or self.config.client.namespace,
        )

    def get(self, name: str, namespace: str = None) -> InferenceService:
        """Gets an InferenceService.

        Args:
            name: The name of the InferenceService.
            namespace: The namespace of the InferenceService.

        Returns:
            The InferenceService.
        """
        resource = self.get_custom_resource(
            group=self.group,
            version=self.version,
            plural=self.plural,
            name=name,
            namespace=namespace or self.config.client.namespace,
        )
        return InferenceService(
            name=resource["metadata"]["name"],
            predictor=PredictorSpec(**resource["spec"]["predictor"]),
        )

    def list(self, namespace: str = None) -> list[InferenceService]:
        """Lists InferenceServices.

        Args:
            namespace: The namespace to list InferenceServices in.

        Returns:
            A list of InferenceServices.
        """
        return [
            InferenceService(
                name=item["metadata"]["name"],
                predictor=PredictorSpec(**item["spec"]["predictor"]),
            )
            for item in self.list_custom_resources(
                group=self.group,
                version=self.version,
                plural=self.plural,
                namespace=namespace or self.config.client.namespace,
            )
        ]

    def update(self, inferenceservice: InferenceService):
        """Updates an InferenceService.

        Args:
            inferenceservice: The InferenceService to update.
        """
        return self.patch_custom_resource(
            group=self.group,
            version=self.version,
            plural=self.plural,
            name=inferenceservice.metadata["name"],
            body=inferenceservice.model_dump(by_alias=True, exclude_none=True),
            namespace=inferenceservice.metadata.get("namespace")
            or self.config.client.namespace,
        )

    def delete(self, name: str, namespace: str = None):
        """Deletes an InferenceService.

        Args:
            name: The name of the InferenceService.
            namespace: The namespace of the InferenceService.
        """
        return self.delete_custom_resource(
            group=self.group,
            version=self.version,
            plural=self.plural,
            name=name,
            namespace=namespace or self.config.client.namespace,
        )
