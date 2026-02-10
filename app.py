# app.py

import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Geofencing Safety Checker", layout="wide")

st.title("Geofencing Safety Checker")
st.write("""
Enter up to 50 business locations below.  
The system will detect sensitive locations like YMCA, schools, hospitals, nursing homes, religious organizations, and more.
""")

num_rows = 50

# ----------------------
# Sensitive categories and rules
# ----------------------
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

restricted_states_medical = ["NV", "NY", "MA", "WA", "MD", "OR", "CA"]
high_school_parking_restricted_states = ["MD"]
modpa_states = ["MD"]
modpa_restricted_facilities = ["Mental Health Facility", "Sexual Health Facility", "Reproductive Health Facility"]
military_bases = ["Military Base"]

# ----------------------
# Helper function
# ----------------------
def check_address(name, address, state):
    reasons = []
    detected_categories = []
    safe = True
    combined_text = f"{name} {address}".lower()

    # Check sensitive categories
    for category, keywords in sensitive_categories.items():
        for keyword in keywords:
            if keyword.lower() in combined_text:
                detected_categories.append(category)
                safe = False
                reasons.append(f"Targeting {category} is not allowed")
                break

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

# ----------------------
# Session state for table
# ----------------------
if 'input_data' not in st.session_state:
    st.session_state['input_data'] = pd.DataFrame({
        'Business Name': ['']*num_rows,
        'Address': ['']*num_rows
    })

# ----------------------
# Reset button
# ----------------------
if st.button("Reset Table"):
    st.session_state['input_data'] = pd.DataFrame({
        'Business Name': ['']*num_rows,
        'Address': ['']*num_rows
    })
    st.success("Table has been reset!")

# ----------------------
# Editable table
# ----------------------
input_df = st.data_editor(
    st.session_state['input_data'],
    num_rows=num_rows,
    use_container_width=True
)

# ----------------------
# Check Safety button
# ----------------------
if st.button("Check Safety"):
    results = []
    for _, row in input_df.iterrows():
        name = str(row['Business Name']).strip()
        address = str(row['Address']).strip()
        if not name and not address:
            continue

        # Simple state extraction (last 2 uppercase letters before ZIP)
        state_match = re.search(r",\s*([A-Z]{2})\s*\d{5}$", address)
        state = state_match.group(1) if state_match else "Unknown"

        check = check_address(name, address, state)
        results.append(check)

    result_df = pd.DataFrame(results)
    st.write(result_df)

    # CSV download
    csv = result_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Results as CSV",
        data=csv,
        file_name="geofence_results.csv",
        mime="text/csv"
    )
