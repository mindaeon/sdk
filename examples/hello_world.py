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

from kubeflow.pipelines.api import PipelineClient, RunClient
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


if __name__ == "__main__":
    compiler = Compiler()
    pipeline_yaml = compiler.compile(hello_world_pipeline(name="world"))

    # In a real-world scenario, you would save this YAML to a file
    # and upload it to Kubeflow Pipelines.
    print(pipeline_yaml)

    # You can also use the client to interact with the API.
    pipeline_client = PipelineClient()
    run_client = RunClient()

    # Create a pipeline
    # pipeline = pipeline_client.create_pipeline("hello-world-pipeline")
    # print(pipeline)

    # Create a pipeline version
    # with open("pipeline.yaml", "w") as f:
    #     f.write(pipeline_yaml)
    #
    # pipeline_version = pipeline_client.create_pipeline_version(
    #     pipeline.pipeline_id, "v1", "pipeline.yaml"
    # )
    # print(pipeline_version)

    # Create a run
    # run = run_client.create_run(
    #     "hello-world-run",
    #     pipeline_version_reference={
    #         "pipeline_id": pipeline.pipeline_id,
    #         "pipeline_version_id": pipeline_version.pipeline_version_id,
    #     },
    # )
    # print(run)
