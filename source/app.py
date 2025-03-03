import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from crime import *
from shootings import *
from gunrecovery import *

def home():
    st.title('Home')
    st.write("Welcome to the Boston Shootings and Gun Recovery Data App!")


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