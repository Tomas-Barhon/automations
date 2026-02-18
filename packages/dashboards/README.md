# Personal Dashboard

A minimalist personal dashboard built with Dash and Plotly for tracking finances and more.

## Features

- **Financial Overview Tab**: Track income, expenses, and savings with interactive charts
- Clean, modern UI using Bootstrap Flatly theme
- Responsive design that works on desktop and mobile
- Easy to extend with additional tabs

## Setup

1. Install dependencies:
```bash
cd dashboards
uv sync
```

2. Run the app:
```bash
uv run python src/app.py
```

3. Open your browser to: `http://localhost:8050`

## Customization

### Adding Your Own Data

Replace the `get_sample_data()` function in `src/app.py` with your own data source:

```python
def get_sample_data() -> pd.DataFrame:
    """Load your actual financial data."""
    # Load from CSV, database, or API
    return pd.read_csv('your_data.csv')
```

### Adding New Tabs

1. Create a new tab content function similar to `create_financial_overview_tab()`
2. Add the tab to the `dbc.Tabs` component in the layout
3. Update the `render_tab_content` callback to handle the new tab

## Tech Stack

- **Dash**: Web application framework
- **Plotly**: Interactive charting
- **Dash Bootstrap Components**: Modern UI components
- **Pandas**: Data manipulation
