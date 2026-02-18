"""Dashboard layouts and tab content."""

import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import dcc, html
from data import get_sample_data

# Solar theme colors
SOLAR_COLORS = {
    "base03": "#002b36",
    "base02": "#073642",
    "base01": "#586e75",
    "base00": "#657b83",
    "base0": "#839496",
    "base1": "#93a1a1",
    "base2": "#eee8d5",
    "base3": "#fdf6e3",
    "yellow": "#b58900",
    "orange": "#cb4b16",
    "red": "#dc322f",
    "magenta": "#d33682",
    "violet": "#6c71c4",
    "blue": "#268bd2",
    "cyan": "#2aa198",
    "green": "#859900",
}


def create_expenses_tab() -> dbc.Container:
    """
    Create financial overview tab content.

    Returns
    -------
    dbc.Container
        Dashboard layout for financial overview.
    """
    data = get_sample_data()
    current_month_income = data["income"].iloc[-1]
    current_month_expenses = data["expenses"].iloc[-1]
    current_month_savings = data["savings"].iloc[-1]
    avg_savings_rate = (data["savings"].sum() / data["income"].sum()) * 100

    # Summary cards
    summary_cards = dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.H6(
                                    "Current Income",
                                    className="text-muted mb-2",
                                ),
                                html.H3(
                                    f"${current_month_income:,.0f}",
                                    className="mb-0",
                                ),
                            ]
                        )
                    ],
                    className="shadow-sm",
                ),
                width=12,
                lg=3,
            ),
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.H6(
                                    "Current Expenses",
                                    className="text-muted mb-2",
                                ),
                                html.H3(
                                    f"${current_month_expenses:,.0f}",
                                    className="mb-0",
                                ),
                            ]
                        )
                    ],
                    className="shadow-sm",
                ),
                width=12,
                lg=3,
            ),
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.H6(
                                    "Current Savings",
                                    className="text-muted mb-2",
                                ),
                                html.H3(
                                    f"${current_month_savings:,.0f}",
                                    className="mb-0 text-success",
                                ),
                            ]
                        )
                    ],
                    className="shadow-sm",
                ),
                width=12,
                lg=3,
            ),
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.H6(
                                    "Avg. Savings Rate",
                                    className="text-muted mb-2",
                                ),
                                html.H3(
                                    f"{avg_savings_rate:.1f}%",
                                    className="mb-0 text-info",
                                ),
                            ]
                        )
                    ],
                    className="shadow-sm",
                ),
                width=12,
                lg=3,
            ),
        ],
        className="mb-4",
    )

    # Chart: Monthly Income vs Expenses
    income_expenses_fig = go.Figure()
    income_expenses_fig.add_trace(
        go.Bar(
            x=data["date"],
            y=data["income"],
            name="Income",
            marker_color=SOLAR_COLORS["green"],
        )
    )
    income_expenses_fig.add_trace(
        go.Bar(
            x=data["date"],
            y=data["expenses"],
            name="Expenses",
            marker_color=SOLAR_COLORS["red"],
        )
    )
    income_expenses_fig.update_layout(
        title="Monthly Income vs Expenses",
        xaxis_title="Month",
        yaxis_title="Amount ($)",
        template="plotly_dark",
        paper_bgcolor=SOLAR_COLORS["base02"],
        plot_bgcolor=SOLAR_COLORS["base03"],
        font={"color": SOLAR_COLORS["base0"]},
        barmode="group",
        height=400,
        margin={"l": 40, "r": 40, "t": 60, "b": 40},
    )

    # Chart: Savings Trend
    savings_fig = go.Figure()
    savings_fig.add_trace(
        go.Scatter(
            x=data["date"],
            y=data["savings"],
            mode="lines+markers",
            name="Savings",
            line={"color": SOLAR_COLORS["cyan"], "width": 3},
            marker={"size": 8},
        )
    )
    savings_fig.update_layout(
        title="Monthly Savings Trend",
        xaxis_title="Month",
        yaxis_title="Savings ($)",
        template="plotly_dark",
        paper_bgcolor=SOLAR_COLORS["base02"],
        plot_bgcolor=SOLAR_COLORS["base03"],
        font={"color": SOLAR_COLORS["base0"]},
        height=400,
        margin={"l": 40, "r": 40, "t": 60, "b": 40},
    )

    return dbc.Container(
        [
            summary_cards,
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                dcc.Graph(figure=income_expenses_fig)
                            ),
                            className="shadow-sm",
                        ),
                        width=12,
                        lg=6,
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(dcc.Graph(figure=savings_fig)),
                            className="shadow-sm",
                        ),
                        width=12,
                        lg=6,
                    ),
                ],
                className="mb-4",
            ),
        ],
        fluid=True,
    )


def create_investing_tab() -> dbc.Container:
    """
    Create investing tab content.

    Returns
    -------
    dbc.Container
        Dashboard layout for investing overview.
    """
    return dbc.Container(
        [
            html.H2("Investing", className="mb-4"),
            dbc.Alert(
                "Coming soon! This section will track your investment portfolio.",
                color="info",
            ),
        ],
        fluid=True,
    )


def create_flat_payments_tab() -> dbc.Container:
    """
    Create flat payments tab content.

    Returns
    -------
    dbc.Container
        Dashboard layout for flat payments tracking.
    """
    return dbc.Container(
        [
            html.H2("Flat Payments", className="mb-4"),
            dbc.Alert(
                "Coming soon! This section will track rent, utilities, and other flat-related expenses.",
                color="info",
            ),
        ],
        fluid=True,
    )


def create_jarvis_tab() -> dbc.Container:
    """
    Create Jarvis AI tab content.

    Returns
    -------
    dbc.Container
        Dashboard layout for Jarvis AI assistant.
    """
    return dbc.Container(
        [
            html.H2("Jarvis AI", className="mb-4"),
            dbc.Alert(
                "Coming soon! Your AI assistant for financial insights and automation.",
                color="info",
            ),
        ],
        fluid=True,
    )


def create_services_tab() -> dbc.Container:
    """
    Create services tab content.

    Returns
    -------
    dbc.Container
        Dashboard layout for subscription services tracking.
    """
    return dbc.Container(
        [
            html.H2("Services", className="mb-4"),
            dbc.Alert(
                "Coming soon! This section will track your subscription services and recurring payments.",
                color="info",
            ),
        ],
        fluid=True,
    )
