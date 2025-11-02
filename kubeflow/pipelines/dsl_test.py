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

from kubeflow.pipelines import dsl
from kubeflow.pipelines.types.component_spec import InputSpec


def test_component_decorator():
    """Tests the @dsl.component decorator."""

    @dsl.component(
        name="test-component",
        image="test-image",
        inputs=[InputSpec(name="test-input", type="String")],
    )
    def my_component(test_input: str):
        pass

    assert my_component.component_spec.name == "test-component"
    assert my_component.component_spec.implementation.image == "test-image"
    assert len(my_component.component_spec.inputs) == 1
    assert my_component.component_spec.inputs[0].name == "test-input"


def test_pipeline_decorator():
    """Tests the @dsl.pipeline decorator."""

    @dsl.pipeline(name="test-pipeline")
    def my_pipeline():
        pass

    pipeline = my_pipeline()
    assert pipeline.name == "test-pipeline"
