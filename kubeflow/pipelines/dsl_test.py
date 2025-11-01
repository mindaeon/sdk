# Copyright 2025 The Kubeflow Authors.
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

from kubeflow.pipelines import dsl


def test_component_decorator():
    """Tests the @dsl.component decorator."""

    @dsl.component
    def my_component(a: int, b: str) -> str:
        """My component."""
        return f"{b} {a}"

    assert my_component.component_spec.name == "my_component"
    assert my_component.component_spec.description == "My component."
    assert len(my_component.component_spec.inputs) == 2
    assert my_component.component_spec.inputs[0].name == "a"
    assert my_component.component_spec.inputs[0].type == "<class 'int'>"
    assert my_component.component_spec.inputs[1].name == "b"
    assert my_component.component_spec.inputs[1].type == "<class 'str'>"
    assert len(my_component.component_spec.outputs) == 1
    assert my_component.component_spec.outputs[0].name == "output"
    assert my_component.component_spec.outputs[0].type == "<class 'str'>"


def test_component_decorator_no_inputs_no_outputs():
    """Tests the @dsl.component decorator with no inputs and no outputs."""

    @dsl.component
    def my_component():
        """My component."""
        print("hello")

    assert my_component.component_spec.name == "my_component"
    assert my_component.component_spec.description == "My component."
    assert len(my_component.component_spec.inputs) == 0
    assert len(my_component.component_spec.outputs) == 0


def test_component_decorator_no_inputs_with_output():
    """Tests the @dsl.component decorator with no inputs and with an output."""

    @dsl.component
    def my_component() -> str:
        """My component."""
        return "hello"

    assert my_component.component_spec.name == "my_component"
    assert my_component.component_spec.description == "My component."
    assert len(my_component.component_spec.inputs) == 0
    assert len(my_component.component_spec.outputs) == 1
    assert my_component.component_spec.outputs[0].name == "output"
    assert my_component.component_spec.outputs[0].type == "<class 'str'>"
