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

from kubeflow.core.config import KubeflowConfig


class KatibClient:
    """A client for interacting with the Kubeflow Katib API."""

    def __init__(self, config: KubeflowConfig = None):
        """Initializes a KatibClient.

        Args:
            config: The KubeflowConfig object to use for authentication.
        """
        self._config = config
        self._experiment_client = None
        self._suggestion_client = None
        self._trial_client = None

    def experiments(self):
        """Returns an ExperimentClient for managing Katib experiments."""
        if self._experiment_client is None:
            from kubeflow.katib.api.experiment_client import ExperimentClient

            self._experiment_client = ExperimentClient(config=self._config)
        return self._experiment_client

    def suggestions(self):
        """Returns a SuggestionClient for managing Katib suggestions."""
        if self._suggestion_client is None:
            from kubeflow.katib.api.suggestion_client import SuggestionClient

            self._suggestion_client = SuggestionClient(config=self._config)
        return self._suggestion_client

    def trials(self):
        """Returns a TrialClient for managing Katib trials."""
        if self._trial_client is None:
            from kubeflow.katib.api.trial_client import TrialClient

            self._trial_client = TrialClient(config=self._config)
        return self._trial_client
