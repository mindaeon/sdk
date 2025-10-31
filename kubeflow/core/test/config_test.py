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
import unittest
from kubeflow.core.config import KubeflowConfig

class TestKubeflowConfig(unittest.TestCase):
    def test_from_env(self):
        os.environ["KUBEFLOW_CLIENT__NAMESPACE"] = "env-namespace"
        config = KubeflowConfig()
        self.assertEqual(config.client.namespace, "env-namespace")
        del os.environ["KUBEFLOW_CLIENT__NAMESPACE"]

    def test_from_env_legacy(self):
        os.environ["KUBEFLOW_CLIENT_NAMESPACE"] = "env-namespace"
        config = KubeflowConfig()
        self.assertEqual(config.client.namespace, "default")
        del os.environ["KUBEFLOW_CLIENT_NAMESPACE"]

    def test_default_values(self):
        config = KubeflowConfig()
        self.assertEqual(config.client.namespace, "default")

if __name__ == "__main__":
    unittest.main()
