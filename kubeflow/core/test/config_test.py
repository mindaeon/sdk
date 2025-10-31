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
# limitations under a uthor.

import os
import unittest
from kubeflow.core.config import KubeflowConfig
import yaml

class TestKubeflowConfig(unittest.TestCase):
    def test_from_yaml(self):
        with open("test_config.yaml", "w") as f:
            yaml.safe_dump({"client": {"namespace": "yaml-namespace"}}, f)

        os.environ["KUBEFLOW_CONFIG_FILE"] = "test_config.yaml"
        config = KubeflowConfig()
        self.assertEqual(config.client.namespace, "yaml-namespace")

        del os.environ["KUBEFLOW_CONFIG_FILE"]
        os.remove("test_config.yaml")

    def test_env_overrides_yaml(self):
        with open("test_config.yaml", "w") as f:
            yaml.safe_dump({"client": {"namespace": "yaml-namespace"}}, f)

        os.environ["KUBEFLOW_CONFIG_FILE"] = "test_config.yaml"
        os.environ["KUBEFLOW_CLIENT__NAMESPACE"] = "env-namespace"
        config = KubeflowConfig()
        self.assertEqual(config.client.namespace, "env-namespace")

        del os.environ["KUBEFLOW_CONFIG_FILE"]
        del os.environ["KUBEFLOW_CLIENT__NAMESPACE"]
        os.remove("test_config.yaml")

    def test_default_values(self):
        config = KubeflowConfig()
        self.assertEqual(config.client.namespace, "default")

if __name__ == "__main__":
    unittest.main()
