"""
Defines the sidebar control components for filtering data on the main Maps page.
"""
from dash import html, callback, Input, Output
import dash_mantine_components as dmc
from utils.constants import MIN_DATE
from datetime import date, timedelta

controls = html.Div([
    # Selector for the type of map visualization
    dmc.SegmentedControl(
        id="map-type",
        data=['3D-Map', 'Heatmap', 'Vertical E/W', 'Vertical N/S'],
        value='3D-Map',
        fullWidth=True
    ),
    html.P(),
    html.H5("Dates:"),
    # Slider controlling the time window of earthquakes shown
    dmc.RangeSlider(id="last-date",
                    value=[9 * int(MIN_DATE.days / 10), MIN_DATE.days],
                    min=0,
                    max=MIN_DATE.days,
                    step=1,
                    minRange=7,  # Require at least a 7-day span
                    className='slider_shortbottom'
                    ),
    html.P(id='first-date-text', children='First:'),
    html.P(id='last-date-text', children='Last:'),
    html.H5("Minimum Magnitude:"),
    # Slider filtering out earthquakes below a certain magnitude threshold
    dmc.Slider(id='min-magnitudo',
               value=0,
               min=0,
               max=4,
               marks=[
                   {"value": 0, "label": "0"},
                   {"value": 1, "label": "1"},
                   {"value": 2, "label": "2"},
                   {"value": 3, "label": "3"},
                   {"value": 4, "label": "4"},
               ],
               step=0.1,
               className='slider'
               # tooltip={"template": "minimum magnitudo {value}", "placement": "top", "always_visible": False}
               ),
    html.P(),

    html.H5("Depth (km):"),
    # Slider filtering earthquakes by vertical depth
    dmc.RangeSlider(id="depth-km",
                    min=-7.5,
                    max=0,
                    step=0.1,
                    value=[-7.5, 0],
                    minRange=0.5,
                    className='slider'
                    ),
], className='controlsbox')


@callback(
    Output('first-date-text', 'children'),
    Output('last-date-text', 'children'),
    Input('last-date', 'value'),
)
def update_date(slider_value):
    """
    Translates integer slider values into human-readable date strings.
    """
    first_date = ((date.today() - MIN_DATE) + timedelta(days=slider_value[0])).strftime('%Y-%m-%d')
    last_date = ((date.today() - MIN_DATE) + timedelta(days=slider_value[1])).strftime('%Y-%m-%d')
    return f'First: {first_date}', f'Last: {last_date}'
