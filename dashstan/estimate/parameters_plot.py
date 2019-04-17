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


import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.graph_objs as go
import re

from dashstan import dashstantab


class ParametersPlot(dashstantab.DashStanTab):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label='Parameters-Plot'
        self.data = self.get_data_warmup()
        self._build_children()
        self._build_callbacks()

    def _build_children(self):
        self.children = [
            html.H4(children='Regex Search:', style={'float': 'left'}),
            dcc.Input(id='parameters-regex', value='', type='text', style={'margin': '5px'}),
            html.Div(id='error-bar')
        ]

    def _build_callbacks(self):
        @self.app.callback(
            Output('error-bar', 'children'),
            [Input('parameters-regex', 'value')]
        )
        def error_bar_plot(parameters_regex):
            parameters = self.get_parameters(lp__=False)
            if parameters_regex != '':
                parameters = [parameter for parameter in parameters if re.match(parameters_regex, parameter)]
            traces = [go.Box(x=self.data[parameter],
                             name=parameter,
                             marker=dict(color='black'))
                      for parameter in parameters]
            layout = go.Layout(
                showlegend=False,
            )
            return dcc.Graph(id='error-bar-graph',
                             figure={
                                 'data': traces,
                                 'layout': layout,
                             })
