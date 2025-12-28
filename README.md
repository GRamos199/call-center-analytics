# Call Center Analytics Dashboard

Cost and Productivity Analytics for Call Center Operations

## Overview

This project builds a data pipeline and analytical model for call center cost and productivity analysis, enabling stakeholders to understand operational costs and agent performance.

## Project Structure

```
analytics/
├── main.py                 # Main Streamlit application entry point
├── classes/
│   ├── base_tab.py        # Base class for dashboard tabs with styling
│   ├── monthly_tab.py     # Monthly analytics view
│   └── weekly_tab.py      # Weekly analytics view
├── utils/
│   ├── data_loader.py     # ETL data loading and caching
│   ├── metric_loader.py   # Analytics metrics calculations
│   └── icons_service.py   # UI icons management
├── reporting/
│   ├── monthly/           # Monthly report components
│   └── weekly/            # Weekly report components
└── data/
    ├── calls.csv          # Call operational data
    ├── agents.csv         # Agent information
    └── costs.csv          # Cost configuration
```

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Running the Dashboard

```bash
cd analytics
streamlit run main.py
```

The dashboard will be available at `http://localhost:8501`

## Features

### Monthly Analytics
- Cost per agent analysis
- Cost per client metrics
- Daily trends and visualizations
- Top performers ranking

### Weekly Analytics
- Weekly performance indicators
- Day-by-day breakdown
- Agent performance comparison
- Cost and productivity trends

## Key Metrics

- **Cost per Agent**: Total operational cost attributed to each agent
- **Cost per Client**: Cost allocated to service each client
- **Call Volume**: Total number of calls handled
- **Average Call Duration**: Mean duration of calls
- **Productivity**: Calls handled per agent
- **Hours Worked**: Total hours invested per agent

## Data Sources

The application uses synthetic but realistic call center data:
- `calls.csv`: Individual call records with duration and participants
- `agents.csv`: Agent information and department
- `costs.csv`: Cost configuration and rates

## Technology Stack

- **Python**: Data processing and ETL
- **Streamlit**: Interactive dashboard framework
- **Pandas**: Data manipulation
- **Plotly**: Interactive visualizations
- **DuckDB**: Efficient data operations

## Next Steps

1. Configure real data sources
2. Add more granular time-based analytics
3. Implement agent performance goals
4. Add forecasting models
5. Integrate with operational databases
