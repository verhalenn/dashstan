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


class TreeDepth(html.Div):

    def __init__(self, app, data, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.data = data
        self.data_warmup = self.data[self.data['warmup'] == 0]
        self.build_children()

    def build_children(self):
        self.chains = self._get_chains()
        treedeph_step = self._build_treedepth_step()
        treedepth_log_violin = self._build_treedepth_log_violin()
        treedepth_metro_violin = self._build_treedepth_metro_violin()
        self.children = [
            treedeph_step,
            treedepth_log_violin,
            treedepth_metro_violin,
            html.Div(children=self._build_treedepth_histograms())
        ]

    def _build_treedepth_step(self):
        traces = [go.Scatter(x=chain['draw'],
                             y=chain['treedepth__'],
                             mode='lines',
                             name='Chain: {}'.format(chain['chain'].iloc[0]),
                             ) for chain in self.chains]
        layout = go.Layout(
            title='Treedepth'
        )

        return dcc.Graph(id='treedepth_step',
                         figure={
                             'data': traces,
                             'layout': layout,
                         })

    def _build_treedepth_log_violin(self):
        traces = [{
            'type': 'violin',
            'x': self.data_warmup['treedepth__'],
            'y': self.data_warmup['lp__'],
        }]

        layout = go.Layout(
            xaxis={
                'title': 'Treedepth'
            },
            yaxis={
                'title': 'Log Probability'
            }
        )

        return dcc.Graph(id='treedepth_log_violin',
                         figure={
                             'data': traces,
                             'layout': layout,
                         })

    def _build_treedepth_metro_violin(self):
        traces = [{
            'type': 'violin',
            'x': self.data_warmup['treedepth__'],
            'y': self.data_warmup['accept_stat__'],
        }]

        layout = go.Layout(
            xaxis={
                'title': 'Treedepth'
            },
            yaxis={
                'title': 'Mean Metrop. Acceptance'
            }
        )

        return dcc.Graph(id='treedepth_metro_violin',
                         figure={
                             'data': traces,
                             'layout': layout,
                         })

    def _build_treedepth_histograms(self):
        treedepth_all_data = [go.Histogram(x=self.data_warmup['treedepth__'])]
        treedepth_non_divergent_data = [go.Histogram(x=self.data_warmup['treedepth__'][self.data_warmup[
                                                                                           'divergent__'] == 0])]
        treedepth_divergent_data = [go.Histogram(x=self.data_warmup['treedepth__'][self.data_warmup[
                                                                                           'divergent__'] == 1])]
        treedepth_all_layout = go.Layout(title='Treedepth All')
        treedepth_non_divergent_layout = go.Layout(title='Treedepth Non Divergent')
        treedepth_divergent_layout = go.Layout(title='Treedepth Divergent')
        treedepth_all = dcc.Graph(id='treedepth_hist_all',
                                  figure={
                                      'data': treedepth_all_data,
                                      'layout': treedepth_all_layout
                                  })
        treedepth_non_divergent = dcc.Graph(id='treedepth_hist_non_divergent',
                                            figure={
                                                'data': treedepth_non_divergent_data,
                                                'layout': treedepth_non_divergent_layout,
                                            })

        treedepth_divergent = dcc.Graph(id='treedepth_hist_divergent',
                                            figure={
                                                'data': treedepth_divergent_data,
                                                'layout': treedepth_divergent_layout
                                            })

        return [treedepth_all, treedepth_non_divergent, treedepth_divergent]

    def _get_chains(self):
        chain_data = self.data_warmup
        return [chain_data[chain_data['chain'] == chain] for chain in chain_data['chain'].unique()]
