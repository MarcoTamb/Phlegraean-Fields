"""
Global configuration constants for the dashboard.
"""
from datetime import timedelta

URL_MAIN = '/'
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
APP_TITLE = "Bradyseism Monitor"
GITHUB_URL = 'https://github.com/MarcoTamb/Phlegrean-Fields'

# Time window for historical earthquake data (3650 = ~10 years)
MIN_DATE = timedelta(days=3650)

# Central coordinates for Campi Flegrei caldera
LATITUDE = '40.8270'
LONGITUDE = '14.1420'

# Maximum search radius (in kilometers) from the central coordinates
MAX_DISTANCE_KM = 10

# Rate limit for data refresh in the frontend and cache timeout (1 hour)
UPDATE_SECONDS = 3600
