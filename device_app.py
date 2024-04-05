# Import packages
import dash
from dash import Dash, html, dash_table, dcc, callback, Output, Input, ctx
import pandas as pd
import plotly.express as px
from device_controller import DeviceController
from actuators import ACommand

#Initialize the device controller her to get the methods
device_controller = DeviceController()

# Initialize the app
app = Dash(__name__)

app.layout = html.Div([
    html.Div(children='Control the Raspberry Pi with Buttons'),
    html.Hr(),
    dcc.Button('Fan On', id='fan-on-button'),
    dcc.Button('Fan Off', id='fan-off-button')
])


@callback(
    Output('fan-on-button', 'n-clicks'),
    Output('fan-off-button', 'n-clicks'),
    Input('fan-on-button', 'n-clicks'),
    Input('fan-off-button', 'n-clicks'),
    prevent_initial_call=True
)

def fan_button_controller(on, off):
    #I got this idea from here: 
    #https://dash.plotly.com/dash-html-components/button#determining-which-button-changed-with-dash.ctx
    if ctx.triggered_id == 'fan-on-button.n_clicks':
        gofuckyourself = [ACommand(ACommand.Type.FAN, "1")]
        device_controller.control_actuators(gofuckyourself)
        return 0, None
    elif ctx.triggered_id == 'fan-off-button.n_clicks':
        fuckoff = [ACommand(ACommand.Type.FAN, "0")]
        device_controller.control_actuators(fuckoff)
        return None, 0 
    else:
        return None, None


# Run the app
if __name__ == '__main__':
    app.run(debug=True)