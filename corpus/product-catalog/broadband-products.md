# Broadband Product Catalogue — ISP NexFibre UK

> **Document type:** Synthesised product catalogue (fictional ISP "NexFibre UK")
> **Purpose:** Training / evaluation corpus for the telecom-ai-agent-framework RAG system.
> **Licence:** MIT (same as repository) — no real ISP data; all product names, codes, and
> prices are fictional and for illustrative purposes only.
> **Last updated:** 2026-05-19

---

## Product Tiers Overview

NexFibre UK offers five residential and four business broadband tiers, all delivered over
a full-fibre (FTTH/FTTP) network using GPON or XGS-PON technology. Legacy copper (ADSL/FTTC)
products are in end-of-life and no longer available for new orders.

| Tier | Product Code | Technology | Down | Up | Contention | Monthly (£) | Contract |
|------|-------------|------------|------|-----|------------|-------------|----------|
| R1 | `BBR-FTTH-100` | GPON | 100 Mbps | 20 Mbps | 50:1 | 24.99 | 18 months |
| R2 | `BBR-FTTH-250` | GPON | 250 Mbps | 55 Mbps | 40:1 | 34.99 | 18 months |
| R3 | `BBR-FTTH-500` | GPON | 500 Mbps | 115 Mbps | 30:1 | 44.99 | 24 months |
| R4 | `BBR-FTTH-1G` | GPON | 1000 Mbps | 220 Mbps | 20:1 | 54.99 | 24 months |
| R5 | `BBR-FTTH-2G` | XGS-PON | 2000 Mbps | 2000 Mbps | 10:1 | 74.99 | 24 months |
| B1 | `BBB-FTTH-500` | GPON | 500 Mbps | 115 Mbps | 10:1 | 69.99 | 24 months |
| B2 | `BBB-FTTH-1G` | GPON | 1000 Mbps | 220 Mbps | 5:1 | 89.99 | 24 months |
| B3 | `BBB-FTTH-2G` | XGS-PON | 2000 Mbps | 2000 Mbps | 3:1 | 119.99 | 24 months |
| B4 | `BBB-FTTH-10G` | XGS-PON | 10000 Mbps | 10000 Mbps | 1:1 | 249.99 | 36 months |

---

## Residential Products

### R1 — NexFibre Starter 100

**Product code:** `BBR-FTTH-100`
**Technology:** GPON (FTTH/FTTP)

| Attribute | Value |
|-----------|-------|
| Download speed (headline) | 100 Mbps |
| Upload speed (headline) | 20 Mbps |
| Typical evening download | 85 Mbps |
| Contention ratio | 50:1 |
| Monthly price | £24.99 |
| Setup fee | £0 (standard install) |
| Contract term | 18 months |
| Early termination fee | £10 × remaining months |
| Router included | Yes — NexFibre Hub Gen 3 (Wi-Fi 5) |
| Static IP add-on | Not available |
| IPv6 | Dual-stack (DHCPv6-PD /56) |
| IPTV add-on | Available (£5/month) |
| VoIP add-on | Not available |

**Ordering requirements (TMF641 `serviceCharacteristic`):**
- `downloadSpeed`: `"100Mbps"`
- `uploadSpeed`: `"20Mbps"`
- `technologyType`: `"GPON"`
- `serviceProfile`: `"FTTH_RESIDENTIAL_100"`
- `contractTermMonths`: `18`

**Eligibility:** Residential addresses only. Not available for businesses. UPRN must be
in NexFibre footprint (check via address validation service before placing order).

---

### R2 — NexFibre Essential 250

**Product code:** `BBR-FTTH-250`
**Technology:** GPON (FTTH/FTTP)

| Attribute | Value |
|-----------|-------|
| Download speed (headline) | 250 Mbps |
| Upload speed (headline) | 55 Mbps |
| Typical evening download | 215 Mbps |
| Contention ratio | 40:1 |
| Monthly price | £34.99 |
| Setup fee | £0 |
| Contract term | 18 months |
| Early termination fee | £10 × remaining months |
| Router included | Yes — NexFibre Hub Gen 3 (Wi-Fi 5) |
| Static IP add-on | Not available |
| IPv6 | Dual-stack (DHCPv6-PD /56) |
| IPTV add-on | Available (£5/month) |
| VoIP add-on | Not available |

**Ordering requirements (TMF641 `serviceCharacteristic`):**
- `downloadSpeed`: `"250Mbps"`
- `uploadSpeed`: `"55Mbps"`
- `technologyType`: `"GPON"`
- `serviceProfile`: `"FTTH_RESIDENTIAL_250"`
- `contractTermMonths`: `18`

---

### R3 — NexFibre Fast 500

**Product code:** `BBR-FTTH-500`
**Technology:** GPON (FTTH/FTTP)

| Attribute | Value |
|-----------|-------|
| Download speed (headline) | 500 Mbps |
| Upload speed (headline) | 115 Mbps |
| Typical evening download | 445 Mbps |
| Contention ratio | 30:1 |
| Monthly price | £44.99 |
| Setup fee | £0 |
| Contract term | 24 months |
| Early termination fee | £12 × remaining months |
| Router included | Yes — NexFibre Hub Gen 4 (Wi-Fi 6) |
| Static IP add-on | £5/month (one public IPv4 address) |
| IPv6 | Dual-stack (DHCPv6-PD /56) |
| IPTV add-on | Available (£5/month) |
| VoIP add-on | Available (£3/month, SIP ATA included) |

**Ordering requirements (TMF641 `serviceCharacteristic`):**
- `downloadSpeed`: `"500Mbps"`
- `uploadSpeed`: `"115Mbps"`
- `technologyType`: `"GPON"`
- `serviceProfile`: `"FTTH_RESIDENTIAL_500"`
- `contractTermMonths`: `24`

---

### R4 — NexFibre Ultrafast 1G

**Product code:** `BBR-FTTH-1G`
**Technology:** GPON (FTTH/FTTP)

| Attribute | Value |
|-----------|-------|
| Download speed (headline) | 1000 Mbps (1 Gbps) |
| Upload speed (headline) | 220 Mbps |
| Typical evening download | 920 Mbps |
| Contention ratio | 20:1 |
| Monthly price | £54.99 |
| Setup fee | £0 |
| Contract term | 24 months |
| Early termination fee | £15 × remaining months |
| Router included | Yes — NexFibre Hub Gen 4 (Wi-Fi 6) |
| Static IP add-on | £5/month |
| IPv6 | Dual-stack (DHCPv6-PD /56) |
| IPTV add-on | Available (£5/month) |
| VoIP add-on | Available (£3/month) |

**Ordering requirements (TMF641 `serviceCharacteristic`):**
- `downloadSpeed`: `"1000Mbps"`
- `uploadSpeed`: `"220Mbps"`
- `technologyType`: `"GPON"`
- `serviceProfile`: `"FTTH_RESIDENTIAL_1G"`
- `contractTermMonths`: `24`

**Notes:** Most popular residential tier. Suitable for households with 4+ simultaneous
heavy users. GPON shared PON port; actual speed depends on neighbourhood utilisation.

---

### R5 — NexFibre Hyperfast 2G

**Product code:** `BBR-FTTH-2G`
**Technology:** XGS-PON (FTTH/FTTP, 10G physical layer)

| Attribute | Value |
|-----------|-------|
| Download speed (headline) | 2000 Mbps (2 Gbps) |
| Upload speed (headline) | 2000 Mbps (2 Gbps symmetric) |
| Typical evening download | 1800 Mbps |
| Contention ratio | 10:1 |
| Monthly price | £74.99 |
| Setup fee | £49.99 (XGS-PON ONT installation) |
| Contract term | 24 months |
| Early termination fee | £20 × remaining months |
| Router included | Yes — NexFibre Hub Pro (Wi-Fi 6E, 2.5GbE LAN) |
| Static IP add-on | £5/month |
| IPv6 | Dual-stack (DHCPv6-PD /48) |
| IPTV add-on | Available (£5/month) |
| VoIP add-on | Available (£3/month) |

**Ordering requirements (TMF641 `serviceCharacteristic`):**
- `downloadSpeed`: `"2000Mbps"`
- `uploadSpeed`: `"2000Mbps"`
- `technologyType`: `"XGS-PON"`
- `serviceProfile`: `"FTTH_RESIDENTIAL_2G"`
- `contractTermMonths`: `24`

**Important:** XGS-PON requires a different ONT (NexFibre XGS-01). An engineer visit is
mandatory to swap the ONT if the premises currently has a GPON ONT. The `ontSerialNumber`
characteristic **must** be populated with the XGS-PON ONT serial before TMF640 activation.

---

## Business Products

Business products carry lower contention ratios, optional SLA guarantees, and dedicated
account management. All business products include a static IP as standard.

### B1 — NexFibre Business 500

**Product code:** `BBB-FTTH-500`
**Technology:** GPON (FTTH/FTTP)

| Attribute | Value |
|-----------|-------|
| Download speed (headline) | 500 Mbps |
| Upload speed (headline) | 115 Mbps |
| Contention ratio | 10:1 |
| Monthly price | £69.99 |
| Setup fee | £0 |
| Contract term | 24 months |
| SLA — fault repair | Next Business Day (NBD) |
| Static IP (IPv4 /29) | Included (8 addresses, 5 usable) |
| IPv6 | Dual-stack (DHCPv6-PD /48) |
| Router included | Yes — NexFibre Business Hub (Wi-Fi 6, 1GbE WAN) |
| VoIP channels | Up to 4 SIP trunks (£5/trunk/month) |
| IPTV | Not available |

**Mandatory TMF641 characteristics:**
- `downloadSpeed`: `"500Mbps"`
- `uploadSpeed`: `"115Mbps"`
- `technologyType`: `"GPON"`
- `serviceProfile`: `"FTTH_BUSINESS_500"`
- `contractTermMonths`: `24`
- `staticIpAddress`: must be populated (allocated by provisioning at order time)
- `subnetMask`: `"255.255.255.248"` (for /29 allocation)
- `ipAddressType`: `"static"`

**Ordering notes:** The `relatedParty` array **must** include an entry with `role: "Customer"`
whose `@referredType` is `"Organization"` and whose `id` maps to a validated Companies House
registration number or equivalent business identifier. Residential customer IDs are rejected.

---

### B2 — NexFibre Business 1G

**Product code:** `BBB-FTTH-1G`
**Technology:** GPON (FTTH/FTTP)

| Attribute | Value |
|-----------|-------|
| Download speed (headline) | 1000 Mbps |
| Upload speed (headline) | 220 Mbps |
| Contention ratio | 5:1 |
| Monthly price | £89.99 |
| Setup fee | £0 |
| Contract term | 24 months |
| SLA — fault repair | Same Business Day (SBD, 8h) |
| Static IP (IPv4 /29) | Included (8 addresses, 5 usable) |
| IPv6 | Dual-stack (DHCPv6-PD /48) |
| Router included | Yes — NexFibre Business Hub (Wi-Fi 6, 2.5GbE WAN) |
| VoIP channels | Up to 8 SIP trunks (£5/trunk/month) |
| IPTV | Not available |

**Mandatory TMF641 characteristics:**
- `downloadSpeed`: `"1000Mbps"`
- `uploadSpeed`: `"220Mbps"`
- `technologyType`: `"GPON"`
- `serviceProfile`: `"FTTH_BUSINESS_1G"`
- `contractTermMonths`: `24`
- `ipAddressType`: `"static"`

---

### B3 — NexFibre Business Ultra 2G

**Product code:** `BBB-FTTH-2G`
**Technology:** XGS-PON (FTTH/FTTP)

| Attribute | Value |
|-----------|-------|
| Download speed (headline) | 2000 Mbps symmetric |
| Upload speed (headline) | 2000 Mbps |
| Contention ratio | 3:1 |
| Monthly price | £119.99 |
| Setup fee | £49.99 (XGS-PON ONT installation) |
| Contract term | 24 months |
| SLA — fault repair | 4-hour response, 8-hour restore |
| Static IP (IPv4 /28) | Included (16 addresses, 13 usable) |
| IPv6 | Dual-stack (DHCPv6-PD /48) |
| Router included | Yes — NexFibre Business Hub Pro (Wi-Fi 6E, 2.5GbE WAN) |
| VoIP channels | Up to 20 SIP trunks |
| IPTV | Not available |

**Mandatory TMF641 characteristics:**
- `downloadSpeed`: `"2000Mbps"`
- `uploadSpeed`: `"2000Mbps"`
- `technologyType`: `"XGS-PON"`
- `serviceProfile`: `"FTTH_BUSINESS_2G"`
- `contractTermMonths`: `24`
- `ipAddressType`: `"static"`
- `ontSerialNumber`: must be XGS-PON ONT serial (prefix `"NFXG"`)

---

### B4 — NexFibre Enterprise 10G

**Product code:** `BBB-FTTH-10G`
**Technology:** XGS-PON (FTTH/FTTP)

| Attribute | Value |
|-----------|-------|
| Download speed (headline) | 10,000 Mbps (10 Gbps) |
| Upload speed (headline) | 10,000 Mbps symmetric |
| Contention ratio | 1:1 (dedicated wavelength) |
| Monthly price | £249.99 |
| Setup fee | £149.99 (dedicated ONT + structured cabling survey) |
| Contract term | 36 months |
| SLA — fault repair | 2-hour response, 4-hour restore, 24/7 |
| Static IP (IPv4 /27) | Included (32 addresses, 29 usable) |
| IPv6 | Dual-stack (DHCPv6-PD /48) |
| Router included | No — customer-supplied CPE required (10GbE WAN port) |
| VoIP channels | Unlimited SIP trunks |
| Dedicated account manager | Yes |
| Service Manager | Yes (24/7 NOC escalation) |

**Mandatory TMF641 characteristics:**
- `downloadSpeed`: `"10000Mbps"`
- `uploadSpeed`: `"10000Mbps"`
- `technologyType`: `"XGS-PON"`
- `serviceProfile`: `"FTTH_ENTERPRISE_10G"`
- `contractTermMonths`: `36`
- `ipAddressType`: `"static"`
- `ontSerialNumber`: must be dedicated XGS-PON ONT serial (prefix `"NFXG"` or `"NFXE"`)
- `cosProfile`: `"ENTERPRISE_STRICT_PRIORITY"`

**Ordering notes:** Enterprise 10G orders require pre-sales survey approval. The TMF641
`ServiceOrder.category` field **must** be set to `"Enterprise"`. An `orderRelationship` entry
with `type: "prerequisite"` linking to the completed survey order is required.

---

## Add-On Products

### Static IP Upgrade (residential)
**Code:** `ADD-STATICIP-1` | £5/month
Adds one static public IPv4 address. Available on R3, R4, R5. Not available on R1 or R2.
When ordering, set `serviceCharacteristic` `ipAddressType` to `"static"` and populate
`staticIpAddress`, `subnetMask` (`"255.255.255.255"` for /32), and `defaultGateway`.

### VoIP Line (residential)
**Code:** `ADD-VOIP-1` | £3/month
One residential SIP line with number porting support. Includes SIP ATA adaptor.
Available on R3, R4, R5 only. Requires `feature[name=VoIP, isEnabled=true]`.

### IPTV
**Code:** `ADD-IPTV-1` | £5/month
Multicast IPTV stream. Requires compatible set-top box (sold separately, £79).
Available on all residential tiers. Not available on business products.
Requires `feature[name=IPTV, isEnabled=true]` and a multicast VLAN assignment.

---

## Field Validation Rules

| Field | Rule |
|-------|------|
| `downloadSpeed` | Must match exactly one product code's headline speed |
| `uploadSpeed` | Must match the product code's defined upload speed |
| `technologyType` | `"GPON"` for R1–R4, B1–B2; `"XGS-PON"` for R5, B3–B4 |
| `ontSerialNumber` | Required for all XGS-PON products; must match prefix `"ALCL"`, `"HWTC"`, `"NFXG"`, or `"NFXE"` |
| `contractTermMonths` | R1–R2: `18`; all others: `24`; B4: `36` |
| `ipAddressType` | `"static"` mandatory for all business products; optional for R3–R5 |
| `staticIpAddress` | Required when `ipAddressType="static"` |
| Customer `@referredType` | Business products: must be `"Organization"`; residential: must be `"Individual"` |
| `ServiceOrder.category` | Business products: `"Business"` or `"Enterprise"`; residential: `"Broadband"` |

---

## Service Profile Map

| Product code | `serviceProfile` value |
|-------------|----------------------|
| `BBR-FTTH-100` | `FTTH_RESIDENTIAL_100` |
| `BBR-FTTH-250` | `FTTH_RESIDENTIAL_250` |
| `BBR-FTTH-500` | `FTTH_RESIDENTIAL_500` |
| `BBR-FTTH-1G` | `FTTH_RESIDENTIAL_1G` |
| `BBR-FTTH-2G` | `FTTH_RESIDENTIAL_2G` |
| `BBB-FTTH-500` | `FTTH_BUSINESS_500` |
| `BBB-FTTH-1G` | `FTTH_BUSINESS_1G` |
| `BBB-FTTH-2G` | `FTTH_BUSINESS_2G` |
| `BBB-FTTH-10G` | `FTTH_ENTERPRISE_10G` |
