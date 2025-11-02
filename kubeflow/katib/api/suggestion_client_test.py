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

from kubeflow.katib.api.suggestion_client import SuggestionClient
from kubeflow.katib.types import Suggestion


def test_create_suggestion():
    with patch(
        "kubeflow.core.base_client.KubeconfigAuthProvider"
    ), patch(
        "kubeflow.core.base_client.client.ApiClient"
    ), patch(
        "kubeflow.core.base_client.client.CustomObjectsApi"
    ) as mock_custom_api:
        def mock_create_suggestion(body, **_):
            return body
        mock_custom_api.return_value.create_namespaced_custom_object.side_effect = mock_create_suggestion
        client = SuggestionClient()
        suggestion = Suggestion(
            apiVersion="kubeflow.org/v1beta1",
            kind="Suggestion",
            metadata={"name": "my-suggestion"},
        )
        client.create(suggestion=suggestion, namespace="my-namespace")
        mock_custom_api.return_value.create_namespaced_custom_object.assert_called_with(
            group="kubeflow.org",
            version="v1beta1",
            plural="suggestions",
            body=suggestion.to_dict(),
            namespace="my-namespace",
        )


def test_get_suggestion():
    with patch(
        "kubeflow.core.base_client.KubeconfigAuthProvider"
    ), patch(
        "kubeflow.core.base_client.client.ApiClient"
    ), patch(
        "kubeflow.core.base_client.client.CustomObjectsApi"
    ) as mock_custom_api:
        mock_custom_api.return_value.get_namespaced_custom_object.return_value = {
            "apiVersion": "kubeflow.org/v1beta1",
            "kind": "Suggestion",
            "metadata": {"name": "my-suggestion"},
        }
        client = SuggestionClient()
        suggestion = client.get(name="my-suggestion", namespace="my-namespace")
        assert suggestion.metadata["name"] == "my-suggestion"


def test_list_suggestions():
    with patch(
        "kubeflow.core.base_client.KubeconfigAuthProvider"
    ), patch(
        "kubeflow.core.base_client.client.ApiClient"
    ), patch(
        "kubeflow.core.base_client.client.CustomObjectsApi"
    ) as mock_custom_api:
        mock_custom_api.return_value.list_namespaced_custom_object.return_value = {
            "items": [
                {
                    "apiVersion": "kubeflow.org/v1beta1",
                    "kind": "Suggestion",
                    "metadata": {"name": "my-suggestion"},
                }
            ]
        }
        client = SuggestionClient()
        suggestions = client.list(namespace="my-namespace")
        assert len(suggestions) == 1
        assert suggestions[0].metadata["name"] == "my-suggestion"


def test_delete_suggestion():
    with patch(
        "kubeflow.core.base_client.KubeconfigAuthProvider"
    ), patch(
        "kubeflow.core.base_client.client.ApiClient"
    ), patch(
        "kubeflow.core.base_client.client.CustomObjectsApi"
    ) as mock_custom_api:
        client = SuggestionClient()
        client.delete(name="my-suggestion", namespace="my-namespace")
        mock_custom_api.return_value.delete_namespaced_custom_object.assert_called_with(
            group="kubeflow.org",
            version="v1beta1",
            plural="suggestions",
            name="my-suggestion",
            namespace="my-namespace",
        )
