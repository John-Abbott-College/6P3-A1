# Import packages
import dash
from dash import html, callback, callback_context, ctx
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from device_controller import DeviceController
from actuators import ACommand

#Initialize the device controller her to get the methods
device_controller = DeviceController()

# Initialize the app
app = dash.Dash(__name__)

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
#I got the idea to stack the buttons vertically using flex from here:
# https://community.plotly.com/t/vertically-stack-radioitems-as-buttongroup/72302/3
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



# Run the app
if __name__ == '__main__':
    app.run(debug=True)