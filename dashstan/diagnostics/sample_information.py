from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.figure_factory as ff


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
            iter_lp_graph,
            iter_metro_graph,
            lp_hist,
            metro_hist,
            metro_lp_plot,
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
            title='Mean Metrop. Acceptance'
        )
        return dcc.Graph(id='iter_metro_graph',
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
            title='Log Posterior'
        )

        return dcc.Graph(id='iter_lp_graph',
                         figure={
                             'data': traces,
                             'layout': layout,
                         })

    def _build_lp_hist(self):
        layout = go.Layout(
            title='Log Posterior'
        )
        return dcc.Graph(id='lp_hist',
                         figure={
                             'data': [go.Histogram(x=self.data_warmup['lp__'])],
                             'layout': layout,
                         })

    def _build_metro_hist(self):
        layout = go.Layout(
            title='Mean Metrop. Acceptance'
        )
        return dcc.Graph(id='metro_hist',
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
            xaxis={
                'title': 'Mean Metrop. Acceptance',
            },
            yaxis={
                'title': 'Log Posterior',
            },
        )
        return dcc.Graph(id='metro_lp_plot',
                         figure={
                             'data': traces,
                             'layout': layout,
                         })
