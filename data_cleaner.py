import streamlit as st
import pandas as pd

def apply_cleaning(df, column, strategy):
    """Executes strategies for null handling."""
    if strategy == "Delete Row":
        # Drop rows where the specific column has NaN values
        df = df.dropna(subset=[column]).reset_index(drop=True)
    
    elif strategy == "Forward Fill":
        df[column] = df[column].ffill()
        
    elif strategy == "Backward Fill":
        df[column] = df[column].bfill()
        
    elif strategy == "Fill with Mean":
        if pd.api.types.is_numeric_dtype(df[column]):
            df[column] = df[column].fillna(df[column].mean())
            
    return df