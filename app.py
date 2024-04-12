
# Import packages
import dash
from dash import html, callback, callback_context, ctx, dcc
from dash.dependencies import Input, Output
from device_controller import DeviceController
from actuators import ACommand
import plotly.graph_objs as graphing
import time
#TESTTESTTEST

#Had to make the arrays to read the outputs of the sensor
temperature_readings = []
humidity_readings = []
time_readings = []

#Initialize the device controller her to get the methods
device_controller = DeviceController()

# Initialize the app
app = dash.Dash(__name__)

#I put the readings in another method to separate the concerns from displaying the data
#I had to put it here after experimenting where it could go. 
#It wouldn't work it I put it above the actual method I was calling it from
def sensor_reading_updates(n):
    read_time = time.strftime('%H:%M:%S')
    temperature, humidity = device_controller.read_sensors()
    humidity_readings.append(humidity)    
    temperature_readings.append(temperature)   
    time_readings.append(read_time)


#I got the idea to stack the buttons vertically using flex from here:
# https://community.plotly.com/t/vertically-stack-radioitems-as-buttongroup/72302/3
#I got the idea to style the buttons from here:
#https://dash.plotly.com/tutorial#html-and-css
#https://blog.finxter.com/plotly-dash-button-component/

app.layout = html.Div([
    html.H3(children='Control the Raspberry Pi with Buttons', style={'color':'#000', 'font-family':'Verdana', 'text-align': 'center'}),
    html.Hr(),
    html.Div([
        html.Button('Turn Light On', id='light-button', style={'background-color': '#DB1F48', 
        'color':'white', 'border-color': '#DB1F48','font-family': 'Arial, sans-serif', 
        'margin': '10px', 'border-radius':'4px'}),
        html.Button('Fan On', id='fan-on-button', style={'background-color': '#004369', 
        'color':'white', 'border-color': '#004369','font-family': 'Arial, sans-serif', 
        'margin': '10px', 'border-radius':'4px'}),
        html.Button('Fan Off', id='fan-off-button', style={'background-color': '#FFC0CB', 
        'color':'white', 'border-color': '#FFC0CB', 'font-family': 'Arial, sans-serif', 
        'border-radius':'4px'}),        
    ], style={'display': 'flex', 'flex-direction': 'column', 
        'align-items': 'center', 'margin-bottom': '20px', 'text-align': 'center'}),  

    html.Div([
      html.H3(children='Temperature and Humidity Graph', style={'color':'#000', 'font-family':'Verdana', 'text-align': 'center'}),
        dcc.Graph(id='live-temp-humid-graph'),
        dcc.Interval(
                id='interval-readings',
                interval=5000, 
                n_intervals=0
            )
        ], style={'margin-bottom': '50px', 'textAlign': 'center'})    
    ], style={'margin': '50px auto', 'width': '50%', 'text-align': 'center'}
)


@app.callback(
    Output('light-button', 'n_clicks'),
    Input('light-button', 'n_clicks'),
)

#I got the button with the if statement and ctx idea from here: 
#https://dash.plotly.com/dash-html-components/button#determining-which-button-changed-with-dash.ctx
def light_button_controller(on):
    if 'light-button' == ctx.triggered_id: 
        device_controller.control_actuators([ACommand(ACommand.Type.LIGHT_PULSE, "2")])
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

@app.callback(
    Output('live-temp-humid-graph', 'figure'),
    Input('interval-readings', 'n_intervals'),
    prevent_initial_call=True
)



#I got the help for this part from these sources:
#https://dash.plotly.com/tutorial
#https://www.youtube.com/watch?v=g3VQAVz_0qo
#https://plotly.com/python/reference/scatter/
def sensor_graph_readings(n):

    sensor_reading_updates(n)

    figure_made = graphing.Figure()
   

    #Updating the humidity part of the graph here    
    figure_made.add_trace(graphing.Scatter(
        x=time_readings,
        y=humidity_readings,
        name='Humidity (%)',
        mode='lines+markers+text',
        line=dict(
            color='black'
        )
    ))
    #Updating the temperature part of the graph here    
    figure_made.add_trace(graphing.Scatter(
        x=time_readings,
        y=temperature_readings,
        name='Temperature (°C)',
        mode='lines+markers+text',
        line=dict(
            color='red'
        )
    ))

    #Adding both graphs to the layout
    layout = graphing.Layout(     
        title='Temperature/Humidity Readings',  
        xaxis=dict(title='Time'),
        yaxis=dict(title='Temperature/Humidity'),
    )


    figure_made.update_layout(layout)
    
    return figure_made



# Run the app
if __name__ == '__main__':
    app.run(debug=True)