#      DashStan a dashboard to analyse and diagnose Markov chain Monte Carlo simulations.
#      Copyright (C) 2019.  Nicholas Ver Halen
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>

import pickle
import os
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from .diagnostics import Diagnostics
from .estimate import Estimate

EXTERNAL_STYLESHEETS = ['https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css']

class DashStan(dash.Dash):
    def __init__(self, data=None, **kwargs):
        """

        :param data: Raw Stan simulation data.
        :param kwargs:
        """
        super().__init__(**kwargs)
        self.raw_data = data
        self.data = self._convert_data(data=self.raw_data)
        self.app = dash.Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS)
        self.app.config.suppress_callback_exceptions = True
        # TODO Create an object that is a child of tab with a callable page.
        self._TABS = {
            'Diagnostics': Diagnostics(app=self.app, data=self.data),
            'Estimate': Estimate(app=self.app, raw_data=self.raw_data, data=self.data),
        }

    def build_layout(self):
        self.app.layout = html.Div(className='container-fluid', children=[
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

    def run(self, debug=False):
        self.build_layout()
        self.build_callbacks()
        self.app.run_server(debug=debug)

    def _convert_data(self, data):
        return data.to_dataframe(inc_warmup=True)


class DashStanExample(DashStan):
    def __init__(self, debug=False, **kwargs):
        dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(dir, 'sampledata', 'sampledata.pkl')
        with open(file_path, 'rb') as f:
            self.pickle_data = pickle.load(f)
        super().__init__(data=self.pickle_data['fit'], **kwargs)
        self.run(debug=debug)
