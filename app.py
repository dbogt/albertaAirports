# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 13:01:19 2023

@author: Bogdan Tudose
"""
#%% Import Packages
import pandas as pd
import streamlit as st
import plotly.express as px

#%% Import Data
@st.cache
def grabData():
    url = 'https://economicdashboard.alberta.ca/Download/DownloadFile?extension=JSON&requestUrl=https%3A%2F%2Feconomicdashboard.alberta.ca%2Fapi%2FAirPassengers'
    df = pd.read_json(url)
    df.info()
    df['Date'] = pd.to_datetime(df['When'])
    return df

df = grabData()

st.title("Alberta Airport Data")
st.write("Source:https://economicdashboard.alberta.ca/AirPassengers")

st.header("All Data")
chartType = st.selectbox("Pick chart type", ['Bar','Line'])
if chartType == 'Line':
    figAir = px.line(df, x="Date", y='Alberta', color='Airport')
else:
    figAir = px.bar(df, x="Date", y='Alberta', color='Airport')
st.plotly_chart(figAir, use_container_width=True)

#%% Airport Sepcific Data
st.header("Filtered Data by Airport")
airports = sorted(df['Airport'].unique())
pickAirport = st.multiselect("Pick airport(s) to filter", airports, airports)
filterDF = df[df['Airport'].isin(pickAirport)]
figAirport = px.bar(filterDF, x="Date", y='Alberta', color='FlightType')
st.plotly_chart(figAirport, use_container_width=True)

#%% Flight Type Data
st.header("Filtered Data by Flight Type")
types = sorted(df['FlightType'].unique())
pickAirport = st.multiselect("Pick flight type(s) to filter", types, types)
filterDF2 = df[df['FlightType'].isin(pickAirport)]
figFlightType = px.bar(filterDF2, x="Date", y='Alberta', color='Airport', barmode="group")
st.plotly_chart(figFlightType, use_container_width=True)

#%%
st.header("Raw Data")
st.dataframe(df)

