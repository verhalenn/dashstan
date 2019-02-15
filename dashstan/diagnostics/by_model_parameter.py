import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.figure_factory as ff


class ByModelParameter(html.Div):

    def __init__(self, app, data, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.data = data
        self.build_children()
        self.build_callbacks()

    def build_children(self):
        not_parameters = ['chain', 'draw', 'warmup', 'accept_stat__', 'stepsize__',
                          'treedepth__', 'n_leapfrog__', 'divergent__', 'energy__']
        self.children = [
            # TODO include warmup checkbox
            dcc.Dropdown(
                id='parameter-input',
                options=[
                    {'label': x, 'value': x} for x in self.data.columns if x not in not_parameters
                ]
            ),
            dcc.Graph(id='chain-graph'),
            dcc.Graph(id='parameter-dist-plot'),
            dcc.Graph(id='parameter-lp-plot')
        ]

    def build_callbacks(self):
        @self.app.callback(
            Output(component_id='chain-graph', component_property='figure'),
            [Input(component_id='parameter-input', component_property='value')]
        )
        def render_chain_graph(value):
            chain_data = self.data[self.data['warmup'] == 0]
            chains = [chain_data[chain_data['chain'] == chain] for chain in chain_data['chain'].unique()]
            traces = [go.Scatter({'x': chain['draw'],
                                  'y': chain[value],
                                  'mode': 'lines',
                                  'name': 'Chain: {}'.format(chain['chain'].iloc[0]),
                                  }) for chain in chains]
            return {
                'data': traces,
            }

        @self.app.callback(
            Output(component_id='parameter-dist-plot', component_property='figure'),
            [Input(component_id='parameter-input', component_property='value')]
        )
        def render_dist_plot(value):
            dist_data = [self.data[self.data['warmup'] == 0][value]]
            labels = [value]
            return {
                'data': ff.create_distplot(dist_data, labels),
            }

        @self.app.callback(
            Output(component_id='parameter-lp-plot', component_property='figure'),
            [Input(component_id='parameter-input', component_property='value')]
        )
        def render_lp_plot(value):
            lp_data = self.data[self.data['warmup'] == 0]
            traces = [go.Scatter(
                        x=lp_data[value],
                        y=lp_data['lp__'],
                        mode='markers')]
            return {
                'data': traces
            }
