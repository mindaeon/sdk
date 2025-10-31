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

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import os
import yaml

class ClientConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="kubeflow_client_",
        env_nested_delimiter="__",
    )
    namespace: str = "default"

class KubeflowConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="kubeflow_",
        env_nested_delimiter="__",
        extra="ignore",
    )
    client: ClientConfig = Field(default_factory=ClientConfig)
    config_file: str | None = None

    def __init__(self, **values):
        config_data = {}

        # Load YAML file if provided
        config_file = os.environ.get("KUBEFLOW_CONFIG_FILE")
        if config_file and os.path.exists(config_file):
            with open(config_file, "r") as f:
                yaml_config = yaml.safe_load(f) or {}
            self._merge(config_data, yaml_config)

        # Load env vars with nested double underscore pattern
        for key, value in os.environ.items():
            if key.startswith("KUBEFLOW_"):
                self._assign_nested(config_data, key, value)

        merged = self._merge(config_data, values)
        merged["config_file"] = config_file
        super().__init__(**merged)

    @staticmethod
    def _assign_nested(base: dict, key: str, value: str):
        if not key.startswith("KUBEFLOW_"):
            return
        key = key[len("KUBEFLOW_"):]
        parts = key.lower().split("__")
        d = base
        for part in parts[:-1]:
            d = d.setdefault(part, {})
        d[parts[-1]] = value

    @staticmethod
    def _merge(a: dict, b: dict):
        for k, v in (b or {}).items():
            if isinstance(v, dict):
                a[k] = KubeflowConfig._merge(a.get(k, {}), v)
            else:
                a[k] = v
        return a
