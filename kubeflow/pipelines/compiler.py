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

import yaml

from kubeflow.pipelines.dsl import Pipeline


class Compiler:
    """A compiler for Kubeflow Pipelines."""

    def compile(self, pipeline: Pipeline) -> str:
        """Compiles a pipeline to KFP IR YAML."""
        pipeline_spec = {
            "pipeline_spec": {
                "components": {},
                "deployment_spec": {"executors": {}},
                "pipeline_info": {"name": pipeline.name},
                "root": {"dag": {"tasks": {}}},
            }
        }

        for task in pipeline.tasks:
            component_spec = task["component_spec"]
            pipeline_spec["pipeline_spec"]["components"][
                component_spec.name
            ] = component_spec.model_dump()
            pipeline_spec["pipeline_spec"]["root"]["dag"]["tasks"][
                task["name"]
            ] = {
                "caching_options": {"enable_cache": True},
                "component_ref": {"name": component_spec.name},
                "task_info": {"name": task["name"]},
            }

        return yaml.dump(pipeline_spec)
