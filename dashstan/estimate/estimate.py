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
#      along with this prooram.  If not, see <https://www.gnu.org/licenses/>

from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from .parameters_plot import ParametersPlot

class Estimate(html.Div):

    def __init__(self, app, raw_data, data, **kwargs):
        super().__init__(**kwargs)
        self.raw_data = raw_data
        self.data = data
        self.app = app
        self._estimate_tabs = {
            'parameters_plot': ParametersPlot(label='Parameters Plot', app=self.app, data=self.data)
        }
        self._build_children()
        self._build_callbacks()

    def _build_children(self):
        self.children = [
            dcc.Tabs(id='estimate-tabs', value='parameters_plot', children=[
                dcc.Tab(label=self._estimate_tabs[key].get_label(), value=key) for key in self._estimate_tabs
            ]),
            html.Div(id='estimate-holder')
        ]

    def _build_callbacks(self):
        @self.app.callback(
            Output('estimate-holder', 'children'),
            [Input('estimate-tabs', 'value')]
        )
        def render_estimate_tab(value):
            return self._estimate_tabs[value]