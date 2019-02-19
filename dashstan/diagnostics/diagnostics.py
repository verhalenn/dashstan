import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from .by_model_parameter import ByModelParameter
from .sample_information import SampleInformation


class Diagnostics(html.Div):

    def __init__(self, app, data, **kwargs):
        super().__init__(**kwargs)
        self.data = data
        self.app = app
        self._diagnostics_tabs = {
            'by_model_parameter': {
                'label': 'By Model Parameter',
                'page': ByModelParameter(app=self.app, data=self.data)
            },
            'samlpe_information': {
                'label': 'Sample Information',
                'page': SampleInformation(app=self.app, data=self.data)
            },
        }
        self.build_children()
        self.build_callbacks()

    def build_callbacks(self):
        @self.app.callback(
            Output(component_id='diagnostics-holder', component_property='children'),
            [Input(component_id='diagnostics-tabs', component_property='value')]
        )
        def render_diagnostics_tab(value):
            return self._diagnostics_tabs[value]['page']

    def build_children(self):
        self.children = [
            dcc.Tabs(id='diagnostics-tabs', value='by_model_parameter', children=[
                dcc.Tab(label=self._diagnostics_tabs[key]['label'], value=key) for key in self._diagnostics_tabs
            ]),
            html.Div(id='diagnostics-holder'),
        ]
