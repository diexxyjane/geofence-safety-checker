# app.py

import streamlit as st
import pandas as pd
import re
from geofence_checker import check_address

st.title("Geofencing Safety Checker")
st.write("""
Enter up to 50 business locations below.  
The system will automatically detect sensitive locations like YMCA, schools, hospitals, and more.
""")

num_rows = 50
if 'input_data' not in st.session_state:
    st.session_state['input_data'] = pd.DataFrame({
        'Business Name': ['']*num_rows,
        'Address': ['']*num_rows
    })

# Editable table
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

        # Flexible state detection (2 uppercase letters near end of line)
        state_match = re.search(r",\s*([A-Z]{2})\s*\d{5}$", address)
        state = state_match.group(1) if state_match else "Unknown"

        # Run safety check
        check = check_address(name, address, state)
        results.append(check)

    result_df = pd.DataFrame(results)
    st.write(result_df)

    # Download CSV
    csv = result_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Results as CSV",
        data=csv,
        file_name="geofence_results.csv",
        mime="text/csv"
    )
