from dash import dcc, html, dash_table


figures_component = html.Div(children=[
    dcc.Graph(id='price-graph'),
    dcc.Graph(id='profit-and-loss-graph'),
    dcc.Graph(id='indicators-graph'),
    html.Div(
        children=dash_table.DataTable(
            id='trade-summary',
            data=[]
        )
    )
])
