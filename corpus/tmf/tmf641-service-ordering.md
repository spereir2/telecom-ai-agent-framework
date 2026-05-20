# TMF641 Service Ordering Management API — Excerpts

> **Source:** [tmforum-apis/TMF641_ServiceOrder](https://github.com/tmforum-apis/TMF641_ServiceOrder)
> **File:** `TMF641-ServiceOrdering-v4.1.0.swagger.json`
> **Commit:** 4dd2866c (2026-04-28)
> **License:** Apache License 2.0 — Copyright © TM Forum 2020. All Rights Reserved.
> **Attribution:** Field descriptions and API overview are reproduced from the TMF641 OpenAPI specification
> published by TM Forum under the Apache-2.0 licence at https://github.com/tmforum-apis/TMF641_ServiceOrder

---

## Overview

**API:** TMF 641 — Service Ordering Management
**Version:** 4.1.0

The Service Order API provides a standardised mechanism for managing Service Orders — a type of order
that can be used to place an order between an internal Customer Order Management system and a Service
Order Management system, or between a service provider and a partner and vice versa.

A service order describes a list of **service order items**. Each order item references an action on an
existing or future service. Services covered include Customer Facing Services (CFS) as well as Resource
Facing Services (RFS).

From a component perspective, a service order should be available:
- from a **Service Orchestration Component** (may mix CFS and RFS)
- from an **Infrastructure Control & Management component** (RFS only)

---

## Operations

| Method | Path | Description |
|--------|------|-------------|
| GET | `/serviceOrder` | List or find ServiceOrder objects |
| POST | `/serviceOrder` | Creates a ServiceOrder |
| GET | `/serviceOrder/{id}` | Retrieves a ServiceOrder by ID |
| PATCH | `/serviceOrder/{id}` | Partially updates a ServiceOrder |
| DELETE | `/serviceOrder/{id}` | Deletes a ServiceOrder |
| GET | `/cancelServiceOrder` | List or find CancelServiceOrder objects |
| POST | `/cancelServiceOrder` | Creates a CancelServiceOrder |
| GET | `/cancelServiceOrder/{id}` | Retrieves a CancelServiceOrder by ID |
| POST | `/hub` | Register a listener for event notifications |
| DELETE | `/hub/{id}` | Unregister a listener |

---

## Resource: ServiceOrder

A `ServiceOrder` is the root entity that orchestrates one or more service order items.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | server-assigned | ID created on repository side |
| `href` | string | server-assigned | Hyperlink to access the order |
| `externalId` | string | no | ID given by the consumer to facilitate searches |
| `description` | string | no | Free-text description of the service order |
| `category` | string | no | Used to categorise the order (e.g. `Broadband`, `TVOption`) |
| `priority` | string | no | Priority hint for the OM system |
| `orderDate` | string (date-time) | server-assigned | Date the order was created |
| `requestedStartDate` | string (date-time) | no | Order start date requested by the consumer |
| `requestedCompletionDate` | string (date-time) | no | Requested delivery date from the consumer's perspective |
| `expectedCompletionDate` | string (date-time) | server-set | Expected delivery date set by the provider |
| `completionDate` | string (date-time) | server-set | Effective delivery date set by the provider |
| `startDate` | string (date-time) | server-set | Date when order processing began |
| `cancellationDate` | string (date-time) | no | Date the order was cancelled |
| `cancellationReason` | string | no | Reason for cancellation |
| `notificationContact` | string | no | Contact to which order status information is sent |
| `state` | ServiceOrderStateType | server-set | Current lifecycle state of the order |
| `serviceOrderItem` | ServiceOrderItem[] | **required** | List of service order items (≥ 1) |
| `relatedParty` | RelatedParty[] | no | Parties involved in this order and their roles |
| `note` | Note[] | no | Free-text annotations on the order |
| `orderRelationship` | OrderRelationship[] | no | Links to prerequisite or dependent orders |
| `externalReference` | ExternalReference[] | no | References to external order management systems |
| `@type` | string | no | Subclass name when extending this resource |
| `@baseType` | string | no | Superclass name when sub-classing |
| `@schemaLocation` | string | no | URI to a JSON-Schema for additional attributes |

### ServiceOrderStateType (enum)

Valid lifecycle states for a `ServiceOrder`:

| Value | Meaning |
|-------|---------|
| `acknowledged` | Order received and validated; no processing begun |
| `rejected` | Order failed pre-processing validation |
| `pending` | Order awaiting external action before it can proceed |
| `held` | Order is on hold (e.g. waiting for a technician) |
| `inProgress` | Order is actively being processed |
| `assessingCancellation` | Cancellation request received; evaluating feasibility |
| `pendingCancellation` | Cancellation approved; awaiting execution |
| `cancelled` | Order has been cancelled |
| `completed` | All order items fulfilled successfully |
| `failed` | One or more order items failed; order aborted |
| `partial` | Some items completed; others failed |

---

## Resource: ServiceOrderItem

Each item within a `ServiceOrder` describes one service action.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | **required** | Identifier of this line item (unique within the order) |
| `quantity` | integer | no | Quantity ordered (default 1) |
| `action` | OrderItemActionType | **required** | The action to perform on the service |
| `service` | ServiceRefOrValue | **required** | The service to be acted on |
| `state` | ServiceOrderItemStateType | server-set | Lifecycle state of this item |
| `appointment` | AppointmentRef | no | Appointment set up for this item (e.g. site visit) |
| `serviceOrderItemRelationship` | ServiceOrderItemRelationship[] | no | Relationships to other items in this order |
| `errorMessage` | Error[] | no | Errors that caused a state change |
| `@type` | string | no | Subclass name |

### OrderItemActionType (enum)

| Value | Meaning |
|-------|---------|
| `add` | Create a new service instance |
| `modify` | Change characteristics of an existing service |
| `delete` | Terminate/remove a service |
| `noChange` | Reference an existing service without modification (e.g. for bundling) |

### ServiceOrderItemStateType (enum)

`acknowledged` · `rejected` · `pending` · `held` · `inProgress` · `assessingCancellation` · `pendingCancellation` · `cancelled` · `completed` · `failed` · `partial`

---

## Resource: Service (within ServiceOrderItem)

The `service` field in a `ServiceOrderItem` is a `ServiceRefOrValue`. When creating a new service
(`action: add`), provide a full `Service` object. When referencing an existing service, a `ServiceRef`
(id + href) is sufficient.

### Service fields relevant to FTTH provisioning

| Field | Type | Required for `add` | Description |
|-------|------|---------------------|-------------|
| `id` | string | no (server assigns) | Unique identifier of the service |
| `href` | string | no | Self-reference URI |
| `name` | string | **recommended** | Human-readable service name |
| `serviceType` | string | **recommended** | Business type (e.g. `FTTH`, `FTTC`, `LL`) |
| `category` | string | no | `CFS` (Customer Facing) or `RFS` (Resource Facing) |
| `description` | string | no | Free-text description |
| `isBundle` | boolean | no | True if this is a ServiceBundle grouping multiple services |
| `isServiceEnabled` | boolean | no | False = provisioned but not yet active |
| `hasStarted` | boolean | no | True once activation has begun |
| `startDate` | string (date-time) | no | Requested or actual service start date |
| `endDate` | string (date-time) | no | Service end date |
| `state` | ServiceStateType | server-set | Service lifecycle state |
| `serviceCharacteristic` | ServiceCharacteristic[] | context-dependent | Technical and commercial attributes |
| `place` | Place[] | **required for FTTH** | Installation address(es) |
| `relatedParty` | RelatedParty[] | **required** | Customer, technician, account manager |
| `serviceSpecification` | ServiceSpecificationRef | recommended | Reference to the service catalogue spec |
| `supportingService` | Service[] | no | Child services (e.g. ONU activation as RFS) |
| `supportingResource` | Resource[] | no | Physical resources (port, OLT, ONT) |
| `@type` | string | no | Subclass discriminator |

### ServiceStateType (enum)

| Value | Meaning |
|-------|---------|
| `feasibilityChecked` | Address/coverage check completed |
| `designed` | Service designed in the OSS/inventory |
| `reserved` | Resources reserved pending installation |
| `inactive` | Provisioned but not yet activated |
| `active` | Service is live and in service |
| `terminated` | Service has ended |

---

## Resource: ServiceCharacteristic

A `ServiceCharacteristic` carries a typed name/value pair that describes a technical or commercial
attribute of a service.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Identifier of the characteristic instance |
| `name` | string | **Required.** Name of the characteristic (e.g. `downloadSpeed`, `vlanId`) |
| `value` | Any | The characteristic's value — type depends on `valueType` |
| `valueType` | string | Data type of `value` (e.g. `string`, `integer`, `object`) |
| `characteristicRelationship` | CharacteristicRelationship[] | Links to related characteristics |
| `@type` | string | Subclass name |

### Common FTTH ServiceCharacteristic names

| `name` | `valueType` | Example value | Notes |
|--------|-------------|---------------|-------|
| `downloadSpeed` | string | `"1000Mbps"` | CFS-level commercial speed |
| `uploadSpeed` | string | `"220Mbps"` | CFS-level commercial speed |
| `technologyType` | string | `"GPON"` | Fibre technology (GPON, XGS-PON, AON) |
| `vlanId` | integer | `100` | RFS-level L2 VLAN assignment |
| `svlanId` | integer | `200` | S-VLAN (QinQ stacking) |
| `ontSerialNumber` | string | `"ALCL12345678"` | Physical ONT serial for auto-discovery |
| `oltPortId` | string | `"OLT-01/0/1/3"` | OLT PON port identifier |
| `ipAddressType` | string | `"dynamic"` | `dynamic` or `static` |
| `staticIpAddress` | string | `"203.0.113.10"` | Only when `ipAddressType=static` |
| `subnetMask` | string | `"255.255.255.248"` | Only for static IP |
| `defaultGateway` | string | `"203.0.113.9"` | Only for static IP |
| `pppoeUsername` | string | `"user@isp.example"` | PPPoE credentials |
| `serviceProfile` | string | `"FTTH_RESIDENTIAL_1G"` | Provisioning profile ID in the OLT |
| `contractTermMonths` | integer | `24` | Contract duration |

---

## Resource: RelatedParty

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Party identifier in the BSS/CRM |
| `href` | string | Hyperlink to party resource |
| `name` | string | Display name |
| `role` | string | Role in this order context (see below) |
| `@referredType` | string | Actual type (e.g. `Individual`, `Organization`) |

Common roles: `Customer`, `Requester`, `Installer`, `TechnicianSupervisor`, `AccountManager`

---

## Resource: Note

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Identifier within the containing entity |
| `author` | string | Author of the note |
| `date` | string (date-time) | Timestamp |
| `text` | string | Free-text content |

---

## Cancel Service Order

A `CancelServiceOrder` is created by POSTing to `/cancelServiceOrder` with:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `serviceOrder` | ServiceOrderRef | **required** | Reference to the order to cancel |
| `cancellationReason` | string | **required** | Reason for the cancellation request |
| `requestedCancellationDate` | string (date-time) | no | Desired cancellation effective date |

The resource transitions through `assessingCancellation` → `pendingCancellation` → `cancelled` (or
back to `inProgress` if cancellation is rejected).

---

## Example: FTTH Residential ServiceOrder (POST body)

```json
{
  "@type": "ServiceOrder",
  "externalId": "CRM-ORD-20240501-001",
  "category": "Broadband",
  "description": "New FTTH residential 1Gbps service for 12 Baker Street",
  "priority": "2",
  "requestedCompletionDate": "2024-05-15T00:00:00Z",
  "relatedParty": [
    {
      "id": "CUST-99001",
      "name": "Jane Doe",
      "role": "Customer",
      "@referredType": "Individual"
    }
  ],
  "serviceOrderItem": [
    {
      "id": "1",
      "action": "add",
      "service": {
        "@type": "Service",
        "name": "FTTH-1G-Residential",
        "serviceType": "FTTH",
        "category": "CFS",
        "serviceCharacteristic": [
          { "name": "downloadSpeed", "value": "1000Mbps", "valueType": "string" },
          { "name": "uploadSpeed",   "value": "220Mbps",  "valueType": "string" },
          { "name": "technologyType","value": "GPON",     "valueType": "string" },
          { "name": "serviceProfile","value": "FTTH_RESIDENTIAL_1G", "valueType": "string" },
          { "name": "contractTermMonths", "value": 24, "valueType": "integer" }
        ],
        "place": [
          {
            "@type": "GeographicAddress",
            "name": "Installation address",
            "streetNr": "12",
            "streetName": "Baker Street",
            "city": "London",
            "postcode": "W1U 6TS",
            "country": "GB"
          }
        ]
      }
    }
  ]
}
```

---

*Excerpted from the TMF641 OpenAPI specification. Copyright © TM Forum 2020. Licensed under Apache-2.0.*
*Source: https://github.com/tmforum-apis/TMF641_ServiceOrder — commit 4dd2866c*
