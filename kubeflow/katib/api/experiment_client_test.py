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
from kubeflow_katib_api.models import (
    V1beta1AlgorithmSpec,
    V1beta1ExperimentSpec,
    V1beta1FeasibleSpace,
    V1beta1ObjectiveSpec,
    V1beta1ParameterSpec,
)
from kubeflow.katib.api.experiment_client import ExperimentClient
from kubeflow.katib.types import Optimizer
from kubeflow.katib.types.search_types import Search

# TODO(Bobgy): test the real API server instead of mocking the client.


def test_create_experiment():
    optimizer = Optimizer(
        name="my-experiment",
        search_space={
            "learning_rate": Search.uniform(min=0.1, max=0.5),
            "num_layers": Search.uniform(min=2, max=10),
            "optimizer": Search.choice(["adam", "sgd"]),
        },
        objective={
            "type": "maximize",
            "goal": 0.99,
        },
        algorithm={"name": "random", "settings": {"random_state": "10"}},
    )
    with patch(
        "kubeflow.core.base_client.KubeconfigAuthProvider"
    ), patch(
        "kubeflow.core.base_client.client.ApiClient"
    ), patch(
        "kubeflow.core.base_client.client.CustomObjectsApi"
    ) as mock_custom_api:
        def mock_create_experiment(body, **_):
            return body
        mock_custom_api.return_value.create_namespaced_custom_object.side_effect = mock_create_experiment
        client = ExperimentClient()
        client.create(optimizer=optimizer, namespace="my-namespace")
        mock_custom_api.return_value.create_namespaced_custom_object.assert_called_with(
            body={
                "apiVersion": "kubeflow.org/v1beta1",
                "kind": "Experiment",
                "metadata": {
                    "name": "my-experiment",
                    "namespace": "my-namespace",
                },
                "spec": V1beta1ExperimentSpec(
                    objective=V1beta1ObjectiveSpec(
                        type="maximize",
                        goal=0.99,
                    ),
                    algorithm=V1beta1AlgorithmSpec(
                        algorithm_name="random",
                        algorithm_settings=[
                            {"name": "random_state", "value": "10"},
                        ],
                    ),
                    parameters=[
                        V1beta1ParameterSpec(
                            name="learning_rate",
                            parameter_type="double",
                            feasible_space=V1beta1FeasibleSpace(
                                min="0.1", max="0.5", distribution="uniform"
                            ),
                        ),
                        V1beta1ParameterSpec(
                            name="num_layers",
                            parameter_type="double",
                            feasible_space=V1beta1FeasibleSpace(
                                min="2", max="10", distribution="uniform"
                            ),
                        ),
                        V1beta1ParameterSpec(
                            name="optimizer",
                            parameter_type="categorical",
                            feasible_space=V1beta1FeasibleSpace(list=["adam", "sgd"]),
                        ),
                    ],
                ).to_dict(),
            },
            group="kubeflow.org",
            namespace="my-namespace",
            plural="experiments",
            version="v1beta1",
        )


def test_delete_experiment():
    with patch(
        "kubeflow.core.base_client.KubeconfigAuthProvider"
    ), patch(
        "kubeflow.core.base_client.client.ApiClient"
    ), patch(
        "kubeflow.core.base_client.client.CustomObjectsApi"
    ) as mock_custom_api:
        client = ExperimentClient()
        client.delete(name="my-experiment", namespace="my-namespace")
        mock_custom_api.return_value.delete_namespaced_custom_object.assert_called_with(
            name="my-experiment",
            group="kubeflow.org",
            namespace="my-namespace",
            plural="experiments",
            version="v1beta1",
        )


def test_pause_experiment():
    with patch(
        "kubeflow.core.base_client.KubeconfigAuthProvider"
    ), patch(
        "kubeflow.core.base_client.client.ApiClient"
    ), patch(
        "kubeflow.core.base_client.client.CustomObjectsApi"
    ) as mock_custom_api:
        client = ExperimentClient()
        client.pause(name="my-experiment", namespace="my-namespace")
        mock_custom_api.return_value.patch_namespaced_custom_object.assert_called_with(
            name="my-experiment",
            group="kubeflow.org",
            namespace="my-namespace",
            plural="experiments",
            version="v1beta1",
            body={"spec": {"resumePolicy": "Never"}},
        )


def test_resume_experiment():
    with patch(
        "kubeflow.core.base_client.KubeconfigAuthProvider"
    ), patch(
        "kubeflow.core.base_client.client.ApiClient"
    ), patch(
        "kubeflow.core.base_client.client.CustomObjectsApi"
    ) as mock_custom_api:
        client = ExperimentClient()
        client.resume(name="my-experiment", namespace="my-namespace")
        mock_custom_api.return_value.patch_namespaced_custom_object.assert_called_with(
            name="my-experiment",
            group="kubeflow.org",
            namespace="my-namespace",
            plural="experiments",
            version="v1beta1",
            body={"spec": {"resumePolicy": "LongRunning"}},
        )


def test_get_optimal_trial():
    with patch(
        "kubeflow.core.base_client.KubeconfigAuthProvider"
    ), patch(
        "kubeflow.core.base_client.client.ApiClient"
    ), patch(
        "kubeflow.core.base_client.client.CustomObjectsApi"
    ) as mock_custom_api:
        mock_custom_api.return_value.get_namespaced_custom_object.return_value = {
            "apiVersion": "kubeflow.org/v1beta1",
            "kind": "Experiment",
            "metadata": {"name": "my-experiment"},
            "status": {
                "currentOptimalTrial": {
                    "parameterAssignments": [
                        {"name": "lr", "value": "0.01"},
                        {"name": "num-layers", "value": "4"},
                    ]
                }
            },
        }
        client = ExperimentClient()
        optimal_trial = client.get_optimal_trial(
            name="my-experiment", namespace="my-namespace"
        )
        assert optimal_trial == {
            "parameterAssignments": [
                {"name": "lr", "value": "0.01"},
                {"name": "num-layers", "value": "4"},
            ]
        }
