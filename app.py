# app.py

import streamlit as st
import pandas as pd
import re
from geofence_checker import check_address

st.title("Geofencing Safety Checker")
st.write("Enter up to 50 business locations. Leave location_type empty; system will auto-detect sensitive locations.")

num_rows = 50
if 'input_data' not in st.session_state:
    st.session_state['input_data'] = pd.DataFrame({
        'Business Name': ['']*num_rows,
        'Address': ['']*num_rows
    })

# Use the correct Data Editor
input_df = st.data_editor(
    st.session_state['input_data'], 
    num_rows=num_rows, 
    use_container_width=True
)

if st.button("Check Safety"):
    results = []
    for _, row in input_df.iterrows():
        name = str(row['Business Name']).strip()
        address = str(row['Address']).strip()
        if not name and not address:
            continue

        # Extract state
        state_match = re.search(r",\s*([A-Z]{2})\s*\d{5}$", address)
        state = state_match.group(1) if state_match else "Unknown"

        # Auto detect sensitive location
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

        check = check_address(name, address, state, location_type)
        results.append(check)

    result_df = pd.DataFrame(results)
    st.write(result_df)

    csv = result_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Results as CSV",
        data=csv,
        file_name="geofence_results.csv",
        mime="text/csv"
    )

