"""
pages/home.py: Registers the root path and stitches controls and layout together.
"""
from dash import register_page, html, dcc
import dash_bootstrap_components as dbc
from layout.chart import chart_wrapper
from layout.controls import controls

# Register Dash page route
register_page(__name__, path='/')

# Simple grid implementation mapping the sidebar controls to the main chart wrapper
layout = html.Div(
    children=[
        html.Div(controls, className='controls'),
        html.Div(dcc.Loading(chart_wrapper), className='charts'),
    ],
    className='grid-box',
)
