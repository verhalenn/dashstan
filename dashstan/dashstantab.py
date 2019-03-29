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

import dash_html_components as html


class DashStanTab(html.Div):

    def __init__(self, app, data, label, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.data = data
        self.label = label

    def get_label(self):
        return self.label

    def get_parameters(self, lp__=True):
        not_parameters = ['chain', 'draw', 'warmup', 'accept_stat__', 'stepsize__',
                          'treedepth__', 'n_leapfrog__', 'divergent__', 'energy__']
        if not lp__:
            not_parameters.append('lp__')
        return [column for column in self.data.columns if column not in not_parameters]

    def get_chains(self):
        chain_data = self.data_warmup
        return [chain_data[chain_data['chain'] == chain] for chain in chain_data['chain'].unique()]
