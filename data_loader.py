import streamlit as st
import pandas as pd

def upload_file():
    uploaded_file = st.file_uploader("Import CSV or Excel file", type=['csv', 'xlsx'])
    
    # Check if a file has actually been uploaded first
    if uploaded_file is not None:
        try:
            # Now it is safe to check the name attribute
            if uploaded_file.name.endswith('.csv'):
                return pd.read_csv(uploaded_file)
            
            else:
                excel_file = pd.ExcelFile(uploaded_file)
                sheet_names = excel_file.sheet_names
                
                if len(sheet_names) > 1:
                    selected_sheet = st.selectbox(
                        "Select Sheet:",
                        sheet_names
                    )
                else:
                    selected_sheet = sheet_names[0]
                
                return pd.read_excel(uploaded_file, sheet_name=selected_sheet)
                
        except Exception as e:
            st.error(f"Error loading file: {e}")
            return None
            
    # If no file is uploaded, just return None quietly
    return None