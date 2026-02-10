# geofence_checker.py

# States where medical geofencing is restricted
restricted_states_medical = ["NV", "NY", "MA", "WA", "MD", "OR", "CA"]

# General restricted locations
restricted_locations = [
    "Daycare", "Childcare", "Elementary School", "Middle School",
    "Children's Hospital", "Playground", "Activity Center", "Museum",
    "Individual Home", "Nursing Home", "Cultural Center", 
    "Ethnic Center", "Place of Worship", "Homeless Shelter", 
    "Rehabilitation Center"
]

# MODPA Maryland restrictions
modpa_states = ["MD"]
modpa_restricted_facilities = ["Mental Health Facility", "Sexual Health Facility", "Reproductive Health Facility"]

# Military bases
military_bases = ["Military Base"]

# High school parking restricted states
high_school_parking_restricted_states = ["MD"]

# Keywords to detect sensitive locations
sensitive_keywords = [
    "daycare", "childcare", "elementary", "middle school", "high school",
    "children", "hospital", "playground", "activity center",
    "museum", "nursing home", "cultural", "ethnic",
    "place of worship", "homeless shelter", "rehab",
    "ymca", "medical center", "assisted living"
]

def check_address(name, address, state):
    reasons = []
    safe = True
    location_type_detected = []

    combined_text = f"{name} {address}".lower()

    # Check for YMCA first - always NOT SAFE
    if "ymca" in combined_text:
        safe = False
        reasons.append("YMCA locations are always NOT SAFE")
        location_type_detected.append("YMCA")

    # Check sensitive keywords
    for keyword in sensitive_keywords:
        if keyword in combined_text and keyword.lower() != "ymca":
            location_type_detected.append(keyword.title())
            # Daycares, schools, children hospitals
            if keyword.lower() in ["daycare", "childcare", "elementary", "middle school", "children's hospital"]:
                safe = False
                reasons.append(f"Targeting {keyword.title()} is not allowed")
            # High school parking special rules
            if keyword.lower() == "high school" and state in high_school_parking_restricted_states:
                safe = False
                reasons.append(f"High school parking lots are not allowed in {state}")
            # Medical centers in restricted states
            if keyword.lower() in ["hospital", "medical center"] and state in restricted_states_medical:
                safe = False
                reasons.append(f"Cannot geofence medical location in {state}")
            # Nursing homes / assisted living
            if keyword.lower() in ["nursing home", "assisted living"]:
                safe = False
                reasons.append(f"Targeting {keyword.title()} is not allowed")
            # Place of worship, cultural, rehab, etc.
            if keyword.lower() in ["place of worship", "cultural", "ethnic", "homeless shelter", "rehab", "activity center", "museum", "playground"]:
                safe = False
                reasons.append(f"Targeting {keyword.title()} is not allowed")

    # Military base
    for base in military_bases:
        if base.lower() in combined_text:
            reasons.append("Only public entrances are allowed for military bases")

    # MODPA Maryland restriction
    if state in modpa_states:
        for facility in modpa_restricted_facilities:
            if facility.lower() in combined_text:
                safe = False
                reasons.append(f"MODPA: Geofencing within 1750ft of {facility} is prohibited")

    result = "SAFE" if safe else "NOT SAFE"

    return {
        "name": name,
        "address": address,
        "state": state,
        "result": result,
        "reasons": reasons,
        "detected_types": ", ".join(location_type_detected) if location_type_detected else "Unknown"
    }
