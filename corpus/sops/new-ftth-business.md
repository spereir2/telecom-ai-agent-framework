# SOP: New FTTH Business Service Activation

> **Document type:** Standard Operating Procedure (synthesised for RAG corpus)
> **SOP ID:** SOP-PROV-002
> **Version:** 1.8
> **Owner:** Provisioning Engineering — NexFibre UK (fictional)
> **Licence:** MIT (same as repository) — fictional ISP; no real operational data.

---

## Purpose

This SOP defines the end-to-end process for activating a new FTTH/FTTP business service
for a NexFibre UK business customer. It supplements SOP-PROV-001 (residential) with the
additional steps, validation rules, and SLA requirements specific to business products.

---

## Scope

Applies to business product codes: `BBB-FTTH-500`, `BBB-FTTH-1G`, `BBB-FTTH-2G`, `BBB-FTTH-10G`.

For Enterprise 10G (`BBB-FTTH-10G`) see the additional section at the end of this document.
For residential customers see SOP-PROV-001.

---

## Key Differences from Residential Activation

| Aspect | Residential (SOP-PROV-001) | Business (this SOP) |
|--------|---------------------------|---------------------|
| Customer `@referredType` | `"Individual"` | `"Organization"` |
| `ServiceOrder.category` | `"Broadband"` | `"Business"` |
| Static IP | Optional add-on | **Mandatory — included as standard** |
| IP allocation size | /32 (single) | /29 minimum; /28 for B3; /27 for B4 |
| VLAN range | 100–199 (exchange-specific) | 200–299 (exchange-specific) |
| Contention ratio | 50:1 to 10:1 | 10:1 to 1:1 |
| SLA fault repair | Best effort | NBD (B1), SBD 8h (B2), 4h/8h (B3), 2h/4h (B4) |
| Pre-sales requirement | None (standard) | Survey required for B4; recommended for B3 |
| Account manager | None | Assigned for B2+ |
| Engineer visit | When ONT absent | Always required for new business install |

---

## Prerequisites

1. **Address validation** — UPRN confirmed in NexFibre footprint (SOP-PROV-003).
   For `BBB-FTTH-2G` and `BBB-FTTH-10G`: XGS-PON availability must also be confirmed.
2. **Business identity verification** — The `relatedParty[role=Customer]` entry must:
   - Have `@referredType: "Organization"`.
   - Carry a CRM customer ID that maps to a verified business entity (Companies House
     number for UK, or equivalent).
   - Not be a residential customer ID — the OMS will reject with `CUSTOMER_TYPE_MISMATCH`.
3. **Credit check** — A business credit check (hard) must be completed. Reference stored
   in `externalReference[type=CreditCheckRef].id`.
4. **Static IP allocation** — An IP block must be pre-reserved from the business IP pool
   **before** the order is submitted. The allocated `staticIpAddress` and `subnetMask`
   must be included in `serviceCharacteristic` at order creation time.
5. **SLA agreement** — Customer must have accepted the relevant Service Level Agreement
   document (linked via `externalReference[type=SLAReference].href`).
6. **No blocking orders** — Same check as SOP-PROV-001.
7. **Pre-sales survey** (B3/B4 only) — A completed survey order must be referenced via
   `orderRelationship[type=prerequisite].id`.

---

## Step 1 — IP Block Allocation (before order creation)

**Actor:** IP Address Management (IPAM) system or provisioning agent

**Action:**
1. Log into IPAM portal and allocate an IP block:
   - B1 (`BBB-FTTH-500`): allocate `/29` (8 addr, 5 usable)
   - B2 (`BBB-FTTH-1G`): allocate `/29` (8 addr, 5 usable)
   - B3 (`BBB-FTTH-2G`): allocate `/28` (16 addr, 13 usable)
   - B4 (`BBB-FTTH-10G`): allocate `/27` (32 addr, 29 usable)
2. Record: `staticIpAddress` (first usable), `subnetMask`, `defaultGateway`.
3. Mark the block as `reserved` in IPAM with the CRM order reference.

**Why this is pre-order:** Business SLAs do not permit holding the order in `pending`
while waiting for an IP block. The static IP characteristics **must** be present in the
POST body or the order will be rejected with `MISSING_STATIC_IP`.

---

## Step 2 — Create Service Order (TMF641)

**Actor:** OMS or provisioning agent

**Action:** POST to `/serviceOrder` with:

```
ServiceOrder.category              = "Business"
ServiceOrder.priority              = "1"   (business orders take priority over residential)
ServiceOrder.externalId            = <CRM order reference>
ServiceOrder.relatedParty          = [
  { role: "Customer",        id: <org CRM ID>,    @referredType: "Organization" },
  { role: "AccountManager",  id: <AM employee ID>, @referredType: "Individual"  }
]
ServiceOrder.externalReference     = [
  { type: "CreditCheckRef",  id: <credit check reference> },
  { type: "SLAReference",    href: <SLA document URL>     }
]
ServiceOrder.serviceOrderItem      = [{
  id: "1",
  action: "add",
  service: {
    serviceType: <from product code>,
    category: "CFS",
    serviceCharacteristic: [
      downloadSpeed, uploadSpeed, technologyType, serviceProfile, contractTermMonths,
      ipAddressType: "static",
      staticIpAddress: <from IPAM Step 1>,
      subnetMask:      <from IPAM Step 1>,
      defaultGateway:  <from IPAM Step 1>
    ],
    place: [ { @type: "GeographicAddress", ...address including UPRN } ]
  }
}]
```

**Additional validation for business orders:**
- `ipAddressType` must be `"static"` — rejection: `STATIC_IP_REQUIRED_FOR_BUSINESS`
- `staticIpAddress` must be present — rejection: `MISSING_STATIC_IP`
- `relatedParty[role=Customer].@referredType` must be `"Organization"` — rejection: `CUSTOMER_TYPE_MISMATCH`
- `ServiceOrder.priority` should be `"1"` for all business products

---

## Step 3 — Resource Assessment

**Actor:** Provisioning Orchestrator (automated)
**Trigger:** Order reaches `acknowledged`

**Actions:**
1. Query Network Inventory for PON port serving the UPRN.
   - Confirm PON port is in the business VLAN segment (200–299).
   - If not, escalate to network engineering — do not attempt to use residential VLAN range.
2. Allocate `vlanId` from business pool (200–299).
3. Determine `svlanId` (provider/outer VLAN) for QinQ encapsulation.
4. For B3/B4: confirm XGS-PON availability and capacity.
5. Activate the IPAM reservation (move block from `reserved` to `allocated`).
6. Update order to `inProgress`.

---

## Step 4 — Engineer Appointment (mandatory for all business installs)

**Actor:** Field Workforce Management (FWM)

**Why mandatory:** Business installs always require an engineer to:
- Verify the premises entry point and internal wiring.
- Install (or verify) the ONT and ensure it is wall-mounted and properly labelled.
- Connect the ONT to the customer's CPE/router via Ethernet patch.
- Conduct an on-site acceptance test (speed test, latency, packet loss).
- Record the `ontSerialNumber` on the FWM work order.

**Appointment scheduling:**
- B1/B2: Appointment offered within 2 working days; morning (8–12) or afternoon (13–17).
- B3: Appointment within 1 working day; dedicated engineer (4-hour window).
- B4: Appointment within 1 working day; senior engineer + NOC support on standby.

**FWM updates back to OMS:**
- `ServiceOrderItem.appointment.id` → confirmed appointment reference
- `ServiceOrderItem.service.serviceCharacteristic[ontSerialNumber]` → actual ONT serial

---

## Step 5 — Activate RFS via TMF640

**Actor:** Provisioning Orchestrator
**Trigger:** Engineer work order completed; `ontSerialNumber` confirmed

**Action:** POST `/service` with the full RFS Service object (same structure as
SOP-PROV-001 Step 4, with business-specific additions):

Additional characteristics vs residential:
- `cosProfile`: `"FTTH_BUSINESS_SLA"` (B1/B2) or `"ENTERPRISE_STRICT_PRIORITY"` (B3/B4)
- `bwProfileDown` / `bwProfileUp`: use business profiles (lower contention, strict shaping)
- For B3/B4: `gemPortId` and `tcontId` use priority T-CONT for guaranteed bandwidth

**Polling:** Same as SOP-PROV-001. Timeout: 5 minutes; retry once before raising incident.

---

## Step 6 — Enable Service and SLA Verification

**Actor:** Provisioning Orchestrator

**Action:** PATCH `/service/{id}` → `{ "isServiceEnabled": true, "state": "active" }`

**Post-activation checks (business only):**
1. Run automated speed test via OLT management plane: verify ≥ 90% of headline speed.
2. Verify latency ≤ 10ms to NexFibre core router.
3. Confirm static IP is routable (ping from core router to `staticIpAddress` succeeds).
4. For B3/B4: verify SLA monitoring agent has registered the service for 24/7 alerting.

**Failure:** If any post-activation check fails, immediately PATCH `/service/{id}`:
`{ "isServiceEnabled": false }` and raise a P1 incident.

---

## Step 7 — Customer Handover

**Actor:** Account Manager + Notifications Service

**Actions:**
1. Send handover email containing:
   - Service start date and billing cycle.
   - **Static IP details:** IP address, subnet mask, default gateway, primary and secondary DNS.
   - SLA reference and fault reporting contact (24/7 NOC number for B3/B4).
   - CPE configuration guide (router must support 2.5GbE WAN for B3/B4).
   - Account portal credentials.
2. Account Manager schedules 30-day check-in call (B2 and above).
3. For B4: Service Manager completes on-boarding call within 1 working day.

---

## Business-Specific Error Codes

| Error code | Meaning | Recovery |
|------------|---------|----------|
| `CUSTOMER_TYPE_MISMATCH` | residential customer ID on business order | Use correct Organization CRM ID |
| `MISSING_STATIC_IP` | `staticIpAddress` not present | Complete IPAM pre-allocation (Step 1) |
| `STATIC_IP_REQUIRED_FOR_BUSINESS` | `ipAddressType` is not `"static"` | Set `ipAddressType: "static"` |
| `IPAM_BLOCK_NOT_RESERVED` | IP block not pre-reserved in IPAM | Log into IPAM and reserve block first |
| `VLAN_RANGE_CONFLICT` | Business VLAN range not available at exchange | Escalate to network engineering |
| `XGS_PON_NOT_AVAILABLE` | XGS-PON not deployed at this exchange | Offer GPON alternative (B1/B2 only) |
| `CREDIT_CHECK_REQUIRED` | Hard credit check reference missing | Complete credit check, add `externalReference` |
| `SLA_AGREEMENT_MISSING` | SLA reference not in `externalReference` | Obtain signed SLA, add reference |

---

## Enterprise 10G (BBB-FTTH-10G) Additional Requirements

The Enterprise 10G product has additional steps not required for B1–B3:

### Pre-Sales Survey (mandatory)
A certified NexFibre field engineer must complete a premises survey before any order can be placed.
The survey verifies:
- Suitable cable entry path for dedicated fibre run.
- Adequate power and ventilation for the XGS-PON ONT.
- Customer CPE has a 10GbE WAN port (or a 10GbE-capable switch in the path).

The survey produces a **Survey Approval Reference** that must be included in the order:
`orderRelationship[type=prerequisite, id=<survey approval ref>]`

Orders without a valid survey reference will be rejected with `SURVEY_REQUIRED`.

### CPE Requirements
NexFibre does not supply a router for B4. The customer's CPE must:
- Support a 10GbE WAN interface (SFP+ or 10GBase-T).
- Support BGP (if requesting AS and IP transit) — not standard.
- Support IEEE 802.1Q VLAN tagging if QinQ is required.

### Dedicated Wavelength
B4 services use a dedicated XGS-PON wavelength at 1Gbps+ burst, not shared with other customers.
The provisioning system must allocate a dedicated T-CONT with type `TYPE_4` (fixed bandwidth)
at the full 10Gbps rate. Use `cosProfile: "ENTERPRISE_STRICT_PRIORITY"`.

### NOC Integration
Before the order is marked `completed`:
1. Register the service in the NOC monitoring platform (service ID, IP range, SLA tier).
2. Configure SNMP traps from the OLT port to the NOC.
3. Assign an on-call Service Manager and record their contact details in the CRM.

---

## SLA Targets

| Product | Fault repair target | Proactive monitoring |
|---------|--------------------|-----------------------|
| B1 `BBB-FTTH-500` | Next Business Day (NBD) | Business hours |
| B2 `BBB-FTTH-1G` | Same Business Day (SBD), 8 hours | Business hours |
| B3 `BBB-FTTH-2G` | 4h response, 8h restore (24/7) | 24/7 NOC |
| B4 `BBB-FTTH-10G` | 2h response, 4h restore (24/7) | 24/7 NOC + dedicated SM |

| Activation milestone | B1/B2 target | B3/B4 target |
|---------------------|-------------|-------------|
| Order `acknowledged` | ≤ 30 seconds | ≤ 30 seconds |
| Engineer appointment offered | ≤ 2 working days | ≤ 1 working day |
| Service `active` post-install | ≤ 4 hours | ≤ 2 hours |
| Order `completed` | ≤ 5 working days | ≤ 3 working days |

---

## Related Documents

- SOP-PROV-001: New FTTH Residential Service Activation
- SOP-PROV-003: Address and Coverage Validation
- TMF641 Service Ordering API Reference (`corpus/tmf/tmf641-service-ordering.md`)
- TMF640 Service Activation API Reference (`corpus/tmf/tmf640-service-activation.md`)
- Broadband Product Catalogue (`corpus/product-catalog/broadband-products.md`)

---

*This document is synthesised fiction for use as a RAG training corpus. It does not describe
real NexFibre UK operational procedures. © 2026 telecom-ai-agent-framework contributors. MIT Licence.*
