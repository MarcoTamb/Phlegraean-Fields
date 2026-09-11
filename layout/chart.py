"""
Handles the generation of all map-based Plotly figures (3D, Heatmap, Scatter) used in the homepage.
Includes image processing for the surface map overlay.
"""
from dash import dcc, html, callback, Output, Input, ctx, State
import plotly.express as px
import pandas as pd
from utils.data import get_earthquake_data, LATITUDE, LONGITUDE
from utils.constants import MIN_DATE
import plotly.graph_objects as go
import numpy as np
from skimage import io
from skimage.color import rgb2gray
from skimage.transform import rescale
from datetime import timedelta, date, datetime

x_axis_range = [10, -10]
y_axis_range = [10, -10]

# --- Image Processing for 3D Surface Map ---
# Load, grayscale, and scale down the surface image overlay
original = io.imread('assets/map.png')[:, :, :3]
img = rgb2gray(original)
img = rescale(img, 0.7, anti_aliasing=True)

# Generate coordinate meshes mapped to image dimensions
xx = np.linspace(y_axis_range[0], y_axis_range[1], img.shape[1])
yy = np.linspace(x_axis_range[0], x_axis_range[1], img.shape[0])
zz = np.zeros(img.shape[:2])

# Custom grayscale color mapping
pl_grey = [[0.0, 'rgb(0, 0, 0)'],
           [0.05, 'rgb(13, 13, 13)'],
           [0.1, 'rgb(29, 29, 29)'],
           [0.15, 'rgb(45, 45, 45)'],
           [0.2, 'rgb(64, 64, 64)'],
           [0.25, 'rgb(82, 82, 82)'],
           [0.3, 'rgb(94, 94, 94)'],
           [0.35, 'rgb(108, 108, 108)'],
           [0.4, 'rgb(122, 122, 122)'],
           [0.45, 'rgb(136, 136, 136)'],
           [0.5, 'rgb(150, 150, 150)'],
           [0.55, 'rgb(165, 165, 165)'],
           [0.6, 'rgb(181, 181, 181)'],
           [0.65, 'rgb(194, 194, 194)'],
           [0.7, 'rgb(206, 206, 206)'],
           [0.75, 'rgb(217, 217, 217)'],
           [0.8, 'rgb(226, 226, 226)'],
           [0.85, 'rgb(235, 235, 235)'],
           [0.9, 'rgb(243, 243, 243)'],
           [0.95, 'rgb(249, 249, 249)'],
           [1.0, 'rgb(255, 255, 255)']]

surfcolor = np.fliplr(img)

# Create the surface trace that acts as "ground level" (Z=0) in 3D plots
map_trace = go.Surface(go.Surface(x=xx,
                                  y=yy,
                                  z=zz,
                                  surfacecolor=surfcolor,
                                  colorscale=pl_grey,
                                  showscale=False,
                                  opacity=0.6,
                                  hovertemplate='E/W offset (km): %{x}<br>N/S offset (km): %{y}<br>%Depth (km): %{z}<extra></extra>'
                                  ))

# Default blank figure to prevent bugs before data loads/if data doesn't load
blank = go.Figure(go.Scatter(x=[], y=[]))
blank.update_layout(template=None)
blank.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
blank.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)
blank.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
})

# UI Wrapper for the chart
chart_wrapper = html.Div(
    [
        html.H6(id='description', className='chart-title'),
        html.Div(
            dcc.Graph(
                id='3d-chart',
                figure=blank,
                className='main-chart'
            ),
        )
    ]
)


@callback(
    Output(component_id='3d-chart', component_property='figure'),
    Input(component_id='map-type', component_property='value'),
    Input(component_id='min-magnitudo', component_property='value'),
    Input(component_id='last-date', component_property='value'),
    Input(component_id='depth-km', component_property='value'),
    Input('refresh', 'data'),
)
def update_chart(chart_type, min_magnitude, last_date_slider, depth, refresh_data):
    """
    Main routing callback for generating maps based on active UI controls.
    Applies Pandas masking to filter out unwanted dates, magnitudes, or depths.
    """
    first_date = (date.today() - MIN_DATE) + timedelta(days=last_date_slider[0])
    last_date = (datetime.now() - MIN_DATE) + timedelta(days=last_date_slider[1])

    # Retrieve cached data and apply all control filters
    chart_data = get_earthquake_data().copy()
    mask = (
            (chart_data['Magnitude'] > min_magnitude) &
            (chart_data['Time'] > pd.to_datetime(first_date)) &
            (chart_data['Time'] <= pd.to_datetime(last_date)) &
            (chart_data['Depth/Km'] > depth[0]) &
            (chart_data['Depth/Km'] <= depth[1])
    )
    chart_data = chart_data[mask]

    # Generate the appropriate figure based on selected segmented control
    if chart_type == '3D-Map':
        chart = three_d_chart(chart_data)
        chart.update_layout(uirevision='true', font=dict(color="white"), plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)')
    elif chart_type == 'Heatmap':
        chart = heatmap(chart_data)
        chart.update_layout(uirevision='true', font=dict(color="white"), plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)')
    elif chart_type in ['Vertical E/W', 'Vertical N/S']:
        chart = vertical(chart_data, chart_type[-3:])
        chart.update_layout(uirevision='true', font=dict(color="white"), plot_bgcolor='rgba(128,128,128,10)',
                            paper_bgcolor='rgba(0,0,0,0)')
    else:
        chart = []

    return chart


def three_d_chart(chart_data, camera_status=dict(
    up=dict(x=-0, y=1, z=1),
    center=dict(x=0, y=0, z=-1),
    eye=dict(x=0, y=10, z=5)
)):
    """
    Generates a 3D scatter plot of earthquake epicenters.
    The Z-axis represents depth, while X and Y represent geographical offsets.
    """
    # Create the base 3D scatter plot
    fig = px.scatter_3d(
        chart_data,
        x='x_position',
        y='y_position',
        z='Depth/Km',
        size='Magnitude',
        color='Magnitude',
        range_color=[0, 5],
        labels={
            'x_position': 'E/W offset (km)',
            'y_position': 'N/S offset (km)',
            'Depth/Km': 'Depth (km)',
            'Magnitude': 'Magnitude',
            'Time': 'Time',
            '#EventID': 'EventID',
        },
        hover_data=["Time"]
    )

    # Configure the scene dimensions and aspect ratio to stretch the horizontal plane
    fig.update_layout(
        scene=dict(
            xaxis=dict(range=x_axis_range, ),
            yaxis=dict(range=y_axis_range),
            zaxis=dict(range=[-7.5, 0]),
            aspectratio={'x': 8, 'y': 8, 'z': 3}
        ),
        margin=dict(r=0, l=0, b=0, t=0)
    )

    # Overlay the pre-processed grayscale surface map (ground level)
    fig.add_trace(map_trace)

    # Set the initial camera angle for a clear view of the subsurface
    fig.update_layout(
        scene_camera=camera_status
    )

    return fig


def heatmap(chart_data):
    """
    Generates a 2D Mapbox density heatmap of earthquakes based on magnitude and frequency.
    """
    fig = px.density_mapbox(chart_data,
                            lat='Latitude',
                            lon='Longitude',
                            z='Magnitude',
                            radius=10,
                            center=dict(
                                lat=float(LATITUDE),
                                lon=float(LONGITUDE),
                            ),
                            zoom=12,
                            mapbox_style="open-street-map",
                            labels={
                                'x_position': 'E/W offset (km)',
                                'y_position': 'N/S offset (km)',
                                'Depth/Km': 'Depth (km)',
                                'Magnitude': 'Magnitude',
                                'Time': 'Time',
                                '#EventID': 'EventID',
                            },
                            hover_data=["Time"]
                            )
    # Minimize margins to maximize map real estate
    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
    )
    return fig


def vertical(chart_data, axis_choice):
    """
    Generates a 2D vertical cross-section (depth profile) of the earthquakes.
    The horizontal axis dynamically switches between East/West and North/South offsets.
    """
    # Determine which offset column to plot on the X-axis
    if axis_choice == 'E/W':
        x_element = 'x_position'
    elif axis_choice == 'N/S':
        x_element = 'y_position'
    else:
        return []
    # Create the cross-section scatter plot
    fig = px.scatter(chart_data,
                     x=x_element,
                     y='Depth/Km',
                     size='Magnitude',
                     color='Magnitude',
                     labels={
                         'x_position': 'E/W offset (km)',
                         'y_position': 'N/S offset (km)',
                         'Depth/Km': 'Depth (km)',
                         'Magnitude': 'Magnitude',
                         'Time': 'Time',
                         '#EventID': 'EventID',
                     },
                     hover_data=["Time"]
                     )

    # Lock the axes ranges to maintain consistent scaling during data updates
    fig.update_xaxes(range=[-6, 6])
    fig.update_yaxes(range=[-10, 0])

    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
    )
    return fig


@callback(
    Output('description', 'children'),
    Input('map-type', 'value'),
)
def update_description(type_of_chart):
    """
    Dynamically updates the descriptive title above the chart wrapper
    whenever the user switches the map visualization type.
    """
    if type_of_chart == '3D-Map':
        return "Interactive 3D map of all the earthquakes' epicenters"
    elif type_of_chart == 'Heatmap':
        return "Heatmap showing the earthquakes' epicenters' positions on the surface"
    elif type_of_chart == 'Vertical E/W':
        return "Vertical view showing the earthquakes' epicenters' depth vs the East-West axis"
    elif type_of_chart == 'Vertical N/S':
        return "Vertical view showing the earthquakes' epicenters' depth vs the  North-South axis"
    else:
        return 'This should never be displayed'
