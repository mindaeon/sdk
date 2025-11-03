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

"""Test the Kubeflow Dashboard SDK."""

from unittest.mock import MagicMock, patch

from kubeflow.dashboard.clients.dashboard_client import DashboardClient
from kubeflow.dashboard.types import Owner, Profile, ProfileSpec, ResourceQuota


@patch("kubeflow.core.base_client.KubeconfigAuthProvider")
@patch("kubernetes.client.ApiClient")
@patch("kubernetes.client.CustomObjectsApi")
def test_create_profile(mock_custom_api, mock_api_client, mock_auth):
    """Test creating a profile."""
    profile = Profile(
        apiVersion="kubeflow.org/v1",
        kind="Profile",
        metadata={"name": "my-profile"},
        spec=ProfileSpec(
            owner=Owner(kind="User", name="user@example.com"),
            resource_quota_spec=ResourceQuota(
                hard={
                    "cpu": "1",
                    "memory": "1Gi",
                }
            ),
        ),
    )
    client = DashboardClient()
    client.custom_api = MagicMock()
    client.custom_api.create_cluster_custom_object.return_value = (
        profile.model_dump(by_alias=True)
    )
    client.create_profile(profile=profile)
    client.custom_api.create_cluster_custom_object.assert_called_once_with(
        group="kubeflow.org",
        version="v1",
        plural="profiles",
        body=profile.model_dump(by_alias=True),
    )


@patch("kubeflow.core.base_client.KubeconfigAuthProvider")
@patch("kubernetes.client.ApiClient")
@patch("kubernetes.client.CustomObjectsApi")
def test_get_profile(mock_custom_api, mock_api_client, mock_auth):
    """Test getting a profile."""
    api_response = {
        "apiVersion": "kubeflow.org/v1",
        "kind": "Profile",
        "metadata": {"name": "my-profile"},
        "spec": {"owner": {"kind": "User", "name": "user@example.com"}},
    }
    client = DashboardClient()
    client.custom_api = MagicMock()
    client.custom_api.get_cluster_custom_object.return_value = api_response
    profile = client.get_profile(name="my-profile")
    client.custom_api.get_cluster_custom_object.assert_called_once_with(
        group="kubeflow.org",
        version="v1",
        plural="profiles",
        name="my-profile",
    )
    assert profile.kind == "Profile"
    assert profile.metadata["name"] == "my-profile"


@patch("kubeflow.core.base_client.KubeconfigAuthProvider")
@patch("kubernetes.client.ApiClient")
@patch("kubernetes.client.CustomObjectsApi")
def test_delete_profile(mock_custom_api, mock_api_client, mock_auth):
    """Test deleting a profile."""
    client = DashboardClient()
    client.custom_api = MagicMock()
    client.delete_profile(name="my-profile")
    client.custom_api.delete_cluster_custom_object.assert_called_once_with(
        group="kubeflow.org",
        version="v1",
        plural="profiles",
        name="my-profile",
    )
