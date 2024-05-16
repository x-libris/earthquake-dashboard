import requests
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import io
import streamlit as st
import datetime

usgs_links= [
  'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv',
  'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.csv',
  'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.csv',
  'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.csv',
]

def get_usgs_data(links: dict):
  dataframes = []
  
  for link in links: # Retrieve data from USGS links, convert to dataframe, filter/sort, and append to master list.
    if requests.get(link).status_code == 200:
      eq_data = pd.read_csv(io.BytesIO(requests.get(link).content)) # io.BytesIO() to avoid saving new CSV files 
      eq_data = eq_data[eq_data['type'] == 'earthquake']
      eq_data = eq_data[['time', 'latitude', 'longitude', 'depth', 'mag', 'place']]
      eq_data = eq_data.sort_values(by=['time'], ascending=False)
      eq_data.columns = eq_data.columns.str.upper()
      dataframes.append(eq_data)
    else:
      return None
  # Return dataframes from master list as dictionary for easier access with st.selectbox() // easier indexing.
  eqdf_dict = {
    'Last month' : dataframes[0],
    'Last week' : dataframes[1],
    'Last day' : dataframes[2],
    'Last hour' : dataframes[3],
  }

  return eqdf_dict

def get_map_dist(df: pd.DataFrame, freq: str, time: datetime):
  fig, ax = plt.subplots()
  # Load worldmap shape file from https://www.naturalearthdata.com/downloads/110m-cultural-vectors/
  countries = gpd.read_file('./ne_110m_admin_0_countries')
  countries.plot(color="lightgrey", ax=ax)
  # Generate scatter plot from lat/long data over worldmap.
  df.plot(x="LONGITUDE", y="LATITUDE", kind="scatter", c="MAG", colormap="Reds", 
          title=f"Global Distribution of Earthquakes ({freq})", ax=ax)
  plt.figtext(0.5, 0.01, f"Generated from data recovered at {time}", wrap=True, 
              horizontalalignment='center', fontsize=12)

  return plt

def get_mag_vs_depth(df: pd.DataFrame, freq: str, time: datetime):
  fig, ax = plt.subplots()

  df.plot(x="MAG", y="DEPTH", kind="scatter", c="MAG", colormap="Reds", 
          title=f"Magnitude vs Depth ({freq})", ax=ax)
  ax.set_ylabel("DEPTH (kilometers)")
  ax.grid(visible=True, which='major')
  plt.figtext(0.5, -0.01, f"Generated from data recovered at {time}", wrap=True, 
              horizontalalignment='center', fontsize=12)
  ax.invert_yaxis() # Invert axis to demonstrate depth more intuitively

  return plt

def main():
  st.title("Earthquake Dashboard")
  data_fetch_time = ''

  if 'eq_data' not in st.session_state: # Load USGS data only once per session state
    with st.spinner('Fetching data on recent earthquakes...'):
      st.session_state.eq_data = get_usgs_data(usgs_links)
      data_fetch_time = datetime.datetime.now() # Data collection timestamp for figures
    if type(st.session_state.eq_data) == type(None):
      st.write('There was an error connecting to the database. Please reload webpage and try again.')
  
  st.write(f'Data fetched from USGS live feed successfully at {data_fetch_time}')
  
  freq = st.selectbox(label='See earthquakes from...', options=list(st.session_state.eq_data.keys()), 
                      placeholder='Select frequency...', index=None)
      
  if freq is not None:
    st.header(f'Displaying data from {freq}')

    with st.spinner('Generating figures...'):

      col1, col2 = st.columns(2, gap='medium') 

      with col1:
        st.pyplot(get_map_dist(st.session_state.eq_data[freq], freq, data_fetch_time))

      with col2:
        st.pyplot(get_mag_vs_depth(st.session_state.eq_data[freq], freq, data_fetch_time))

      st.dataframe(st.session_state.eq_data[freq])

# Run application:
main()
