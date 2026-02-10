# app.py

import streamlit as st
from geofence_checker import check_address
import re
import pandas as pd

st.title("Geofencing Safety Checker - Copy & Paste Input")

st.write("""
Paste multiple addresses below in the following format (one per line):

`Business Name - Address, City, State ZIP`

Example:  
The Oxford Apartments - 6009 Oxon Hill Rd Oxon Hill, MD 20745
""")

# Text input box
addresses_text = st.text_area("Paste addresses here", height=300)

if st.button("Check Safety"):
    if not addresses_text.strip():
        st.warning("Please paste at least one address")
    else:
        results = []
        # Split lines
        lines = addresses_text.strip().split("\n")
        
        for line in lines:
            # Attempt to split name and address by ' - '
            if " - " in line:
                name_part, address_part = line.split(" - ", 1)
            else:
                # If no dash, just use entire line as address
                name_part = line
                address_part = line
            
            # Extract state from the address using regex (last 2 uppercase letters)
            state_match = re.search(r",\s*([A-Z]{2})\s*\d{5}$", address_part)
            if state_match:
                state = state_match.group(1)
            else:
                state = "Unknown"
            
            # Use last word in address as location_type placeholder (can customize)
            location_type = "Unknown"  # You can add logic to detect type if needed
            
            check = check_address(name_part, address_part, state, location_type)
            results.append(check)
        
        # Display results
        df = pd.DataFrame(results)
        st.write(df)
        
        # Option to download
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download results as CSV",
            data=csv,
            file_name="geofence_results.csv",
            mime="text/csv"
        )
