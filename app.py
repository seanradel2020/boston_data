import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from crime import *

def home():
    st.title('Home')
    st.write("Welcome to the Boston Shootings and Gun Recovery Data App!")

def shootings_data_page():
    st.title('Boston Shootings Data')

    # Load the shootings data
    shootings_csv_path = 'shootings.csv'
    shootings_data = pd.read_csv(shootings_csv_path)

    # Add a column for Hispanic victims
    shootings_data['Hispanic'] = shootings_data['victim_ethnicity_nibrs'].apply(lambda x: 'Hispanic' if x != 'Not Hispanic or Latinx' else 'Not Hispanic')

    # Display the shootings DataFrame
    st.write(shootings_data)

    # Filter data for Black or African American, White, and Hispanic victims
    race_counts = shootings_data['victim_race'].value_counts()
    hispanic_count = shootings_data['Hispanic'].value_counts().get('Hispanic', 0)
    race_counts['Hispanic'] = hispanic_count

    # Plot the data for race and ethnicity
    fig, ax = plt.subplots()
    race_counts.plot(kind='bar', ax=ax)
    ax.set_title('Number of Victims by Race and Ethnicity Since 2015')
    ax.set_xlabel('Race/Ethnicity')
    ax.set_ylabel('Number of Victims')
    st.pyplot(fig)

    # Filter data for gender
    gender_counts = shootings_data['victim_gender'].value_counts()

    # Plot the data for gender
    fig, ax = plt.subplots()
    gender_counts.plot(kind='bar', ax=ax)
    ax.set_title('Number of Victims by Gender Since 2015')
    ax.set_xlabel('Gender')
    ax.set_ylabel('Number of Victims')
    st.pyplot(fig)

def gun_recovery_data_page():
    st.title('Gun Recovery Data')

    # Load the gun recovery data
    gunrecovery_csv_path = 'gunrecovery.csv'
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
    shootings_csv_path = 'shootings.csv'
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


def main():
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Shootings Data", "Gun Recovery Data", "Crime Map"])

    # Page selection
    if page == "Home":
        home()
    elif page == "Shootings Data":
        shootings_data_page()
    elif page == "Gun Recovery Data":
        gun_recovery_data_page()
    elif page == "Crime Map":
        crime_reports()

if __name__ == '__main__':
    main()