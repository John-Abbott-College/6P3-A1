# Import packages
import dash
from dash import html, callback, callback_context, ctx, dcc
from dash.dependencies import Input, Output
from device_controller import DeviceController
from actuators import ACommand
import plotly.graph_objs as graphing
import time

#Initialize the device controller her to get the methods
device_controller = DeviceController()

#Had to make the 
temperature_readings = []
humidity_readings = []
time_readings = []

# Initialize the app
app = dash.Dash(__name__, suppress_callback_exceptions=True)


#I got the idea to stack the buttons vertically using flex from here:
# https://community.plotly.com/t/vertically-stack-radioitems-as-buttongroup/72302/3
app.layout = html.Div([
    html.H3(children='Control the Raspberry Pi with Buttons', style={'color':'#FFC0CB', 'font-family':'Verdana', 'text-align': 'center'}),
    html.Hr(),
    html.Div([
        html.Button('Turn Light On', id='light-button', style={'background-color': '#FFC0CB', 
        'color':'white', 'border-color': '#FFC0CB','font-family': 'Arial, sans-serif', 
        'margin': '10px', 'border-radius':'4px'}),
        html.Button('Fan On', id='fan-on-button', style={'background-color': '#FFC0CB', 
        'color':'white', 'border-color': '#FFC0CB','font-family': 'Arial, sans-serif', 
        'margin': '10px', 'border-radius':'4px'}),
        html.Button('Fan Off', id='fan-off-button', style={'background-color': '#FFC0CB', 
        'color':'white', 'border-color': '#FFC0CB', 'font-family': 'Arial, sans-serif', 
        'border-radius':'4px'}),        
    ], style={'display': 'flex', 'flex-direction': 'column', 
        'align-items': 'center', 'margin-bottom': '20px', 'text-align': 'center'}),  
    
    dcc.Tabs(id='tabs', value='tab-1',
            children=[
                dcc.Tab(label='Temperature Levels', value='tab-1'),
                dcc.Tab(label='Humidity Levels', value='tab-2')
            ]),
    html.Div(id='tabs-content', style={'margin-bottom':'50px'})
    ], style={'margin': '50px auto', 'width': '50%', 'text-align': 'center'}
)



tab1_content=html.Div([
    dcc.Graph(id='temperature-graph'),
    dcc.Interval(id='temperature-interval', 
                interval=5000,
                n_intervals=0)
])

tab2_content=html.Div([
    dcc.Graph(id='humidity-graph'),
    dcc.Interval(id='humidity-interval', 
                interval=5000,
                n_intervals=0)
])


@app.callback(
    Output('light-button', 'n_clicks'),
    Input('light-button', 'n_clicks'),
)

#I got the button with the if statement and ctx idea from here: 
#https://dash.plotly.com/dash-html-components/button#determining-which-button-changed-with-dash.ctx
def light_button_controller(on):
    if 'light-button' == ctx.triggered_id: 
        device_controller.control_actuators([ACommand(ACommand.Type.LIGHT_PULSE, "3")])
        return 1


@app.callback(
    Output('fan-on-button', 'n_clicks'),
    Output('fan-off-button', 'n_clicks'),
    Input('fan-on-button', 'n_clicks'),
    Input('fan-off-button', 'n_clicks'),
    prevent_initial_call=True
)

#I got the button with the if statement and ctx idea from here: 
#https://dash.plotly.com/dash-html-components/button#determining-which-button-changed-with-dash.ctx
def fan_button_controller(on, off):  
    if 'fan-on-button' == ctx.triggered_id: 
        device_controller.control_actuators([ACommand(ACommand.Type.FAN, "1")])
        return 1,0
    elif 'fan-off-button' == ctx.triggered_id:  
        device_controller.control_actuators([ACommand(ACommand.Type.FAN, "0")])
        return 0,1 
    else:
        return 0,0


#New stuff with tabs and graphs here:

def render_content(tab):
    if tab=='tab-1':
        return tab1_content
    elif tab=='tab-2':
        return tab2_content

@app.callback(
    Output('temperature-graph', 'figure'),
    Input('temperature-interval', 'n_intervals'),
    suppress_callback_exceptions=True
)
def temperature_graph_readings(n):
    read_time = time.strftime('%H:%M:%S')
    temperature, _ = device_controller.read_sensors()

    temperature_readings.append(temperature)
    time_readings.append(read_time)

    temperature_line_plot = graphing.Scatter(
        x=time_readings,
        y=temperature_readings,
        name='Temperature (°C)',
        mode='lines+markers',
        line=dict(
            color='red'
        )
    )

    layout = graphing.Layout(
        title='Temperature Readings',
        xaxis=dict(title='Time'),
        yaxis=dict(title='Temperature')
    )

    figure_made = graphing.Figure(data=[temperature_line_plot], layout=layout)
    return figure_made


@app.callback(
    Output('humidity-graph', 'figure'),
    Input('humidity-interval', 'n_intervals'),
    suppress_callback_exceptions=True
)
def humidity_graph_readings(n):
    read_time = time.strftime('%H:%M:%S')
    _, humidity = device_controller.read_sensors()

    humidity_readings.append(humidity)
    time_readings.append(read_time)

    humidity_line_plot = graphing.Scatter(
        x=time_readings,
        y=humidity_readings,
        name='Humidity (%)',
        mode='lines+markers',
        line=dict(
            color='pink'
        )
    )

    layout = graphing.Layout(
        title='Humidity Readings',
        xaxis=dict(title='Time'),
        yaxis=dict(title='Humidity')
    )

    figure_made = graphing.Figure(data=[humidity_line_plot], layout=layout)
    return figure_made

# Run the app
if __name__ == '__main__':
    app.run(debug=True)