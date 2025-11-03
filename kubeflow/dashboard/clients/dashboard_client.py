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

"""The Kubeflow Dashboard SDK."""

from kubeflow.core.base_client import BaseClient

from ..types import Profile


class DashboardClient(BaseClient):
    """A client for interacting with the Kubeflow Central Dashboard.

    This component is responsible for managing multi-user isolation, which is
    based on `Profile` custom resources.
    """

    def create_profile(self, profile: Profile):
        """Creates a new `Profile`.

        Args:
            profile: The `Profile` object to create.
        """
        self.create_cluster_custom_resource(
            group="kubeflow.org",
            version="v1",
            plural="profiles",
            body=profile.model_dump(by_alias=True),
        )

    def get_profile(self, name: str) -> Profile:
        """Gets a `Profile`.

        Args:
            name: The name of the `Profile` to get.

        Returns:
            The `Profile` object.
        """
        resource = self.get_cluster_custom_resource(
            group="kubeflow.org",
            version="v1",
            plural="profiles",
            name=name,
        )
        return Profile(**resource.model_dump(by_alias=True))

    def delete_profile(self, name: str):
        """Deletes a `Profile`.

        Args:
            name: The name of the `Profile` to delete.
        """
        self.delete_cluster_custom_resource(
            group="kubeflow.org",
            version="v1",
            plural="profiles",
            name=name,
        )
