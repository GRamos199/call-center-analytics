# Getting Started

## Quick Start

### Option 1: Using the Start Script (Recommended)

```bash
./start.sh
```

This script will:
1. Create a virtual environment if it doesn't exist
2. Activate the virtual environment
3. Install all dependencies from `requirements.txt`
4. Start the Streamlit dashboard

### Option 2: Manual Setup

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Generate synthetic data (optional, already included)
python3 analytics/utils/data_generator.py

# Run the application
cd analytics
streamlit run main.py
```

## Verify Installation

Before running the application, verify everything is set up correctly:

```bash
source venv/bin/activate
python3 check_project.py
```

This should show all green checkmarks ✅

## Access the Dashboard

Once Streamlit is running, open your browser and navigate to:

```
http://localhost:8501
```

## Project Structure

```
analytics/
├── main.py                    # Main application entry point
├── classes/                   # Dashboard tab classes
│   ├── base_tab.py           # Base class with common styling
│   ├── monthly_tab.py        # Monthly analytics view
│   └── weekly_tab.py         # Weekly analytics view
├── utils/                     # Utility modules
│   ├── data_loader.py        # Data loading and caching
│   ├── metric_loader.py      # Metrics calculations
│   ├── icons_service.py      # UI icons management
│   └── data_generator.py     # Synthetic data generation
├── data/                      # CSV data files
│   ├── calls.csv             # Call records
│   ├── agents.csv            # Agent information
│   └── costs.csv             # Cost configuration
└── reporting/                # Report templates (for future use)
```

## Features

### 📅 Monthly Analytics
- Cost per agent analysis with top performers
- Cost per client metrics
- Daily trends visualization
- Agent ranking and performance metrics

### 📆 Weekly Analytics
- Weekly performance indicators
- Day-by-day breakdown
- Agent performance comparison
- Cost and productivity trends

## Dashboard Metrics

- **Total Calls**: Number of calls handled
- **Average Duration**: Mean call length
- **Active Agents**: Number of working agents
- **Unique Clients**: Number of unique customers
- **Cost per Agent**: Operational cost per agent
- **Cost per Client**: Service cost allocation
- **Productivity**: Calls handled per agent

## Data

The application uses synthetic but realistic call center data:

- **587 call records** with duration and participant information
- **6 agents** from different departments (Sales and Support)
- **Cost configuration** with hourly rates and overhead costs

## Customization

### Modifying Colors and Styling

Edit the `COLORS` dictionary in [analytics/classes/base_tab.py](analytics/classes/base_tab.py#L11):

```python
COLORS = {
    "primary": "#FF6B6B",
    "secondary": "#4ECDC4",
    # ... more colors
}
```

### Generating New Data

To generate fresh synthetic data:

```bash
source venv/bin/activate
python3 analytics/utils/data_generator.py
```

### Adding Custom Icons

Edit [analytics/utils/icons_service.py](analytics/utils/icons_service.py) to add new icons or modify existing ones.

## Troubleshooting

### Module Import Errors

If you get import errors, ensure:
1. Virtual environment is activated: `source venv/bin/activate`
2. Dependencies are installed: `pip install -r requirements.txt`
3. Working directory is correct: `cd /home/george/call-center-analytics`

### Streamlit Not Found

Install Streamlit explicitly:

```bash
source venv/bin/activate
pip install streamlit>=1.28.0
```

### Data Files Not Found

Ensure you're running from the correct directory and data files exist in `analytics/data/`:

```bash
ls -la analytics/data/
```

## Next Steps

1. **Connect Real Data**: Replace CSV files with your actual call center data
2. **Add More Metrics**: Extend `MetricLoader` with additional KPIs
3. **Custom Reports**: Create additional tabs by extending `BaseTab`
4. **Database Integration**: Replace CSV with DuckDB or PostgreSQL
5. **Authentication**: Add user authentication for production use
