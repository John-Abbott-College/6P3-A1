from dash import Dash, html, dcc, callback, Output, Input
from device_controller import DeviceController, ACommand, AReading
import plotly.graph_objs as go
from datetime import datetime
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
                html.Div(
                    [html.H2("Sensor Readings"), 
                     dcc.Graph(id="temperature-graph", className="dash-graph"),
                     dcc.Graph(id="humidity-graph", className="dash-graph")],
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

@app.callback(
    [Output("temperature-graph", "figure"), Output("humidity-graph", "figure")],
    [Input("interval-component", "n_intervals")]
)
def update_graphs(n):
    data = device_manager.read_sensors()
    current_time = datetime.now()

    temperature_readings = [(current_time, reading.value) for reading in data if reading.reading_type == AReading.Type.TEMPERATURE]
    humidity_readings = [(current_time, reading.value) for reading in data if reading.reading_type == AReading.Type.HUMIDITY]

    temp_times, temp_values = zip(*temperature_readings) if temperature_readings else ([], [])
    humid_times, humid_values = zip(*humidity_readings) if humidity_readings else ([], [])

    temperature_figure = go.Figure(
        data=[
            go.Scatter(
                x=temp_times, y=temp_values, mode="lines+markers", name="Temperature"
            )
        ],
        layout=go.Layout(
            title="Temperature Over Time",
            xaxis=dict(title="Time"),
            yaxis=dict(title="Temperature (°C)"),
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            autosize=True,
        ),
    )

    humidity_figure = go.Figure(
        data=[
            go.Scatter(
                x=humid_times, y=humid_values, mode="lines+markers", name="Humidity"
            )
        ],
        layout=go.Layout(
            title="Humidity Over Time",
            xaxis=dict(title="Time"),
            yaxis=dict(title="Humidity (%)"),
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            autosize=True,
        ),
    )

    return temperature_figure, humidity_figure



if __name__ == "__main__":
    app.run_server(debug=True)
