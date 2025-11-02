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

from unittest.mock import patch

from kubernetes.client import Configuration

from kubeflow.spark_operator.clients import SparkClient
from kubeflow.spark_operator.types import (
    DriverSpec,
    ExecutorSpec,
    SparkApplication,
    SparkApplicationSpec,
)

# Create a fake config for the client to use
fake_conf = Configuration()
fake_conf.host = "http://localhost:8080"


def test_spark_client_create():
    """Tests the create method of the SparkClient."""
    spark_application = SparkApplication(
        name="my-spark-app",
        spec=SparkApplicationSpec(
            type="Scala",
            sparkVersion="3.1.1",
            mode="cluster",
            mainApplicationFile="local:///opt/spark/examples/jars/spark-examples_2.12-3.1.1.jar",
            driver=DriverSpec(cores=1, memory="512m"),
            executor=ExecutorSpec(instances=1, cores=1, memory="512m"),
        ),
    )

    with patch(
        "kubeflow.core.base_client.KubeconfigAuthProvider"
    ) as mock_auth_provider, patch(
        "kubeflow.core.base_client.BaseClient.create_custom_resource"
    ) as mock_create:
        mock_auth_provider.return_value.get_api_client_configuration.return_value = (
            fake_conf
        )
        client = SparkClient()
        client.create(spark_application)
        mock_create.assert_called_with(
            group="sparkoperator.k8s.io",
            version="v1beta2",
            plural="sparkapplications",
            body=spark_application.model_dump(by_alias=True, exclude_none=True),
            namespace="default",
        )
