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

import os
from typing import Literal, Optional

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
import yaml


class AuthConfig(BaseModel):
    provider: Literal["kubeconfig", "incluster"] = "kubeconfig"


class ClientConfig(BaseModel):
    namespace: str = "default"


class KubeflowConfig(BaseSettings):
    """
    Unified configuration for Kubeflow client and environment.

    Priority (highest → lowest):
      1. Constructor arguments
      2. Environment variables (e.g., KUBEFLOW_CLIENT__NAMESPACE)
      3. YAML file (path from KUBEFLOW_CONFIG_FILE env var)
      4. Defaults
    """

    auth: AuthConfig = Field(default_factory=AuthConfig)
    client: ClientConfig = Field(default_factory=ClientConfig)
    config_file: Optional[str] = None

    model_config = SettingsConfigDict(
        env_prefix="KUBEFLOW_",
        env_nested_delimiter="__",
        extra="ignore",
    )

    def __init__(self, **values):
        # Let pydantic load from ENV and constructor args first
        super().__init__(**values)

        # Get the set of fields populated by higher-priority sources
        fields_set = self.model_fields_set

        # Load YAML config if available
        config_file_path = self.config_file or os.getenv("KUBEFLOW_CONFIG_FILE")
        if config_file_path and os.path.exists(config_file_path):
            with open(config_file_path) as f:
                yaml_data = yaml.safe_load(f) or {}

            # Apply YAML values only if not already set
            if "auth" not in fields_set and "auth" in yaml_data:
                self.auth = AuthConfig(**yaml_data.get("auth", {}))
            if "client" not in fields_set and "client" in yaml_data:
                self.client = ClientConfig(**yaml_data.get("client", {}))
