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

from abc import ABC, abstractmethod

from kubernetes import client, config


class AuthProvider(ABC):
    """Abstract base class for authentication providers."""

    @abstractmethod
    def get_api_client_configuration(self) -> client.Configuration:
        """
        Returns a Kubernetes client configuration.

        Returns:
            client.Configuration: The Kubernetes client configuration.
        """
        pass


class KubeconfigAuthProvider(AuthProvider):
    """
    Authentication provider that loads credentials from a local kubeconfig file.
    """

    def get_api_client_configuration(self) -> client.Configuration:
        """
        Loads Kubernetes configuration from the default kubeconfig file.

        Returns:
            client.Configuration: The Kubernetes client configuration.
        """
        config.load_kube_config()
        return client.Configuration.get_default_copy()


class InClusterAuthProvider(AuthProvider):
    """
    Authentication provider that uses the in-cluster service account token.
    """

    def get_api_client_configuration(self) -> client.Configuration:
        """
        Loads Kubernetes configuration from the in-cluster service account.

        Returns:
            client.Configuration: The Kubernetes client configuration.
        """
        config.load_incluster_config()
        return client.Configuration.get_default_copy()
