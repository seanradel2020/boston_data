import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pydeck as pdk
import numpy as np
""" Example data for crime_reports.csv:
INCIDENT_NUMBER,OFFENSE_CODE,OFFENSE_CODE_GROUP,OFFENSE_DESCRIPTION,DISTRICT,REPORTING_AREA,SHOOTING,OCCURRED_ON_DATE,YEAR,MONTH,DAY_OF_WEEK,HOUR,UCR_PART,STREET,Lat,Long,Location
232007173,3115,,INVESTIGATE PERSON,B3, ,0,2023-01-27 22:44:00+00,2023,1,Friday   ,22,,FAVRE ST,42.271661031027065,-71.09953455161765,"(42.271661031027065, -71.09953455161765)"
232004454,3301,,VERBAL DISPUTE,B2,316,0,2023-01-17 20:21:00+00,2023,1,Tuesday  ,20,,HAROLD ST,42.3125962960786,-71.09287583752645,"(42.3125962960786, -71.09287583752645)"
232006290,3115,,INVESTIGATE PERSON,A1, ,0,2023-01-24 00:00:00+00,2023,1,Tuesday  ,0,,HANOVER ST,42.3656993584582,-71.05289203191269,"(42.3656993584582, -71.05289203191269)"
232024939,3114,,INVESTIGATE PROPERTY,B3, ,0,2023-03-31 17:14:00+00,2023,3,Friday   ,17,,BLUE HILL AVE,42.29278799134922,-71.08851953962399,"(42.29278799134922, -71.08851953962399)"
232006708,423,,ASSAULT - AGGRAVATED,B2, ,0,2023-01-26 09:00:00+00,2023,1,Thursday ,9,,HUTCHINGS ST,42.310268910354935,-71.08931055058088,"(42.310268910354935, -71.08931055058088)"


"""


def crime_reports():
    st.title('Crime Reports Heatmap')

    # Load the crime reports data
    crime_reports_csv_path = 'crime_reports.csv'
    crime_reports_data = pd.read_csv(crime_reports_csv_path)

    # Extract latitude and longitude columns
    crime_reports_data = crime_reports_data.dropna(subset=['Lat', 'Long'])

    # Rename columns to match expected names
    crime_reports_data.rename(columns={'Lat': 'latitude', 'Long': 'longitude'}, inplace=True)
 
    crime_reports_data['OFFENSE_DESCRIPTION'] = crime_reports_data['OFFENSE_DESCRIPTION'].str.upper()

    # Create a color mapping for each offense code
    def get_color(offense_code):
        if 111 <= offense_code <= 611:
            return [255, 0, 0]  # Red
        elif 611 < offense_code <= 1000:
            return [255, 165, 0]  # Orange
        elif 1000 < offense_code <= 1825:
            return [255, 255, 0]  # Yellow
        else:
            return [255, 255, 224]  # Light Yellow (White-Yellow)

    offense_codes = crime_reports_data['OFFENSE_CODE'].unique()
    color_map = {code: get_color(code) for code in offense_codes}

    # Add color column to the data
    crime_reports_data['color'] = crime_reports_data['OFFENSE_CODE'].map(color_map)

    # Sidebar for color selection
    st.sidebar.title("Filter Offenses by Color")
    color_options = {
        "Red (111-611)": [255, 0, 0],
        "Orange (612-1000)": [255, 165, 0],
        "Yellow (1001-1825)": [255, 255, 0],
        "Light Yellow (1826 and above)": [255, 255, 224]
    }
    selected_colors = st.sidebar.multiselect(
        "Select Colors to Display",
        options=list(color_options.keys()),
        default=list(color_options.keys())
    )

    # Filter data based on selected colors
    selected_color_values = [color_options[color] for color in selected_colors]
    filtered_data = crime_reports_data[crime_reports_data['color'].apply(lambda x: x in selected_color_values)]

    # Create a pydeck layer
    layer = pdk.Layer(
        'ScatterplotLayer',
        data=filtered_data,
        get_position='[longitude, latitude]',
        get_color='color',
        get_radius=10,  # Adjusted size
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
    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "{OFFENSE_DESCRIPTION}\nDate: {OCCURRED_ON_DATE}"}
    )
    st.pydeck_chart(r)

    # Display the color key
    st.write("Color Key:")
    for code in sorted(color_map.keys()):
        color = color_map[code]
        color_hex = '#%02x%02x%02x' % tuple(color)
        description = crime_reports_data[crime_reports_data['OFFENSE_CODE'] == code]['OFFENSE_DESCRIPTION'].iloc[0]
        count = crime_reports_data[crime_reports_data['OFFENSE_CODE'] == code].shape[0]
        st.markdown(f"<span style='color:{color_hex};'>■</span> Offense Code {code}: {description} ({count} occurrences)", unsafe_allow_html=True)
