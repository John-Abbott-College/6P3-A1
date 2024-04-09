#!/usr/bin/env python3

from dash import Dash, html, callback_context, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from device_controller_lab5 import DeviceController
from actuators import ACommand
from sensors import AReading

TIME_AXIS="x_time"
HUMIDITY_AXIS=f"y_{AReading.Type.TEMPERATURE.name}"
TEMPERATURE_AXIS=f"y_{AReading.Type.HUMIDITY.name}"
LUMINOSITY_AXIS=f"y_{AReading.Type.LUMINOSITY.name}"

device_controller = DeviceController()

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.LUMEN],
    suppress_callback_exceptions=True)

app.layout = html.Div(children=[
    html.H1(children='Eclipse Measurements'),
    dcc.Graph(id='luminosity-graph'),
    dcc.Graph(id='temperature-graph'),
    dcc.Graph(id='humidity-graph'),
    dcc.Interval(
        id='interval-component',
        interval=1 * 1000,  # in milliseconds
        n_intervals=0
    ),
    # to store temp and humidity readings
    dcc.Store(id='graph-data', storage_type='memory')
])


@app.callback(Output('graph-data', 'data'),
              Input('interval-component', 'n_intervals'),
              State('graph-data', 'data'))
def update_graph_data(n, data):
    if data is None:
        data = {TIME_AXIS: [], TEMPERATURE_AXIS: [], HUMIDITY_AXIS: [], LUMINOSITY_AXIS: []}

    sensor_readings = device_controller.read_sensors()

    temperatures = [
        reading.value for reading in sensor_readings if reading.reading_type is AReading.Type.TEMPERATURE]
    humidities = [
        reading.value for reading in sensor_readings if reading.reading_type is AReading.Type.HUMIDITY]
    luminosities = [
        reading.value for reading in sensor_readings if reading.reading_type is AReading.Type.LUMINOSITY]

    data[TIME_AXIS].append(n)
    data[TEMPERATURE_AXIS].extend(temperatures if temperatures else None)
    data[HUMIDITY_AXIS].extend(humidities if humidities else None)
    data[LUMINOSITY_AXIS].extend(luminosities if luminosities else None)
    return data


@app.callback(Output('luminosity-graph', 'figure'),
              Input('graph-data', 'data'))
def update_luminosity_graph(data):
    if data is None:
        return go.Figure()

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data[TIME_AXIS],
            y=data[LUMINOSITY_AXIS],
            mode='lines',
            name=f'Luminosity ({AReading.Unit.LUX.value})',
            line=dict(
                color="purple")))

    fig.update_layout(
        title="Luminosity Readings",
        xaxis_title="Time (s)",
        yaxis_title="Lux (lx)",
        legend_title="Legend",
        legend=dict(font=dict(color="white")),
        xaxis=dict(
            showline=True,
            showgrid=True,
        ),
        yaxis=dict(
            showline=True,
            showgrid=True,
        )
    )
    return fig




@app.callback(Output('temperature-graph', 'figure'),
              Input('graph-data', 'data'))
def update_temperature_graph(data):
    if data is None:
        return go.Figure()

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data[TIME_AXIS],
            y=data[TEMPERATURE_AXIS],
            mode='lines',
            name=f'Temperature ({AReading.Unit.CELSIUS.value})',
            line=dict(
                color="cyan")))

    fig.update_layout(
        title="Temperature Readings",
        xaxis_title="Time (s)",
        yaxis_title="deg C",
        legend_title="Legend",
        legend=dict(font=dict(color="white")),
        xaxis=dict(
            showline=True,
            showgrid=True,
        ),
        yaxis=dict(
            showline=True,
            showgrid=True,
        )
    )
    return fig


@app.callback(Output('humidity-graph', 'figure'),
              Input('graph-data', 'data'))
def update_humidity(data):
    if data is None:
        return go.Figure()

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data[TIME_AXIS],
            y=data[HUMIDITY_AXIS],
            mode='lines',
            name=f'Humidity ({AReading.Unit.HUMIDITY.value})',
            line=dict(
                color="orange")))

    fig.update_layout(
        title="Humidity Readings",
        xaxis_title="Time (s)",
        yaxis_title="% Humidity",
        legend_title="Legend",
        legend=dict(font=dict(color="white")),
        xaxis=dict(
            showline=True,
            showgrid=True,
        ),
        yaxis=dict(
            showline=True,
            showgrid=True,
        )
    )
    return fig


if __name__ == '__main__':
    app.run_server(host="0.0.0.0", debug=False)