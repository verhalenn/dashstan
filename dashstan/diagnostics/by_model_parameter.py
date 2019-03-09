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

from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.figure_factory as ff


class ByModelParameter(html.Div):

    def __init__(self, app, data, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.data = data
        self.build_children()
        self.build_callbacks()

    def build_children(self):
        not_parameters = ['chain', 'draw', 'warmup', 'accept_stat__', 'stepsize__',
                          'treedepth__', 'n_leapfrog__', 'divergent__', 'energy__']
        parameters = [column for column in self.data.columns if column not in not_parameters]
        self.children = [
            # TODO include warmup checkbox
            # TODO include divergent checkbox
            dcc.Dropdown(
                id='parameter-input',
                value=parameters[0],
                options=[
                    {'label': parameter, 'value': parameter} for parameter in parameters
                ]
            ),
            dcc.Graph(id='chain-graph'),
            dcc.Graph(id='parameter-dist-plot'),
            dcc.Graph(id='parameter-lp-plot')
        ]

    def build_callbacks(self):
        @self.app.callback(
            Output(component_id='chain-graph', component_property='figure'),
            [Input(component_id='parameter-input', component_property='value')]
        )
        def render_chain_graph(value):
            chain_data = self.data[self.data['warmup'] == 0]
            chains = [chain_data[chain_data['chain'] == chain] for chain in chain_data['chain'].unique()]
            traces = [go.Scatter({'x': chain['draw'],
                                  'y': chain[value],
                                  'mode': 'lines',
                                  'name': 'Chain: {}'.format(chain['chain'].iloc[0]),
                                  }) for chain in chains]
            layout = go.Layout(
                title='Parameter:' + value,
            )
            return {
                'data': traces,
                'layout': layout,
            }

        @self.app.callback(
            Output(component_id='parameter-dist-plot', component_property='figure'),
            [Input(component_id='parameter-input', component_property='value')]
        )
        def render_dist_plot(value):
            dist_data = [self.data[self.data['warmup'] == 0][value]]
            labels = [value]
            layout = go.Layout(
                title=value,
            )
            return {
                'data': ff.create_distplot(dist_data, labels),
                'layout': layout
            }

        # TODO change hover to nearest if possible.
        @self.app.callback(
            Output(component_id='parameter-lp-plot', component_property='figure'),
            [Input(component_id='parameter-input', component_property='value')]
        )
        def render_lp_plot(value):
            lp_data = self.data[self.data['warmup'] == 0]
            traces = [go.Scatter(
                x=lp_data[value],
                y=lp_data['lp__'],
                mode='markers')]
            layout = go.Layout(
                xaxis={
                    'title': value,
                },
                yaxis={
                    'title': 'Log Posterior'
                },
            )
            return {
                'data': traces,
                'layout': layout,
            }
