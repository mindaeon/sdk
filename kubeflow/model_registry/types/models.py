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

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class BaseResource(BaseModel):
    """Base class for all Model Registry resources."""

    id: str
    create_time_since_epoch: str = Field(alias="createTimeSinceEpoch")
    last_update_time_since_epoch: str = Field(alias="lastUpdateTimeSinceEpoch")
    description: Optional[str] = None
    external_id: Optional[str] = Field(alias="externalId", default=None)
    name: Optional[str] = None
    custom_properties: Optional[Dict[str, "MetadataValue"]] = Field(
        alias="customProperties", default=None
    )


class RegisteredModelCreate(BaseModel):
    """A registered model to be created."""

    name: str
    owner: Optional[str] = None
    state: Optional[str] = None
    description: Optional[str] = None
    external_id: Optional[str] = Field(alias="externalId", default=None)
    custom_properties: Optional[Dict[str, "MetadataValue"]] = Field(
        alias="customProperties", default=None
    )


class RegisteredModel(RegisteredModelCreate, BaseResource):
    """A registered model in model registry."""


class ModelVersionCreate(BaseModel):
    """A model version to be created."""

    name: str
    registered_model_id: str = Field(alias="registeredModelId")
    author: Optional[str] = None
    state: Optional[str] = None
    description: Optional[str] = None
    external_id: Optional[str] = Field(alias="externalId", default=None)
    custom_properties: Optional[Dict[str, "MetadataValue"]] = Field(
        alias="customProperties", default=None
    )


class ModelVersion(ModelVersionCreate, BaseResource):
    """Represents a ModelVersion belonging to a RegisteredModel."""


class ModelArtifactCreate(BaseModel):
    """A model artifact to be created."""

    name: str
    model_format_name: Optional[str] = Field(alias="modelFormatName", default=None)
    storage_key: Optional[str] = Field(alias="storageKey", default=None)
    storage_path: Optional[str] = Field(alias="storagePath", default=None)
    model_format_version: Optional[str] = Field(
        alias="modelFormatVersion", default=None
    )
    service_account_name: Optional[str] = Field(
        alias="serviceAccountName", default=None
    )
    uri: Optional[str] = None
    state: Optional[str] = None
    description: Optional[str] = None
    external_id: Optional[str] = Field(alias="externalId", default=None)
    custom_properties: Optional[Dict[str, "MetadataValue"]] = Field(
        alias="customProperties", default=None
    )


class ModelArtifact(ModelArtifactCreate, BaseResource):
    """An ML model artifact."""


class MetadataValue(BaseModel):
    """A value in properties."""

    int_value: Optional[str] = Field(alias="intValue", default=None)
    double_value: Optional[float] = Field(alias="doubleValue", default=None)
    string_value: Optional[str] = Field(alias="stringValue", default=None)
    struct_value: Optional[str] = Field(alias="structValue", default=None)
    proto_value: Optional[str] = Field(alias="protoValue", default=None)
    bool_value: Optional[bool] = Field(alias="boolValue", default=None)
