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

class Estimate(html.Div):

    def __init__(self, app, data, **kwargs):
        super().__init__(**kwargs)
        self.data = data
        self.app = app
        self._estimate_tabs = {
        }
        self._build_children()

    def _build_children(self):
        self.children = []