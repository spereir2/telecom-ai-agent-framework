SYSTEM_PROMPT = """You are an order-intake assistant for a UK telecommunications operator.
Your job is to convert a customer's natural-language request into a structured ServiceOrder
aligned with TMF641 (Service Ordering Management).

Rules:
- Output ONLY a single JSON object that matches the provided schema. No prose, no markdown fences.
- service_type values: "ftth_residential", "ftth_business", "fttc", "leased_line".
- bandwidth.unit values: "Mbps", "Gbps".
- country_code is ISO-3166-1 alpha-2 (default "GB" if a UK address is given).
- customer_type defaults to "residential" unless the request mentions a business, company, or office.
- If a field is not stated, omit it (do not invent values).
- For UK postcodes, preserve the original spacing and casing as given.
"""

FEW_SHOT_EXAMPLES = [
    {
        "input": "Set me up with 100 down 20 up FTTH at 5 Acacia Avenue, Manchester M14 5RZ. Name's Tom Wright.",
        "output": {
            "customer": {"full_name": "Tom Wright", "customer_type": "residential"},
            "service_address": {
                "line1": "5 Acacia Avenue",
                "city": "Manchester",
                "postcode": "M14 5RZ",
                "country_code": "GB",
            },
            "product": {
                "service_type": "ftth_residential",
                "bandwidth": {"downstream": 100, "upstream": 20, "unit": "Mbps"},
            },
        },
    },
    {
        "input": "Business fibre, 1Gbps symmetric with static IP, 24-month term. Acme Ltd, Office 4, 200 Aldersgate, London EC1A 4HD.",
        "output": {
            "customer": {"full_name": "Acme Ltd", "customer_type": "business"},
            "service_address": {
                "line1": "Office 4",
                "line2": "200 Aldersgate",
                "city": "London",
                "postcode": "EC1A 4HD",
                "country_code": "GB",
            },
            "product": {
                "service_type": "ftth_business",
                "bandwidth": {"downstream": 1, "upstream": 1, "unit": "Gbps"},
                "contract_term_months": 24,
                "static_ip": True,
            },
        },
    },
]


def build_user_prompt(natural_language_order: str) -> str:
    examples = "\n\n".join(
        f"Example input: {ex['input']}\nExample output: {ex['output']}"
        for ex in FEW_SHOT_EXAMPLES
    )
    return (
        f"{examples}\n\n"
        f"Now convert this request:\n{natural_language_order}"
    )
