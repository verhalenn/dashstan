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
        self.data = self._convert_data(data=data)
        self.app = dash.Dash(__name__)
        self.app.config.suppress_callback_exceptions = True
        # TODO Create an object that is a child of tab with a callable page.
        self._TABS = {
            'Diagnostics': Diagnostics(app=self.app, data=self.data),
            'Test': None,
        }

    def build_layout(self):
        self.app.layout = html.Div([
            html.H1('DashStan'),
            dcc.Tabs(id='main_tabs', value='Diagnostics', children=[
                dcc.Tab(label=key, value=key) for key in self._TABS
            ]),
            html.Div(id='dash-holder'),
        ])

    def build_callbacks(self):
        @self.app.callback(Output('dash-holder', 'children'),
                           [Input('main_tabs', 'value')])
        def render_tab(value):
            return self._TABS[value]

    def run(self):
        self.build_layout()
        self.build_callbacks()
        self.app.run_server()

    def _convert_data(self, data):
        return data.to_dataframe(inc_warmup=True)


class DashStanExample(DashStan):
    def __init__(self, **kwargs):
        dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(dir, 'sampledata', 'sampledata.pkl')
        print(file_path)
        with open(file_path, 'rb') as f:
            self.pickle_data = pickle.load(f)
        super().__init__(data=self.pickle_data['fit'], **kwargs)
        self.run()
