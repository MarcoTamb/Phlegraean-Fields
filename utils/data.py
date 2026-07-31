"""
Handles data ingestion and transformation from the INGV earthquake API.
"""
import requests
from datetime import date
import pandas as pd
from io import StringIO
from geopy import distance
from utils.constants import MIN_DATE, LATITUDE, LONGITUDE, MAX_DISTANCE_KM
from utils.cache import cache

# Calculate the earliest date to fetch based on MIN_DATE constant
start_date = date.today() - MIN_DATE


def get_y(coordinates):
    """
    Calculates the North/South offset in kilometers from the central latitude.
    Positive values indicate North; negative values indicate South.
    """
    if float(coordinates[0]) > float(LATITUDE):
        return distance.distance(coordinates, (LATITUDE, coordinates[1])).kilometers
    else:
        return - distance.distance(coordinates, (LATITUDE, coordinates[1])).kilometers


def get_x(coordinates):
    """
    Calculates the East/West offset in kilometers from the central longitude.
    Positive values indicate East; negative values indicate West.
    """
    if float(coordinates[1]) > float(LONGITUDE):
        return distance.distance(coordinates, (coordinates[0], LONGITUDE)).kilometers
    else:
        return - distance.distance(coordinates, (coordinates[0], LONGITUDE)).kilometers


# Cache the output of this function to avoid hammering the INGV API.
# The cache timeout is managed by the default timeout in cache.py (3600s).
@cache.memoize()
def get_earthquake_data():
    """
    Fetches raw earthquake data from the INGV API, handles fallback to local CSV
    on failure, and computes Cartesian offsets for 3D mapping.
    """
    print("Fetching fresh data from INGV...")
    try:
        # Construct the API query using defined constants
        query = f'https://webservices.ingv.it/fdsnws/event/1/query?starttime={start_date.strftime("%Y-%m-%d")}T00%3A00%3A00&endtime={date.today().strftime("%Y-%m-%d")}T23%3A59%3A59&minmag=-1&maxmag=10&mindepth=-10&maxdepth=1000&orderby=time-asc&lat={LATITUDE}&lon={LONGITUDE}&maxradiuskm={MAX_DISTANCE_KM}&format=text'

        # Execute request with a 20-second timeout
        data_query = requests.get(query, timeout=20)
        data_query.raise_for_status()  # Raises an error for 404, 500 status codes

        # Parse the pipe-separated text response into a DataFrame
        df = pd.read_csv(StringIO(data_query.text), sep='|', parse_dates=['Time'])
        print("Success!")

        # uncomment to update the fall-back csv file
        # df.to_csv('query.csv', sep='|', index=False)
    except Exception as e:
        # Fallback mechanism: load from local CSV if API is unreachable
        # print exception in terminal
        print(f"INGV API fetch failed: {e}")
        # read fallback csv
        df = pd.read_csv('query.csv', sep='|', parse_dates=['Time'])

    # Invert depth values so that underground depths are represented negatively on the Z-axis
    df['Depth/Km'] = -df['Depth/Km']

    # Combine coordinates for distance processing
    df['latitude_longitude'] = list(zip(df.Latitude, df.Longitude))
    # Calculate Cartesian X and Y offsets (in km) relative to the epicenter
    df['x_position'] = df['latitude_longitude'].apply(get_x)
    df['y_position'] = df['latitude_longitude'].apply(get_y)

    return df
