# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 15:48:35 2021

@author: USER
"""

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk
#import geopandas as gp
#import folium as fo
#import pyproj
#from streamlit_folium import folium_static


# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide")


##import data
df = pd.read_csv('https://raw.githubusercontent.com/thatbeer/odsample/master/20190101.csv')
df2 = pd.read_csv('https://raw.githubusercontent.com/thatbeer/odsample/master/20190102.csv')
df3 = pd.read_csv('https://raw.githubusercontent.com/thatbeer/odsample/master/20190103.csv')
df4 = pd.read_csv('https://raw.githubusercontent.com/thatbeer/odsample/master/20190104.csv')
df5 = pd.read_csv('https://raw.githubusercontent.com/thatbeer/odsample/master/20190105.csv')
##connect df
frame = [df,df2,df3,df4,df5]
dfs = pd.concat(frame)

##edit table
dfs.drop(columns=['Unnamed: 0'],inplace=True)
dfs = dfs.dropna(axis=1)
dfs['timestart'] = pd.to_datetime(dfs['timestart'])
dfs['timestop'] = pd.to_datetime(dfs['timestop'])

st.title('Geodata')
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
                elevation_scale=50,
                elevation_range=[0, 3000],
                pickable=True,
                extruded=True,
            ),
        ]
    ))

# LAYING OUT THE TOP SECTION OF THE APP
row1_1, row1_2 = st.columns((2,3))

with row1_1:
    st.title("CUSV CORS DATA")
    hour_selected = st.slider('Select hour of the interval',0,23)

with row1_2:
    st.write(
    """
    ##
    test
    test.
    """)

# FILTERING DATA BY HOUR SELECTED
dfs = dfs[dfs['timestart'].dt.hour == hour_selected]

# LAYING OUT THE MIDDLE SECTION OF THE APP WITH THE MAPS
row2_1, row2_2, row2_3, row2_4 = st.columns((2,1,1,1))

# SETTING THE ZOOM LOCATIONS FOR THE CU
cusvk = [13.738, 100.532]
zoom_level = 12
midpoint = (np.average(dfs["latstartl"]), np.average(dfs["lonstartl"]))

with row2_1:
    st.write("**CUSV SIGNAL %i:00 and %i:00**" % (hour_selected, (hour_selected + 1) % 24))
    map(dfs, midpoint[0], midpoint[1], 11)

with row2_2:
    st.write("**CUSV**")
    map(dfs, cusvk[0],cusvk[1], zoom_level)

# FILTERING DATA FOR THE HISTOGRAM
filtered = dfs[
    (dfs['timestart'].dt.hour >= hour_selected) & (dfs['timestart'].dt.hour < (hour_selected + 1))
    ]

hist = np.histogram(filtered['timestart'].dt.minute, bins=60, range=(0, 60))[0]

chart_data = pd.DataFrame({"minute": range(60), "Data": hist})




# LAYING OUT THE HISTOGRAM SECTION

st.write("LOWW")

st.write("**just test bluh between %i:00 and %i:00**" % (hour_selected, (hour_selected + 1) % 24))

st.altair_chart(alt.Chart(chart_data)
    .mark_area(
        interpolate='step-after',
    ).encode(
        x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
        y=alt.Y("data:Q"),
        tooltip=['minute', 'data']
    ).configure_mark(
        opacity=0.5,
        color='red'
    ), use_container_width=True)














