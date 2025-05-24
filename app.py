# app.py
import streamlit as st
from src.financial_snapshot import show_financial_snapshot
from src.retirement_planner import show_retirement_planner

st.set_page_config(page_title="Retirement Lifestyle Planner", layout="wide")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Financial Snapshot", "Retirement Planner"])

# Route to pages
if page == "Financial Snapshot":
    show_financial_snapshot()
elif page == "Retirement Planner":
    show_retirement_planner()