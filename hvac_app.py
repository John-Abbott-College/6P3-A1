#!/usr/bin/python3

# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
from device_controller import DeviceController
from sensors import ISensor, AReading
from time import sleep
from actuators import IActuator, ACommand
from datetime import datetime

device_manager = DeviceController()
sensors_active = False
actuators_active = False

# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    dcc.Interval(id="countdown-interval", interval=4000, n_intervals=0),
    html.Div(children='HVAC Controller and Reader System'),
    html.Hr(),
    html.Button('Activate LED/Fan: Off', id='activate-actuators', n_clicks=0),
    html.Button('Read Temperature/Humidity: Off', id='activate-sensors', n_clicks=0),
    dcc.Graph(id='sensor-graph', figure=px.histogram(pd.read_csv('./measurements.csv'), x='time', y='value', histfunc='avg'))
])

# Add controls to build the interaction
@callback(
    Output('activate-actuators','children'),
    Input('activate-actuators', 'n_clicks')
)
def activate_actuators(n_clicks):
    if n_clicks % 2 != 0:
        actuators_active = True
        return 'Activate LED/Fan: On'
    actuators_active = False
    return 'Activate LED/Fan: Off'


# Add controls to build the interaction
@callback(
    Output('activate-sensors','children'),
    Input('activate-sensors', 'n_clicks')
)
def activate_sensors(n_clicks):
    if n_clicks % 2 != 0:
        sensors_active = True
        return 'Read Temperature/Humidity: On'
    sensors_active = False
    return 'Read Temperature/Humidity: Off'

@callback(
    Output('sensor-graph','figure'),
    Input("countdown-interval", "n_intervals"),
    Input('activate-sensors', 'n_clicks'),
    Input('activate-actuators', 'n_clicks')
)
def sensor_actuator_countdown(n_intervals, n_clicks_sensors, n_clicks_actuators):
    if n_clicks_sensors % 2 != 0:
        device_manager.read_sensors()
    if n_clicks_actuators % 2 != 0:
        fake_command = [
            ACommand(ACommand.Type.FAN, "1"),
            ACommand(ACommand.Type.LIGHT_PULSE, "1")
        ]
        device_manager.control_actuators(fake_command)
    return px.histogram(pd.read_csv('./measurements.csv'), x='time', y='value', histfunc='avg')

# Run the app
if __name__ == '__main__':
    
    app.run(debug=True)