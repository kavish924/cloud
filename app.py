import streamlit as st
import pandas as pd
import os
import datetime
from database import (
    create_tables, 
    add_scan_report, 
    get_all_scan_reports, 
    search_scan_reports
)
from storage import save_uploaded_file, get_file_url

# ---------------------------
# STREAMLIT UI
# ---------------------------
def main():
    st.set_page_config(
        page_title="Hospital Scan Report Portal",
        page_icon="🩻",
        layout="wide"
    )
    
    with st.sidebar:
        st.title("🩻 Hospital Scan Portal")
        st.markdown("---")
        
        menu = ["Register Scan Report", "View All Reports", "Search by Patient"]
        choice = st.selectbox("Navigation", menu)
        
        st.markdown("---")
        st.markdown("Made with ❤️ by Medical Imaging Team")
    
    # Ensure tables exist
    create_tables()

    if choice == "Register Scan Report":
        display_register_form()

    elif choice == "View All Reports":
        display_all_reports()

    elif choice == "Search by Patient":
        display_search_interface()

def display_register_form():
    st.header("Register New Scan Report")
    st.markdown("Enter the patient and scan details below")
    
    col1, col2 = st.columns(2)
    
    with st.form("scan_form", clear_on_submit=True):
        with col1:
            patient_name = st.text_input("Patient Name")
            age = st.number_input("Age", min_value=0, max_value=120)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            scan_type = st.selectbox("Scan Type", ["X-ray", "MRI", "CT Scan", "Ultrasound", "Other"])
        
        with col2:
            scan_date = st.date_input("Scan Date", datetime.date.today())
            radiologist_name = st.text_input("Radiologist Name")
            scan_summary = st.text_area("Scan Result Summary")
            scan_file = st.file_uploader("Upload Scan Image (optional)", type=["pdf", "jpg", "png", "jpeg"])

        submitted = st.form_submit_button("Submit Scan Report")
        
        if submitted:
            if not patient_name:
                st.error("Patient name is required")
                return
                
            file_url = ""
            if scan_file is not None:
                file_url = save_uploaded_file(scan_file)
                
            success = add_scan_report(
                patient_name, age, gender, scan_type, scan_summary,
                str(scan_date), radiologist_name, file_url
            )
            
            if success:
                st.success(f"Scan report for '{patient_name}' added successfully!")
                st.balloons()
            else:
                st.error("Error adding scan report. Please try again.")

def display_all_reports():
    st.header("All Scan Reports")
    
    df = get_all_scan_reports()
    
    if df.empty:
        st.info("No scan reports found in the database.")
        return
        
    # Display report count
    st.subheader(f"Total Reports: {len(df)}")
    
    # Drop file_url from display
    display_df = df.drop(columns=["file_url"] if "file_url" in df.columns else [])
    
    # Add a download button
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "Download Reports as CSV",
        csv,
        "scan_reports.csv",
        "text/csv",
        key='download-csv'
    )
    
    st.dataframe(display_df, use_container_width=True)

def display_search_interface():
    st.header("Search Scan Reports")
    
    search_name = st.text_input("Enter patient name to search")
    
    if search_name:
        df = search_scan_reports(search_name)
        
        if not df.empty:
            st.subheader(f"Search Results: {len(df)} reports found")
            
            for i, row in df.iterrows():
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"### 🧍 Patient: {row['patient_name']}")
                        st.markdown(f"**Details:** {row['gender']}, {row['age']} years old")
                        st.markdown(f"**Scan Type:** {row['scan_type']} on {row['scan_date']}")
                        st.markdown(f"**Radiologist:** {row['radiologist_name']}")
                        
                        with st.expander("View Summary"):
                            st.info(row['scan_summary'])
                    
                    with col2:
                        if row['file_url']:
                            file_url = get_file_url(row['file_url'])
                            st.markdown(f"[![Scan Image]({file_url})]({file_url})")
                    
                    st.markdown("---")
        else:
            st.warning(f"No patients found matching '{search_name}'")

if __name__ == '__main__':
    main()