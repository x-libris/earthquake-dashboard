The Earthquake Dashboard application utilizes real-time USGS data to generate figures on recent earthquakes.
The user can choose to see earthquakes from various timeframes (last hour, last week, etc.), and the application will
generate an interactive table, as well as downloadable plots on global distribution and magnitude/depth distribution.

The application uses the following dataset recoverable from Natural Earth to generate its global distribution plot:
https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/110m/cultural/ne_110m_admin_0_countries.zip

USGS data is recovered from the feeds available by its Earthquake Hazards Program:
https://earthquake.usgs.gov/earthquakes/feed/v1.0/csv.php

Python libraries required to run the application:
- requests
- pandas
- geopandas
- matplotlib
- streamlit
- io (in standard library)
- datetime (in standard library)

How to Use:

1) Install dependencies: Using pip, install the required libraries listed above. Dependencies can also be installed from the 'requirements.txt' file.
2) Run the app: Navigate to the directory containing the app script (e.g., eq_dashboard.py) and run the following command in your terminal: streamlit run eq_dashboard.py
   * please ensure that the extracted folder from Natural Earth is in the same directory as eq_dashboard.py
