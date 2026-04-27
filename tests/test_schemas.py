import pytest
from pydantic import ValidationError

from telecom_ai.schemas import (
    Customer,
    CustomerType,
    OrderState,
    Product,
    RequestedBandwidth,
    ServiceAddress,
    ServiceOrder,
    ServiceType,
)


def _valid_order_kwargs() -> dict:
    return {
        "customer": Customer(full_name="Jane Doe"),
        "service_address": ServiceAddress(
            line1="12 Baker Street", city="London", postcode="W1U 6TS", country_code="gb"
        ),
        "product": Product(
            service_type=ServiceType.FTTH_RESIDENTIAL,
            bandwidth=RequestedBandwidth(downstream=100),
        ),
    }


def test_service_order_minimal_valid() -> None:
    order = ServiceOrder(**_valid_order_kwargs())
    assert order.state is OrderState.DRAFT
    assert order.order_id.startswith("ord_")
    assert order.service_address.country_code == "GB"
    assert order.customer.customer_type is CustomerType.RESIDENTIAL


def test_country_code_uppercased() -> None:
    addr = ServiceAddress(line1="x", city="y", postcode="ABC", country_code="gb")
    assert addr.country_code == "GB"


def test_bandwidth_must_be_positive() -> None:
    with pytest.raises(ValidationError):
        RequestedBandwidth(downstream=0)


def test_postcode_min_length() -> None:
    with pytest.raises(ValidationError):
        ServiceAddress(line1="x", city="y", postcode="ab", country_code="GB")


def test_contract_term_bounds() -> None:
    with pytest.raises(ValidationError):
        Product(
            service_type=ServiceType.FTTH_BUSINESS,
            bandwidth=RequestedBandwidth(downstream=100),
            contract_term_months=120,
        )


def test_round_trip_json() -> None:
    order = ServiceOrder(**_valid_order_kwargs())
    payload = order.model_dump_json()
    restored = ServiceOrder.model_validate_json(payload)
    assert restored.product.bandwidth.downstream == 100
