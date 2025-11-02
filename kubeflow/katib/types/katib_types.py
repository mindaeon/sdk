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

from typing import Any, Optional

from pydantic import BaseModel

from kubeflow.core.k8s_resource import K8sResource


class ExperimentSpec(BaseModel):
    """The specification of a Katib Experiment."""

    pass


class ExperimentStatus(BaseModel):
    """The status of a Katib Experiment."""

    pass


class Experiment(K8sResource):
    """A Katib Experiment."""

    spec: Optional[ExperimentSpec] = None
    status: Optional[ExperimentStatus] = None


class SuggestionSpec(BaseModel):
    """The specification of a Katib Suggestion."""

    pass


class SuggestionStatus(BaseModel):
    """The status of a Katib Suggestion."""

    pass


class Suggestion(K8sResource):
    """A Katib Suggestion."""

    spec: Optional[SuggestionSpec] = None
    status: Optional[SuggestionStatus] = None


class TrialSpec(BaseModel):
    """The specification of a Katib Trial."""

    pass


class TrialStatus(BaseModel):
    """The status of a Katib Trial."""

    pass


class Trial(K8sResource):
    """A Katib Trial."""

    spec: Optional[TrialSpec] = None
    status: Optional[TrialStatus] = None
