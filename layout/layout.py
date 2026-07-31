"""
Defines the main application shell and navigation bar[cite: 4].
Contains the global interval timer for automatic data refreshing.
"""
from dash import html, callback, Output, Input, State, page_container, dcc
import dash_bootstrap_components as dbc
from utils.constants import URL_MAIN, GITHUB_URL, PLOTLY_LOGO, MIN_DATE, UPDATE_SECONDS, APP_TITLE
from datetime import date
from dash_iconify import DashIconify

# Calculate the start date based on the MIN_DATE constant for INGV URLs
start_date = date.today() - MIN_DATE
# Define navigation links for the top Navbar
links = [
    dbc.NavItem(dbc.NavLink(
        "Maps",
        href=URL_MAIN,
        className='links'
    )),
    dbc.NavItem(dbc.NavLink(
        "Statistics",
        href='/stats',
        className='links'
    )),
    dbc.NavItem(dbc.NavLink(
        "About",
        href='/about',
        className='links'
    )),
    # Dropdown menu for external INGV resources
    dbc.DropdownMenu(
        children=[
            dbc.DropdownMenuItem("INGV websites", header=True),
            dbc.DropdownMenuItem("INGV Home", href='https://www.ingv.it/'),
            dbc.DropdownMenuItem("INGV Earthquakes", href='https://terremoti.ingv.it/'),
            dbc.DropdownMenuItem("INGV Monitoring",
                                 href='https://www.ov.ingv.it/index.php/monitoraggio-e-infrastrutture/bollettini-tutti'
                                 ),
        ],
        nav=True,
        in_navbar=True,
        label=html.Span("INGV", style={'color': 'var(--bs-nav-link-color)'}),
        className='links'
    ),
    # GitHub repository link with icon
    dbc.NavItem(dbc.NavLink(
        [DashIconify(icon="ion:logo-github", height=25, style={'margin-right': '5px'}), "GitHub"],
        href=GITHUB_URL,
        className='links'
    )),
]

# Main application layout wrapper
app_layout = html.Div(
    [
        # Navigation bar initialization
        dbc.NavbarSimple(
            children=links,
            brand=[html.Img(src=PLOTLY_LOGO, height="30px"), dbc.NavbarBrand(APP_TITLE, className="ms-2")],
            brand_href='/',
            color="dark",
            dark=True,
        ),
        # Placeholder where individual page layouts will be rendered
        page_container,
        # Hidden interval component triggering periodic data updates
        dcc.Interval(
            id='update-data',
            interval=UPDATE_SECONDS * 1000,  # in milliseconds
            n_intervals=0
        ),
        # Store component to hold refresh state across callbacks
        dcc.Store(id='refresh', data=[])
    ],
    className='page'
)


@callback(
    Output('refresh', 'data'),
    Input('update-data', 'n_intervals')
)
def trigger_refresh(interval):
    """
    Updates the 'refresh' store every time the interval triggers.
    Downstream charts use this store as an input to pull fresh data.
    """
    return interval
