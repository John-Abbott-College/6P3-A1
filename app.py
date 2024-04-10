from dash import Dash, html, callback, Output, Input, State
from device_controller import DeviceController, ACommand
import os


device_manager = DeviceController()

app = Dash(__name__)

app.layout = html.Div(
    [
        html.Div(
            [
                html.H1("Device Controller"),
            ],
            className="header",
        ),
        html.Div(
            [
                html.Div(
                    [html.H2("Actuators"), 
                     html.Button("Turn Fan On", id="fan-button", n_clicks=0),
                     html.Button("Turn LED On", id="led-button", n_clicks=0)],
                    className="device-container",
                ),
            ],
            className="device-type-container",
        ),
    ]
)


@app.callback(
    Output("fan-button", "children"),
    [Input("fan-button", "n_clicks")],
    [State("fan-button", "children")]
)
def fan_button_clicked(n_clicks, button_text):
    if n_clicks is None:
        return button_text

    state = button_text.split(" ")[-1]
    new_state = "On" if state == "Off" else "Off"
    device_manager.control_actuators([ACommand(ACommand.Type.FAN, new_state.lower())])

    return f"Turn Fan {new_state}"


@app.callback(
    Output("led-button", "children"),
    [Input("led-button", "n_clicks")],
    [State("led-button", "children")]
)
def led_button_clicked(n_clicks, button_text):
    if n_clicks is None:
        return button_text

    state = button_text.split(" ")[-1]
    new_state = "On" if state == "Off" else "Off"
    device_manager.control_actuators([ACommand(ACommand.Type.LIGHT_PULSE, new_state.lower())])

    return f"Turn LED {new_state}"


if __name__ == "__main__":
    app.run_server(debug=True)
