import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

@st.cache_data
def load_data():
    df = pd.read_csv("marketing_data.csv", parse_dates=["date"])
    df["CTR"] = df["clicks"] / df["impressions"]
    df["CVR"] = df["conversions"] / df["clicks"].replace(0, np.nan)
    df["CPC"] = df["spend_usd"] / df["clicks"].replace(0, np.nan)
    df["CPA"] = df["spend_usd"] / df["conversions"].replace(0, np.nan)
    return df

df = load_data()

st.title("Marketing A/B Test KPI Dashboard")
st.write("Synthetic dataset mimicking Agoda-style performance marketing.")

col1, col2, col3 = st.columns(3)
col1.metric("Total Impressions", f"{df['impressions'].sum():,}")
col2.metric("Total Clicks", f"{df['clicks'].sum():,}")
overall_ctr = df['clicks'].sum() / df['impressions'].sum()
col3.metric("Overall CTR", f"{overall_ctr:.2%}")

st.sidebar.header("Filters")
channel = st.sidebar.multiselect("Channel", options=sorted(df["channel"].unique()), default=list(df["channel"].unique()))
country = st.sidebar.multiselect("Country", options=sorted(df["country"].unique()), default=list(df["country"].unique()))
group = st.sidebar.multiselect("Variant (A/B)", options=sorted(df["group"].unique()), default=list(df["group"].unique()))

mask = df["channel"].isin(channel) & df["country"].isin(country) & df["group"].isin(group)
filtered = df[mask]

st.subheader("KPI by Variant")
variant_agg = filtered.groupby("group").agg(
    impressions=("impressions", "sum"),
    clicks=("clicks", "sum"),
    conversions=("conversions", "sum"),
    spend_usd=("spend_usd", "sum"),
).reset_index()
variant_agg["CTR"] = variant_agg["clicks"] / variant_agg["impressions"]
variant_agg["CVR"] = variant_agg["conversions"] / variant_agg["clicks"].replace(0, np.nan)
variant_agg["CPA"] = variant_agg["spend_usd"] / variant_agg["conversions"].replace(0, np.nan)

st.dataframe(variant_agg)

st.subheader("CTR by Country and Variant")
chart = alt.Chart(filtered).mark_bar().encode(
    x="country:N",
    y=alt.Y("mean(CTR):Q", title="Average CTR"),
    color="group:N",
    column="channel:N"
)
st.altair_chart(chart, use_container_width=True)

st.subheader("Daily Conversions")
daily = filtered.groupby("date").agg(conversions=("conversions", "sum")).reset_index()
line = alt.Chart(daily).mark_line().encode(
    x="date:T",
    y="conversions:Q"
)
st.altair_chart(line, use_container_width=True)
