from device_controller import Device_Controller
from actuators import ACommand
import dash
from dash import Dash, html, dcc
from dash.dependencies import Input, Output



app = Dash(__name__)

deviceController = Device_Controller()


app.layout = html.Div([
    html.Div([
        dcc.Input(id='led-input', type='number', min=0, max=255, value=0, style={'width': '100px', 'margin-right': '5px'}),
        html.Button('Set LED', id='led-button', n_clicks=0)
    ], style={'margin-bottom': '40px'}),

    html.Div([
        html.Button('Turn ON Fan', id='fan-on-button', n_clicks=0, style={'width': '70px'}),
    ], style={'margin-bottom': '10px'}),

    html.Div([
        html.Button('Turn OFF Fan', id='fan-off-button', n_clicks=0, style={'width': '70px'})
    ]),

    html.Div(id='sensor-values'),

    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # in milliseconds
        n_intervals=0
    )
    
])

@app.callback(
    Output('sensor-values', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_sensor_values(n):
    sensor_values = deviceController.read_sensors()
    return [html.P(f'{reading.reading_type.value}: {reading.value}{reading.reading_unit.value}') for reading in sensor_values]



@app.callback(
    Output('led-input', 'value'),
    [Input('led-button', 'n_clicks')],
    [dash.dependencies.State('led-input', 'value')]
)
def turn_on_led(n_clicks, led_value):
    if n_clicks > 0:
        command = ACommand(ACommand.Type.LIGHT_ON_OFF, str(led_value))
        deviceController.control_actuators(commands=[command])


@app.callback(
    Output('fan-on-button', 'n_clicks'),
    Input('fan-on-button', 'n_clicks')
)
def turn_on_fan(n_clicks):
    if n_clicks > 0:
        # Add your function to turn on the fan here
        command = ACommand(ACommand.Type.FAN, "1")
        deviceController.control_actuators(commands=[command])

@app.callback(
    Output('fan-off-button', 'n_clicks'),
    Input('fan-off-button', 'n_clicks')
)
def turn_off_fan(n_clicks):
    if n_clicks > 0:
        # Add your function to turn off the fan here
        command = ACommand(ACommand.Type.FAN, "0")
        deviceController.control_actuators(commands=[command])



if __name__ == "__main__":
    """This script is intented to be used as a module, however, code below can be used for testing.
    """
    app.run()