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

    # Check sensitive catego
