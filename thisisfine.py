# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 16:43:54 2021

@author: USER
"""


import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk

# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide")

##import data
DATE_TIME = "timestart"
df = pd.read_csv('https://raw.githubusercontent.com/thatbeer/odsample/master/20190101.csv')
df2 = pd.read_csv('https://raw.githubusercontent.com/thatbeer/odsample/master/20190102.csv')
df3 = pd.read_csv('https://raw.githubusercontent.com/thatbeer/odsample/master/20190103.csv')
df4 = pd.read_csv('https://raw.githubusercontent.com/thatbeer/odsample/master/20190104.csv')
df5 = pd.read_csv('https://raw.githubusercontent.com/thatbeer/odsample/master/20190105.csv')
##connect df
frame = [df,df2,df3,df4,df5]
data = pd.concat(frame)

##edit table
data.drop(columns=['Unnamed: 0'],inplace=True)
data = data.dropna(axis=1)
data['timestart'] = pd.to_datetime(data['timestart'])
print(data)
data['lat'] = data['latstartl']
data['lon'] = data['lonstartl']
print(data)
# CREATING FUNCTION FOR MAPS

def map(data, lat, lon, zoom):
    st.write(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state={
            "latitude": lat,
            "longitude": lon,
            "zoom": zoom,
            "pitch": 50,
        },
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=data,
                get_position=["lon", "lat"],
                radius=100,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
        ]
    ))

# LAYING OUT THE TOP SECTION OF THE APP
row1_1, row1_2 = st.columns((2,3))

with row1_1:
    st.title("Streamlit with Heroku Bangkok metros using")
    hour_selected = st.slider('Select hour of the interval',0,23)
    #day_selected = st.slider('Select dat of interval',1,5)

with row1_2:
    st.write(
    """
    ##
    This app is made for education in Geospatial Data Science and Analysis subject : Streamlit with Heroku.
    """)


# FILTERING DATA BY HOUR SELECTED
data = data[data[DATE_TIME].dt.hour == hour_selected]
#data = data[(data[DATE_TIME].dt.hour == hour_selected) & data[DATE_TIME].dt.day == day_selected]

# LAYING OUT THE MIDDLE SECTION OF THE APP WITH THE MAPS
row2_1, row2_2, row2_3 = st.columns((3,1,1))

# SETTING THE ZOOM LOCATIONS FOR THE CU
cusvk = [13.738, 100.532]
don =[13.914, 100.605]
zoom_level = 10
midpoint = (np.average(data["lat"]), np.average(data["lon"]))

with row2_1:
    st.write("**Bangkok using metros from %i:00 and %i:00**" % (hour_selected, (hour_selected + 1) % 24))
    map(data, midpoint[0], midpoint[1], 11)

with row2_2:
    st.write("**CHULA**")
    map(data, cusvk[0],cusvk[1], zoom_level)
with row2_3:
    st.write("**DON MUANG**")
    map(data, don[0],don[1], zoom_level)
    
    
    
# FILTERING DATA FOR THE HISTOGRAM
filtered = data[
    (data[DATE_TIME].dt.hour >= hour_selected) & (data[DATE_TIME].dt.hour < (hour_selected + 1))
    ]

hist = np.histogram(filtered[DATE_TIME].dt.minute, bins=60, range=(0, 60))[0]

chart_data = pd.DataFrame({"minute": range(60), "pickups": hist})

# LAYING OUT THE HISTOGRAM SECTION

st.write("")

st.write("**Breakdown of rides per minute between %i:00 and %i:00**" % (hour_selected, (hour_selected + 1) % 24))

st.altair_chart(alt.Chart(chart_data)
    .mark_area(
        interpolate='step-after',
    ).encode(
        x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
        y=alt.Y("pickups:Q"),
        tooltip=['minute', 'pickups']
    ).configure_mark(
        opacity=0.5,
        color='red'
    ), use_container_width=True)
