# SOP: Address and Coverage Validation

> **Document type:** Standard Operating Procedure (synthesised for RAG corpus)
> **SOP ID:** SOP-PROV-003
> **Version:** 3.1
> **Owner:** Provisioning Engineering — NexFibre UK (fictional)
> **Licence:** MIT (same as repository) — fictional ISP; no real operational data.

---

## Purpose

This SOP defines how to validate a customer address before any FTTH service order is submitted.
It ensures the premises is within NexFibre's fibre footprint, has an available network connection
point, and that the address is correctly formatted for use in TMF641/TMF640 API calls.

Performing address validation before order creation prevents the most common rejection reason:
`ADDRESS_NOT_SERVICEABLE`, which accounts for ~35% of all order failures.

---

## Scope

Applies to all order types handled by SOP-PROV-001 (residential) and SOP-PROV-002 (business).
Must be completed as a prerequisite step before any `POST /serviceOrder` call.

---

## Key Concepts

### UPRN (Unique Property Reference Number)
A persistent 12-digit identifier assigned to every addressable property in Great Britain by
Ordnance Survey (AddressBase Premium). The UPRN is the canonical key for NexFibre's network
inventory lookups. All provisioning API calls must include the UPRN in the `place` object.

### Footprint Status
NexFibre's footprint database records one of four statuses per UPRN:

| Status | Meaning | Action |
|--------|---------|--------|
| `SERVICEABLE` | Premises is on-net; NCP exists; orders accepted | Proceed to order |
| `PLANNED` | In-build area; network not yet complete | Cannot order; add to waitlist |
| `SURVEY_REQUIRED` | Premises is off-net but may be connectable | Trigger off-net survey |
| `NOT_SERVICEABLE` | Outside coverage; no planned deployment | Decline order; log for future |

### NCP (Network Connection Point)
The physical endpoint in NexFibre's network that serves a specific UPRN — typically a
fibre distribution point (FDP) chamber or building entry point. The NCP record carries:
- The serving OLT hostname and port
- The available technology (GPON, XGS-PON, or both)
- The number of available ONT slots

---

## Step 1 — Capture and Normalise the Address

**Actor:** CRM agent, digital channel, or provisioning system

**Required inputs:**

| Field | Format | Example |
|-------|--------|---------|
| House/building number | String | `"12"` |
| Street name | String (no number) | `"Baker Street"` |
| Locality (optional) | String | `"Marylebone"` |
| City/town | String | `"London"` |
| Postcode | UK format (uppercase, with space) | `"W1U 6TS"` |

**Normalisation rules:**
1. Strip leading/trailing whitespace from all fields.
2. Convert postcode to uppercase and ensure there is exactly one space before the inward code
   (e.g. `"w1u6ts"` → `"W1U 6TS"`; `"W1U6TS"` → `"W1U 6TS"`).
3. Expand common street-type abbreviations: `St` → `Street`, `Rd` → `Road`, `Ave` → `Avenue`.
4. Remove punctuation from street name (except hyphens in hyphenated names).

**Rejection:** If postcode does not match `^[A-Z]{1,2}[0-9][0-9A-Z]?\s[0-9][A-Z]{2}$`,
return `INVALID_POSTCODE` without querying any downstream service.

---

## Step 2 — UPRN Lookup

**Actor:** Address Validation Service (internal API)

**Endpoint:** `GET /address-lookup?postcode={postcode}&houseNumber={houseNumber}`

**Response fields:**

| Field | Type | Description |
|-------|------|-------------|
| `uprn` | string | 12-digit UPRN |
| `fullAddress` | string | Canonical formatted address |
| `streetNr` | string | House/building number |
| `streetName` | string | Canonical street name |
| `locality` | string | Sub-locality (may be empty) |
| `city` | string | City |
| `stateOrProvince` | string | County/region |
| `postcode` | string | Normalised postcode |
| `country` | string | `"GB"` |
| `confidence` | integer | Match confidence 0–100 |
| `matchType` | string | `EXACT`, `CLOSE`, `FUZZY` |

**Handling match types:**
- `EXACT` (confidence ≥ 95): use the UPRN and proceed.
- `CLOSE` (confidence 80–94): present the canonical address to the agent/customer for confirmation before proceeding.
- `FUZZY` (confidence < 80): do not proceed; ask the customer to re-enter their address.

**Multiple matches:** If the postcode + house number returns more than one UPRN (e.g. a block
of flats), present the list of canonical addresses and require the customer to select the
exact unit (e.g. `"Flat 3, 12 Baker Street"`).

**No match:** Return `ADDRESS_NOT_FOUND`. Ask the customer to check their postcode and
house number. Do not submit an order.

---

## Step 3 — Footprint Check

**Actor:** Network Inventory (NI) system

**Endpoint:** `GET /coverage?uprn={uprn}`

**Response:**

```json
{
  "uprn": "100023336956",
  "footprintStatus": "SERVICEABLE",
  "technologies": ["GPON", "XGS-PON"],
  "ncp": {
    "id": "NCP-LDNG-00412",
    "oltHostname": "OLT-LDNG-01",
    "oltPortId": "0/0/1/3",
    "availableSlots": 28,
    "maxSlots": 64
  },
  "exchangeCode": "LDNG",
  "buildType": "EXISTING_BUILD"
}
```

**Handling by `footprintStatus`:**

| Status | Agent action |
|--------|-------------|
| `SERVICEABLE` | Record the `ncp` details; proceed to Step 4 |
| `PLANNED` | Inform customer of expected go-live date; add UPRN to waitlist via `POST /waitlist`; decline order |
| `SURVEY_REQUIRED` | Raise an off-net survey ticket; inform customer of 10–15 working day assessment period; do not submit order |
| `NOT_SERVICEABLE` | Decline the order; log the UPRN in the demand register for future planning; inform customer |

**Technology check for product validation:**
- Products `BBR-FTTH-100` through `BBR-FTTH-1G` and `BBB-FTTH-500`/`BBB-FTTH-1G` require `"GPON"` in `technologies`.
- Products `BBR-FTTH-2G`, `BBB-FTTH-2G`, `BBB-FTTH-10G` require `"XGS-PON"` in `technologies`.
- If the customer requests an XGS-PON product but only GPON is available, offer the highest
  available GPON product as an alternative. Do not submit an XGS-PON order without XGS-PON
  in the `technologies` list — it will fail with `TECHNOLOGY_NOT_AVAILABLE`.

**Available slot check:**
- If `availableSlots == 0`, the PON port is full. Do not proceed.
- Raise a capacity planning ticket and put the order in `held` state.
- Inform the customer of the delay (typically 10–20 working days for a new PON port split).

---

## Step 4 — Compile Validated Address Object

**Actor:** Provisioning system

Once UPRN is confirmed and footprint status is `SERVICEABLE`, compile the `Place` object
for use in TMF641 and TMF640 API calls:

```json
{
  "@type": "GeographicAddress",
  "name": "Installation address",
  "streetNr": "12",
  "streetName": "Baker Street",
  "locality": "Marylebone",
  "city": "London",
  "stateOrProvince": "Greater London",
  "postcode": "W1U 6TS",
  "country": "GB",
  "uprn": "100023336956"
}
```

**Rules:**
- `uprn` **must** be populated — the provisioning orchestrator uses it for all downstream
  NI lookups. An order without `uprn` in the `place` object will fail internal validation
  with `UPRN_REQUIRED`.
- `country` must be `"GB"` for all UK addresses.
- Do not abbreviate `streetName` — use the canonical form from the UPRN lookup response.
- `locality` is optional but should be included if non-empty.

---

## Step 5 — Existing Service Check

**Actor:** Network Inventory (NI) and Service Inventory

**Endpoint:** `GET /service?place.uprn={uprn}&state=active,inactive,reserved`

**Purpose:** Check whether NexFibre already has an active or in-flight service at this UPRN.

| Scenario | Action |
|----------|--------|
| No existing service | Proceed — this is a genuine new order |
| Active service (same customer) | This is a modification/upgrade — use `action: modify`, not `action: add` |
| Active service (different customer) | Cease-and-reprovision flow — require signed cease notice before proceeding |
| Reserved/inactive service | Existing order in flight — check for duplicate; contact the original order owner |

**Important:** Submitting `action: add` when an active service already exists at the UPRN
will be rejected with `DUPLICATE_SERVICE`. Always check for existing services first.

---

## Step 6 — Record Validation Result

**Actor:** Provisioning system

Record the following in the CRM and in the order audit log:
1. UPRN confirmed: `<uprn>`
2. Footprint status: `SERVICEABLE`
3. Available technologies: `["GPON", "XGS-PON"]` (example)
4. NCP: `NCP-LDNG-00412`
5. OLT: `OLT-LDNG-01`, port `0/0/1/3`
6. Validation timestamp: ISO 8601 UTC
7. Validation expiry: 30 days from validation timestamp (re-validate if order is not
   submitted within 30 days — footprint status may change)

Store these as `externalReference` entries on the `ServiceOrder`:

```json
"externalReference": [
  { "type": "AddressValidationRef", "id": "AV-20240501-001234", "name": "Address validated 2024-05-01" },
  { "type": "NCPRef",               "id": "NCP-LDNG-00412" }
]
```

---

## Common Address Validation Errors

| Error code | Cause | Resolution |
|------------|-------|------------|
| `INVALID_POSTCODE` | Postcode format invalid | Normalise postcode; re-enter |
| `ADDRESS_NOT_FOUND` | No UPRN match | Customer re-enters address; try partial match |
| `ADDRESS_NOT_SERVICEABLE` | UPRN outside footprint | Inform customer; log for demand planning |
| `TECHNOLOGY_NOT_AVAILABLE` | XGS-PON requested but only GPON at UPRN | Offer GPON alternative |
| `NO_AVAILABLE_SLOTS` | PON port at capacity | Place on hold; raise capacity ticket |
| `UPRN_REQUIRED` | `place` object missing `uprn` | Re-run validation and populate `uprn` |
| `DUPLICATE_SERVICE` | Active service already at UPRN | Check if modify/cease needed instead |
| `VALIDATION_EXPIRED` | Validation > 30 days old | Re-run Steps 2–5 |

---

## UPRN Lookup Failure Handling

If the Address Validation Service (Step 2) is unavailable (HTTP 5xx or timeout):

1. Do not proceed with the order.
2. Log the failure with the customer's input address and timestamp.
3. Retry after 60 seconds (up to 3 retries).
4. After 3 failures, escalate to the platform operations team.
5. Inform the customer of the delay and provide a reference number.

**Never** skip UPRN lookup and proceed with a manually entered address — the NI lookup
in the provisioning orchestrator requires a validated UPRN.

---

## Address Formats for Edge Cases

### Flats and apartments

| Input | Correct `streetSuffix` | `streetNr` |
|-------|----------------------|------------|
| `Flat 3, 12 Baker Street` | `"Flat 3"` | `"12"` |
| `Apartment 2B, Regency House, 45 High Road` | `"Apartment 2B"` | `"45"` (Regency House → `streetName` suffix) |

When a building name is present, use `streetSuffix` for the sub-unit and `streetName`
for the full street name including any building name as the UPRN lookup return dictates.

### Business premises

Business premises may have a `buildingName` in addition to or instead of a `streetNr`.
Always prefer the canonical `fullAddress` from the UPRN lookup response over manual entry.

### New-build properties

New-build properties may have a UPRN assigned (via Ordnance Survey provisional UPRN) but
may not yet appear in NexFibre's footprint database. In this case:
1. Confirm the UPRN with OS AddressBase.
2. Raise a manual footprint registration request with the NexFibre Network Build team.
3. Expected lead time: 5 working days for properties in an active build area.

---

## Related Documents

- SOP-PROV-001: New FTTH Residential Service Activation
- SOP-PROV-002: New FTTH Business Service Activation
- TMF641 Service Ordering API Reference (`corpus/tmf/tmf641-service-ordering.md`)
- TMF640 Service Activation API Reference (`corpus/tmf/tmf640-service-activation.md`)
- Broadband Product Catalogue (`corpus/product-catalog/broadband-products.md`)

---

*This document is synthesised fiction for use as a RAG training corpus. It does not describe
real NexFibre UK operational procedures. © 2026 telecom-ai-agent-framework contributors. MIT Licence.*
