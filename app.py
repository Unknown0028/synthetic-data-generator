import os
import streamlit as st
from gdpr_helpers import Anonymizer


# Streamlit UI
st.title("Data Anonymization with GDPR Helpers")

# File upload
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded_file is not None:
    # Save the uploaded file
    dataset_path = f"temp_{uploaded_file.name}"
    with open(dataset_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"You uploaded: {uploaded_file.name}")

    # Ensure the uploaded file is a CSV
    if not dataset_path.endswith('.csv'):
        st.error("Error: Please upload a CSV file.")
        st.stop()

    # Display the content of the uploaded file
    st.write(f"Sample data:\n{uploaded_file.getvalue().decode('utf-8')[:100]}")  # Print first 100 characters

    # Define the project name and configurations
    project_name = "project"
    run_mode = "cloud"
    transforms_config = "gdpr-helpers/src/config/transforms_config.yaml"
    synthetics_config = "gdpr-helpers/src/config/synthetics_config.yaml"
    endpoint = "https://api.gretel.cloud"

    # Create the Anonymizer object
    try:
        am = Anonymizer(
            project_name=project_name,
            run_mode=run_mode,
            transforms_config=transforms_config,
            synthetics_config=synthetics_config,
            endpoint=endpoint
        )
    except ImportError:
        st.error("Error: 'gdpr-helpers' library not found. Please install it.")
        st.stop()

    # Anonymize the dataset
    st.write("Anonymizing data... This may take a while.")
    try:
        am.anonymize(dataset_path=dataset_path)
        st.success("Anonymization process complete!")
    except Exception as e:
        st.error(f"An error occurred during anonymization: {str(e)}")
        st.stop()

    # Define paths for synthetic data and anonymization report
    file_name_base = os.path.splitext(os.path.basename(dataset_path))[0]
    synthetic_data_path = f'artifacts/{file_name_base}-synthetic_data.csv'
    anonymization_report_path = f'artifacts/{file_name_base}-anonymization_report.html'

    # Check if synthetic data and anonymization report files exist
    if os.path.exists(synthetic_data_path) and os.path.exists(anonymization_report_path):
        # Display download links
        st.write("Download links:")
        st.markdown(f"[Synthetic Data]({synthetic_data_path})")
        st.markdown(f"[Anonymization Report]({anonymization_report_path})")

        # Provide download buttons for Streamlit
        with open(synthetic_data_path, "rb") as f:
            st.download_button(label="Download Synthetic Data", data=f, file_name=f"{file_name_base}-synthetic_data.csv")
        with open(anonymization_report_path, "rb") as f:
            st.download_button(label="Download Anonymization Report", data=f, file_name=f"{file_name_base}-anonymization_report.html")
    else:
        st.error("Error: Synthetic data or anonymization report files were not created. Please check the anonymization process.")
else:
    st.info("Please upload a CSV file to start the anonymization process.")
