#!/usr/bin/env python3

from dash import Dash, html, callback_context
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from device_controller import DeviceController
from actuators import ACommand

device_manager = DeviceController()

app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True)

app.layout = html.Div(children=[
    html.H1(children='Device Controller'),

    dbc.Button("Turn Fan On", id="fan-on-btn", className="mr-2"),
    dbc.Button("Turn Fan Off", id="fan-off-btn", className="mr-2"),

    dbc.Button("Turn LED On", id="led-on-btn", className="mr-2"),
    dbc.Button("Turn LED Off", id="led-off-btn", className="mr-2"),

    html.Div(id='output-placeholder'),
])

# Callback for all control buttons


@app.callback(
    Output('output-placeholder', 'children'),
    [Input('fan-on-btn', 'n_clicks'),
     Input('fan-off-btn', 'n_clicks'),
     Input('led-on-btn', 'n_clicks'),
     Input('led-off-btn', 'n_clicks')],
    prevent_initial_call=True
)
def control_devices(
        fan_on_clicks,
        fan_off_clicks,
        led_on_clicks,
        led_off_clicks):
    ctx = callback_context

    if not ctx.triggered:
        button_id = 'No buttons clicked yet'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'fan-on-btn':
        fan_on_command = ACommand(ACommand.Type.FAN, "on")
        device_manager.control_actuators([fan_on_command])
        return "Fan turned on."
    elif button_id == 'fan-off-btn':
        fan_off_command = ACommand(ACommand.Type.FAN, "off")
        device_manager.control_actuators([fan_off_command])
        return "Fan turned off."
    elif button_id == 'led-on-btn':
        led_on_command = ACommand(ACommand.Type.LIGHT_ON_OFF, "on")
        device_manager.control_actuators([led_on_command])
        return "LED turned on."
    elif button_id == 'led-off-btn':
        led_off_command = ACommand(ACommand.Type.LIGHT_ON_OFF, "off")
        device_manager.control_actuators([led_off_command])
        return "LED turned off."

    return "Unknown action"


if __name__ == '__main__':
    app.run_server(debug=True)
