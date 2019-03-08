from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.figure_factory as ff

class TreeDepth(html.Div):

    def __init__(self, app, data, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self. data = data
        self.data_warmup = self.data[self.data['warmup'] == 0]
        self.build_children()

    def build_children(self):
        self.chains = self._get_chains()
        treedeph_step = self._build_treedepth_step()
        self.children = [
            treedeph_step,
        ]

    def _build_treedepth_step(self):
        traces = [go.Scatter(x=chain['draw'],
                             y=chain['treedepth__'],
                             mode='lines',
                             name='Chain: {}'.format(chain['chain'].iloc[0]),
                             ) for chain in self.chains]

        return dcc.Graph(id='treedepth_step',
                         figure={
                             'data': traces,
                         })


    def _get_chains(self):
        chain_data = self.data_warmup
        return [chain_data[chain_data['chain'] == chain] for chain in chain_data['chain'].unique()]
