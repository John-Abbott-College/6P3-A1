from dash import Dash, html, Input, Output, callback
import dash_bootstrap_components as dbc
from device_controller import DeviceController
from actuators import ACommand
from sensors import AReading

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

device_controller = DeviceController()

app.layout = html.Div([
    html.H1("HVAC IoT System"),
    dbc.Button("Turn LED ON", color="success", className="me-1", id="led-on"),
    dbc.Button("Turn LED OFF", color="danger", className="me-1", id="led-off"),
])

@app.callback(
    Input("led-on", "value"),
    force_no_output=True
)
def turn_led_on():
    device_controller.control_actuators([ACommand(ACommand.Type.FAN, "1")])

if __name__ == '__main__':
    app.run(debug=True)
