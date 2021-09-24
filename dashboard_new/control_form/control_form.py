from dash import html
import dashboard_new.control_form.permanent_controls as permanent_controls
import dashboard_new.control_form.strategy_related_controls as strategy_related_controls
import dashboard_new.control_form.callbacks

control_form = html.Div(
    children=[
        permanent_controls.permanent_control,
        strategy_related_controls.strategy_related_control
    ]
)
