import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
import streamlit.components.v1 as components

@st.cache_resource
def get_profile_report(df):
    profile = ProfileReport(
        df, 
        title="Data Audit",
        explorative=True,
        minimal=False
    )
    
    # --- THE CRITICAL FIX ---
    profile.config.html.navbar_show = False  # Removes the internal second sidebar/nav
    profile.config.html.full_width = True     # Ensures it fills the Streamlit container
    profile.config.html.style.theme = None   # Uses the standard Jupyter look
    
    return profile.to_html()

def run_automated_discovery(df):
    st.header("🔍 Automated AI Report")
    
    st.markdown("""
    *For a full-screen view without any layout constraints, use the button below.*
    """)

    if st.button("🚀 Generate AI Report"):
        with st.spinner("Analyzing dataset..."):
            try:
                report_html = get_profile_report(df)
                
                # High-resolution Download (Best for external sharing)
                st.download_button(
                    label="📂 Open Full-Screen Report",
                    data=report_html,
                    file_name="Clean_Data_Report.html",
                    mime="text/html",
                    use_container_width=True
                )
                
                st.divider()
                
                # The "White Box" wrapper ensures black text is readable and 
                # CSS doesn't bleed into your main Streamlit sidebar.
                components.html(
                    f"""
                    <div style="background-color: white; border-radius: 10px; padding: 10px;">
                        {report_html}
                    </div>
                    """, 
                    height=1000, 
                    scrolling=True
                )
                
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.info("Click to generate the report on your current cleaned data.")

def filter_data(df):
    """Manual row-level filtering logic."""
    st.subheader("🎯 Dynamic Filtering")
    col = st.selectbox("Select column to filter by:", df.columns, key="filter_box")
    
    if df[col].dtype == 'object' or df[col].dtype.name == 'category':
        unique_vals = df[col].unique().tolist()
        selected = st.multiselect(f"Select values from {col}:", unique_vals)
        if selected:
            df = df[df[col].isin(selected)]
    elif pd.api.types.is_numeric_dtype(df[col]):
        min_v, max_v = float(df[col].min()), float(df[col].max())
        range_val = st.slider(f"Range for {col}:", min_v, max_v, (min_v, max_v))
        df = df[(df[col] >= range_val[0]) & (df[col] <= range_val[1])]
    
    st.dataframe(df, use_container_width=True)
    return df

def group_data(df):
    """Manual categorical aggregation logic."""
    st.subheader("🧮 Grouped Aggregation")
    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    num_cols = df.select_dtypes(include=['number']).columns
    
    if len(cat_cols) > 0 and len(num_cols) > 0:
        c1, c2, c3 = st.columns(3)
        g_col = c1.selectbox("Group By:", cat_cols)
        n_col = c2.selectbox("Measure:", num_cols)
        op = c3.selectbox("Function:", ["mean", "sum", "count", "min", "max"])
        
        if st.button("Run Aggregation"):
            res = df.groupby(g_col)[n_col].agg(op).reset_index()
            st.dataframe(res, use_container_width=True)
    else:
        st.warning("Ensure you have both categorical and numerical columns.")