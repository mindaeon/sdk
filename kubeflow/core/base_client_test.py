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

from unittest.mock import patch

import pytest
from kubernetes import client
from kubeflow.core.base_client import BaseClient
from kubeflow.core.config import KubeflowConfig


@patch("kubeflow.core.base_client.KubeconfigAuthProvider")
def test_base_client_kubeconfig_auth(mock_kubeconfig_provider):
    """Tests that BaseClient uses KubeconfigAuthProvider by default."""
    mock_kubeconfig_provider.return_value.get_api_client_configuration.return_value = (
        client.Configuration()
    )
    BaseClient()
    mock_kubeconfig_provider.assert_called_once()


@patch("kubeflow.core.base_client.InClusterAuthProvider")
def test_base_client_incluster_auth(mock_incluster_provider):
    """Tests that BaseClient uses InClusterAuthProvider when configured."""
    mock_incluster_provider.return_value.get_api_client_configuration.return_value = (
        client.Configuration()
    )
    config = KubeflowConfig(auth={"provider": "incluster"})
    BaseClient(config=config)
    mock_incluster_provider.assert_called_once()


def test_base_client_invalid_auth_provider():
    """Tests that BaseClient raises an error for an invalid provider."""
    with pytest.raises(ValueError):
        config = KubeflowConfig()
        # Manually set an invalid provider to bypass pydantic validation
        config.auth.provider = "invalid"
        BaseClient(config=config)
