import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from sensors import ISensor, AReading
from actuators import ACommand
from device_controller import DeviceController
from time import sleep
import plotly.graph_objs as go

app = dash.Dash(__name__)

device_manager = DeviceController()

# Initialize empty lists to store data for plotting
temperature_data = []
humidity_data = []

app.layout = html.Div([
    html.H1("Actuator Control with Live Plot", className='centered-heading'),
    html.Div([
        html.Button("Toggle LED", id="led-button", n_clicks=0, className='rounded-button'),
        html.Button("Toggle Fan", id="fan-button", n_clicks=0, className='rounded-button')
    ], className='centered-buttons'),
    html.Div([
        html.Div(id="led-output", className='status-label'),
        html.Div(id="fan-output", className='status-label')
    ], style={'text-align': 'center', 'margin-top': '20px'}),  # Center and add margin between labels
    dcc.Graph(id='live-plot', animate=True),  # Live plot of temperature/humidity data
    dcc.Interval(
        id='interval-component',
        interval=5*1000,  # in milliseconds
        n_intervals=0
    )
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

@app.callback(Output('live-plot', 'figure'), [Input('interval-component', 'n_intervals')])
def update_graph(n):
    # Read sensor data
    readings = device_manager.read_sensors()
    temperature_data.append(readings[0].value)
    humidity_data.append(readings[1].value)

    # Create traces
    temperature_trace = go.Scatter(
        x=list(range(len(temperature_data))),
        y=temperature_data,
        mode='lines+markers',
        name='Temperature'
    )
    humidity_trace = go.Scatter(
        x=list(range(len(humidity_data))),
        y=humidity_data,
        mode='lines+markers',
        name='Humidity'
    )

    return {'data': [temperature_trace, humidity_trace], 'layout': go.Layout(xaxis=dict(title='Time'), yaxis=dict(title='Value'), )}

if __name__ == "__main__":
    app.run_server(debug=True)