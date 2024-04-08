import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from actuators import ACommand
from device_controller import DeviceController

app = dash.Dash(__name__)

device_manager = DeviceController()

app.layout = html.Div([
    html.H1("Actuator Control", className='centered-heading'),
    html.Div([
        html.Button("Toggle LED", id="led-button", n_clicks=0, className='rounded-button'),
        html.Button("Toggle Fan", id="fan-button", n_clicks=0, className='rounded-button')
    ], className='centered-buttons'),
    html.Div([
        html.Div(id="led-output", className='status-label'),
        html.Div(id="fan-output", className='status-label')
    ], style={'text-align': 'center', 'margin-top': '20px'})  # Center and add margin between labels
])

@app.callback(
    Output("led-output", "children"),
    [Input("led-button", "n_clicks")]
)
def toggle_led(n_clicks):
    if n_clicks % 2 == 1:
        commands = [ACommand(ACommand.Type.LIGHT_ON_OFF, "ON")]
    else:
        commands = [ACommand(ACommand.Type.LIGHT_ON_OFF, "OFF")]
    device_manager.control_actuators(commands)
    return f"LED: {'ON' if n_clicks % 2 == 1 else 'OFF'}"

@app.callback(
    Output("fan-output", "children"),
    [Input("fan-button", "n_clicks")]
)
def toggle_fan(n_clicks):
    if n_clicks % 2 == 1:
        commands = [ACommand(ACommand.Type.FAN, "ON")]
    else:
        commands = [ACommand(ACommand.Type.FAN, "OFF")]
    device_manager.control_actuators(commands)
    return f"Fan: {'ON' if n_clicks % 2 == 1 else 'OFF'}"

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
