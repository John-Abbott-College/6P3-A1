from dash import Dash, html, Input, Output
import dash_bootstrap_components as dbc
from device_controller import DeviceController
from actuators import ACommand

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

device_controller = DeviceController()

app.layout = html.Div([
    html.H1("HVAC IoT System"),
    dbc.Button("Turn Fan ON", color="success", className="me-1", id="fan-on"),
    dbc.Button("Turn Fan OFF", color="danger", className="me-1", id="fan-off"),

    dbc.Button("Turn LED ON", color="success", className="me-1", id="led-on"),
    dbc.Button("Turn LED OFF", color="danger", className="me-1", id="led-off"),

    html.Div(id='output0'),
    html.Div(id='output1'),
    html.Div(id='output2'),
    html.Div(id='output3'),
], style={'padding': 16})

# Fan ON
@app.callback(
    Output("output0", "children"),
    Input("fan-on", "n_clicks"),
)
def turn_fan_on(n_clicks):
    if n_clicks is not None and n_clicks > 0:
        device_controller.control_actuators([ACommand(ACommand.Type.FAN, "1")])
    return ""

# Fan OFF
@app.callback(
    Output("output1", "children"),
    Input("fan-off", "n_clicks"),
)
def turn_fan_off(n_clicks):
    if n_clicks is not None and n_clicks > 0:
        device_controller.control_actuators([ACommand(ACommand.Type.FAN, "0")])
    return ""

# LED Pulse
@app.callback(
    Output("output2", "children"),
    Input("led-on", "n_clicks"),
)
def turn_led_on(n_clicks):
    if n_clicks is not None and n_clicks > 0:
        device_controller.control_actuators([ACommand(ACommand.Type.LIGHT_ON_OFF, "1")])
    return ""

# LED Off
@app.callback(
    Output("output3", "children"),
    Input("led-off", "n_clicks"),
)
def turn_led_on(n_clicks):
    if n_clicks is not None and n_clicks > 0:
        device_controller.control_actuators([ACommand(ACommand.Type.LIGHT_ON_OFF, "0")])
    return ""

if __name__ == '__main__':
    app.run(debug=True)
