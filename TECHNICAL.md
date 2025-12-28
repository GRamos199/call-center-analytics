# Technical Architecture

## Overview

The Call Center Analytics Dashboard is built with a modular, scalable architecture that separates concerns into different layers:

```
┌─────────────────────────────────────────┐
│      Streamlit UI (main.py)             │
│   - Monthly Tab                         │
│   - Weekly Tab                          │
└──────────────┬──────────────────────────┘
               │
┌──────────────┴──────────────────────────┐
│    Tab Classes (classes/)               │
│   - BaseTab (styling & common methods)  │
│   - MonthlyTab (monthly view)           │
│   - WeeklyTab (weekly view)             │
└──────────────┬──────────────────────────┘
               │
┌──────────────┴──────────────────────────┐
│    Utilities (utils/)                   │
│   - DataLoader (ETL & caching)          │
│   - MetricLoader (analytics engine)     │
│   - IconsService (UI elements)          │
└──────────────┬──────────────────────────┘
               │
┌──────────────┴──────────────────────────┐
│    Data Layer (data/)                   │
│   - calls.csv                           │
│   - agents.csv                          │
│   - costs.csv                           │
└─────────────────────────────────────────┘
```

## Components

### Data Layer (`analytics/data/`)

CSV files containing:
- **calls.csv**: Call records with timestamps and participants
- **agents.csv**: Agent information and department
- **costs.csv**: Cost configuration and rates

### Utils Layer (`analytics/utils/`)

#### DataLoader (`data_loader.py`)
- Loads CSV data with type conversion
- Implements in-memory caching for performance
- Validates data integrity
- Provides date range information

```python
loader = DataLoader()
calls_df = loader.load_calls_data()  # Returns cached DataFrame
```

#### MetricLoader (`metric_loader.py`)
- Calculates all KPIs and business metrics
- Supports period-to-period comparisons (delta calculations)
- Generates daily, weekly, monthly aggregations

```python
metrics = MetricLoader(data_loader)
cost_per_agent = metrics.calculate_cost_per_agent(start_date, end_date)
deltas = metrics.calculate_deltas(current_period, previous_period)
```

#### IconsService (`icons_service.py`)
- Centralized icon management
- Unicode and emoji-based icons from popular libraries
- Easy icon mapping for metrics

```python
icon = IconsService.get_metric_icon("cost_per_agent")  # Returns 💰
```

### Classes Layer (`analytics/classes/`)

#### BaseTab (`base_tab.py`)
- Abstract base class for all dashboard tabs
- Defines color scheme and styling
- Provides helper methods for rendering
- Common UI patterns

```python
class MonthlyTab(BaseTab):
    def render(self):
        self.render_header()
        self.render_metric("Label", value, delta)
```

#### MonthlyTab (`monthly_tab.py`)
- Monthly analytics view
- KPI metrics with deltas
- Agent performance ranking
- Trend visualizations

#### WeeklyTab (`weekly_tab.py`)
- Weekly analytics view
- Daily breakdown
- Agent comparison
- Weekly trends

### UI Layer (`main.py`)

- Entry point for Streamlit application
- Tab management
- Sidebar navigation
- Page configuration

## Data Flow

1. **Data Loading**: `DataLoader` reads CSV files and caches them
2. **Metric Calculation**: `MetricLoader` computes KPIs using loaded data
3. **Tab Rendering**: Tab classes format metrics for display
4. **UI Rendering**: Streamlit renders the final dashboard

## Key Metrics

### Cost Metrics
- **Cost per Agent**: Total operational cost attributed to each agent
  - Calculated as: `hours_worked × hourly_rate`
- **Cost per Client**: Cost allocated to service each client
  - Calculated as: `total_hours_per_client × hourly_rate`

### Productivity Metrics
- **Total Calls**: Count of all call records
- **Average Call Duration**: Mean duration in minutes
- **Calls per Agent**: Average calls per unique agent
- **Active Agents**: Count of unique agents in period

### Trend Metrics (Deltas)
- **Value**: Absolute change from previous period
- **Percentage**: Percent change ((current - previous) / previous × 100)
- **Trend**: Direction indicator (up, down, flat)

## Database Schema (CSV Format)

### calls.csv
```
call_id      | INTEGER | Unique call identifier
agent_id     | INTEGER | Reference to agent
client_id    | INTEGER | Reference to client
date         | DATE    | Call date
start_time   | DATETIME| Call start timestamp
end_time     | DATETIME| Call end timestamp
duration_minutes | FLOAT| Duration in minutes
```

### agents.csv
```
agent_id     | INTEGER | Unique agent identifier
agent_name   | STRING  | Agent name
department   | STRING  | Department (Sales/Support)
hire_date    | DATE    | Hiring date
```

### costs.csv
```
cost_type    | STRING  | Type of cost
amount       | FLOAT   | Cost amount
currency     | STRING  | Currency (USD)
description  | STRING  | Description
```

## Performance Considerations

### Caching Strategy
- Data is cached in memory after first load
- Cache can be cleared via UI button or programmatically
- Appropriate for datasets < 1GB

### Optimization Points
- CSV loading uses pandas (efficient for small files)
- Filtering is done in-memory with pandas
- Consider DuckDB for larger datasets (50GB+)

## Extension Points

### Adding New Metrics
Extend `MetricLoader` with new calculation methods:

```python
def calculate_custom_metric(self, date_from, date_to):
    # Your calculation logic
    return metric_dataframe
```

### Adding New Tabs
Create new tab class extending `BaseTab`:

```python
class CustomTab(BaseTab):
    def __init__(self):
        super().__init__(title="Custom", icon="📊")
    
    def render(self):
        self.render_header()
        # Your tab content
```

### Styling Customization
Modify color scheme in `BaseTab.COLORS`:

```python
COLORS = {
    "primary": "#FF6B6B",
    "secondary": "#4ECDC4",
    # Add or modify colors
}
```

## Future Enhancements

1. **Database Backend**: Replace CSV with DuckDB/PostgreSQL
2. **Real-time Updates**: WebSocket integration for live data
3. **Forecasting**: ML models for trend prediction
4. **Advanced Filtering**: Multi-select date ranges and agents
5. **Export Features**: PDF/Excel report generation
6. **Authentication**: User roles and data access control
7. **Performance Monitoring**: Query execution time tracking

## Dependencies

- **streamlit**: UI framework
- **pandas**: Data manipulation
- **numpy**: Numerical operations
- **plotly**: Interactive visualizations
- **duckdb**: Efficient data querying (optional)
- **python-dateutil**: Date utilities
