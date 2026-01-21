"""
ShopSmart Sales Dashboard

A Streamlit dashboard for visualizing e-commerce sales data.
"""

import streamlit as st

# Page configuration - must be the first Streamlit command
st.set_page_config(
    page_title="ShopSmart Sales Dashboard",
    page_icon="📊",
    layout="wide"
)


def main():
    """Main application entry point."""
    st.title("ShopSmart Sales Dashboard")


if __name__ == "__main__":
    main()
