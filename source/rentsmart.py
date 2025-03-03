import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pydeck as pdk
import numpy as np
import requests

"""
https://data.boston.gov/api/3/action/datastore_search

EXAMPLE DATA 
[{'_id': 1, 'date': '2025-03-01 23:28:00+00', 'violation_type': 'Sanitation Requests', 'description': 'Rodent Activity', 'address': '2809-2811 Washington St, 02119', 'neighborhood': 'Roxbury', 'zip_code': '02119', 'parcel': '1100359000', 'owner': 'JONES WANDA 
H', 'year_built': '1895', 'year_remodeled': None, 'property_type': 'Residential 2-family', 'latitude': '42.321659568738234', 'longitude': '-71.09233060479556'}, {'_id': 2, 'date': '2025-03-01 21:34:57.847+00', 'violation_type': 'Sanitation Requests', 'description': 'Abandoned Vehicles', 'address': '23 M St, 02127', 'neighborhood': 'South Boston', 'zip_code': '02127', 'parcel': '0603622000', 'owner': 'HAYES CHERYL J', 'year_built': '1905', 'year_remodeled': '2005', 'property_type': 'Residential 2-family', 'latitude': '42.33744948826995', 'longitude': '-71.03357043789833'}, {'_id': 3, 'date': '2025-03-01 20:42:39.04+00', 'violation_type': 'Sanitation Requests', 'description': 'Rodent Activity', 'address': '101 Cushing Ave, 02125', 'neighborhood': 'Dorchester', 'zip_code': '02125', 'parcel': '1301526000', 'owner': 'ZOUEIN ANTOINE', 'year_built': '1927', 'year_remodeled': '1997', 'property_type': 'Residential 3-family', 'latitude': '42.31330952974282', 'longitude': '-71.06278055744447'}, {'_id': 4, 'date': '2025-03-01 20:04:03.15+00', 'violation_type': 'Sanitation Requests', 'description': 'Abandoned Vehicles', 'address': '392 Seaver St, 02121', 'neighborhood': 'Dorchester', 'zip_code': '02121', 'parcel': '1400990000', 'owner': 'EDGE REAL ESTATE INVESTMENTS LLC', 'year_built': '1905', 'year_remodeled': '2018', 'property_type': 'Residential 3-family', 'latitude': '42.303859556176455', 'longitude': '-71.08164062061361'}, {'_id': 5, 'date': '2025-03-01 17:31:09.523+00', 'violation_type': 'Sanitation Requests', 'description': 'Abandoned Vehicles', 'address': '21 Goodrich Rd, 02130', 'neighborhood': 'Jamaica Plain', 'zip_code': '02130', 'parcel': '1901988000', 'owner': 'GUILLEMIN ANDRE D', 'year_built': '1930', 'year_remodeled': '1975', 'property_type': 'Residential 2-family', 'latitude': '42.315979599987905', 'longitude': '-71.1150806696801'}]

"""

# Define the API endpoint
API_URL = "https://data.boston.gov/api/3/action/datastore_search"
RESOURCE_ID = "dc615ff7-2ff3-416a-922b-f0f334f085d0"  # Replace with the actual resource ID
#https://data.boston.gov/api/3/action/datastore_search?resource_id=dc615ff7-2ff3-416a-922b-f0f334f085d0&limit=5
def get_violation_data():
    # Query the API to get the data
    params = {
        "resource_id": RESOURCE_ID,
        "limit": 400000  # Adjust the limit as needed
    }
    response = requests.get(API_URL, params=params)
    print(response)
    data = response.json()
    return data["result"]["records"]

def violation_count_by_owner():
    # Get the violation data
    data = get_violation_data()
    
    # Convert the data to a DataFrame
    df = pd.DataFrame(data)
    
    # Group by owner and count the number of violations and properties
    owner_violation_counts = df.groupby("owner").agg(
        violation_count=pd.NamedAgg(column="_id", aggfunc="count"),
        property_count=pd.NamedAgg(column="address", aggfunc="nunique")
    ).reset_index()
    
    # Sort by violation count in descending order and get the top 100 owners
    owner_violation_counts = owner_violation_counts.sort_values(by="violation_count", ascending=False)
    
    return owner_violation_counts

def search_owner_properties(owner_name):
    # Get the violation data
    data = get_violation_data()
    
    # Convert the data to a DataFrame
    df = pd.DataFrame(data)
    
    # Filter the data by owner name
    owner_data = df[df['owner'].str.contains(owner_name, case=False, na=False)]
    
    # Add a count column to enumerate the violations
    owner_data['violation_number'] = range(1, len(owner_data) + 1)
    
    return owner_data

def Violations():
    # Streamlit app
    st.title("Top 100 Owners with the Most Violations")

    # Get the top 100 owners
    top_owners = violation_count_by_owner()

    # Display the data in a table
    st.write(top_owners)

    # Plot the data (top 10 owners)
    top_10_owners = top_owners.head(10)
    fig, ax = plt.subplots(figsize=(10, 8))
    top_10_owners.plot(kind="bar", x="owner", y="violation_count", ax=ax, legend=False)
    ax.set_title("Top 10 Owners with the Most Violations")
    ax.set_xlabel("Owner")
    ax.set_ylabel("Violation Count")
    plt.xticks(rotation=90)
    st.pyplot(fig)

   # Search by owner name
    st.title("Search by Owner Name")
    owner_name = st.text_input("Enter owner name")
    if owner_name:
        owner_data = search_owner_properties(owner_name)
        st.write(owner_data[['violation_number', 'date', 'description', 'address']])
        
        # Plot the properties with violations on a map using pydeck
        if not owner_data.empty:
            owner_data['latitude'] = owner_data['latitude'].astype(float)
            owner_data['longitude'] = owner_data['longitude'].astype(float)
            
            # Count the number of violations per address
            address_violation_counts = owner_data.groupby(['latitude', 'longitude', 'address']).size().reset_index(name='violation_count')
            
            # Define the color scale based on the number of violations
            address_violation_counts['color'] = address_violation_counts['violation_count'].apply(lambda x: [255, 0, 0] if x == 1 else [255, 165, 0] if x == 2 else [255, 255, 0] if x == 3 else [255, 255, 224])
            
            # Create a pydeck layer
            layer = pdk.Layer(
                'ScatterplotLayer',
                data=address_violation_counts,
                get_position='[longitude, latitude]',
                get_color='color',
                get_radius=25,  # Adjusted size
                pickable=True
            )

            # Set the viewport location
            view_state = pdk.ViewState(
                latitude=42.3601,
                longitude=-71.0589,
                zoom=11,
                pitch=50
            )

            # Render the deck.gl map
            r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "{address}\nViolations: {violation_count}"})
            st.pydeck_chart(r)
