"""Personal Dashboard Application."""

from datetime import datetime

import dash
import dash_bootstrap_components as dbc
from dash import html

# Initialize app with Solar theme and Font Awesome icons
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.SOLAR,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css",
    ],
    suppress_callback_exceptions=True,
)


# Sidebar menu
sidebar = html.Div(
    [
        html.H2("Dashboard", className="text-center mb-4"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink(
                    [
                        html.I(className="fas fa-chart-line me-2"),
                        "Expenses",
                    ],
                    href="#",
                    id="expenses-link",
                    active=True,
                ),
                dbc.NavLink(
                    [
                        html.I(className="fas fa-chart-pie me-2"),
                        "Investing",
                    ],
                    href="#",
                    id="investing-link",
                    active=False,
                ),
                dbc.NavLink(
                    [
                        html.I(className="fas fa-home me-2"),
                        "Flat Payments",
                    ],
                    href="#",
                    id="flat-link",
                    active=False,
                ),
                dbc.NavLink(
                    [
                        html.I(className="fas fa-robot me-2"),
                        "Jarvis AI",
                    ],
                    href="#",
                    id="jarvis-link",
                    active=False,
                ),
                dbc.NavLink(
                    [
                        html.I(className="fas fa-cogs me-2"),
                        "Services",
                    ],
                    href="#",
                    id="services-link",
                    active=False,
                ),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style={
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "16rem",
        "padding": "2rem 1rem",
        "background-color": "#002b36",
    },
)

# Main content area
content = html.Div(
    [
        # Header
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.H1("Personal Dashboard", className="mb-1"),
                        html.P(
                            (
                                f"Last updated: "
                                f"{datetime.now().strftime('%B %d, %Y')}"
                            ),
                            className="text-muted",
                        ),
                    ],
                    className="my-4",
                )
            )
        ),
        # Page content
        html.Div(id="page-content"),
    ],
    style={"margin-left": "18rem", "padding": "2rem 1rem"},
)

# App layout
app.layout = html.Div([sidebar, content])

if __name__ == "__main__":
    # Import and register callbacks with the app
    from callbacks import register_callbacks

    register_callbacks(app)
    app.run(debug=True, host="0.0.0.0", port=8050)
