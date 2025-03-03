import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def shootings_data_page():
    st.title('Boston Shootings Data')

    # Load the shootings data
    shootings_csv_path = '../data/shootings.csv'
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
