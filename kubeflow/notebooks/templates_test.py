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

from kubeflow.notebooks.templates import JUPYTER_TEMPLATE, VSCODE_TEMPLATE


def test_jupyter_template():
    """Tests the Jupyter template."""
    assert JUPYTER_TEMPLATE.name == "jupyter"
    assert JUPYTER_TEMPLATE.template.spec["containers"][0]["name"] == "jupyter"
    assert (
        JUPYTER_TEMPLATE.template.spec["containers"][0]["image"] == "jupyter/base-notebook:latest"
    )
    assert JUPYTER_TEMPLATE.template.spec["containers"][0]["ports"][0]["containerPort"] == 8888


def test_vscode_template():
    """Tests the VSCode template."""
    assert VSCODE_TEMPLATE.name == "vscode"
    assert VSCODE_TEMPLATE.template.spec["containers"][0]["name"] == "vscode"
    assert VSCODE_TEMPLATE.template.spec["containers"][0]["image"] == "codercom/code-server:latest"
    assert VSCODE_TEMPLATE.template.spec["containers"][0]["ports"][0]["containerPort"] == 8080
