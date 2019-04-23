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
import plotly.graph_objs as go

STANDARD_HEIGHT = 300
STANDARD_MARGIN = dict(l=50, r=20, t=50, b=50, pad=5)

class SampleInformation(html.Div):

    def __init__(self, app, data, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.data = data
        self.data_warmup = self.data[self.data['warmup'] == 0]
        self.build_children()

    def build_children(self):
        chains = self._get_chains()
        # Build the log posterior trace plot from chains.
        iter_lp_graph = self._build_lp_trace(chains=chains)
        iter_metro_graph = self._build_metro_graph(chains=chains)
        lp_hist = self._build_lp_hist()
        metro_hist = self._build_metro_hist()
        metro_lp_plot = self._build_metro_lp_plot()
        self.children = [
            html.Div(className='container-fluid', children=[
                html.Div(className='row', children=[
                    html.Div(className='col', children=[
                        metro_lp_plot,
                    ]),
                    html.Div(className='col',  children=[
                        iter_lp_graph,
                        iter_metro_graph,
                    ]),
                    html.Div(className='col', children=[
                        lp_hist,
                        metro_hist,
                    ]),
                ]),
            ]),
        ]

    def _get_chains(self):
        chain_data = self.data_warmup
        return [chain_data[chain_data['chain'] == chain] for chain in chain_data['chain'].unique()]

    def _build_metro_graph(self, chains):
        traces = [go.Scatter({'x': chain['draw'],
                              'y': chain['accept_stat__'],
                              'mode': 'lines',
                              'name': 'Chain: {}'.format(chain['chain'].iloc[0]),
                              }) for chain in chains]
        layout = go.Layout(
            title='Mean Metrop. Acceptance',
            legend=dict(orientation='h'),
            margin=STANDARD_MARGIN,
        )
        return dcc.Graph(id='iter_metro_graph',
                         style=dict(height=STANDARD_HEIGHT),
                         figure={
                             'data': traces,
                             'layout': layout,
                         })

    def _build_lp_trace(self, chains):
        traces = [go.Scatter({'x': chain['draw'],
                              'y': chain['lp__'],
                              'mode': 'lines',
                              'name': 'Chain: {}'.format(chain['chain'].iloc[0]),
                              }) for chain in chains]
        layout = go.Layout(
            title='Log Posterior',
            legend=dict(orientation='h'),
            margin=STANDARD_MARGIN,
        )

        return dcc.Graph(id='iter_lp_graph',
                         style=dict(height=STANDARD_HEIGHT),
                         figure={
                             'data': traces,
                             'layout': layout,
                         })

    def _build_lp_hist(self):
        layout = go.Layout(
            title='Log Posterior',
            margin=STANDARD_MARGIN,
        )
        return dcc.Graph(id='lp_hist',
                         style=dict(height=STANDARD_HEIGHT),
                         figure={
                             'data': [go.Histogram(x=self.data_warmup['lp__'])],
                             'layout': layout,
                         })

    def _build_metro_hist(self):
        layout = go.Layout(
            margin=STANDARD_MARGIN,
            title='Mean Metrop. Acceptance'
        )
        return dcc.Graph(id='metro_hist',
                         style=dict(height=STANDARD_HEIGHT),
                         figure={
                             'data': [go.Histogram(x=self.data_warmup['accept_stat__'])],
                             'layout': layout
                         })

    def _build_metro_lp_plot(self):
        traces = [go.Scatter({'x': self.data_warmup['accept_stat__'],
                              'y': self.data_warmup['lp__'],
                              'mode': 'markers',
                              })]
        layout = go.Layout(
            margin=STANDARD_MARGIN,
            xaxis={
                'title': 'Mean Metrop. Acceptance',
            },
            yaxis={
                'title': 'Log Posterior',
            },
        )
        return dcc.Graph(id='metro_lp_plot',
                         style=dict(height=STANDARD_HEIGHT*2),
                         figure={
                             'data': traces,
                             'layout': layout,
                         })
