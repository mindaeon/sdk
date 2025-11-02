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

from unittest import mock

from kubeflow.notebooks.models import Notebook, NotebookSpec, NotebookTemplateSpec
from kubeflow.notebooks.simulator import NotebookSimulator


@mock.patch("docker.from_env")
def test_create_notebook(mock_docker_from_env):
    """Tests creating a simulated notebook."""
    simulator = NotebookSimulator()
    notebook = Notebook(
        name="test-notebook",
        spec=NotebookSpec(
            template=NotebookTemplateSpec(
                spec={
                    "containers": [
                        {
                            "name": "jupyter",
                            "image": "jupyter/base-notebook:latest",
                            "ports": [{"containerPort": 8888}],
                        }
                    ]
                }
            )
        ),
    )
    simulator.create(notebook)
    simulator.client.containers.run.assert_called_with(
        "jupyter/base-notebook:latest",
        detach=True,
        ports={"8888/tcp": None},
    )


@mock.patch("docker.from_env")
def test_get_notebook(mock_docker_from_env):
    """Tests getting a simulated notebook."""
    simulator = NotebookSimulator()
    simulator.get("test-notebook")
    simulator.client.containers.get.assert_called_with("test-notebook")


@mock.patch("docker.from_env")
def test_delete_notebook(mock_docker_from_env):
    """Tests deleting a simulated notebook."""
    simulator = NotebookSimulator()
    container = mock.MagicMock()
    simulator.client.containers.get.return_value = container
    simulator.delete("test-notebook")
    simulator.client.containers.get.assert_called_with("test-notebook")
    container.stop.assert_called_with()
    container.remove.assert_called_with()
