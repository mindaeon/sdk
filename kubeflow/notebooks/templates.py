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

from pydantic import BaseModel

from .models import NotebookTemplateSpec


class NotebookTemplate(BaseModel):
    """A template for creating a Notebook."""

    name: str
    template: NotebookTemplateSpec


JUPYTER_TEMPLATE = NotebookTemplate(
    name="jupyter",
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
    ),
)

VSCODE_TEMPLATE = NotebookTemplate(
    name="vscode",
    template=NotebookTemplateSpec(
        spec={
            "containers": [
                {
                    "name": "vscode",
                    "image": "codercom/code-server:latest",
                    "ports": [{"containerPort": 8080}],
                }
            ]
        }
    ),
)
