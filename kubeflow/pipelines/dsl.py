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

import inspect
from functools import wraps
from typing import Callable, List

from kubeflow.pipelines.types.component_spec import (
    ComponentSpec,
    InputSpec,
    OutputSpec,
    ContainerSpec,
)


class Pipeline:
    """A pipeline context."""

    def __init__(self, name: str):
        self.name = name
        self.tasks = []

    def __enter__(self):
        Pipeline.active_pipeline = self
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        Pipeline.active_pipeline = None


def component(
    name: str,
    image: str,
    inputs: List[InputSpec] = None,
    outputs: List[OutputSpec] = None,
    command: List[str] = None,
):
    """Decorator for pipeline components."""

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if Pipeline.active_pipeline:
                task = {
                    "name": name,
                    "component_spec": wrapper.component_spec,
                    "arguments": kwargs,
                }
                Pipeline.active_pipeline.tasks.append(task)
            return func(*args, **kwargs)

        wrapper.component_spec = ComponentSpec(
            name=name,
            description=func.__doc__,
            inputs=inputs or [],
            outputs=outputs or [],
            implementation=ContainerSpec(
                image=image,
                command=command or [],
            ),
        )
        return wrapper

    return decorator


def pipeline(name: str):
    """Decorator for pipelines."""

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with Pipeline(name) as p:
                func(*args, **kwargs)
            return p

        return wrapper

    return decorator
