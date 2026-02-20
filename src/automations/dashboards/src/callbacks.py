"""Dashboard callbacks for handling interactivity."""

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output
from layouts import (
    create_expenses_tab,
    create_flat_payments_tab,
    create_investing_tab,
    create_jarvis_tab,
    create_services_tab,
)


def register_callbacks(app):
    """
    Register all callbacks with the app.

    Parameters
    ----------
    app : dash.Dash
        The Dash application instance.
    """

    @app.callback(
        [
            Output("page-content", "children"),
            Output("expenses-link", "active"),
            Output("investing-link", "active"),
            Output("flat-link", "active"),
            Output("jarvis-link", "active"),
            Output("services-link", "active"),
        ],
        [
            Input("expenses-link", "n_clicks"),
            Input("investing-link", "n_clicks"),
            Input("flat-link", "n_clicks"),
            Input("jarvis-link", "n_clicks"),
            Input("services-link", "n_clicks"),
        ],
    )
    def render_page_content(
        expenses_clicks: int | None,
        investing_clicks: int | None,
        flat_clicks: int | None,
        jarvis_clicks: int | None,
        services_clicks: int | None,
    ) -> tuple[dbc.Container, bool, bool, bool, bool, bool]:
        """
        Render content based on sidebar navigation.

        Parameters
        ----------
        expenses_clicks : int | None
            Number of clicks on expenses link.
        investing_clicks : int | None
            Number of clicks on investing link.
        flat_clicks : int | None
            Number of clicks on flat payments link.
        jarvis_clicks : int | None
            Number of clicks on Jarvis AI link.
        services_clicks : int | None
            Number of clicks on services link.

        Returns
        -------
        tuple[dbc.Container, bool, bool, bool, bool, bool]
            Page content and active states for each nav link.
        """
        ctx = dash.callback_context

        if not ctx.triggered:
            return (
                create_expenses_tab(),
                True,
                False,
                False,
                False,
                False,
            )

        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if button_id == "expenses-link":
            return (
                create_expenses_tab(),
                True,
                False,
                False,
                False,
                False,
            )
        elif button_id == "investing-link":
            return (
                create_investing_tab(),
                False,
                True,
                False,
                False,
                False,
            )
        elif button_id == "flat-link":
            return (
                create_flat_payments_tab(),
                False,
                False,
                True,
                False,
                False,
            )
        elif button_id == "jarvis-link":
            return (
                create_jarvis_tab(),
                False,
                False,
                False,
                True,
                False,
            )
        elif button_id == "services-link":
            return (
                create_services_tab(),
                False,
                False,
                False,
                False,
                True,
            )

        return (
            create_expenses_tab(),
            True,
            False,
            False,
            False,
            False,
        )
