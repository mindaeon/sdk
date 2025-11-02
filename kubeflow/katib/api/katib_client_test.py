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

from unittest.mock import patch

from kubeflow.katib.api.katib_client import KatibClient


@patch("kubeflow.katib.api.experiment_client.ExperimentClient")
@patch("kubeflow.katib.api.suggestion_client.SuggestionClient")
@patch("kubeflow.katib.api.trial_client.TrialClient")
def test_katib_client(
    mock_trial_client, mock_suggestion_client, mock_experiment_client
):
    """Tests that the KatibClient initializes and provides access to its sub-clients."""
    client = KatibClient()
    assert client.experiments() == mock_experiment_client.return_value
    assert client.suggestions() == mock_suggestion_client.return_value
    assert client.trials() == mock_trial_client.return_value
