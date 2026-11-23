"""Who can sign in. In real life this list comes from each client's own login system (SSO)."""

USERS = {
    "anand@northstar":  {"client": "northstar", "role": "counsellor", "centre": "Tech Park"},
    "divya@northstar":  {"client": "northstar", "role": "counsellor", "centre": "City"},
    "kevin@northstar":  {"client": "northstar", "role": "manager",    "centre": None},
    "priya@meridian":   {"client": "meridian",  "role": "counsellor", "centre": "Centre 4"},
    "rahul@meridian":   {"client": "meridian",  "role": "counsellor", "centre": "Centre 9"},
    "sanjay@meridian":  {"client": "meridian",  "role": "manager",    "centre": None},
}
