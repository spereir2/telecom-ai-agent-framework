from enum import Enum

from pydantic import BaseModel, Field, field_validator


class ServiceType(str, Enum):
    FTTH_RESIDENTIAL = "ftth_residential"
    FTTH_BUSINESS = "ftth_business"
    FTTC = "fttc"
    LEASED_LINE = "leased_line"


class BandwidthUnit(str, Enum):
    MBPS = "Mbps"
    GBPS = "Gbps"


class RequestedBandwidth(BaseModel):
    downstream: float = Field(gt=0)
    upstream: float | None = Field(default=None, gt=0)
    unit: BandwidthUnit = BandwidthUnit.MBPS


class ServiceAddress(BaseModel):
    line1: str = Field(min_length=1)
    line2: str | None = None
    city: str = Field(min_length=1)
    postcode: str = Field(min_length=3, max_length=12)
    country_code: str = Field(min_length=2, max_length=2, description="ISO-3166-1 alpha-2")

    @field_validator("country_code")
    @classmethod
    def upper_country(cls, v: str) -> str:
        return v.upper()
