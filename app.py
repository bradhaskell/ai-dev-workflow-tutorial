"""
ShopSmart Sales Dashboard

A Streamlit dashboard for visualizing e-commerce sales data.
"""

import streamlit as st
import pandas as pd

# Page configuration - must be the first Streamlit command
st.set_page_config(
    page_title="ShopSmart Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# Data file path
DATA_FILE = "data/sales-data.csv"


@st.cache_data
def load_data() -> pd.DataFrame | None:
    """Load and cache sales data from CSV file.

    Returns:
        DataFrame with sales data, or None if loading fails.
    """
    try:
        df = pd.read_csv(DATA_FILE)

        # Check for empty file
        if df.empty:
            st.warning("The data file is empty. No data to display.")
            return None

        # Parse date column
        df["date"] = pd.to_datetime(df["date"])

        return df

    except FileNotFoundError:
        st.error(f"Data file not found: {DATA_FILE}. Please ensure the file exists.")
        return None
    except pd.errors.EmptyDataError:
        st.warning("The data file is empty. No data to display.")
        return None


def main():
    """Main application entry point."""
    st.title("ShopSmart Sales Dashboard")

    # Load data
    df = load_data()

    if df is None:
        st.stop()


if __name__ == "__main__":
    main()
