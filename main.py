"""
Entry point for the Bradyseism Monitor Dash application.
Initializes the app, configures the UI theme, sets up routing, and binds the cache.
"""

from layout.layout import app_layout
from utils.constants import APP_TITLE
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash import Dash
from utils.cache import cache

# Define external CSS stylesheets, using Bootstrap Darkly theme for styling
stylesheets = [
    dbc.themes.DARKLY
]

# Initialize a multi-page Dash application
app = Dash(__name__, external_stylesheets=stylesheets, use_pages=True)

# Initialize the cache
cache.init_app(app.server)

# Wrap the main layout in a MantineProvider to allow for Dash Mantine Components theming
app.layout = dmc.MantineProvider(
    theme={},
    children=app_layout
)

# Set the browser tab title
app.title = APP_TITLE

# Expose the Flask server for deployment
server = app.server

if __name__ == '__main__':
    print('Running app')
    app.run(debug=True)
