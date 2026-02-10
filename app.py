# app.py

import streamlit as st
import pandas as pd
from geofence_checker import check_address

st.title("Geofencing Safety Checker")

st.write("""
Upload a CSV file with these columns: **name, address, state, location_type**.  
The app will tell you if each location is SAFE to target and provide reasons if NOT SAFE.
""")

uploaded_file = st.file_uploader("Upload CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    results = []
    for _, row in df.iterrows():
        check = check_address(row['name'], row['address'], row['state'], row['location_type'])
        results.append(check)
    
    result_df = pd.DataFrame(results)
    st.write(result_df)
    
    # Option to download results
    csv = result_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download results as CSV",
        data=csv,
        file_name='geofence_results.csv',
        mime='text/csv'
    )
