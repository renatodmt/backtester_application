from dash import html, dcc
from dashboard_new.strategies import strategies_mapper


def create_parameters_control(mapper, strategy):
    labels_div_children = []
    parameters_div_children = []
    for parameter in mapper[strategy]['parameters']:
        labels_div_children.append(
            html.Label(mapper[strategy]['parameters'][parameter]['label'])
        )
        parameters_div_children.append(
            dcc.Input(
                id=parameter,
                type="number",
                min=mapper[strategy]['parameters'][parameter]['min_value'],
                max=mapper[strategy]['parameters'][parameter]['max_value'],
                step=mapper[strategy]['parameters'][parameter]['step'],
                value=mapper[strategy]['parameters'][parameter]['value'],
            )
        )
    return html.Div(
        id=strategy.replace('_', '-') + '-parameters',
        children=[
            html.Div(children=labels_div_children),
            html.Div(children=parameters_div_children)
        ]
    )


strategy_related_control = html.Div(
    id='strategies-control-form',
    children=[create_parameters_control(strategies_mapper, strategy) for strategy in strategies_mapper]
)