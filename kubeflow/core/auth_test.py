# Copyright 2024 The Kubeflow Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law of an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from unittest.mock import patch

from kubernetes import client

from kubeflow.core.auth import InClusterAuthProvider, KubeconfigAuthProvider


@patch("kubernetes.config.load_kube_config")
def test_kubeconfig_auth_provider(mock_load_kube_config):
    """Tests the KubeconfigAuthProvider."""
    provider = KubeconfigAuthProvider()
    config = provider.get_api_client_configuration()

    mock_load_kube_config.assert_called_once()
    assert isinstance(config, client.Configuration)


@patch("kubernetes.config.load_incluster_config")
def test_in_cluster_auth_provider(mock_load_incluster_config):
    """Tests the InClusterAuthProvider."""
    provider = InClusterAuthProvider()
    config = provider.get_api_client_configuration()

    mock_load_incluster_config.assert_called_once()
    assert isinstance(config, client.Configuration)
