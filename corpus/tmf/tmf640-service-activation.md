# TMF640 Service Activation and Configuration API — Excerpts

> **Source:** [tmforum-apis/TMF640_ActivationConfiguration](https://github.com/tmforum-apis/TMF640_ActivationConfiguration)
> **File:** `TMF640-ServiceActivation-v4.0.0.swagger.json`
> **Commit:** 34ffd1ae (2026-04-28)
> **License:** Apache License 2.0 — Copyright © TM Forum 2019. All Rights Reserved.
> **Attribution:** Field descriptions and API overview are reproduced from the TMF640 OpenAPI specification
> published by TM Forum under the Apache-2.0 licence at https://github.com/tmforum-apis/TMF640_ActivationConfiguration

---

## Overview

**API:** TMF 640 — Service Activation and Configuration
**Version:** 4.0.0

The Service Activation and Configuration API provides the ability to **activate and configure** a
Service resource in the OSS inventory. It is typically invoked downstream of TMF641 (Service Ordering)
once a service order item reaches `inProgress` state and the orchestrator needs to drive actual
provisioning.

The API features the **Monitor pattern**: asynchronous POST/PATCH operations return a `Monitor` resource
so the caller can track activation progress without polling the service resource directly.

---

## Operations

| Method | Path | Description |
|--------|------|-------------|
| GET | `/service` | List or find Service objects |
| POST | `/service` | Creates a Service (triggers activation) |
| GET | `/service/{id}` | Retrieves a Service by ID |
| PATCH | `/service/{id}` | Partially updates (reconfigures) a Service |
| DELETE | `/service/{id}` | Deletes (deactivates) a Service |
| GET | `/monitor` | List or find Monitor objects |
| GET | `/monitor/{id}` | Retrieves a Monitor by ID |
| POST | `/hub` | Register a listener for event notifications |
| DELETE | `/hub/{id}` | Unregister a listener |

---

## Resource: Service

The `Service` resource is the central entity — it represents a live (or in-flight) service instance
in the OSS inventory.

| Field | Type | Required for `POST` | Description |
|-------|------|----------------------|-------------|
| `id` | string | server-assigned | Unique identifier of the service |
| `href` | string | server-assigned | Self-reference URI |
| `name` | string | **recommended** | Human-readable service name |
| `serviceType` | string | **recommended** | Business type (e.g. `FTTH`, `FTTC`, `VoIP`) |
| `category` | string | no | `CFS` or `RFS` |
| `description` | string | no | Free-text description |
| `isBundle` | boolean | no | True if this is a ServiceBundle |
| `isServiceEnabled` | boolean | no | False = provisioned but not yet enabled |
| `isStateful` | boolean | no | True = service can change without affecting others |
| `hasStarted` | boolean | no | True once activation sequence has begun |
| `startMode` | string | no | `0`=Unknown `1`=Automatic `2`=Manual `3`=OnDemand |
| `startDate` | string (date-time) | no | Service start date |
| `endDate` | string (date-time) | no | Service end date |
| `serviceDate` | string (date-time) | server-set | Date the service record was created |
| `state` | ServiceStateType | server-set | Current lifecycle state |
| `serviceCharacteristic` | ServiceCharacteristic[] | context-dependent | Technical parameters |
| `feature` | Feature[] | no | Optional feature flags |
| `place` | Place[] | **required for FTTH** | Installation/service address |
| `relatedParty` | RelatedParty[] | **required** | Customer, technician, account manager |
| `serviceSpecification` | ServiceSpecificationRef | recommended | Catalogue spec this instance is derived from |
| `serviceRelationship` | ServiceRelationship[] | no | Links to related services (parent/child/cross) |
| `serviceOrderItem` | ServiceOrderItemRef[] | no | Back-reference to originating order items |
| `supportingService` | SupportingService[] | no | Child RFS services supporting this CFS |
| `supportingResource` | SupportingResource[] | no | Physical resources (OLT port, ONT, etc.) |
| `note` | Note[] | no | Operational annotations |
| `@type` | string | no | Subclass discriminator |

### ServiceStateType (enum)

| Value | Meaning |
|-------|---------|
| `feasibilityChecked` | Coverage/feasibility check completed; no resources reserved |
| `designed` | Service designed in OSS inventory; spec resolved to a configuration |
| `reserved` | Network resources (OLT port, VLAN, IP) reserved but not yet active |
| `inactive` | Fully provisioned in the network but traffic is blocked/disabled |
| `active` | Service is live; traffic is flowing |
| `terminated` | Service has been deactivated and resources released |

---

## Resource: ServiceCharacteristic

Carries a typed name/value pair representing a technical or commercial attribute.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Identifier of this characteristic instance |
| `name` | string | **Required.** Attribute name |
| `value` | Any | Attribute value |
| `valueType` | string | Data type: `string`, `integer`, `boolean`, `object` |
| `characteristicRelationship` | CharacteristicRelationship[] | Links between related characteristics |

### RFS-level characteristics for FTTH/GPON activation

| `name` | `valueType` | Example | Description |
|--------|-------------|---------|-------------|
| `oltHostname` | string | `"OLT-LDNG-01"` | Hostname or IP of the OLT chassis |
| `oltPortId` | string | `"0/0/1/3"` | Shelf/slot/port/pon notation |
| `ontSerialNumber` | string | `"ALCL12345678"` | ONT/ONU serial for zero-touch provisioning |
| `ontIndex` | integer | `5` | ONT index on the PON port (0–127) |
| `gemPortId` | integer | `1024` | GEM port assigned to this service |
| `tcontId` | integer | `2` | T-CONT ID for upstream traffic scheduling |
| `vlanId` | integer | `100` | Service VLAN (C-VLAN) |
| `svlanId` | integer | `200` | Provider VLAN (S-VLAN / outer tag) |
| `cosProfile` | string | `"FTTH_BEST_EFFORT"` | Class of service / QoS profile name |
| `bwProfileDown` | string | `"1G_DOWN"` | Downstream bandwidth profile |
| `bwProfileUp` | string | `"220M_UP"` | Upstream bandwidth profile |
| `ipAddressType` | string | `"dynamic"` | `dynamic` (DHCP) or `static` |
| `staticIpAddress` | string | `"203.0.113.10"` | Only present when `ipAddressType=static` |
| `subnetMask` | string | `"255.255.255.248"` | Static IP subnet mask |
| `defaultGateway` | string | `"203.0.113.9"` | Static IP default gateway |
| `pppoeUsername` | string | `"user@isp.example"` | PPPoE authentication username |
| `pppoePassword` | string | `"s3cr3t"` | PPPoE authentication password (encrypted in transit) |
| `serviceProfile` | string | `"FTTH_RESIDENTIAL_1G"` | OLT service profile applied to the ONT port |
| `lineProfile` | string | `"FTTH_LINE_GPON_1G"` | OLT line profile (upstream/downstream shaping) |
| `activationScript` | string | `"scripts/gpon_activate_v2.sh"` | Optional: provisioning script reference |

---

## Resource: Feature

Represents an optional capability that can be enabled or disabled on a `Service`.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier of the feature |
| `name` | string | **Required.** Feature name |
| `isEnabled` | boolean | True if enabled (default: true) |
| `isBundle` | boolean | True if this is a feature group |
| `featureCharacteristic` | Characteristic[] | Parameters of this feature |
| `featureRelationship` | FeatureRelationship[] | Dependency/exclusion links |
| `constraint` | ConstraintRef[] | Business rules constraining this feature |

### Common FTTH features

| Feature `name` | `isEnabled` default | Description |
|----------------|---------------------|-------------|
| `StaticIP` | false | Allocate a static public IP; requires `staticIpAddress` characteristic |
| `IPv6` | true | Enable IPv6 dual-stack on the CPE |
| `VoIP` | false | Enable VoIP VLAN and SIP registration |
| `IPTV` | false | Enable multicast VLAN for IPTV delivery |
| `BusinessGrade_SLA` | false | Enable enhanced QoS profiles and SLA monitoring |
| `RemoteManagement` | true | Allow ISP remote access to CPE for diagnostics |
| `WifiManagement` | true | Centralised Wi-Fi management via TR-069/CWMP |

---

## Resource: Monitor

The `Monitor` resource is returned by asynchronous POST/PATCH operations and allows the caller to
track activation progress.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Monitor instance identifier |
| `href` | string | Self-reference URI |
| `sourceHref` | string | Href of the resource being monitored |
| `state` | string | `InProgress` · `InError` · `Completed` |
| `request` | Request | The original request (method, path, body) |
| `response` | Response | The eventual response (status code, body) |

### Activation polling workflow

1. Client POSTs to `/service` → server returns `HTTP 201` with a `Monitor` in the body.
2. Client polls `GET /monitor/{id}` until `state` is `Completed` or `InError`.
3. On `Completed`: the `response.body` contains the activated `Service` resource.
4. On `InError`: `response.body` contains error detail; the source service may be in `inactive` state.

---

## Resource: Place

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier of the place |
| `href` | string | Hyperlink reference |
| `name` | string | Human-readable label (e.g. `"Installation address"`) |
| `@type` | string | Subclass: use `GeographicAddress` for a physical address |

### GeographicAddress sub-type (typical FTTH fields)

| Field | Description |
|-------|-------------|
| `streetNr` | House or building number |
| `streetName` | Street name (without number) |
| `streetSuffix` | Suffix such as `"Flat 3"` or `"Unit B"` |
| `locality` | Locality / suburb |
| `city` | City or town |
| `stateOrProvince` | State or county |
| `postcode` | Postal code |
| `country` | ISO 3166-1 alpha-2 code (e.g. `"GB"`) |
| `uprn` | Unique Property Reference Number (UK-specific) |

---

## Resource: RelatedParty

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Party identifier |
| `href` | string | Link to party resource |
| `name` | string | Display name |
| `role` | string | Role in this activation context |
| `@referredType` | string | Actual party type (`Individual`, `Organization`) |

Common roles in TMF640 context: `Customer`, `ServiceProvider`, `FieldTechnician`, `NetworkOperator`

---

## Activation State-Machine Summary

```
[feasibilityChecked]
        |  address valid + coverage confirmed
        v
    [designed]
        |  resource reservation triggered
        v
    [reserved]
        |  ONT discovered / VLAN allocated / IP reserved
        v
    [inactive]  ← POST /service with full characteristics
        |  activation script executed on OLT
        v
     [active]  ← PATCH /service { isServiceEnabled: true }
        |  decommission request
        v
  [terminated]
```

---

## Example: FTTH RFS Activation (POST /service)

```json
{
  "@type": "Service",
  "name": "RFS-FTTH-12BakerSt-GPON",
  "serviceType": "FTTH",
  "category": "RFS",
  "isServiceEnabled": false,
  "serviceCharacteristic": [
    { "name": "oltHostname",     "value": "OLT-LDNG-01",           "valueType": "string" },
    { "name": "oltPortId",       "value": "0/0/1/3",               "valueType": "string" },
    { "name": "ontSerialNumber", "value": "ALCL12345678",           "valueType": "string" },
    { "name": "vlanId",          "value": 100,                     "valueType": "integer" },
    { "name": "svlanId",         "value": 200,                     "valueType": "integer" },
    { "name": "serviceProfile",  "value": "FTTH_RESIDENTIAL_1G",   "valueType": "string" },
    { "name": "bwProfileDown",   "value": "1G_DOWN",               "valueType": "string" },
    { "name": "bwProfileUp",     "value": "220M_UP",               "valueType": "string" },
    { "name": "ipAddressType",   "value": "dynamic",               "valueType": "string" }
  ],
  "place": [
    {
      "@type": "GeographicAddress",
      "streetNr": "12",
      "streetName": "Baker Street",
      "city": "London",
      "postcode": "W1U 6TS",
      "country": "GB",
      "uprn": "100023336956"
    }
  ],
  "relatedParty": [
    { "id": "CUST-99001", "name": "Jane Doe", "role": "Customer" }
  ]
}
```

Expected response: `HTTP 201 Created` with a `Monitor` resource. Poll `GET /monitor/{id}` until
`state == "Completed"`, then confirm the service `state` is `inactive` (ready for final enable PATCH).

---

## Example: Enable Service (PATCH /service/{id})

```json
{
  "isServiceEnabled": true,
  "state": "active"
}
```

---

*Excerpted from the TMF640 OpenAPI specification. Copyright © TM Forum 2019. Licensed under Apache-2.0.*
*Source: https://github.com/tmforum-apis/TMF640_ActivationConfiguration — commit 34ffd1ae*
