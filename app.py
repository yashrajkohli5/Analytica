import streamlit as st
import pandas as pd

# Modular Imports
from data_loader import upload_file
from data_info import show_basic_info, get_null_report
from data_reshaper import reshape_logic
from data_cleaner import apply_cleaning
from data_transformer import change_datatypes
from data_pivot_table import create_pivot_table
from data_discovery import filter_data, group_data, run_automated_discovery
from data_viz import run_eda

st.set_page_config(page_title="Analytica Pro", layout="wide", page_icon="🧼")

def update_df(new_df):
    """Handles state history and updates the main dataframe."""
    if "history" not in st.session_state:
        st.session_state.history = []
    st.session_state.history.append(st.session_state.main_df.copy())
    if len(st.session_state.history) > 5:
        st.session_state.history.pop(0)
    st.session_state.main_df = new_df
    st.rerun()

def main():
    st.title("🧼 Analytica: Data Engineering & Discovery")
    
    df_input = upload_file()

    if df_input is not None:
        if "main_df" not in st.session_state:
            st.session_state.main_df = df_input
            st.session_state.history = []

        with st.sidebar:
            st.caption("Engine v1.5")
            
            # Reordered Steps: AI Discovery is now last
            steps = [
                "1. Data Overview", 
                "2. Reshape Data", 
                "3. Cleaning Center", 
                "4. Type Conversion", 
                "5. Pivot Table", 
                "6. Filtering & Grouping", 
                "7. Visual EDA",
                "8. Automated AI Report"
            ]
            
            st.markdown("### 🛠️ Workflow")
            menu = st.radio("Navigate:", steps, label_visibility="collapsed")
            
            st.divider()
            c1, c2 = st.columns(2)
            if c1.button("↩️ Undo"):
                if st.session_state.history:
                    st.session_state.main_df = st.session_state.history.pop()
                    st.rerun()
            if c2.button("♻️ Reset"):
                st.session_state.main_df = df_input
                st.session_state.history = []
                st.rerun()
            st.divider()
            st.markdown("### 💾 Export Progress")
            
            # Pre-calculate CSV
            csv_data = st.session_state.main_df.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                label="📥 Download CSV",
                data=csv_data,
                file_name="analytica_processed_data.csv",
                mime="text/csv",
                use_container_width=True
            )

        # Navigation Switcher
        if menu == "1. Data Overview":
            show_basic_info(st.session_state.main_df)

        elif menu == "2. Reshape Data":
            new_df = reshape_logic(st.session_state.main_df)
            if not new_df.equals(st.session_state.main_df):
                update_df(new_df)

        elif menu == "3. Cleaning Center":
            st.header("🛠️ Cleaning Center")
            
            # 1. Identify current nulls
            null_cols = get_null_report(st.session_state.main_df)
            
            # 2. Case: The data has nulls to be fixed
            if null_cols:
                col_fix = st.selectbox("Select Column to Clean:", null_cols)
                mode = st.selectbox("Strategy:", ["Delete Row", "Forward Fill", "Backward Fill", "Fill with Mean"])
                
                if st.button("Execute Clean"):
                    cleaned_df = apply_cleaning(st.session_state.main_df, col_fix, mode)
                    
                    if cleaned_df[col_fix].dtype == 'object':
                        cleaned_df[col_fix] = cleaned_df[col_fix].astype(str)
                    
                    # Store message and mark that we JUST cleaned something
                    st.session_state.last_cleaned_msg = f"✅ Column '{col_fix}' has been cleaned using {mode}."
                    st.session_state.just_finished_action = True
                    
                    update_df(cleaned_df)

            # 3. Case: Data is clean (either from the start or just finished)
            else:
                # Only show "No missing values found" if we DIDN'T just finish a cleaning action
                if not st.session_state.get("just_finished_action", False):
                    st.success("✨ No missing values!")
                else:
                    # If we just finished, show the final completion message instead
                    st.success("Data is now Cleaned.")
                    # Reset the flag so if they leave and come back, it shows the "No missing values" message
                    st.session_state.just_finished_action = False

            # Display individual column success message if it exists
            if "last_cleaned_msg" in st.session_state:
                st.success(st.session_state.last_cleaned_msg)
                del st.session_state.last_cleaned_msg

            st.divider()
            
            # --- DUPLICATE HANDLING ---
            st.subheader("👯 Duplicate Handling")
            dupes = st.session_state.main_df.duplicated().sum()
            
            if dupes > 0:
                st.warning(f"Found {dupes} duplicate rows.")
                if st.button(f"Remove {dupes} Duplicates"):
                    new_df = st.session_state.main_df.drop_duplicates().reset_index(drop=True)
                    update_df(new_df)
                    st.success(f"✅ {dupes} duplicate rows removed successfully.")
            else:
                st.info("No duplicate rows found.")

        elif menu == "4. Type Conversion":
            new_df = change_datatypes(st.session_state.main_df)
            if not new_df.equals(st.session_state.main_df):
                update_df(new_df)

        elif menu == "5. Pivot Table":
            create_pivot_table(st.session_state.main_df)

        elif menu == "6. Filtering & Grouping":
            t1, t2 = st.tabs(["🎯 Row Filtering", "🧮 Aggregation"])
            with t1: filter_data(st.session_state.main_df)
            with t2: group_data(st.session_state.main_df)

        elif menu == "7. Visual EDA":
            run_eda(st.session_state.main_df)

        elif menu == "8. Automated AI Report":
            run_automated_discovery(st.session_state.main_df)

    else:
        st.info("👋 Welcome! Please upload your CSV file to begin.")

if __name__ == "__main__":

    main()

