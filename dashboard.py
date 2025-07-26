import streamlit as st
import pandas as pd
import json

# Load data
summary = pd.read_csv("summary.csv").iloc[0]
equity_curve = pd.DataFrame(json.loads(summary["Equity Curve (JSON)"]))

# Metrics
st.title("Trading Summary Dashboard")
st.metric("Total Equity", summary["Total Equity"])
st.metric("Profit Factor", summary["Profit Factor"])
st.metric("Expectancy", summary["Expectancy"])
st.metric("Max Drawdown ($)", summary["Max Drawdown ($)"])
st.metric("Max Drawdown (%)", summary["Max Drawdown (%)"])
st.metric("System Winrate", summary["System Winrate"])
st.metric("Winrate", summary["Winrate (%)"])

# Donut Chart using Plotly
import plotly.express as px

labels = ['Wins', 'Losses']
values = [summary["Wins"], summary["Losses"]]
fig = px.pie(names=labels, values=values, holes = 0.4, title="Win/Loss Ratio")
st.plotly_chart(fig)

# Equity Curve Chart
fig2 = px.line(equity_curve, x='Date', y='Equity', title='Equity Curve')
st.plotly_chart(fig2)
