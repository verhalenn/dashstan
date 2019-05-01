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

from .treedepth_information import TreeDepth
from .by_model_parameter import ByModelParameter
from .sample_information import SampleInformation
from .divergence_information import DivergenceInformation
from .step_size_information import StepSizeInformation


class Diagnostics(html.Div):

    def __init__(self, app, data, **kwargs):
        super().__init__(**kwargs)
        self.data = data
        self.app = app
        self._diagnostics_tabs = {
            'by_model_parameter': ByModelParameter(app=self.app, data=self.data),
            'sample_information': SampleInformation(app=self.app, data=self.data),
            'divergence_information': DivergenceInformation(app=self.app, data=self.data),
            'treedepth_information': TreeDepth(app=self.app, data=self.data),
            'step_size_information': StepSizeInformation(app=self.app, data=self.data),
        }
        self.build_children()
        self.build_callbacks()

    def build_callbacks(self):
        @self.app.callback(
            Output(component_id='diagnostics-holder', component_property='children'),
            [Input(component_id='diagnostics-tabs', component_property='value')]
        )
        def render_diagnostics_tab(value):
            return self._diagnostics_tabs[value]

    def build_children(self):
        self.children = [
            dcc.Tabs(id='diagnostics-tabs', value='by_model_parameter', children=[
                dcc.Tab(label=self._diagnostics_tabs[key].get_label(), value=key) for key in self._diagnostics_tabs
            ]),
            html.Div(id='diagnostics-holder'),
        ]
