import pickle
import os
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from .diagnostics import Diagnostics


class DashStan(dash.Dash):

    def __init__(self, data=None, **kwargs):
        super().__init__(**kwargs)
        self.data = data
        self.app = dash.Dash(__name__)
        self.app.config.suppress_callback_exceptions = True
        # TODO Create an object that is a child of tab with a callable page.
        self._TABS = {
            'diagnostics': {
                'label': 'Diagnostics',
                'page': Diagnostics(app=self.app),
            },
            'test': {
                'label': 'Test',
                'page': None,
            },
        }

    def build_layout(self):
        self.app.layout = html.Div([
            html.H1('Dash-Stan'),
            dcc.Tabs(id='main_tabs', value='diagnostics', children=[
                dcc.Tab(label=self._TABS[key]['label'], value=key) for key in self._TABS
            ]),
            html.Div(id='dash-holder'),
        ])

    def build_callbacks(self):
        @self.app.callback(Output('dash-holder', 'children'),
                           [Input('main_tabs', 'value')])
        def render_tab(value):
            return self._TABS[value]['page']

    def run(self):
        self.build_layout()
        self.build_callbacks()
        self.app.run_server()


class DashStanExample(DashStan):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # location = os.path.abspath(os.path.join('sampledata', 'sampledata.pkl'))
        dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(dir, 'sampledata', 'sampledata.pkl')
        with open(file_path, 'rb') as f:
            self.data = pickle.load(f)['fit']
        self.run()
