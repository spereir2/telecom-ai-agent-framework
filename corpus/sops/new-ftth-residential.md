# SOP: New FTTH Residential Service Activation

> **Document type:** Standard Operating Procedure (synthesised for RAG corpus)
> **SOP ID:** SOP-PROV-001
> **Version:** 2.4
> **Owner:** Provisioning Engineering — NexFibre UK (fictional)
> **Licence:** MIT (same as repository) — fictional ISP; no real operational data.

---

## Purpose

This SOP defines the end-to-end process for activating a new residential FTTH/FTTP service
for a NexFibre UK customer. It covers the full lifecycle from order receipt through TMF641
to live service confirmation via TMF640.

---

## Scope

Applies to all residential product codes: `BBR-FTTH-100`, `BBR-FTTH-250`, `BBR-FTTH-500`,
`BBR-FTTH-1G`, `BBR-FTTH-2G`. For business customers see SOP-PROV-002.

---

## Prerequisites

Before initiating a new residential FTTH order, the following conditions **must** be met:

1. **Address validation** — The customer's premises must have a valid UPRN and must be within
   NexFibre's fibre footprint. Use the Address Validation Service (SOP-PROV-003) to confirm.
   An order submitted for a non-serviceable address will be auto-rejected with state `rejected`.
2. **Customer identity** — The `relatedParty[role=Customer]` entry must carry a valid CRM
   customer ID. The `@referredType` must be `"Individual"` for residential products.
3. **Product eligibility** — Confirm the requested product code is available at the address
   (e.g. `BBR-FTTH-2G` requires XGS-PON availability; not all exchanges are upgraded).
4. **No blocking orders** — Check for any existing `inProgress` or `pending` service orders
   at the same address. Overlapping orders must be resolved before proceeding.
5. **Credit check** — For new customers, a soft credit check must be completed via the CRM
   before order submission. Orders without a credit-check reference in `externalReference`
   will be flagged for manual review.

---

## Step 1 — Create Service Order (TMF641)

**Actor:** Order Management System (OMS) or provisioning agent

**Action:** POST to `/serviceOrder` with the following minimum required fields:

```
ServiceOrder.category          = "Broadband"
ServiceOrder.externalId        = <CRM order reference>
ServiceOrder.relatedParty      = [{ role: "Customer", id: <CRM customer ID> }]
ServiceOrder.serviceOrderItem  = [{
  id: "1",
  action: "add",
  service: {
    serviceType: <from product code mapping>,
    serviceCharacteristic: [
      downloadSpeed, uploadSpeed, technologyType, serviceProfile, contractTermMonths
    ],
    place: [{ @type: "GeographicAddress", ...address fields including UPRN }]
  }
}]
```

**Validation checks performed by the Order Management system:**
- UPRN is present and resolves to a serviceable address (rejects if not in footprint)
- `serviceProfile` value matches the product code
- `contractTermMonths` matches the product's allowed contract term
- `technologyType` is consistent with the product code (GPON vs XGS-PON)
- For XGS-PON products (`BBR-FTTH-2G`): `ontSerialNumber` is present with valid prefix

**Expected outcome:** Order reaches state `acknowledged` within 30 seconds. The OMS sets
`orderDate` and assigns an `id`.

---

## Step 2 — Order Assessment and Resource Check

**Actor:** Provisioning Orchestrator (automated)
**Trigger:** Order reaches `acknowledged`

**Actions:**
1. Query the Network Inventory (NI) for the PON port serving the UPRN.
   - Retrieve `oltHostname`, `oltPortId` for the serving OLT.
   - Confirm the PON port has available ONT slots (max 64 per GPON port, 128 per XGS-PON port).
2. Check VLAN pool for the exchange — allocate a `vlanId` from the residential VLAN range
   (100–199 for residential; 200–299 for business at this exchange).
3. For dynamic IP: note the DHCP pool; no reservation needed at this stage.
4. For static IP add-on: pre-allocate a public IPv4 address from the residential static pool.
5. Update `ServiceOrder.state` to `inProgress`.
6. Populate the RFS `ServiceCharacteristic` with discovered values:
   `oltHostname`, `oltPortId`, `vlanId`, `svlanId`.

**Failure conditions:**
- No available ONT slots → order transitions to `held`; engineer escalation triggered.
- No VLAN available → order transitions to `held`; network capacity ticket raised.

---

## Step 3 — Engineer Appointment (if required)

**Actor:** Field Workforce Management (FWM)
**Condition:** Required when:
  - No existing ONT at the premises (new-build or first NexFibre customer at address)
  - XGS-PON ONT installation required (product `BBR-FTTH-2G`)
  - Existing ONT is faulty or incompatible with requested product tier

**Actions:**
1. FWM creates an appointment record and populates `ServiceOrderItem.appointment.id`.
2. Customer is notified of the appointment window (morning 8–12 or afternoon 12–17).
3. Engineer installs/verifies ONT, records `ontSerialNumber` on the work order.
4. `ontSerialNumber` is written back to the order item's `serviceCharacteristic`.

**Timeline:** Appointment typically within 5–10 working days of order placement.

**Skip condition:** If the Network Inventory confirms a compatible ONT already exists at the
UPRN (e.g. customer upgrading from `BBR-FTTH-500` to `BBR-FTTH-1G` on GPON), proceed directly
to Step 4. Engineer visit is not required for speed upgrades on the same technology type.

---

## Step 4 — Activate Service via TMF640

**Actor:** Provisioning Orchestrator (automated)
**Trigger:** `ontSerialNumber` present in order characteristics AND appointment completed
(or appointment not required per Step 3 skip condition)

**Action:** POST to `/service` with the full RFS `Service` object:

```
Service.serviceType           = "FTTH"
Service.category              = "RFS"
Service.isServiceEnabled      = false
Service.serviceCharacteristic = [
  oltHostname, oltPortId, ontSerialNumber, ontIndex,
  vlanId, svlanId, gemPortId, tcontId,
  serviceProfile, bwProfileDown, bwProfileUp,
  ipAddressType (+ staticIpAddress if applicable),
  pppoeUsername (if PPPoE authentication model)
]
Service.place                 = [ installation address with UPRN ]
Service.relatedParty          = [ Customer ref ]
```

**Expected response:** `HTTP 201` with a `Monitor` resource. Record `Monitor.id`.

**Polling:** Poll `GET /monitor/{id}` every 10 seconds up to 5 minutes.
- `state == "Completed"` → proceed to Step 5.
- `state == "InError"` → capture error, roll back VLAN reservation, transition order to
  `failed`, trigger manual intervention workflow.

**What the provisioning system does:**
- Pushes ONT configuration to the OLT via NETCONF (or CLI template if NETCONF unavailable).
- Creates GEM port and T-CONT mappings.
- Applies the `serviceProfile` (downstream/upstream policing, CoS mappings).
- Writes the ONT serial to the OLT's zero-touch provisioning (ZTP) whitelist.

---

## Step 5 — Enable Service

**Actor:** Provisioning Orchestrator
**Trigger:** TMF640 Monitor reaches `Completed`; `Service.state` is `inactive`

**Action:** PATCH `/service/{id}`:

```json
{ "isServiceEnabled": true, "state": "active" }
```

**Expected outcome:** Service transitions to `active`. Traffic is now permitted through
the GEM port. CPE DHCP or PPPoE will succeed within 60 seconds of the PATCH being applied.

**Verification:**
1. Query `GET /service/{id}` — confirm `state == "active"`.
2. (Optional) Send a synthetic ping via the OLT management plane to verify CPE is online.
3. Update `ServiceOrderItem.state` to `completed`.
4. Update `ServiceOrder.state` to `completed` (if all items are complete).
5. Populate `ServiceOrder.completionDate` with the current timestamp.

---

## Step 6 — Customer Notification

**Actor:** CRM / Notifications Service
**Trigger:** `ServiceOrder.state == "completed"`

**Actions:**
1. Send welcome email with:
   - Service start date and billing cycle start.
   - Router setup guide (if NexFibre-supplied router).
   - Account portal link.
   - Speed test link and expected typical speeds.
2. For static IP customers: include the allocated IP address, subnet mask, default gateway,
   and DNS server addresses in the welcome email.
3. For XGS-PON (`BBR-FTTH-2G`): include note about 2.5GbE LAN port requirement.

---

## Error Scenarios and Recovery

| Scenario | Detection | Recovery action |
|----------|-----------|-----------------|
| ONT not responding after activation | TMF640 Monitor `InError` | Re-run Step 4 after 15 min; if still failing, raise field escalation |
| Wrong ONT serial | TMF640 Monitor `InError` with `ONT_NOT_FOUND` | Correct `ontSerialNumber` in order, retry Step 4 |
| VLAN already in use | Step 2 resource check fails | Deallocate conflicting VLAN, re-allocate from pool, retry |
| Address not in footprint | Step 1 validation rejects | Notify customer, close order with `rejected` |
| Credit check expired | OMS flags for review | Re-run credit check, update `externalReference`, resubmit |
| Appointment no-show | FWM marks appointment cancelled | Rebook within 3 working days; customer notified |

---

## SLA Targets

| Milestone | Target |
|-----------|--------|
| Order `acknowledged` | ≤ 30 seconds |
| Order to `inProgress` | ≤ 2 minutes (automated path) |
| Engineer appointment offered | ≤ 2 working days |
| Service `active` post-ONT install | ≤ 4 hours |
| Order `completed` | ≤ 10 working days (standard); ≤ 5 working days (priority) |

---

## Related Documents

- SOP-PROV-002: New FTTH Business Service Activation
- SOP-PROV-003: Address and Coverage Validation
- TMF641 Service Ordering API Reference (see `corpus/tmf/tmf641-service-ordering.md`)
- TMF640 Service Activation API Reference (see `corpus/tmf/tmf640-service-activation.md`)
- Broadband Product Catalogue (see `corpus/product-catalog/broadband-products.md`)

---

*This document is synthesised fiction for use as a RAG training corpus. It does not describe
real NexFibre UK operational procedures. © 2026 telecom-ai-agent-framework contributors. MIT Licence.*
