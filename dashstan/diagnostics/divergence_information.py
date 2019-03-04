import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go


class DivergenceInformation(html.Div):

    def __init__(self, app, data, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.data = data
        self.data_warmup = self.data[self.data['warmup'] == 0]
        self.build_children()

    def build_children(self):
        self.chains = self._get_chains()
        divergent_step = self._build_divergent_step()
        divergent_log_violin = self._build_divergent_violin()
        divergent_metro_violin = self._build_divergent_metro_violin()
        self.children = [
            divergent_step,
            divergent_log_violin,
            divergent_metro_violin,
        ]

    def _build_divergent_step(self):
        traces = [go.Scatter({'x': chain['draw'],
                              'y': chain['divergent__'],
                              'mode': 'lines',
                              'name': 'Chain: {}'.format(chain['chain'].iloc[0]),
                              'line': dict(
                                  shape='hvh'
                              )
                              }) for chain in self.chains]
        layout = go.Layout(
            title='Divergent'
        )
        return dcc.Graph(id='divergent_step',
                         figure={
                             'data': traces,
                             'layout': layout,
                         }
                         )

    def _build_divergent_violin(self):
        traces = [
            {'type': 'violin',
             'x': self.data_warmup['divergent__'][self.data_warmup['divergent__'] == divergent],
             'y': self.data_warmup['lp__'][self.data_warmup['divergent__'] == divergent],}
            for divergent in self.data_warmup['divergent__'].unique()
        ]

        return dcc.Graph(id='divergent_log_violin',
                         figure={
                             'data': traces,
                         })

    def _build_divergent_metro_violin(self):
        traces = [
            {'type': 'violin',
             'x': self.data_warmup['divergent__'][self.data_warmup['divergent__'] == divergent],
             'y': self.data_warmup['accept_stat__'][self.data_warmup['divergent__'] == divergent],}
            for divergent in self.data_warmup['divergent__'].unique()
        ]

        return dcc.Graph(id='divergent_metro_violin',
                         figure={
                             'data': traces,
                         })


    def _get_chains(self):
        chain_data = self.data_warmup
        return [chain_data[chain_data['chain'] == chain] for chain in chain_data['chain'].unique()]
