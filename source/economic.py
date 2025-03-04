import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pydeck as pdk
import numpy as np
import requests

#https://data.boston.gov/dataset/economic-indicators-legacy-portal/resource/29e74884-a777-4242-9fcc-c30aaaf3fb10
"""

_id	Year	Month	logan_passengers	logan_intl_flights	hotel_occup_rate	hotel_avg_daily_rate	total_jobs	unemp_rate	labor_force_part_rate	pipeline_unit	pipeline_total_dev_cost	pipeline_sqft	pipeline_const_jobs	foreclosure_pet	foreclosure_deeds	med_housing_price	housing_sales_vol	new_housing_const_permits	new-affordable_housing_permits
84	2019	12	3389382	4155	0.717	183.2	392118	0.02	0.67	1044	1106200000	1697970	1645	0	0	0	0	0	0
83	2019	11	3264105	3959	0.803	238.82	391531	0.021	0.67	480	324300000	688168	539	0	0	0	0	0	0
82	2019	10	3771212	4388	0.907	313.17	390983	0.023	0.671	393	968000000	1261737	972	0	0	0	0	0	0
81	2019	9	3547546	4586	0.895	312.37	385445	0.028	0.665	286	91032000	416015	307	0	0	0	0	0	0
80	2019	8	4120937	5190	0.888	270.54	392536	0.027	0.676	176	882120000	1144908	931	0	0	0	0	0	0
79	2019	7	4072082	5260	0.9	285.02	390678	0.028	0.674	459	789118461	1604849	1074	0	0	0	0	0	0
78	2019	6	3946406	4955	0.898	314.97	390540	0.031	0.675	324	224135602	571159	468	0	0	0	0	0	0
77	2019	5	3879343	4907	0.878	312.01	386895	0.029	0.668	38	143300000	259679	290	0	0	0	0	0	0
76	2019	4	3647276	4847	0.877	287.72	387742	0.022	0.665	35	43000000	110002	100	0	0	0	0	0	0
75	2019	3	3457362	4523	0.812	225.1	388432	0.025	0.668	677	480250000	1323438	1040	0	0	0	0	0	0
Showing 1 to 10 of 84 entries


"""
#https://data.boston.gov/api/3/action/datastore_search?resource_id=29e74884-a777-4242-9fcc-c30aaaf3fb10&limit=5
# Define the API endpoint
API_URL = "https://data.boston.gov/api/3/action/datastore_search"
RESOURCE_ID = "29e74884-a777-4242-9fcc-c30aaaf3fb10"  

def get_economic_data():
    # Query the API to get the data
    params = {
        "resource_id": RESOURCE_ID,
        "limit": 400000  # Adjust the limit as needed
    }
    response = requests.get(API_URL, params=params)
    data = response.json()
    return data["result"]["records"]

def economic():
    # Get the economic data
    data = get_economic_data()

      # Convert the data to a DataFrame
    df = pd.DataFrame(data)

    # Convert columns to appropriate data types
    df['Year'] = df['Year'].astype(int)
    df['Month'] = df['Month'].astype(int)
    df['logan_passengers'] = df['logan_passengers'].astype(int)
    df['logan_intl_flights'] = df['logan_intl_flights'].astype(int)
    df['hotel_occup_rate'] = df['hotel_occup_rate'].astype(float)
    df['hotel_avg_daily_rate'] = df['hotel_avg_daily_rate'].astype(float)
    df['total_jobs'] = df['total_jobs'].astype(int)
    df['unemp_rate'] = df['unemp_rate'].astype(float)
    df['labor_force_part_rate'] = df['labor_force_part_rate'].astype(float)
    df['pipeline_unit'] = df['pipeline_unit'].astype(int)
    df['pipeline_total_dev_cost'] = df['pipeline_total_dev_cost'].astype(float)
    df['pipeline_sqft'] = df['pipeline_sqft'].astype(int)
    df['pipeline_const_jobs'] = df['pipeline_const_jobs'].astype(int)
    df['foreclosure_pet'] = df['foreclosure_pet'].astype(int)
    df['foreclosure_deeds'] = df['foreclosure_deeds'].astype(int)
    df['med_housing_price'] = df['med_housing_price'].astype(float)
    df['housing_sales_vol'] = df['housing_sales_vol'].astype(int)
    df['new_housing_const_permits'] = df['new_housing_const_permits'].astype(int)
    df['new-affordable_housing_permits'] = df['new-affordable_housing_permits'].astype(int)
    
    # Analyze and visualize trends in air travel
    st.write("Logan Airport Passengers Over Time")
    fig, ax = plt.subplots()
    df.groupby(['Year', 'Month'])['logan_passengers'].sum().plot(ax=ax)
    ax.set_xlabel("Year-Month")
    ax.set_ylabel("Logan Passengers")
    st.pyplot(fig)

    st.write("Logan Airport International Flights Over Time")
    fig, ax = plt.subplots()
    df.groupby(['Year', 'Month'])['logan_intl_flights'].sum().plot(ax=ax)
    ax.set_xlabel("Year-Month")
    ax.set_ylabel("Logan International Flights")
    st.pyplot(fig)
    

    # Analyze and visualize hotel industry performance
    st.write("Hotel Occupancy Rate Over Time")
    fig, ax = plt.subplots()
    df.groupby(['Year', 'Month'])['hotel_occup_rate'].mean().plot(ax=ax)
    ax.set_xlabel("Year-Month")
    ax.set_ylabel("Hotel Occupancy Rate")
    st.pyplot(fig)

    # Analyze and visualize employment and labor market
    st.write("Total Jobs Over Time")
    fig, ax = plt.subplots()
    df.groupby(['Year', 'Month'])['total_jobs'].sum().plot(ax=ax)
    ax.set_xlabel("Year-Month")
    ax.set_ylabel("Total Jobs")
    st.pyplot(fig)

    # Analyze and visualize real estate and housing market
    st.write("Median Housing Price Over Time")
    fig, ax = plt.subplots()
    df.groupby(['Year', 'Month'])['med_housing_price'].mean().plot(ax=ax)
    ax.set_xlabel("Year-Month")
    ax.set_ylabel("Median Housing Price")
    st.pyplot(fig)