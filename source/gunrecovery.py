import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def gun_recovery_data_page():
    st.title('Gun Recovery Data')

    # Load the gun recovery data
    gunrecovery_csv_path = '../data/gunrecovery.csv'
    gunrecovery_data = pd.read_csv(gunrecovery_csv_path)

    # Convert dates to datetime and ensure same timezone
    gunrecovery_data['collection_date'] = pd.to_datetime(gunrecovery_data['collection_date']).dt.tz_localize(None)

    # Display the gun recovery DataFrame
    st.write(gunrecovery_data)

    # Aggregate data to get total guns collected per year
    gunrecovery_data['year'] = gunrecovery_data['collection_date'].dt.year
    total_guns_collected = gunrecovery_data.groupby('year')[['crime_guns_recovered', 'guns_recovered_safeguard', 'buyback_guns_recovered']].sum()
    total_guns_collected['total_guns_collected'] = total_guns_collected.sum(axis=1)

    # Plot the total guns collected per year as a bar graph
    fig, ax = plt.subplots()
    total_guns_collected['total_guns_collected'].plot(kind='bar', ax=ax)
    ax.set_title('Total Guns Collected Per Year')
    ax.set_xlabel('Year')
    ax.set_ylabel('Total Guns Collected')
    st.pyplot(fig)

    # Load the shootings data for correlation analysis
    shootings_csv_path = '../data/shootings.csv'
    shootings_data = pd.read_csv(shootings_csv_path)

    # Calculate the number of gun deaths
    gun_deaths = shootings_data[shootings_data['shooting_type_v2'] == 'Fatal'].groupby('shooting_date').size()
    gun_deaths = gun_deaths.reset_index(name='gun_deaths')
    gun_deaths['shooting_date'] = pd.to_datetime(gun_deaths['shooting_date']).dt.tz_localize(None)

    # Merge gun deaths with gun recovery data on collection_date
    merged_data = pd.merge(gunrecovery_data, gun_deaths, left_on='collection_date', right_on='shooting_date', how='left').fillna(0)

    # Aggregate data to get total shootings per year
    shootings_data['year'] = pd.to_datetime(shootings_data['shooting_date']).dt.year
    total_shootings = shootings_data.groupby('year').size().reset_index(name='total_shootings')

    # Merge the aggregated data
    yearly_data = pd.merge(total_guns_collected['total_guns_collected'], total_shootings, on='year', how='outer').fillna(0)

    # Plot the total guns collected and total shootings per year as a bar graph
    fig, ax = plt.subplots()
    width = 0.35  # the width of the bars
    ax.bar(yearly_data['year'] - width/2, yearly_data['total_guns_collected'], width, label='Total Guns Collected')
    ax.bar(yearly_data['year'] + width/2, yearly_data['total_shootings'], width, label='Total Shootings', color='red')
    ax.set_title('Total Guns Collected and Total Shootings Per Year')
    ax.set_xlabel('Year')
    ax.set_ylabel('Count')
    ax.legend()
    st.pyplot(fig)
