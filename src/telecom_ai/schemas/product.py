from pydantic import BaseModel, Field

from telecom_ai.schemas.common import RequestedBandwidth, ServiceType


class Product(BaseModel):
    service_type: ServiceType
    bandwidth: RequestedBandwidth
    contract_term_months: int = Field(default=12, ge=1, le=60)
    static_ip: bool = False
