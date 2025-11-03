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

import pytest

from kubeflow.core.k8s_resource import K8sResource

# A sample Kubernetes resource dictionary for testing
SAMPLE_RESOURCE = {
    "apiVersion": "v1",
    "kind": "Pod",
    "metadata": {
        "name": "test-pod",
        "namespace": "default",
        "uid": "1234-5678",
        "creationTimestamp": "2024-01-01T00:00:00Z",
        "labels": {"app": "test"},
        "annotations": {"owner": "jules"},
    },
    "spec": {"containers": [{"name": "test-container", "image": "test-image"}]},
    "status": {"phase": "Running"},
}


def test_k8s_resource_creation():
    """Tests successful creation of a K8sResource."""
    resource = K8sResource(**SAMPLE_RESOURCE)
    assert resource.api_version == "v1"
    assert resource.kind == "Pod"
    assert resource.metadata["name"] == "test-pod"
    assert resource.spec["containers"][0]["name"] == "test-container"
    assert resource.status["phase"] == "Running"
    assert resource.raw == SAMPLE_RESOURCE


def test_k8s_resource_properties():
    """Tests the convenient property accessors."""
    resource = K8sResource(**SAMPLE_RESOURCE)
    assert resource.name == "test-pod"
    assert resource.namespace == "default"
    assert resource.uid == "1234-5678"
    assert resource.creation_timestamp == "2024-01-01T00:00:00Z"
    assert resource.labels == {"app": "test"}
    assert resource.annotations == {"owner": "jules"}


def test_k8s_resource_missing_optional_fields():
    """Tests that missing optional fields are handled gracefully."""
    resource_dict = {
        "apiVersion": "v1",
        "kind": "ConfigMap",
        "metadata": {"name": "test-cm"},
    }
    resource = K8sResource(**resource_dict)
    assert resource.name == "test-cm"
    assert resource.namespace is None
    assert resource.uid is None
    assert resource.creation_timestamp is None
    assert resource.labels == {}
    assert resource.annotations == {}
    assert resource.spec is None
    assert resource.status is None


def test_k8s_resource_missing_metadata_name():
    """Tests that a missing name in metadata returns an empty string."""
    resource_dict = {"apiVersion": "v1", "kind": "Secret", "metadata": {}}
    resource = K8sResource(**resource_dict)
    assert resource.name == ""


def test_k8s_resource_validation_error():
    """Tests that a validation error is raised for missing required fields."""
    with pytest.raises(ValueError):
        K8sResource(kind="Pod", metadata={})  # Missing apiVersion
