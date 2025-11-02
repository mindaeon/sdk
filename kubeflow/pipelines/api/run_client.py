# Copyright 2025 The Kubeflow Authors.
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

import time
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any

from kubeflow.core.base_client import BaseClient
from kubeflow.core.config import KubeflowConfig
from kubeflow.pipelines.types.run_types import Run, RunState, PipelineVersionReference


class RunClient(BaseClient):
    """A client for interacting with Kubeflow Pipeline Runs."""

    def __init__(self, config: Optional[KubeflowConfig] = None):
        """Initializes the RunClient."""
        super().__init__(config)
        self.api_version = "v2beta1"

    def create_run(
        self,
        run_name: str,
        pipeline_version_reference: PipelineVersionReference,
        runtime_config: Optional[Dict[str, Any]] = None,
        experiment_id: Optional[str] = None,
    ) -> Run:
        """Creates a pipeline run."""
        body = {
            "display_name": run_name,
            "pipeline_version_reference": pipeline_version_reference.model_dump(),
            "runtime_config": runtime_config or {},
        }
        params = {}
        if experiment_id:
            params["experiment_id"] = experiment_id
        response = self.api_client.call_api(
            f"/apis/{self.api_version}/runs", "POST", body=body, query_params=params
        )
        return Run(**response)

    def get_run(self, run_id: str) -> Run:
        """Gets a pipeline run."""
        response = self.api_client.call_api(
            f"/apis/{self.api_version}/runs/{run_id}", "GET"
        )
        return Run(**response)

    def list_runs(self) -> list[Run]:
        """Lists pipeline runs."""
        response = self.api_client.call_api(f"/apis/{self.api_version}/runs", "GET")
        return [Run(**run) for run in response.get("runs", [])]

    def delete_run(self, run_id: str):
        """Deletes a pipeline run."""
        return self.api_client.call_api(
            f"/apis/{self.api_version}/runs/{run_id}", "DELETE"
        )

    def archive_run(self, run_id: str):
        """Archives a pipeline run."""
        return self.api_client.call_api(
            f"/apis/{self.api_version}/runs/{run_id}:archive", "POST"
        )

    def unarchive_run(self, run_id: str):
        """Unarchives a pipeline run."""
        return self.api_client.call_api(
            f"/apis/{self.api_version}/runs/{run_id}:unarchive", "POST"
        )

    def retry_run(self, run_id: str):
        """Retries a pipeline run."""
        return self.api_client.call_api(
            f"/apis/{self.api_version}/runs/{run_id}:retry", "POST"
        )

    def terminate_run(self, run_id: str):
        """Terminates a pipeline run."""
        return self.api_client.call_api(
            f"/apis/{self.api_version}/runs/{run_id}:terminate", "POST"
        )

    def wait_for_run_completion(self, run_id: str, timeout: int = 600) -> Run:
        """Waits for a pipeline run to complete."""
        end_time = datetime.now(timezone.utc) + timedelta(seconds=timeout)
        while datetime.now(timezone.utc) < end_time:
            run = self.get_run(run_id)
            if run.state in [
                RunState.SUCCEEDED,
                RunState.FAILED,
                RunState.SKIPPED,
                RunState.CANCELED,
            ]:
                return run
            time.sleep(10)
        raise TimeoutError(f"Run {run_id} did not complete in {timeout} seconds.")
