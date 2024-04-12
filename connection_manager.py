import dash, threading
from sensors import AReading
from actuators import ACommand


from dash.dependencies import State, Output, Input
from dash import Dash, html, dcc

class ConnectionManager():

    def __init__(self) -> None:
        self.commands: list[ACommand] = []
        self.readings: list[AReading] = []
        self.app = Dash(__name__)

        self.app.layout = html.Div([
            html.Div([
                html.Button('Turn LED On', id='led-on-button', n_clicks=0, style={'width': '100px', 'margin-right': '5px'}),
                html.Button('Turn LED Off', id='led-off-button', n_clicks=0, style={'width': '100px'}),
            ], style={'margin-bottom': '40px'}),

            html.Div(id='led-status'),

            html.Div([
                html.Label('Threshold: '),
                dcc.Input(id='threshold-value', type='number', value=30),
            ], style={'margin-bottom': '10px'}),

            html.Div([
                html.Button('Turn ON Fan', id='fan-on-button', n_clicks=0, style={'width': '70px'}),
            ], style={'margin-bottom': '10px'}),

            html.Div([
                html.Button('Turn OFF Fan', id='fan-off-button', n_clicks=0, style={'width': '70px'})
            ]),

            html.Div(id='sensor-values'),

            dcc.Interval(
                id='int-comp',
                interval=1*1000,
                n_intervals=0
            )
        ])


        @self.app.callback(
            Output('sensor-values', 'children'),
            Input('int-comp', 'n_intervals'),
            State('threshold-value', 'value')
        )
        def update_sensor_values(n, threshold):
            sensor_values = []
            for reading in self.readings:
                sensor_values.append(html.P(f'Temperature: {reading[0]}'))
                sensor_values.append(html.P(f'Humidity: {reading[1]}'))
                if reading[0] >= threshold:  
                    self.commands.append(ACommand(ACommand.Type.FAN, "1"))                            
            return sensor_values

        @self.app.callback(
            Output('fan-on-button', 'n_clicks'),
            Input('fan-on-button', 'n_clicks')
        )
        def turn_on_fan(n_clicks):
            if n_clicks > 0:
                self.commands.append(ACommand(ACommand.Type.FAN, "1"))

        @self.app.callback(
            Output('led-on-button', 'n_clicks'),
            Input('led-on-button', 'n_clicks')
        )
        def turn_on_led(n_clicks):
            if n_clicks > 0:
                self.commands.append(ACommand(ACommand.Type.LIGHT_PULSE, "1"))

        @self.app.callback(
            Output('fan-off-button', 'n_clicks'),
            Input('fan-off-button', 'n_clicks')
        )
        def turn_off_fan(n_clicks):
            if n_clicks > 0:
                self.commands.append(ACommand(ACommand.Type.FAN, "0"))

       
        @self.app.callback(
            Output('led-off-button', 'n_clicks'),
            Input('led-off-button', 'n_clicks')
        )
        def turn_off_led(n_clicks):
            if n_clicks > 0:
                self.commands.append(ACommand(ACommand.Type.LIGHT_PULSE, "0"))

    def connect(self):
        thread  = threading.Thread(target=self.app.run_server, kwargs={'port': 8051})
        thread.daemon = True
        thread.start()

    def send_readings(self, readings: list[AReading]):
        self.readings = readings

    def receive_commands(self):
        commands = self.commands
        self.commands = []
        return commands

        
