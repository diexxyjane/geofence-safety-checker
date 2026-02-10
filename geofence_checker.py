# geofence_checker.py

restricted_states_medical = ["NV", "NY", "MA", "WA", "MD", "OR", "CA"]

restricted_locations = [
    "Daycare", "Elementary School", "Middle School",
    "Children's Hospital", "Playground", "Activity Center", "Museum",
    "Individual Home", "Nursing Home", "Cultural Center", 
    "Ethnic Center", "Place of Worship", "Homeless Shelter", 
    "Rehabilitation Center"
]

modpa_restricted_distance = 1750
modpa_states = ["MD"]
military_bases = ["Military Base"]
high_school_parking_restricted_states = ["MD"]

def check_address(name, address, state, location_type):
    reasons = []
    safe = True
    
    if location_type.lower() in ["hospital", "medical center"] and state in restricted_states_medical:
        safe = False
        reasons.append(f"Cannot geofence medical location in {state}")
    
    for loc in restricted_locations:
        if loc.lower() in location_type.lower() or loc.lower() in name.lower():
            safe = False
            reasons.append(f"Targeting {loc} is not allowed")
    
    if "high school" in location_type.lower() or "high school" in name.lower():
        if state in high_school_parking_restricted_states:
            safe = False
            reasons.append(f"High school parking lots are not allowed in {state}")
    
    if any(base.lower() in location_type.lower() or base.lower() in name.lower() for base in military_bases):
        reasons.append("Only public entrances are allowed for military bases")
    
    if state in modpa_states and location_type.lower() in ["mental health facility", "sexual health facility", "reproductive health facility"]:
        safe = False
        reasons.append("MODPA: Geofencing within 1750ft of this facility is prohibited")
    
    result = "SAFE" if safe else "NOT SAFE"
    return {"name": name, "address": address, "state": state, "result": result, "reasons": reasons}
