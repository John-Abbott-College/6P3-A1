from dash import Dash, html, Input, Output, State, callback_context, dcc
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from device_controller import DeviceController
from actuators import ACommand
from sensors import AReading

app = Dash(__name__, external_stylesheets=[dbc.themes.LUMEN], suppress_callback_exceptions=True)

device_controller = DeviceController()

app.layout = html.Div([
    html.H1("HVAC IoT System"),
    dbc.Button("Turn Fan ON", color="success", className="me-1", id="fan-on"),
    dbc.Button("Turn Fan OFF", color="danger", className="me-1", id="fan-off"),

    dbc.Button("Turn LED ON", color="success", className="me-1", id="led-on"),
    dbc.Button("Turn LED OFF", color="danger", className="me-1", id="led-off"),

    dcc.Graph(id='temperature-graph'),
    dcc.Graph(id='humidity-graph'),
    dcc.Interval(
        id='interval-component',
        interval=1 * 1000,  # in milliseconds
        n_intervals=0
    ),
    # to store temp and humidity readings
    dcc.Store(id='graph-data', storage_type='memory'),

    html.Div(id='output0'),
    html.Div(id='output1'),
    html.Div(id='output2'),
    html.Div(id='output3'),
], style={'padding': 16})

# ========================
# Actuators
# ========================
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

# ========================
# Graphs
# ========================

TIME_AXIS="x_time"
HUMIDITY_AXIS=f"y_{AReading.Type.TEMPERATURE.name}"
TEMPERATURE_AXIS=f"y_{AReading.Type.HUMIDITY.name}"

@app.callback(Output('graph-data', 'data'),
              Input('interval-component', 'n_intervals'),
              State('graph-data', 'data'))
def update_graph_data(n, data):
    if data is None:
        data = {TIME_AXIS: [], TEMPERATURE_AXIS: [], HUMIDITY_AXIS: []}

    sensor_readings = device_controller.read_sensors()

    temperatures = [
        reading.value for reading in sensor_readings if reading.reading_type is AReading.Type.TEMPERATURE]
    humidities = [
        reading.value for reading in sensor_readings if reading.reading_type is AReading.Type.HUMIDITY]

    data[TIME_AXIS].append(n)
    data[TEMPERATURE_AXIS].extend(temperatures if temperatures else None)
    data[HUMIDITY_AXIS].extend(humidities if humidities else None)
    return data

def update_graph(data, unit: AReading.Unit, title: str, color: str):
    if data is None:
        return go.Figure()

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data[TIME_AXIS],
            y=data[TEMPERATURE_AXIS],
            mode='lines',
            name=f'Temperature ({unit.value})',
            line=dict(
                color=color)))

    fig.update_layout(
        title=title,
        xaxis_title="Time (s)",
        yaxis_title=unit.value,
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
    return update_graph(data, AReading.Unit.CELCIUS, "Temperature Readings", "green")

@app.callback(Output('humidity-graph', 'figure'),
              Input('graph-data', 'data'))
def update_temperature_graph(data):
    return update_graph(data, AReading.Unit.HUMIDITY, "Humidity Readings", "orange")

if __name__ == '__main__':
    app.run(debug=True)
