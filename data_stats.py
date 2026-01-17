import streamlit as st

def show_stats(df):
    st.subheader("🔢 Statistical Summary")
    
    # Overview of numerical columns
    st.write("**Numerical Description:**")
    st.dataframe(df.describe())
    
    # Information on Categorical columns
    st.write("**Categorical Summary:**")
    st.dataframe(df.describe(include=['object']))

def show_correlations(df):
    st.subheader("🔗 Feature Correlation")
    # Only calculate for numbers
    numeric_df = df.select_dtypes(include=['number'])
    if not numeric_df.empty:
        corr = numeric_df.corr()
        st.write("Pearson Correlation Matrix:")
        st.dataframe(corr)
    else:
        st.warning("No numeric columns found for correlation analysis.")