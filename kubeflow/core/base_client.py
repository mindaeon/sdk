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

from kubernetes import client

from kubeflow.core.auth import KubeconfigAuthProvider
from kubeflow.core.config import KubeflowConfig
from kubeflow.core.k8s_resource import K8sResource


class BaseClient:
    """Base class for all Kubeflow SDK clients."""

    def __init__(self, config: Optional[KubeflowConfig] = None):
        """Initializes a BaseClient.

        Args:
            config: The KubeflowConfig object to use for authentication.
        """
        self.config = config or KubeflowConfig()
        auth_provider = KubeconfigAuthProvider(
            config=self.config.kubeconfig, context=self.config.context
        )
        k8s_config = auth_provider.get_api_client_configuration()
        self.api_client = client.ApiClient(k8s_config)
        self.custom_api = client.CustomObjectsApi(self.api_client)
        self.core_v1_api = client.CoreV1Api(self.api_client)

    def get_custom_resource(
        self,
        group: str,
        version: str,
        plural: str,
        name: str,
        namespace: Optional[str] = None,
    ) -> K8sResource:
        """Gets a custom resource.

        Args:
            group: The group of the custom resource.
            version: The version of the custom resource.
            plural: The plural name of the custom resource.
            name: The name of the custom resource.
            namespace: The namespace of the custom resource.

        Returns:
            The custom resource as a K8sResource object.
        """
        namespace = namespace or self.config.namespace
        api_response = self.custom_api.get_namespaced_custom_object(
            group=group,
            version=version,
            namespace=namespace,
            plural=plural,
            name=name,
        )
        return K8sResource(**api_response)

    def list_custom_resources(
        self,
        group: str,
        version: str,
        plural: str,
        namespace: Optional[str] = None,
    ) -> list[K8sResource]:
        """Lists custom resources.

        Args:
            group: The group of the custom resources.
            version: The version of the custom resources.
            plural: The plural name of the custom resources.
            namespace: The namespace of the custom resources.

        Returns:
            A list of custom resources as K8sResource objects.
        """
        namespace = namespace or self.config.namespace
        api_response = self.custom_api.list_namespaced_custom_object(
            group=group,
            version=version,
            namespace=namespace,
            plural=plural,
        )
        return [K8sResource(**item) for item in api_response["items"]]

    def create_custom_resource(
        self,
        group: str,
        version: str,
        plural: str,
        body: dict[str, Any],
        namespace: Optional[str] = None,
    ) -> K8sResource:
        """Creates a custom resource.

        Args:
            group: The group of the custom resource.
            version: The version of the custom resource.
            plural: The plural name of the custom resource.
            body: The body of the custom resource.
            namespace: The namespace of the custom resource.

        Returns:
            The created custom resource as a K8sResource object.
        """
        namespace = namespace or self.config.namespace
        api_response = self.custom_api.create_namespaced_custom_object(
            group=group,
            version=version,
            namespace=namespace,
            plural=plural,
            body=body,
        )
        return K8sResource(**api_response)

    def patch_custom_resource(
        self,
        group: str,
        version: str,
        plural: str,
        name: str,
        body: dict[str, Any],
        namespace: Optional[str] = None,
    ):
        """Patches a custom resource.

        Args:
            group: The group of the custom resource.
            version: The version of the custom resource.
            plural: The plural name of the custom resource.
            name: The name of the custom resource.
            body: The body of the patch.
            namespace: The namespace of the custom resource.
        """
        namespace = namespace or self.config.namespace
        self.custom_api.patch_namespaced_custom_object(
            group=group,
            version=version,
            namespace=namespace,
            plural=plural,
            name=name,
            body=body,
        )

    def delete_custom_resource(
        self,
        group: str,
        version: str,
        plural: str,
        name: str,
        namespace: Optional[str] = None,
    ):
        """Deletes a custom resource.

        Args:
            group: The group of the custom resource.
            version: The version of the custom resource.
            plural: The plural name of the custom resource.
            name: The name of the custom resource.
            namespace: The namespace of the custom resource.
        """
        namespace = namespace or self.config.namespace
        self.custom_api.delete_namespaced_custom_object(
            group=group,
            version=version,
            namespace=namespace,
            plural=plural,
            name=name,
        )
