"""
Initializes the caching mechanism for the Dash application.
Uses the local filesystem to store cached data, reducing redundant API calls.
"""

from flask_caching import Cache
from utils.constants import UPDATE_SECONDS

# Configure Flask-Caching to use a local directory ('cache-directory')
cache = Cache(config={
    'CACHE_TYPE': 'FileSystemCache',
    'CACHE_DIR': 'cache-directory',
    'CACHE_DEFAULT_TIMEOUT': UPDATE_SECONDS  # 3600 seconds = 1 hour rate limit - check constants.py file
})
