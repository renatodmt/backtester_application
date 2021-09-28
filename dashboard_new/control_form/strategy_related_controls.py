from dash import html, dcc
from dashboard_new.strategies import strategies_mapper


def create_parameters_control(mapper, strategy):
    div_childs = []
    for parameter in mapper[strategy]['parameters']:
        div_childs.append(
            html.Label(mapper[strategy]['parameters'][parameter]['label'])
        )
        div_childs.append(
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
        children=div_childs,
        className='strategy-related-control-grid'
    )


strategy_related_control = html.Div(
    id='strategies-control-form',
    children=[create_parameters_control(strategies_mapper, strategy) for strategy in strategies_mapper]
)