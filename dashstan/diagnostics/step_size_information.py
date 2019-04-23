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
from dashstan import dashstantab
import plotly.graph_objs as go

STANDARD_HEIGHT = 300
STANDARD_MARGIN = dict(l=50, r=20, t=50, b=50, pad=5)


class StepSizeInformation(dashstantab.DashStanTab):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = 'Step Size Information'
        self.data_warmup = self.data[self.data['warmup'] == 0]
        self._build_children()

    def _build_children(self):
        self.children = [
            html.Div(className='container-fluid', children=[
                # html.Div(className='row col', children=[
                    self._build_step(),
                # ]),
                html.Div(className='row', children=[
                    html.Div(className='col', children=[
                        self._build_step_metro_violin(),
                    ]),
                    html.Div(className='col', children=[
                        self._build_step_log_voilin(),
                    ]),
                ]),
            ]),
        ]

    def _build_step(self):
        traces = [
            go.Scatter(x=chain['draw'],
                       y=chain['stepsize__'],
                       mode='lines',
                       name='Chain: {}'.format(chain['chain'].iloc[0]),
                       ) for chain in self.get_chains()
        ]

        layout = go.Layout(
            title='Sampled Step Size',
            legend=dict(orientation='h', y=0),
            margin=STANDARD_MARGIN,
        )

        return dcc.Graph(id='step-graph',
                         style=dict(height=STANDARD_HEIGHT),
                         figure={
                             'data': traces,
                             'layout': layout,
                         })

    def _build_step_log_voilin(self):
        traces = [{
            'type': 'violin',
            'x': self.get_data_warmup()['stepsize__'].round(4),
            'y': self.get_data_warmup()['lp__']
        }]
        layout = go.Layout(
            margin=STANDARD_MARGIN,
            xaxis={
                'type': 'category',
                'title': 'Step Size'
            },
            yaxis={
                'title': 'Log Probability'
            },
        )

        return dcc.Graph(id='step-lp',
                         style=dict(height=STANDARD_HEIGHT),
                         figure={
                             'data': traces,
                             'layout': layout,
                         }
                         )

    def _build_step_metro_violin(self):
        traces = [{
            'type': 'violin',
            'x': self.get_data_warmup()['stepsize__'].round(4),
            'y': self.get_data_warmup()['accept_stat__']
        }]
        layout = go.Layout(
            xaxis={
                'type': 'category',
                'title': 'Step Size',
            },
            yaxis={
                'title': 'Mean Metrop. Acceptance',
            },
            margin=STANDARD_MARGIN,
        )

        return dcc.Graph(id='step-metrop',
                         style=dict(height=STANDARD_HEIGHT),
                         figure={
                             'data': traces,
                             'layout': layout,
                         }
                         )
