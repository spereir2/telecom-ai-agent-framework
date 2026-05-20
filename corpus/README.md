# Corpus — Source Inventory and Licensing

This directory contains all source material used by the M2 RAG knowledge base.
Every file listed here is checked into the repository and ingested by `make ingest`.

> **Licensing summary:** TMF Open API excerpts are derived from Apache-2.0 source.
> Synthesised product catalogue and SOP documents are original works under MIT.
> See per-file entries below for exact attribution.

---

## File Inventory

### `tmf/tmf641-service-ordering.md`

| Attribute | Value |
|-----------|-------|
| **Content** | API overview, resource schemas, field definitions, state machine, and a worked JSON example for TMF641 v4.1.0 (Service Ordering Management) |
| **Source** | [https://github.com/tmforum-apis/TMF641_ServiceOrder](https://github.com/tmforum-apis/TMF641_ServiceOrder) |
| **Upstream file** | `TMF641-ServiceOrdering-v4.1.0.swagger.json` |
| **Upstream commit** | `4dd2866c` (2026-04-28) |
| **Licence** | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| **Copyright** | Copyright © TM Forum 2020. All Rights Reserved. |
| **Attribution note** | Field descriptions and API overview reproduced from the TMF641 OpenAPI specification published by TM Forum under Apache-2.0. The excerpt format (markdown tables, worked example) is original to this project. Attribution header included at top of file and in closing footer. |

---

### `tmf/tmf640-service-activation.md`

| Attribute | Value |
|-----------|-------|
| **Content** | API overview, resource schemas, field definitions, activation state machine, Monitor pattern, and worked JSON examples for TMF640 v4.0.0 (Service Activation and Configuration) |
| **Source** | [https://github.com/tmforum-apis/TMF640_ActivationConfiguration](https://github.com/tmforum-apis/TMF640_ActivationConfiguration) |
| **Upstream file** | `TMF640-ServiceActivation-v4.0.0.swagger.json` |
| **Upstream commit** | `34ffd1ae` (2026-04-28) |
| **Licence** | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| **Copyright** | Copyright © TM Forum 2019. All Rights Reserved. |
| **Attribution note** | Same as TMF641 above. Attribution headers present in the file. |

---

### `product-catalog/broadband-products.md`

| Attribute | Value |
|-----------|-------|
| **Content** | Synthesised product catalogue for a fictional ISP ("NexFibre UK") with 5 residential tiers (R1–R5) and 4 business tiers (B1–B4), covering GPON and XGS-PON products. Includes speeds, prices, mandatory TMF641 `serviceCharacteristic` values, and field validation rules. |
| **Source** | Original work — no third-party content |
| **Licence** | [MIT](../LICENSE) |
| **Copyright** | © 2026 telecom-ai-agent-framework contributors |
| **Notes** | All product names, codes, and prices are fictional. No real ISP data. Designed to test the RAG system's ability to retrieve product-specific provisioning requirements. |

---

### `sops/new-ftth-residential.md`

| Attribute | Value |
|-----------|-------|
| **Content** | SOP-PROV-001 — End-to-end activation process for new residential FTTH services. Covers order creation (TMF641), resource assessment, engineer appointments, TMF640 activation, service enablement, and customer notification. Includes error scenarios and SLA targets. |
| **Source** | Original work — no third-party content |
| **Licence** | [MIT](../LICENSE) |
| **Copyright** | © 2026 telecom-ai-agent-framework contributors |
| **Notes** | Fictional operational procedure for "NexFibre UK". Designed to test retrieval of multi-step procedural content and error-handling guidance. |

---

### `sops/new-ftth-business.md`

| Attribute | Value |
|-----------|-------|
| **Content** | SOP-PROV-002 — Business FTTH activation, covering differences from residential (mandatory static IP, business customer identity validation, lower contention VLANs, SLA tiers, Enterprise 10G specifics). |
| **Source** | Original work — no third-party content |
| **Licence** | [MIT](../LICENSE) |
| **Copyright** | © 2026 telecom-ai-agent-framework contributors |
| **Notes** | Supplements SOP-PROV-001. Specifically tests retrieval of business-vs-residential distinction and mandatory field differences. |

---

### `sops/address-validation.md`

| Attribute | Value |
|-----------|-------|
| **Content** | SOP-PROV-003 — Address and coverage validation before order submission. Covers UPRN lookup, footprint status, technology availability, ONT slot checks, address object compilation for TMF641/TMF640, existing service checks, and edge cases (flats, new-builds). |
| **Source** | Original work — no third-party content |
| **Licence** | [MIT](../LICENSE) |
| **Copyright** | © 2026 telecom-ai-agent-framework contributors |
| **Notes** | Tests retrieval of pre-order validation steps and field population rules (especially `uprn` requirement). |

---

## Licence Verification Notes

### TMF Open API specs (Apache-2.0)

Both TMF641 and TMF640 OpenAPI specifications are published by TM Forum on GitHub at
`https://github.com/tmforum-apis/` under the Apache License 2.0 (confirmed via `LICENSE`
file in each repository). The Apache-2.0 licence permits reproduction and distribution
with attribution, which this corpus provides via the copyright headers in each TMF excerpt
file and the entries above.

**Redistribution conditions met:**
- Copyright notice preserved in each excerpt file (top attribution block + closing footer).
- Repository URL and commit hash recorded above and in each file.
- No modifications claimed as original — the excerpt clearly states field descriptions
  are reproduced from the upstream OpenAPI specification.

**Note:** The TMF Forum also publishes separate specification *documents* (PDF/Word) under
a TM Forum RAND licence which does **not** permit free redistribution. These documents are
**not** included in this corpus. Only the Apache-2.0 licensed OpenAPI specification files
(`*.swagger.json`) were used as the source material.

---

## Corpus Statistics

| File | Approx. tokens | Primary entities |
|------|---------------|-----------------|
| `tmf/tmf641-service-ordering.md` | ~2 800 | ServiceOrder, ServiceOrderItem, Service, ServiceCharacteristic, enums |
| `tmf/tmf640-service-activation.md` | ~2 600 | Service, Monitor, Feature, Place, activation state machine |
| `product-catalog/broadband-products.md` | ~2 400 | 9 product tiers, add-ons, field validation rules, service profile map |
| `sops/new-ftth-residential.md` | ~2 200 | 6 activation steps, error table, SLA targets |
| `sops/new-ftth-business.md` | ~2 500 | 7 steps + Enterprise 10G addendum, business error codes |
| `sops/address-validation.md` | ~2 300 | UPRN lookup, footprint check, address compilation, edge cases |
| **Total** | **~14 800** | |

Token estimates are approximate (GPT-2 tokeniser). Actual chunk count depends on the
chunker configuration (`~512 tokens / 64 token overlap` per M2 spec).
