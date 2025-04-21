import os
import uuid
from io import BytesIO
import streamlit as st

# Determine if we're using cloud storage
STORAGE_MODE = os.environ.get("STORAGE_MODE", "local")

# Local storage directory
UPLOAD_DIR = "uploaded_scans"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_uploaded_file(uploaded_file):
    """Save an uploaded file and return the file path or URL."""
    if STORAGE_MODE == "s3":
        return save_to_s3(uploaded_file)
    else:
        return save_to_local(uploaded_file)

def save_to_local(uploaded_file):
    """Save file to local filesystem."""
    try:
        # Create a unique filename
        file_ext = os.path.splitext(uploaded_file.name)[1]
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        # Save the file
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        return file_path
    except Exception as e:
        st.error(f"Error saving file: {e}")
        return ""

def save_to_s3(uploaded_file):
    """
    This function would implement S3 storage.
    For demonstration, we'll return a placeholder.
    In a real implementation, you would:
    1. Connect to S3 using boto3
    2. Upload the file to your bucket
    3. Return the S3 URL
    """
    st.warning("S3 storage is configured but not implemented in this demo")
    return "s3://example-bucket/placeholder.jpg"

def get_file_url(file_path_or_url):
    """Get the URL for accessing a file."""
    if not file_path_or_url:
        return ""
        
    # If it's already a URL (starts with http, https, or s3)
    if file_path_or_url.startswith(("http://", "https://", "s3://")):
        return file_path_or_url
        
    # For local files, we can't easily serve them in production
    # In a real app, you'd implement proper file serving
    # This is a simplified version for demonstration
    return file_path_or_url