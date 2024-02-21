# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 13:01:19 2023

@author: Bogdan Tudose
"""
#%% Import Packages
import pandas as pd
import streamlit as st
import plotly.express as px
import requests

#%% Import Data
@st.cache
def grabData():
    codes = {'all':'1c22431c-ad90-4614-a973-9c39f309d9c7',
         'type':'82b15b0b-4475-4034-9ba4-f00188b3784e',
         'airport':'46f88a70-c204-4e15-9168-5366dc8bea6d'}

    params = {'code': ''}
    tables = {}
    jsonFiles = {}
    for dataType, code in codes.items():
        params['code'] = code
        response = requests.get('https://api.economicdata.alberta.ca/api/data', params=params)
        data = response.json()
        jsonFiles[dataType] = data #save down the json file
        df = pd.DataFrame(data)    
        df['Date'] = pd.to_datetime(df['Date'])
        tables[dataType] = df
    return tables
    
dfs = grabData()
df = dfs['airport']
dfType = dfs['type']

st.title("Alberta Airport Data")
st.write("Source:https://economicdashboard.alberta.ca/AirPassengers")

st.header("All Data")
chartType = st.selectbox("Pick chart type", ['Bar','Line'])
if chartType == 'Line':
    figAir = px.line(df, x="Date", y='Value', color='Airport')
else:
    figAir = px.bar(df, x="Date", y='Value', color='Airport')
st.plotly_chart(figAir, use_container_width=True)

#%% Airport Sepcific Data
st.header("Filtered Data by Airport")
airports = sorted(df['Airport'].unique())
pickAirport = st.multiselect("Pick airport(s) to filter", airports, airports)
filterDF = df[df['Airport'].isin(pickAirport)]
figAirport = px.bar(filterDF, x="Date", y='Value', color='Airport')
st.plotly_chart(figAirport, use_container_width=True)

#%% Flight Type Data
st.header("Filtered Data by Flight Type")
types = sorted(dfType['Flight Type'].unique())
pickAirport = st.multiselect("Pick flight type(s) to filter", types, types)
filterDF2 = dfType[dfType['Flight Type'].isin(pickAirport)]
figFlightType = px.bar(filterDF2, x="Date", y='Value', color='Flight Type', barmode="group")
st.plotly_chart(figFlightType, use_container_width=True)

#%%
st.header("Raw Data")
st.dataframe(df)

