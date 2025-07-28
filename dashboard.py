import streamlit as st
import pandas as pd
from supabase_client import supabase
import json
import plotly.express as px

# -- Debug loaded secret
#import streamlit as st

#st.write("🔐 Loaded secrets:")
#st.write("URL:", st.secrets.get("SUPABASE_URL", "❌ Not Found"))
#st.write("key:", st.secrets.get("SUPABASE_PUBLIC_KEY", "NOT FOUND"))

# --- Load latest summary from Supabase ---
response = supabase.table("summary_metrics").select("*").order("date", desc=True).limit(1).execute()

# Extract the latest row
summary = response.data[0]


# Convert numeric fields
summary["wins"] = int(summary["wins"])
summary["losses"] = int(summary["losses"])

# Title
st.title("📈 Trading Summary Dashboard")

# Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Equity", summary["total_equity"])
col2.metric("Profit Factor", summary["profit_factor"])
col3.metric("Expectancy", summary["expectancy"])

col4, col5, col6 = st.columns(3)
col4.metric("Max Drawdown ($)", summary["max_drawdown_usd"])
col5.metric("Max Drawdown (%)", summary["max_drawdown_pct"])
col6.metric("System Winrate", summary.get("system_winrate", "N/A"))

st.metric("Winrate", summary["win_rate"])

# --- Donut Chart ---
labels = ['Wins', 'Losses']
values = [summary["wins"], summary["losses"]]
fig = px.pie(
    names=labels, 
    values=values, 
    hole=0.4, 
    title="Win/Loss Ratio"
)
st.plotly_chart(fig, use_container_width=True)

# --- Smoothed Equity Curve ---
# --- Parse Equity Curve JSON ---
equity_curve = pd.DataFrame(json.loads(summary["equity_curve"]))
st.write("Equity Curve Columns:", equity_curve.columns.tolist())

# Convert to datetime and ensure unique dates
equity_curve["date"] = pd.to_datetime(equity_curve["date"])
equity_curve = equity_curve.groupby("date").last()  # removes duplicates

# Reindex to daily frequency and forward-fill missing values
equity_curve = equity_curve.asfreq("D")
equity_curve["Equity"] = equity_curve["Equity"].ffill()

# Reset index for plotting
equity_curve = equity_curve.reset_index()
equity_curve.rename(columns={"date": "Date", "equity": "Equity"}, inplace=True)

# Plot
fig2 = px.line(equity_curve, x="Date", y="Equity", title="Equity Curve")
st.plotly_chart(fig2, use_container_width=True)
