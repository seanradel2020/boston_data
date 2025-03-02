import streamlit as st
import pandas as pd

def main():
    st.title('Boston Shootings Data')

    # Sample CSV data
    csv_file_path = 'shootings.csv'
    data = pd.read_csv(csv_file_path)

    # Display the DataFrame
    st.write(data)

if __name__ == '__main__':
    main()