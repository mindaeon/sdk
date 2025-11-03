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

from dataclasses import dataclass, field
import os
import tempfile
from typing import Optional
from unittest.mock import patch

import pytest
import yaml

from kubeflow.core.config import KubeflowConfig

# Common status constants
SUCCESS = "success"
FAILED = "failed"


@dataclass
class TestCase:
    name: str
    env_vars: dict = field(default_factory=dict)
    config_data: Optional[dict] = None
    constructor_args: dict = field(default_factory=dict)
    expected_namespace: str = "default"
    expected_auth_provider: str = "kubeconfig"
    expected_status: str = SUCCESS
    expected_error: Optional[type[Exception]] = None
    # Prevent pytest from collecting this dataclass as a test
    __test__ = False


@pytest.mark.parametrize(
    "test_case",
    [
        TestCase(
            name="defaults only",
            expected_namespace="default",
            expected_auth_provider="kubeconfig",
        ),
        TestCase(
            name="yaml config",
            config_data={
                "client": {"namespace": "yaml-ns"},
                "auth": {"provider": "incluster"},
            },
            expected_namespace="yaml-ns",
            expected_auth_provider="incluster",
        ),
        TestCase(
            name="env var config",
            env_vars={
                "KUBEFLOW_CLIENT__NAMESPACE": "env-ns",
                "KUBEFLOW_AUTH__PROVIDER": "incluster",
            },
            expected_namespace="env-ns",
            expected_auth_provider="incluster",
        ),
        TestCase(
            name="env overrides yaml",
            env_vars={
                "KUBEFLOW_CLIENT__NAMESPACE": "env-ns",
                "KUBEFLOW_AUTH__PROVIDER": "kubeconfig",
            },
            config_data={
                "client": {"namespace": "yaml-ns"},
                "auth": {"provider": "incluster"},
            },
            expected_namespace="env-ns",
            expected_auth_provider="kubeconfig",
        ),
        TestCase(
            name="constructor overrides env and yaml",
            constructor_args={
                "client": {"namespace": "constructor-ns"},
                "auth": {"provider": "incluster"},
            },
            env_vars={
                "KUBEFLOW_CLIENT__NAMESPACE": "env-ns",
                "KUBEFLOW_AUTH__PROVIDER": "kubeconfig",
            },
            config_data={"client": {"namespace": "yaml-ns"}},
            expected_namespace="constructor-ns",
            expected_auth_provider="incluster",
        ),
    ],
)
def test_kubeflow_config_loading(test_case: TestCase):
    """Tests the loading precedence of KubeflowConfig."""
    print(f"Executing test: {test_case.name}")
    try:
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".yaml") as f:
            if test_case.config_data is not None:
                yaml.dump(test_case.config_data, f)
            temp_config_path = f.name

        env = test_case.env_vars.copy()
        if test_case.config_data is not None:
            env["KUBEFLOW_CONFIG_FILE"] = temp_config_path

        with patch.dict(os.environ, env, clear=True):
            config = KubeflowConfig(**test_case.constructor_args)

            assert test_case.expected_status == SUCCESS
            assert config.client.namespace == test_case.expected_namespace
            assert config.auth.provider == test_case.expected_auth_provider

    except Exception as e:
        assert test_case.expected_status == FAILED
        assert isinstance(e, test_case.expected_error)
    finally:
        if "temp_config_path" in locals() and os.path.exists(temp_config_path):
            os.remove(temp_config_path)

    print("Test execution complete")
