from datetime import UTC, datetime
from enum import StrEnum
from uuid import uuid4

from pydantic import BaseModel, Field

from telecom_ai.schemas.common import ServiceAddress
from telecom_ai.schemas.customer import Customer
from telecom_ai.schemas.product import Product


class OrderState(StrEnum):
    DRAFT = "draft"
    ACKNOWLEDGED = "acknowledged"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REJECTED = "rejected"


class ServiceOrder(BaseModel):
    """Subset of TMF641 ServiceOrder, scoped to provisioning intake."""

    order_id: str = Field(default_factory=lambda: f"ord_{uuid4().hex[:12]}")
    state: OrderState = OrderState.DRAFT
    customer: Customer
    service_address: ServiceAddress
    product: Product
    requested_completion_date: datetime | None = None
    notes: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
