import streamlit as st
import pandas as pd
from supabse_client import supabase
import json
import plotly.express as px

# --- Load latest summary from Supabase ---
response = supabase.table("summary_metrics").select("*").order("Date", desc=True).limit(1).execute()
summary_row = response.data[0]

# Convert numeric fields
summary["Wins"] = int(summary["Wins"])
summary["Losses"] = int(summary["Losses"])

# Title
st.title("📈 Trading Summary Dashboard")

# Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Equity", summary["Total Equity"])
col2.metric("Profit Factor", summary["Profit Factor"])
col3.metric("Expectancy", summary["Expectancy"])

col4, col5, col6 = st.columns(3)
col4.metric("Max Drawdown ($)", summary["Max Drawdown ($)"])
col5.metric("Max Drawdown (%)", summary["Max Drawdown (%)"])
col6.metric("System Winrate", summary.get("System Winrate", "N/A"))

st.metric("Winrate", summary["Winrate (%)"])

# --- Donut Chart ---
labels = ['Wins', 'Losses']
values = [summary["Wins"], summary["Losses"]]
fig = px.pie(
    names=labels, 
    values=values, 
    hole=0.4, 
    title="Win/Loss Ratio"
)
st.plotly_chart(fig, use_container_width=True)

# --- Smoothed Equity Curve ---
# Convert to datetime and ensure unique dates
equity_curve["Date"] = pd.to_datetime(equity_curve["Date"])
equity_curve = equity_curve.groupby("Date").last()  # removes duplicates

# Reindex to daily frequency and forward-fill missing values
equity_curve = equity_curve.asfreq("D")
equity_curve["Equity"] = equity_curve["Equity"].ffill()

# Reset index for plotting
equity_curve = equity_curve.reset_index()

# Plot
fig2 = px.line(equity_curve, x="Date", y="Equity", title="Equity Curve")
st.plotly_chart(fig2, use_container_width=True)
