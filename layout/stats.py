"""
Handles the generation of statistical charts (histograms and bar charts) used in stats page
for analyzing earthquake frequencies, magnitudes, depths, and time delays.
"""
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import pandas as pd
from utils.data import get_earthquake_data
from utils.constants import MIN_DATE
import plotly.graph_objects as go
import numpy as np
from datetime import timedelta, date

# default blank page to prevent bugs
blank = go.Figure(go.Scatter(x=[], y=[]))
blank.update_layout(template=None)
blank.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
blank.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)
blank.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
})

# UI Wrapper for the statistical chart
stats_wrapper = html.Div(
    [
        html.H6(id='description-stats', className='chart-title'),
        html.Div(
            dcc.Graph(
                id='chart',
                figure=blank,
                className='main-chart'
            ),
        )
    ]
)


@callback(
    Output(component_id='chart', component_property='figure'),
    Input(component_id='chart-type', component_property='value'),
    Input(component_id='min-magnitudo-stats', component_property='value'),
    Input(component_id='date-stats', component_property='value'),
    Input(component_id='depth-km-stats', component_property='value'),
    Input('refresh', 'data'),
)
def update_chart(chart_type, min_magnitudo, last_date_slider, depth, refresh_data):
    """
    Main routing callback for generating statistical charts based on UI controls[cite: 5].
    """
    first_date = (date.today() - MIN_DATE) + timedelta(days=last_date_slider[0])
    last_date = (date.today() - MIN_DATE) + timedelta(days=last_date_slider[1])

    # Retrieve and filter data based on slider values
    chart_data = get_earthquake_data().copy()
    mask = (
            (chart_data['Magnitude'] > min_magnitudo) &
            (chart_data['Time'] > pd.to_datetime(first_date)) &
            (chart_data['Time'] <= pd.to_datetime(last_date)) &
            (chart_data['Depth/Km'] > depth[0]) &
            (chart_data['Depth/Km'] <= depth[1])
    )
    chart_data = chart_data[mask]

    # Route to the appropriate charting function
    if chart_type == 'Dates':
        # Dynamically calculate histogram bins to avoid overcrowding the X-axis
        number_of_days = last_date_slider[1] - last_date_slider[0]
        if number_of_days < 20:
            nbins = number_of_days
        else:
            nbins = min(60, max(20, round(number_of_days / 10)))

        chart = dates_chart(chart_data, nbins)
        chart.update_layout(uirevision=chart_type, font=dict(color="white"), plot_bgcolor='rgba(0, 0, 0, 0)',
                            paper_bgcolor='rgba(0, 0, 0, 0)')

    elif chart_type == 'Time-delta':
        # Calculate the time difference (in hours) between consecutive earthquakes[cite: 5]
        chart_data['lags'] = (chart_data.Time - chart_data.Time.shift(1)) / np.timedelta64(1, 'h')
        chart = lags_chart(chart_data)
        chart.update_layout(uirevision=chart_type, font=dict(color="white"), plot_bgcolor='rgba(0, 0, 0, 0)',
                            paper_bgcolor='rgba(0, 0, 0, 0)')

    elif chart_type == 'Magnitude':
        chart = magnitude_chart(chart_data)
        chart.update_layout(uirevision=chart_type, font=dict(color="white"), plot_bgcolor='rgba(0, 0, 0, 0)',
                            paper_bgcolor='rgba(0, 0, 0, 0)')

    elif chart_type == 'Depth':
        chart = depth_chart(chart_data)
        chart.update_layout(uirevision=chart_type, font=dict(color="white"), plot_bgcolor='rgba(0, 0, 0, 0)',
                            paper_bgcolor='rgba(0, 0, 0, 0)')

    else:
        chart = blank

    return chart


def dates_chart(chart_data, nbins):
    """Generates a histogram of earthquake occurrences over time."""
    fig = (px.histogram(chart_data, x='Time', nbins=nbins, labels={
        'x_position': 'E/W offset (km)', 'y_position': 'N/S offset (km)', 'Depth/Km': 'Depth (km)',
        'Magnitude': 'Magnitude', 'Time': 'Time', '#EventID': 'EventID',
    }))
    fig.update_layout(bargap=0.2, margin=dict(r=0, l=0, b=0, t=0))

    return fig


def lags_chart(chart_data):
    """
    Generates a histogram showing the time delay between consecutive earthquakes.
    Includes a separate bar trace to group and count outliers (lags > 240 hours).
    """
    fig = px.histogram(chart_data[chart_data['lags'] <= 240], x='lags', labels={
        'x_position': 'E/W offset (km)', 'y_position': 'N/S offset (km)', 'Depth/Km': 'Depth (km)',
        'Magnitude': 'Magnitude', 'Time': 'Time', '#EventID': 'EventID', 'lags': 'Lag (hours)'
    })

    # Calculate and plot the count of extreme outliers
    count_over = len(chart_data[chart_data['lags'] > 240])
    fig.add_trace(
        go.Bar(
            x=[240],
            y=[count_over],
            hovertemplate=f'Lag (hours)=>200<br>count={count_over}<extra></extra>',
            showlegend=False
        )
    )
    fig.update_layout(bargap=0.2, margin=dict(r=0, l=0, b=0, t=0))

    return fig


def magnitude_chart(chart_data):
    """Generates a histogram distributing the magnitudes of recorded earthquakes."""
    fig = px.histogram(chart_data, x='Magnitude', labels={
        'x_position': 'E/W offset (km)', 'y_position': 'N/S offset (km)', 'Depth/Km': 'Depth (km)',
        'Magnitude': 'Magnitude', 'Time': 'Time', '#EventID': 'EventID',
    })
    fig.update_layout(bargap=0.2)
    fig.update_layout(
        margin=dict(r=0, l=0, b=0, t=0)
    )

    return fig


def depth_chart(chart_data):
    """Generates a histogram distributing the depths of recorded earthquakes[cite: 5]."""
    fig = px.histogram(chart_data, x='Depth/Km', labels={
        'x_position': 'E/W offset (km)', 'y_position': 'N/S offset (km)', 'Depth/Km': 'Depth (km)',
        'Magnitude': 'Magnitude', 'Time': 'Time', '#EventID': 'EventID',
    })
    fig.update_layout(bargap=0.2)
    fig.update_layout(
        margin=dict(r=0, l=0, b=0, t=0)
    )

    return fig


@callback(
    Output('description-stats', 'children'),
    Input('chart-type', 'value'),
)
def update_description(type_of_chart):
    """Dynamically updates the descriptive title based on the selected stat metric."""
    if type_of_chart == 'Dates':
        return "Frequency of earthquakes over time"
    elif type_of_chart == 'Time-delta':
        return "Delay between consecutive earthquakes (hours)"
    elif type_of_chart == 'Magnitude':
        return "Distributions of the Magnitudes of earthquakes"
    elif type_of_chart == 'Depth':
        return "Distribution of earthquakes' depths"
    else:
        return 'This should never be displayed'
