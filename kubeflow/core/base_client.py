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

from .config import KubeflowConfig
from .auth import AuthProvider, KubeConfigAuthProvider
from typing import Optional
from kubernetes import client

class BaseClient:
    """Base class for Kubeflow clients."""

    def __init__(
        self,
        config: Optional[KubeflowConfig] = None,
        auth_provider: Optional[AuthProvider] = None,
    ):
        """Initializes the BaseClient."""
        if not config:
            config = KubeflowConfig()
        self.config = config

        if not auth_provider:
            auth_provider = KubeConfigAuthProvider()
        self.auth_provider = auth_provider

        self.api_client = client.ApiClient(self.auth_provider.get_credentials())
