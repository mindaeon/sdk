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

from functools import wraps
import inspect
from typing import Callable

from kubeflow.pipelines.types.component_spec import ComponentSpec, InputSpec, OutputSpec


def component(func: Callable):
    """Decorator for pipeline components."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    sig = inspect.signature(func)
    inputs = []
    for param in sig.parameters.values():
        inputs.append(InputSpec(name=param.name, type=str(param.annotation)))

    outputs = []
    if sig.return_annotation is not inspect.Signature.empty:
        outputs.append(OutputSpec(name="output", type=str(sig.return_annotation)))

    wrapper.component_spec = ComponentSpec(
        name=func.__name__,
        description=func.__doc__,
        inputs=inputs,
        outputs=outputs,
    )

    return wrapper
