# %%
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import datetime
import plotly.express as px

# %%
# Load the data
df = pd.read_csv('MVCollisionDataset.csv')
print(df.head)


# %%
# Set page title and layout
st.set_page_config(page_title="NYC Motor Vehicle Collisions", page_icon=":car:", layout="wide")

# %%
print(df.columns)

# %%
# Set up the sidebar
st.sidebar.title("Filters")
time_range = st.sidebar.slider(
    "Time range",
    min_value=pd.to_datetime(df['TIME'], format='%H:%M').min().time(),
    max_value=pd.to_datetime(df['TIME'], format='%H:%M').max().time(),
)
time_range_str = (str(time_range.hour).zfill(2) + ':' + str(time_range.minute).zfill(2),
                  str(time_range.hour).zfill(2) + ':' + str(time_range.minute + 1).zfill(2))
filtered_data = df[
    (pd.to_datetime(df['TIME'], format='%H:%M').dt.strftime('%H:%M').between(*time_range_str))
]


# %%
# Show the map
st.header("Motor Vehicle Collisions in NYC")
st.subheader("Map")
st.markdown("Filtered by date range and borough, if selected")
st.map(filtered_data[['LATITUDE', 'LONGITUDE']].dropna(how="any"))

# %%
def plot_collisions_by_borough(data):
    st.write("Number of Collisions by Borough")
    collisions_by_borough = data["BOROUGH"].value_counts().reset_index()
    collisions_by_borough.columns = ["Borough", "Number of Collisions"]
    collisions_by_borough = collisions_by_borough.sort_values(by="Number of Collisions", ascending=False)
    fig = px.bar(collisions_by_borough, x="Borough", y="Number of Collisions")
    st.plotly_chart(fig)

# %%
def plot_collision_map(data):
    st.write("Location of Collisions")
    tooltip_cols = ["DATE", "TIME", "BOROUGH", "ZIP CODE", "LATITUDE", "LONGITUDE", "NUMBER OF PERSONS INJURED", "NUMBER OF PERSONS KILLED", "CONTRIBUTING FACTOR VEHICLE 1"]
    fig = px.scatter_mapbox(
        data,
        lat="LATITUDE",
        lon="LONGITUDE",
        hover_name="DATE",
        hover_data=tooltip_cols,
        color_discrete_sequence=["red"],
        zoom=9,
        height=600,
    )
    fig.update_layout(mapbox_style="open-street-map")
    st.plotly_chart(fig)

# %%

    plot_collisions_by_borough(df)


    plot_collision_map(df)



# %%
# Show the data table
st.subheader("Data Table")
st.markdown("Filtered by date range and borough, if selected")
st.dataframe(filtered_data[['DATE','TIME', 'BOROUGH', 'ZIP CODE', 'LATITUDE', 'LONGITUDE']])


