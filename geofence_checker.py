# geofence_checker.py

# Restricted states for medical geofencing
restricted_states_medical = ["NV", "NY", "MA", "WA", "MD", "OR", "CA"]

# High school parking restricted states
high_school_parking_restricted_states = ["MD"]

# MODPA Maryland restricted facilities
modpa_states = ["MD"]
modpa_restricted_facilities = ["Mental Health Facility", "Sexual Health Facility", "Reproductive Health Facility"]

# Military bases
military_bases = ["Military Base"]

# Broad sensitive categories and example keywords
sensitive_categories = {
    "Religious Organization": [
        "church", "temple", "mosque", "synagogue", "house of worship",
        "chapel", "religious", "faith center", "spiritual center", "ymca"
    ],
    "School / Childcare": [
        "daycare", "childcare", "preschool", "elementary school", "middle school", "high school", "children"
    ],
    "Medical": [
        "hospital", "medical center", "clinic", "children's hospital", "health facility"
    ],
    "Nursing Home / Assisted Living": [
        "nursing home", "assisted living"
    ],
    "Cultural / Ethnic / Activity Center": [
        "museum", "cultural center", "ethnic center", "activity center", "playground"
    ],
    "Homeless / Rehab": [
        "homeless shelter", "rehab", "rehabilitation center"
    ]
}

def check_address(name, address, state):
    """
    Checks if an address is safe for geofencing based on broad sensitive categories.
    Returns a dictionary with SAFE/NOT SAFE, reasons, and detected categories.
    """
    reasons = []
    detected_categories = []
    safe = True
    combined_text = f"{name} {address}".lower()

    # Check each sensitive category
    for category, keywords in sensitive_categories.items():
        for keyword in keywords:
            if keyword.lower() in combined_text:
                detected_categories.append(category)
                safe = False  # Mark as NOT SAFE for all sensitive categories
                reasons.append(f"Targeting {category} is not allowed")
                break  # Only need to match one keyword per category

    # Military base special case
    for base in military_bases:
        if base.lower() in combined_text:
            reasons.append("Only public entrances are allowed for military bases")

    # High school parking rule
    if "high school" in combined_text and state in high_school_parking_restricted_states:
        safe = False
        reasons.append(f"High school parking lots are not allowed in {state}")

    # Medical restricted states
    if any(kw in combined_text for kw in sensitive_categories["Medical"]) and state in restricted_states_medical:
        safe = False
        reasons.append(f"Cannot geofence medical location in {state}")

    # MODPA restrictions
    if state in modpa_states:
        for facility in modpa_restricted_facilities:
            if facility.lower() in combined_text:
                safe = False
                reasons.append(f"MODPA: Geofencing within 1750ft of {facility} is prohibited")

    result = "SAFE" if safe else "NOT SAFE"
    detected_str = ", ".join(detected_categories) if detected_categories else "None"

    return {
        "name": name,
        "address": address,
        "state": state,
        "result": result,
        "reasons": reasons,
        "detected_categories": detected_str
    }
