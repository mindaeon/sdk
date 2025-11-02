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


class SparkPodSpec(BaseModel):
    """Defines common things that can be customized for a Spark driver or executor pod."""

    cores: Optional[int] = None
    core_limit: Optional[str] = Field(alias="coreLimit", default=None)
    memory: Optional[str] = None
    memory_overhead: Optional[str] = Field(alias="memoryOverhead", default=None)
    image: Optional[str] = None
    service_account: Optional[str] = Field(alias="serviceAccount", default=None)


class DriverSpec(SparkPodSpec):
    """Specification of the driver."""

    pod_name: Optional[str] = Field(alias="podName", default=None)


class ExecutorSpec(SparkPodSpec):
    """Specification of the executor."""

    instances: Optional[int] = None


class SparkApplicationSpec(BaseModel):
    """Defines the desired state of SparkApplication."""

    type: str
    spark_version: str = Field(alias="sparkVersion")
    mode: str
    main_class: Optional[str] = Field(alias="mainClass", default=None)
    main_application_file: str = Field(alias="mainApplicationFile")
    driver: DriverSpec
    executor: ExecutorSpec
    spark_conf: Optional[Dict[str, str]] = Field(alias="sparkConf", default=None)


class SparkApplication(K8sResource):
    """Represents a SparkApplication.

    For more details, see the Spark Operator documentation:
    https://github.com/kubeflow/spark-operator/blob/master/docs/api-docs.md#sparkapplication
    """

    spec: SparkApplicationSpec

    def __init__(
        self,
        name: str,
        spec: SparkApplicationSpec,
        **kwargs,
    ):
        super().__init__(
            apiVersion="sparkoperator.k8s.io/v1beta2",
            kind="SparkApplication",
            metadata={"name": name},
            spec=spec,
            **kwargs,
        )
