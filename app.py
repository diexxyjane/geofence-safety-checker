# app.py

import streamlit as st
import pandas as pd
import re
from geofence_checker import check_address

st.title("Geofencing Safety Checker")

st.write("""
Enter up to 50 business locations below. You can leave the location_type empty; the system will try to detect sensitive locations automatically.
""")

# Create a blank DataFrame with 50 rows
num_rows = 50
if 'input_data' not in st.session_state:
    st.session_state['input_data'] = pd.DataFrame({
        'Business Name': ['']*num_rows,
        'Address': ['']*num_rows
    })

# Editable table for input
input_df = st.experimental_data_editor(st.session_state['input_data'], num_rows=num_rows, use_container_width=True)

if st.button("Check Safety"):
    results = []
    for _, row in input_df.iterrows():
        name = str(row['Business Name']).strip()
        address = str(row['Address']).strip()

        if not name and not address:
            continue  # skip empty rows

        # Try to extract state (last 2 uppercase letters before ZIP)
        state_match = re.search(r",\s*([A-Z]{2})\s*\d{5}$", address)
        state = state_match.group(1) if state_match else "Unknown"

        # Detect location_type automatically based on name keywords
        sensitive_keywords = [
            "daycare", "elementary", "middle school", "high school",
            "children", "hospital", "playground", "activity center",
            "museum", "nursing home", "cultural", "ethnic",
            "place of worship", "homeless shelter", "rehab",
            "ymca", "medical center", "assisted living"
        ]
        location_type = "Unknown"
        for keyword in sensitive_keywords:
            if keyword.lower() in name.lower() or keyword.lower() in address.lower():
                location_type = keyword.title()
                break

        # Run safety check
        check = check_address(name, address, state, location_type)
        results.append(check)

    # Show results
    result_df = pd.DataFrame(results)
    st.write(result_df)

    # Download results
    csv = result_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Results as CSV",
        data=csv,
        file_name="geofence_results.csv",
        mime="text/csv"
    )
