import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html


class DashStan:
    def __init__(self, data=None):
        self.data = data
        self.app = dash.Dash(__name__)
        self.app.layout = html.Div(children=[
            html.H1('Dash-Stan')
        ])
        self.app.run_server()
