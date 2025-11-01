# Copyright 2024 The Kubeflow Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law_ or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Any, Dict, List, Optional

from kubernetes import client

from .auth import InClusterAuthProvider, KubeconfigAuthProvider
from .config import KubeflowConfig
from .k8s_resource import K8sResource


class BaseClient:
    """Base class for Kubeflow clients."""

    def __init__(self, config: Optional[KubeflowConfig] = None):
        """Initializes the BaseClient."""
        if not config:
            config = KubeflowConfig()
        self.config = config

        if self.config.auth.provider == "kubeconfig":
            auth_provider = KubeconfigAuthProvider()
        elif self.config.auth.provider == "incluster":
            auth_provider = InClusterAuthProvider()
        else:
            raise ValueError(
                f"Invalid auth provider: {self.config.auth.provider}"
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
        """Gets a Kubernetes custom resource."""
        namespace = namespace or self.config.client.namespace
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
    ) -> List[K8sResource]:
        """Lists Kubernetes custom resources."""
        namespace = namespace or self.config.client.namespace
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
        body: Dict[str, Any],
        namespace: Optional[str] = None,
    ) -> K8sResource:
        """Creates a Kubernetes custom resource."""
        namespace = namespace or self.config.client.namespace
        api_response = self.custom_api.create_namespaced_custom_object(
            group=group,
            version=version,
            namespace=namespace,
            plural=plural,
            body=body,
        )
        return K8sResource(**api_response)

    def delete_custom_resource(
        self,
        group: str,
        version: str,
        plural: str,
        name: str,
        namespace: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Deletes a Kubernetes custom resource."""
        namespace = namespace or self.config.client.namespace
        return self.custom_api.delete_namespaced_custom_object(
            group=group,
            version=version,
            namespace=namespace,
            plural=plural,
            name=name,
        )
