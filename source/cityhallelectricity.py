import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pydeck as pdk
import numpy as np
import requests

#https://data.boston.gov/api/3/action/datastore_search?resource_id=f123e65d-dc0e-4c83-9348-ed46fec498c0&limit=5

""" Example data for electricity usage: 

_id	DateTime_Measured	Total_Demand_KW
31	2020-03-26 07:30:00	1244
32	2020-03-26 07:15:00	1232
33	2020-03-26 07:00:00	1209
34	2020-03-26 06:45:00	1198
35	2020-03-26 06:30:00	1205
36	2020-03-26 06:15:00	1209
37	2020-03-26 06:00:00	1121
38	2020-03-26 05:45:00	929
39	2020-03-26 05:30:00	917
40	2020-03-26 05:15:00	929

"""

# Define the API endpoint
API_URL = "https://data.boston.gov/api/3/action/datastore_search"
RESOURCE_ID = "f123e65d-dc0e-4c83-9348-ed46fec498c0"  

def get_electricity_data():
    # Query the API to get the data
    params = {
        "resource_id": RESOURCE_ID,
        "limit": 400000  # Adjust the limit as needed
    }
    response = requests.get(API_URL, params=params)
    data = response.json()
    return data["result"]["records"]

def peak_electricity():
    # Get the electricity data
    data = get_electricity_data()
    
    # Convert the data to a DataFrame
    df = pd.DataFrame(data)
    
    # Convert the DateTime_Measured column to datetime
    df['DateTime_Measured'] = pd.to_datetime(df['DateTime_Measured'])
    
    # Ensure the Total_Demand_KW column is numeric
    df['Total_Demand_KW'] = pd.to_numeric(df['Total_Demand_KW'], errors='coerce')
    
    # Drop rows with NaN values in the Total_Demand_KW column
    df = df.dropna(subset=['Total_Demand_KW'])
    
    # Extract the hour from the DateTime_Measured column
    df['Hour'] = df['DateTime_Measured'].dt.hour
    
    # Group by hour and calculate the average electricity usage for each hour
    hourly_usage = df.groupby('Hour')['Total_Demand_KW'].mean().reset_index()
    
    # Identify the hours with the highest average electricity usage
    peak_hours = hourly_usage.sort_values(by='Total_Demand_KW', ascending=False).head(10)
    
    return hourly_usage, peak_hours

def top_and_lowest_usage_days():
    # Get the electricity data
    data = get_electricity_data()
    
    # Convert the data to a DataFrame
    df = pd.DataFrame(data)
    
    # Convert the DateTime_Measured column to datetime
    df['DateTime_Measured'] = pd.to_datetime(df['DateTime_Measured'])
    
    # Ensure the Total_Demand_KW column is numeric
    df['Total_Demand_KW'] = pd.to_numeric(df['Total_Demand_KW'], errors='coerce')
    
    # Drop rows with NaN values in the Total_Demand_KW column
    df = df.dropna(subset=['Total_Demand_KW'])
    
    # Extract the date from the DateTime_Measured column
    df['Date'] = df['DateTime_Measured'].dt.date
    
    # Group by date and calculate the total electricity usage for each day
    daily_usage = df.groupby('Date')['Total_Demand_KW'].sum().reset_index()
    
    # Identify the top 10 highest electricity usage days
    top_days = daily_usage.sort_values(by='Total_Demand_KW', ascending=False).head(10)
    
    # Identify the top 10 lowest electricity usage days
    lowest_days = daily_usage.sort_values(by='Total_Demand_KW', ascending=True).head(10)
    
    return daily_usage, top_days, lowest_days

def electricity():
    # Streamlit app
    st.title("City Hall Electricity Usage Analysis")

    # Get the hourly usage and peak hours
    hourly_usage, peak_hours = peak_electricity()

    # Display the hourly usage data
    st.write("Hourly Electricity Usage")
    st.write(hourly_usage)

    # Plot the hourly usage data
    st.write("Average Electricity Usage by Hour")
    fig, ax = plt.subplots()
    hourly_usage.plot(kind='bar', x='Hour', y='Total_Demand_KW', ax=ax)
    ax.set_xlabel("Hour of the Day")
    ax.set_ylabel("Average Electricity Usage (KW)")
    st.pyplot(fig)


    # Get the daily usage, top usage days, and lowest usage days
    daily_usage, top_days, lowest_days = top_and_lowest_usage_days()

    # Display the daily usage data
    st.write("Daily Electricity Usage")
    st.write(daily_usage)

    # Plot the daily usage data
    st.write("Total Electricity Usage by Day")
    fig, ax = plt.subplots()
    daily_usage.plot(kind='line', x='Date', y='Total_Demand_KW', ax=ax)
    ax.set_xlabel("Date")
    ax.set_ylabel("Total Electricity Usage (KW)")
    st.pyplot(fig)

    # Display the top usage days data
    st.write("Top 10 Highest Electricity Usage Days")
    st.write(top_days)

    # Plot the top usage days data
    st.write("Top 10 Highest Electricity Usage Days")
    fig, ax = plt.subplots()
    top_days.plot(kind='bar', x='Date', y='Total_Demand_KW', ax=ax, color='green')
    ax.set_xlabel("Date")
    ax.set_ylabel("Total Electricity Usage (KW)")
    st.pyplot(fig)

    # Display the lowest usage days data
    st.write("Top 10 Lowest Electricity Usage Days")
    st.write(lowest_days)

    # Plot the lowest usage days data
    st.write("Top 10 Lowest Electricity Usage Days")
    fig, ax = plt.subplots()
    lowest_days.plot(kind='bar', x='Date', y='Total_Demand_KW', ax=ax, color='blue')
    ax.set_xlabel("Date")
    ax.set_ylabel("Total Electricity Usage (KW)")
    st.pyplot(fig)