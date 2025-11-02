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

from kubeflow.katib.api.trial_client import TrialClient
from kubeflow.katib.types import Trial


def test_create_trial():
    with patch(
        "kubeflow.core.base_client.KubeconfigAuthProvider"
    ), patch(
        "kubeflow.core.base_client.client.ApiClient"
    ), patch(
        "kubeflow.core.base_client.client.CustomObjectsApi"
    ) as mock_custom_api:
        def mock_create_trial(body, **_):
            return body
        mock_custom_api.return_value.create_namespaced_custom_object.side_effect = mock_create_trial
        client = TrialClient()
        trial = Trial(
            apiVersion="kubeflow.org/v1beta1",
            kind="Trial",
            metadata={"name": "my-trial"},
        )
        client.create(trial=trial, namespace="my-namespace")
        mock_custom_api.return_value.create_namespaced_custom_object.assert_called_with(
            group="kubeflow.org",
            version="v1beta1",
            plural="trials",
            body=trial.to_dict(),
            namespace="my-namespace",
        )


def test_get_trial():
    with patch(
        "kubeflow.core.base_client.KubeconfigAuthProvider"
    ), patch(
        "kubeflow.core.base_client.client.ApiClient"
    ), patch(
        "kubeflow.core.base_client.client.CustomObjectsApi"
    ) as mock_custom_api:
        mock_custom_api.return_value.get_namespaced_custom_object.return_value = {
            "apiVersion": "kubeflow.org/v1beta1",
            "kind": "Trial",
            "metadata": {"name": "my-trial"},
        }
        client = TrialClient()
        trial = client.get(name="my-trial", namespace="my-namespace")
        assert trial.metadata["name"] == "my-trial"


def test_list_trials():
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
                    "kind": "Trial",
                    "metadata": {"name": "my-trial"},
                }
            ]
        }
        client = TrialClient()
        trials = client.list(namespace="my-namespace")
        assert len(trials) == 1
        assert trials[0].metadata["name"] == "my-trial"


def test_delete_trial():
    with patch(
        "kubeflow.core.base_client.KubeconfigAuthProvider"
    ), patch(
        "kubeflow.core.base_client.client.ApiClient"
    ), patch(
        "kubeflow.core.base_client.client.CustomObjectsApi"
    ) as mock_custom_api:
        client = TrialClient()
        client.delete(name="my-trial", namespace="my-namespace")
        mock_custom_api.return_value.delete_namespaced_custom_object.assert_called_with(
            group="kubeflow.org",
            version="v1beta1",
            plural="trials",
            name="my-trial",
            namespace="my-namespace",
        )
