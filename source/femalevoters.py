import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pydeck as pdk
import numpy as np
import requests

#https://data.boston.gov/api/3/action/datastore_search?resource_id=904a8bef-a278-42ce-81e0-afeb9222e5a4&limit=5

"""
Ward Book	Volume	Page Number	Date	Ward	Precinct	Name	Street of Residence as of May 1	Street Number on May 1	Unit	Age	Country of Birth	State/Province of Birth	County of Birth	Town of Birth	Occupation
25	VC73	1	1897-11-30	25	7	Charlotte Adams	Bentley Street	15		56	United States of America	Iowa		Iowa City	Teacher
25	VC73	1	1898-11-21	25	3	Edna M. Ames	Linden Street	77		23	United States of America	Massachusetts		Boxford	Clerk
25	VC73	1	1898-11-22	25	1	Sarah E. Adams	Aldie Street	50		42	United States of America	Massachusetts		Boston	Teacher
25	VC73	1	1898-11-23	25	6	Amelia E. Adams	Newton Street	36		38	United States of America	Massachusetts		Lowell	none
25	VC73	1	1899-10-16	25	3	Luella Thayer Ames 	Dustin Street	43		31	United States of America	Maine		Richmond	wife
25	VC73	1	1899-11-20	25	1	Anna M. Allen	Amboy Street	7		46	United States of America	New Jersey		Newark	wife
25	VC73	1	1899-11-21	25	1	Mary E. Adams	Aldie Street	62		46	United States of America	Massachusetts		Mansfield	Wife
25	VC73	1	1900-11-17	25	3	Louisa H. Abbott	Quint Avenue	10		38	United States of America	Massachusetts		Boston 	none
25	VC73	1	1900-11-19	25	2	Frances Orcutt 	Mansfield [Street]	44		30	United States of America	Maine		St. George	Wife
25	VC73	1	1900-11-20	25	5	Juliett Akin 	Foster [Street?]	35		55	United States of America	Maine		Smithfield	wife
25	VC73	1	1900-11-21	25	3	Clara D. Ayer	Dustrin [Street]	49		59	United States of America	New Hampshire		Conway 	widow
25	VC73	1	[1902]-11-[08]	25	5	Clara E. Ellis	Oakland Street	9		48	United States of America	Maine		Sebec	Wife
25	VC73	1	[1902]-11-10	25	4	Mary E. Allen	North Beacon Street	43		39	United States of America	Massachusetts		Sheffield	housewife
25	VC73	1	[1902]-11-19	25	7	Charlotte Adams	Academy Hill Road	34		61	United States of America	Iowa		Iowa City	Teacher
25	VC73	1	[1902]-11-19	25	7	Georgie E. Ayer	Nantasket Avenue	4		45	United States of America	New Hampshire		Manchester	Bookkeeper
25	VC73	1	[1902]-11-19	25	3	E. Maud Alwater	Reedsdale Street	6		41	United States of America	Ohio		Massillon	housekeeper
25	VC73	1	1903-11-13	25	1	Vesta E. Adams	Holton Street	36		49	United States of America	Ohio		Marietta	none
25	VC73	1	1903-11-17	25	4	Ella J. Atwood	Waverly Street	44		40	United States of America	Massachusetts		Cambridge	Wife
25	VC73	2	1888-11-27	25	1	Ellen E. Byrne 	Waverly Street	77							
25	VC73	2	1888-11-27	25	3	Katie Barry 	Eastburn [Street]	12		23	United States of America	Massachusetts		Brighton 	Clerk 
25	VC73	2	1892-11-29	25	5	Estella Bacon	Cambridge [Street?]	*		35	United States of America	Wisconsin 		Princeton 	Housekeeper
25	VC73	2	1897-11-30	25	2	Anna M. Bickford	Cambridge [Street?]	391		45	United States of America	Massachusetts		Brighton 	Housewife
25	VC73	2	1897-12-01	25	1	Emma J.B. Brooks	Hopedale Street	13		32	United States of America	Massachusetts		Boston	wife
25	VC73	2	1898-11-18	25	4	Maria Byrne 	Waverly Street	56		44	United States of America	Massachusetts		Brighton 	wife
25	VC73	2	1898-11-21	25	5	Margaret Byrns	Market Street	285		39	United States of America	Massachusetts		Brighton 	wife

"""
#https://data.boston.gov/dataset/women-s-voter-registers-1884-1919/resource/904a8bef-a278-42ce-81e0-afeb9222e5a4
# Define the API endpoint
API_URL = "https://data.boston.gov/api/3/action/datastore_search"
RESOURCE_ID = "904a8bef-a278-42ce-81e0-afeb9222e5a4"  

def get_voter_data():
    # Query the API to get the data
    params = {
        "resource_id": RESOURCE_ID,
        "limit": 400000  # Adjust the limit as needed
    }
    response = requests.get(API_URL, params=params)
    data = response.json()
    return data["result"]["records"]

def occupation_count():
    # Get the voter data
    data = get_voter_data()
    
    # Convert the data to a DataFrame
    df = pd.DataFrame(data)
    
    # Extract the occupation information
    occupations = df['Occupation'].dropna()
    
    # Calculate the count of each occupation
    occupation_counts = occupations.value_counts()
    
    return occupation_counts

def female_voters():
    # Streamlit app
    st.title("Occupation Count of Registered Female Voters")

    # Get the occupation count
    occupation_counts = occupation_count()

    # Display the occupation count data
    st.write("Occupation Count")
    st.write(occupation_counts)

    # Plot the occupation count data as a pie chart
    st.write("Occupation Count Distribution")
    fig, ax = plt.subplots()
    occupation_counts.plot(kind='pie', ax=ax, autopct='%1.1f%%', startangle=90)
    ax.set_ylabel("")
    ax.set_xlabel("")
    ax.set_title("Occupation Distribution")
    st.pyplot(fig)