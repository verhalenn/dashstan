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
from dashstan import dashstantab
import dash_table
import plotly.graph_objs as go
import pandas as pd

class PostSummaryStats(dashstantab.DashStanTab):

    def __init__(self, raw_data, app, data, **kwargs):
        super().__init__(app, data, **kwargs)
        self.label='Post-Summary-Stats'
        self.raw_data = raw_data
        self.summary_stats = self.summary_to_df(raw_data=raw_data)
        self._build_children()

    def _build_children(self):
        self.children = [
            dash_table.DataTable(
                id='Post-Summary-Stats',
                columns=[{'name': i, 'id': i} for i in self.summary_stats.columns],
                data=self.summary_stats.to_dict("rows"),
            )
        ]

    def summary_to_df(self, raw_data):
        columns = raw_data.summary()['summary_colnames']
        data = raw_data.summary()['summary']
        df = pd.DataFrame(data, columns=columns)
        df.insert(0, 'Parameters', raw_data.summary()['summary_rownames'])
        return df

