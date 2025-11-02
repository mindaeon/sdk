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

from kubeflow.katib import (
    V1beta1AlgorithmSpec,
    V1beta1ExperimentSpec,
    V1beta1FeasibleSpace,
    V1beta1ObjectiveSpec,
    V1beta1ParameterSpec,
)
from kubeflow.optimizer import Optimizer, OptimizerClient, SearchSpace

# TODO(Bobgy): test the real API server instead of mocking the client.


def test_create_optimizer():
    search_space = SearchSpace(
        [
            {
                "name": "learning_rate",
                "type": "double",
                "space": {"min": "0.1", "max": "0.5", "step": "0.1"},
            },
            {
                "name": "num_layers",
                "type": "int",
                "space": {"min": "2", "max": "10", "step": "1"},
            },
            {
                "name": "optimizer",
                "type": "categorical",
                "space": {"values": ["adam", "sgd"]},
            },
            {
                "name": "learning_rate2",
                "type": "discrete",
                "space": {"values": ["0.1", "0.3", "0.5"]},
            },
        ]
    )
    optimizer = Optimizer(
        name="my-optimizer",
        search_space=search_space,
        objective={
            "type": "maximize",
            "goal": 0.99,
        },
        algorithm={"name": "random", "settings": {"random_state": "10"}},
    )
    with (
        patch("kubeflow.core.base_client.KubeconfigAuthProvider"),
        patch("kubeflow.core.base_client.client.ApiClient"),
        patch("kubeflow.core.base_client.client.CustomObjectsApi") as mock_custom_api,
    ):
        client = OptimizerClient()
        client.create(optimizer=optimizer, namespace="my-namespace")
        mock_custom_api.return_value.create_namespaced_custom_object.assert_called_with(
            body={
                "apiVersion": "kubeflow.org/v1beta1",
                "kind": "Experiment",
                "metadata": {
                    "name": "my-optimizer",
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
                            feasible_space=V1beta1FeasibleSpace(min="0.1", max="0.5", step="0.1"),
                        ),
                        V1beta1ParameterSpec(
                            name="num_layers",
                            parameter_type="int",
                            feasible_space=V1beta1FeasibleSpace(min="2", max="10", step="1"),
                        ),
                        V1beta1ParameterSpec(
                            name="optimizer",
                            parameter_type="categorical",
                            feasible_space=V1beta1FeasibleSpace(list=["adam", "sgd"]),
                        ),
                        V1beta1ParameterSpec(
                            name="learning_rate2",
                            parameter_type="discrete",
                            feasible_space=V1beta1FeasibleSpace(list=["0.1", "0.3", "0.5"]),
                        ),
                    ],
                ).to_dict(),
            },
            group="kubeflow.org",
            namespace="my-namespace",
            plural="experiments",
            version="v1beta1",
        )


def test_delete_optimizer():
    with (
        patch("kubeflow.core.base_client.KubeconfigAuthProvider"),
        patch("kubeflow.core.base_client.client.ApiClient"),
        patch("kubeflow.core.base_client.client.CustomObjectsApi") as mock_custom_api,
    ):
        client = OptimizerClient()
        client.delete(name="my-optimizer", namespace="my-namespace")
        mock_custom_api.return_value.delete_namespaced_custom_object.assert_called_with(
            name="my-optimizer",
            group="kubeflow.org",
            namespace="my-namespace",
            plural="experiments",
            version="v1beta1",
        )


@pytest.mark.parametrize(
    "backend_config, expected",
    [
        (
            {"backend": "kubernetes"},
            "The optimizer `my-optimizer` in `my-namespace` has been created.",
        ),
        (
            {"backend": "google-cloud"},
            "The optimizer `my-optimizer` in `my-namespace` has been created on Google Cloud.",
        ),
        (
            {"backend": "google-cloud", "project": "my-project"},
            (
                "The optimizer `my-optimizer` in `my-namespace` has been created on "
                "Google Cloud in project `my-project`."
            ),
        ),
        (
            {
                "backend": "google-cloud",
                "project": "my-project",
                "region": "my-region",
            },
            (
                "The optimizer `my-optimizer` in `my-namespace` has been created on "
                "Google Cloud in project `my-project` region `my-region`."
            ),
        ),
    ],
)
def test_backend_config_message(backend_config, expected):
    search_space = SearchSpace(
        [
            {
                "name": "learning_rate",
                "type": "double",
                "space": {"min": "0.1", "max": "0.5", "step": "0.1"},
            }
        ]
    )
    optimizer = Optimizer(
        name="my-optimizer",
        search_space=search_space,
    )
    with (
        patch("kubeflow.core.base_client.KubeconfigAuthProvider"),
        patch("kubeflow.core.base_client.client.ApiClient"),
        patch("kubeflow.core.base_client.client.CustomObjectsApi"),
    ):
        client = OptimizerClient(backend_config=backend_config)
        actual = client.create(optimizer=optimizer, namespace="my-namespace")
        assert actual == expected
