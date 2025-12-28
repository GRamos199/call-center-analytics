"""
Data generation utility.
Generates synthetic call center data for analytics testing.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path


def generate_calls_data(
    start_date: str = "2025-12-01",
    num_days: int = 30,
    num_agents: int = 6,
    num_clients: int = 100,
    calls_per_day: int = 20,
):
    """
    Generate synthetic calls data.
    
    Args:
        start_date: Start date for data generation
        num_days: Number of days to generate
        num_agents: Number of agents
        num_clients: Number of clients
        calls_per_day: Average calls per day
    
    Returns:
        DataFrame with calls data
    """
    start = pd.to_datetime(start_date)
    dates = [start + timedelta(days=i) for i in range(num_days)]
    
    data = []
    call_id = 1
    
    for date in dates:
        num_calls = np.random.poisson(calls_per_day)
        for _ in range(num_calls):
            agent_id = np.random.randint(101, 101 + num_agents)
            client_id = np.random.randint(201, 201 + num_clients)
            
            hour = np.random.randint(8, 17)
            minute = np.random.randint(0, 60)
            second = np.random.randint(0, 60)
            
            start_time = date.replace(hour=hour, minute=minute, second=second)
            duration = np.random.normal(16, 6)
            duration = max(2, min(60, duration))
            end_time = start_time + timedelta(minutes=duration)
            
            data.append({
                "call_id": call_id,
                "agent_id": agent_id,
                "client_id": client_id,
                "date": date.date(),
                "start_time": start_time,
                "end_time": end_time,
                "duration_minutes": duration,
            })
            call_id += 1
    
    return pd.DataFrame(data)


def generate_agents_data(num_agents: int = 6):
    """
    Generate synthetic agents data.
    
    Args:
        num_agents: Number of agents to generate
    
    Returns:
        DataFrame with agents data
    """
    names = [
        "Alice Johnson", "Bob Smith", "Carol White", "David Brown",
        "Emma Davis", "Frank Miller", "Grace Lee", "Henry Wilson",
        "Iris Taylor", "Jack Anderson"
    ]
    departments = ["Sales", "Support"]
    
    data = []
    for i in range(num_agents):
        data.append({
            "agent_id": 101 + i,
            "agent_name": names[i % len(names)],
            "department": np.random.choice(departments),
            "hire_date": (pd.Timestamp.now() - timedelta(days=np.random.randint(30, 730))).date(),
        })
    
    return pd.DataFrame(data)


def generate_costs_data():
    """
    Generate costs configuration data.
    
    Returns:
        DataFrame with costs data
    """
    data = [
        {
            "cost_type": "hourly_rate",
            "amount": 45.50,
            "currency": "USD",
            "description": "Average hourly rate for agents"
        },
        {
            "cost_type": "equipment_per_agent",
            "amount": 500,
            "currency": "USD",
            "description": "Equipment cost per agent per year"
        },
        {
            "cost_type": "infrastructure",
            "amount": 2500,
            "currency": "USD",
            "description": "Monthly infrastructure cost"
        },
        {
            "cost_type": "management",
            "amount": 3000,
            "currency": "USD",
            "description": "Monthly management overhead"
        }
    ]
    
    return pd.DataFrame(data)


def generate_all_data(output_dir: str = "analytics/data"):
    """
    Generate all synthetic data files.
    
    Args:
        output_dir: Directory to save CSV files
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print("Generating calls data...")
    calls_df = generate_calls_data()
    calls_df.to_csv(output_path / "calls.csv", index=False)
    print(f"  Created calls.csv with {len(calls_df)} records")
    
    print("Generating agents data...")
    agents_df = generate_agents_data()
    agents_df.to_csv(output_path / "agents.csv", index=False)
    print(f"  Created agents.csv with {len(agents_df)} records")
    
    print("Generating costs data...")
    costs_df = generate_costs_data()
    costs_df.to_csv(output_path / "costs.csv", index=False)
    print(f"  Created costs.csv with {len(costs_df)} records")
    
    print("\nData generation complete!")


if __name__ == "__main__":
    generate_all_data()
