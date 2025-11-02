# Copyright 2025 The Kubeflow Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from kubeflow.core.k8s_resource import K8sResource


class ModelFormat(BaseModel):
    """Specifies the model format."""
    name: str
    version: Optional[str] = None


class ModelSpec(BaseModel):
    """Defines the model spec."""
    model_format: ModelFormat = Field(alias="modelFormat")
    storage_uri: str = Field(alias="storageUri")
    runtime: Optional[str] = None
    protocol_version: Optional[str] = Field(alias="protocolVersion", default=None)


class PredictorSpec(BaseModel):
    """Defines the model predictor spec."""
    model: ModelSpec


class InferenceServiceSpec(BaseModel):
    """Defines the desired state of InferenceService."""
    predictor: PredictorSpec


class InferenceService(K8sResource):
    """Represents a KServe InferenceService.

    For more details, see the KServe documentation:
    https://kserve.github.io/website/docs/reference/crd-api/#inferenceservice
    """
    spec: InferenceServiceSpec

    def __init__(
        self,
        name: str,
        predictor: PredictorSpec,
        **kwargs,
    ):
        super().__init__(
            apiVersion="serving.kserve.io/v1beta1",
            kind="InferenceService",
            metadata={"name": name},
            spec=InferenceServiceSpec(predictor=predictor),
            **kwargs,
        )
