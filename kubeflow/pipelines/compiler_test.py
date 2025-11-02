# Copyright 2025 The Kubeflow Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law of agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import yaml

from kubeflow.pipelines.compiler import Compiler
from kubeflow.pipelines.dsl import component, pipeline
from kubeflow.pipelines.types.component_spec import InputSpec


@component(
    name="say-hello",
    image="alpine:latest",
    inputs=[InputSpec(name="name", type="String")],
    command=["echo", "hello", "{{$.inputs.parameters['name']}}"],
)
def say_hello(name: str):
    """A simple component that prints a greeting."""
    print(f"Hello, {name}!")


@pipeline(name="hello-world")
def hello_world_pipeline(name: str):
    """A simple pipeline that greets the user."""
    say_hello(name=name)


def test_compiler():
    """Tests the compiler."""
    compiler = Compiler()
    pipeline_yaml = yaml.safe_load(compiler.compile(hello_world_pipeline(name="world")))
    assert "pipeline_spec" in pipeline_yaml
    assert "components" in pipeline_yaml["pipeline_spec"]
    assert "say-hello" in pipeline_yaml["pipeline_spec"]["components"]
    assert "root" in pipeline_yaml["pipeline_spec"]
    assert "dag" in pipeline_yaml["pipeline_spec"]["root"]
    assert "tasks" in pipeline_yaml["pipeline_spec"]["root"]["dag"]
    assert "say-hello" in pipeline_yaml["pipeline_spec"]["root"]["dag"]["tasks"]
