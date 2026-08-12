

DEPOSIT_FIELDS = {
    "application_date": {"x": 0.8118, "y": 0.0855, "w": 0.1188, "h": 0.0255, "type": "date"},
    "deposit_type": {
        "type": "checkbox_group",
        "options": {
            "Fixed Deposit":     {"x": 0.1853, "y": 0.1545, "w": 0.0147, "h": 0.0114},
            "Savings Deposit":   {"x": 0.1841, "y": 0.1927, "w": 0.0159, "h": 0.0127},
            "Recurring Deposit": {"x": 0.3994, "y": 0.1927, "w": 0.0159, "h": 0.0114},
        },
    },
    "deposit_amount_figures": {"x": 0.5418, "y": 0.1405, "w": 0.27,   "h": 0.0227, "type": "text"},
    "deposit_amount_words":   {"x": 0.5365, "y": 0.1659, "w": 0.2771, "h": 0.0141, "type": "text"},
    "deposit_term":           {"x": 0.83,   "y": 0.1414, "w": 0.0906, "h": 0.0564, "type": "text"},
    "term_unit":              {"x": 0.8329, "y": 0.2027, "w": 0.0859, "h": 0.0218, "type": "text"},

    "payment_mode": {
        "type": "checkbox_group",
        "options": {
            "Cheque": {"x": 0.0794, "y": 0.2995, "w": 0.0135, "h": 0.0118},
            "Draft":  {"x": 0.0782, "y": 0.3214, "w": 0.0182, "h": 0.0141},
            "Cash":   {"x": 0.0771, "y": 0.3468, "w": 0.0206, "h": 0.0141},
        },
    },
    "cheque_or_draft_number": {"x": 0.1894, "y": 0.3127, "w": 0.1659, "h": 0.0177, "type": "text"},
    "bank_name":              {"x": 0.3588, "y": 0.315,  "w": 0.1594, "h": 0.0205, "type": "text"},
    "remittance_date":        {"x": 0.2818, "y": 0.3391, "w": 0.0982, "h": 0.0268, "type": "date"},
    "remittance_place":       {"x": 0.4206, "y": 0.3405, "w": 0.1041, "h": 0.0255, "type": "text"},
    "renewal_indicator":      {"x": 0.0641, "y": 0.3777, "w": 0.1318, "h": 0.0205, "type": "text"},
    "existing_fd_rd_number":  {"x": 0.2624, "y": 0.3723, "w": 0.0953, "h": 0.0245, "type": "text"},
    "maturity_date":          {"x": 0.4476, "y": 0.37,   "w": 0.0747, "h": 0.0141, "type": "date"},
    "maturity_amount":        {"x": 0.4476, "y": 0.3864, "w": 0.0782, "h": 0.0141, "type": "text"},

    "first_depositor_name":      {"x": 0.1594, "y": 0.4132, "w": 0.2176, "h": 0.0191, "type": "text"},
    "first_depositor_age":       {"x": 0.4541, "y": 0.4082, "w": 0.0694, "h": 0.0227, "type": "text"},
    "first_depositor_guardian":  {"x": 0.2047, "y": 0.4477, "w": 0.3135, "h": 0.0164, "type": "text"},
    "first_depositor_signature": {"x": 0.2194, "y": 0.76,   "w": 0.3065, "h": 0.0373, "type": "signature"},

    "second_depositor_name":      {"x": 0.1629, "y": 0.4836, "w": 0.2376, "h": 0.015,  "type": "text"},
    "second_depositor_age":       {"x": 0.4488, "y": 0.4759, "w": 0.0759, "h": 0.0214, "type": "text"},
    "second_depositor_guardian":  {"x": 0.2065, "y": 0.5141, "w": 0.3029, "h": 0.0155, "type": "text"},
    "second_depositor_signature": {"x": 0.2206, "y": 0.8036, "w": 0.2988, "h": 0.0355, "type": "signature"},

    "nominee_name":         {"x": 0.1853, "y": 0.5332, "w": 0.1618, "h": 0.0177, "type": "text"},
    "nominee_relationship": {"x": 0.1853, "y": 0.555,  "w": 0.1935, "h": 0.0164, "type": "text"},
    "nominee_age":          {"x": 0.4582, "y": 0.5382, "w": 0.0676, "h": 0.0373, "type": "text"},

    "address":       {"x": 0.5429, "y": 0.2973, "w": 0.3759, "h": 0.0255, "type": "text"},
    "pincode":        {"x": 0.7441, "y": 0.375,  "w": 0.1829, "h": 0.0177, "type": "text"},
    "phone_number":    {"x": 0.6188, "y": 0.3968, "w": 0.2882, "h": 0.0255, "type": "text"},
    "occupation":       {"x": 0.6318, "y": 0.4223, "w": 0.2953, "h": 0.0218, "type": "text"},

    "share_number":      {"x": 0.0794, "y": 0.5945, "w": 0.1635, "h": 0.0177, "type": "text"},
    "folio_number":       {"x": 0.0812, "y": 0.6314, "w": 0.1671, "h": 0.0205, "type": "text"},

    "account_type": {
        "type": "checkbox_group",
        "options": {
            "Sole/First Depositor": {"x": 0.4818, "y": 0.6059, "w": 0.0441, "h": 0.0241},
            "Jointly":               {"x": 0.30,   "y": 0.77,   "w": 0.03,   "h": 0.02},  # NOT re-calibrated — needs a redo, see note above
            "Either or Survivor":    {"x": 0.4188, "y": 0.6286, "w": 0.0435, "h": 0.0205},
            "Anyone or Survivor":    {"x": 0.4424, "y": 0.6491, "w": 0.0565, "h": 0.0232},
        },
    },

    "interest_option": {
        "type": "checkbox_group",
        "options": {
            "Monthly":     {"x": 0.5629, "y": 0.4936, "w": 0.0182, "h": 0.01},
            "Quarterly":   {"x": 0.77,   "y": 0.4936, "w": 0.0147, "h": 0.0155},
            "Half-Yearly": {"x": 0.5665, "y": 0.5177, "w": 0.0118, "h": 0.0091},
            "Yearly":      {"x": 0.7665, "y": 0.5155, "w": 0.0141, "h": 0.01},
        },
    },
    "tax_deducted": {
        "type": "checkbox_group",
        "options": {
            "Yes":            {"x": 0.5665, "y": 0.5691, "w": 0.0159, "h": 0.015},
            "No":              {"x": 0.7688, "y": 0.5714, "w": 0.0171, "h": 0.0091},
            "Not Applicable":   {"x": 0.5653, "y": 0.5945, "w": 0.0141, "h": 0.0114},
        },
    },
    "payment_of_interest": {
        "type": "checkbox_group",
        "options": {
            "Collect Cash":               {"x": 0.5665, "y": 0.6468, "w": 0.0159, "h": 0.0114},
            "Collect Post-Dated Cheque":   {"x": 0.5653, "y": 0.6682, "w": 0.0206, "h": 0.0141},
            "Credit to SBF/Other Account": {"x": 0.7247, "y": 0.685,  "w": 0.2088, "h": 0.0227},
        },
    },


    "account_number":     {"x": 0.10, "y": 0.90, "w": 0.35, "h": 0.03, "type": "text"},

    "introducer_name":    {"x": 0.6629, "y": 0.7423, "w": 0.2641, "h": 0.0218, "type": "text"},
    "introducer_address": {"x": 0.5641, "y": 0.7768, "w": 0.3729, "h": 0.0227, "type": "text"},
}

SHARE_FIELDS = {
    "application_date": {"x": 0.7676, "y": 0.12,   "w": 0.1906, "h": 0.0418, "type": "date"},
    "share_number":     {"x": 0.6735, "y": 0.1823, "w": 0.2965, "h": 0.0627, "type": "text"},
    "applicant_name":   {"x": 0.2165, "y": 0.3559, "w": 0.6959, "h": 0.0382, "type": "text"},
    "age":              {"x": 0.1435, "y": 0.3927, "w": 0.3524, "h": 0.0318, "type": "text"},
    "nationality":      {"x": 0.6241, "y": 0.4018, "w": 0.0771, "h": 0.0395, "type": "text"},
    "father_or_husband_name": {"x": 0.3394, "y": 0.4286, "w": 0.6318, "h": 0.0345, "type": "text"},
    "door_number":      {"x": 0.3288, "y": 0.4618, "w": 0.4818, "h": 0.0227, "type": "text"},
    "street_name":      {"x": 0.3288, "y": 0.4845, "w": 0.6571, "h": 0.0268, "type": "text"},
    "postal_address":   {"x": 0.2518, "y": 0.5241, "w": 0.7224, "h": 0.0536, "type": "text"},
    "nominee_name":     {"x": 0.3318, "y": 0.5918, "w": 0.56,   "h": 0.0486, "type": "text"},
    "nominee_age":      {"x": 0.3265, "y": 0.6609, "w": 0.1106, "h": 0.0395, "type": "text"},
    "nominee_relationship": {"x": 0.4541, "y": 0.6609, "w": 0.3853, "h": 0.0459, "type": "text"},
    "witness_1":        {"x": 0.1229, "y": 0.7641, "w": 0.3653, "h": 0.0268, "type": "text"},
    "witness_2":        {"x": 0.1241, "y": 0.7895, "w": 0.3824, "h": 0.0345, "type": "text"},
    "applicant_signature": {"x": 0.6735, "y": 0.7464, "w": 0.3135, "h": 0.075,  "type": "signature"},
    "application_received_date": {"x": 0.3253, "y": 0.865,  "w": 0.2412, "h": 0.0382, "type": "date"},
    "amount_received":  {"x": 0.3812, "y": 0.9018, "w": 0.2818, "h": 0.0305, "type": "text"},

    "payment_mode": {
        "type": "checkbox_group",
        "options": {
            "Cash":   {"x": 0.2065, "y": 0.9005, "w": 0.0588, "h": 0.0368},
            "Cheque": {"x": 0.2676, "y": 0.9032, "w": 0.0759, "h": 0.0382},
        },
    },

    "clerk_approval":       {"x": 0.0994, "y": 0.935,  "w": 0.2306, "h": 0.0955, "type": "signature"},
    "cashier_approval":     {"x": 0.3747, "y": 0.9427, "w": 0.2753, "h": 0.0686, "type": "signature"},
    "secretary_md_approval":{"x": 0.7218, "y": 0.9209, "w": 0.2888, "h": 0.0968, "type": "signature"},
}

FORM_TEMPLATES = {
    "deposit": {
        "heading_keywords": ["DEPOSIT APPLICATION FORM", "DEPOSIT APPLICATION"],
        "reference_image": "data/templates/deposit_blank.png",
        "fields": DEPOSIT_FIELDS,
        "db_table": "deposit_applications",
    },
    "share": {
        "heading_keywords": ["APPLICATION FOR SHARE", "SHARE APPLICATION"],
        "reference_image": "data/templates/share_blank.png",
        "fields": SHARE_FIELDS,
        "db_table": "share_applications",
    },
}

KEY_FIELDS = {
    "deposit": [
        "application_date", "deposit_type", "deposit_amount_figures",
        "first_depositor_name", "phone_number", "address", "pincode",
        "nominee_name", "account_number", "maturity_date",
    ],
    "share": [
        "application_date", "share_number", "applicant_name", "age",
        "father_or_husband_name", "postal_address", "nominee_name",
        "amount_received", "payment_mode",
    ],
}
