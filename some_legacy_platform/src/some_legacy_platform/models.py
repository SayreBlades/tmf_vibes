"""Pydantic models for the TMF620 ProductOffering."""

from datetime import datetime

from pydantic import BaseModel, Field


class ProductOffering(BaseModel):
    """
    Represents the canonical, internally validated structure of a product
    offering in the catalog. Based on the simplified structure in the data
    files and TMF620 spec, enforcing required fields.
    """

    id: str
    href: str
    name: str
    description: str | None = None
    version: str | None = None
    isBundle: bool | None = Field(default=None, alias="isBundle")
    isSellable: bool | None = Field(default=None, alias="isSellable")
    lifecycleStatus: str | None = None
    lastUpdate: datetime = Field(..., description="Date and time of the last update")
    type: str = Field(alias="@type")
    baseType: str | None = Field(default=None, alias="@baseType")

    model_config = {
        "populate_by_name": True,  # Allows using both field name and alias
        "extra": "ignore",  # Ignore extra fields from JSON
        "json_encoders": {
            # Custom encoder for datetime to ensure ISO 8601 format with Z
            datetime: lambda dt: dt.strftime("%Y-%m-%dT%H:%M:%SZ") if dt else None
        },
    }


class ProductOfferingPartial(BaseModel):
    """
    Represents a potentially partial product offering structure, used specifically
    for API responses where field selection might occur. All fields are optional.
    """

    id: str | None = None
    href: str | None = None
    name: str | None = None
    description: str | None = None
    version: str | None = None
    isBundle: bool | None = Field(default=None, alias="isBundle")
    isSellable: bool | None = Field(default=None, alias="isSellable")
    lifecycleStatus: str | None = None
    lastUpdate: datetime | None = Field(
        default=None, description="Date and time of the last update"
    )
    type: str | None = Field(default=None, alias="@type")
    baseType: str | None = Field(default=None, alias="@baseType")

    model_config = {
        "populate_by_name": True,
        "extra": "ignore",
        "json_encoders": {
            datetime: lambda dt: dt.strftime("%Y-%m-%dT%H:%M:%SZ") if dt else None
        },
    }
