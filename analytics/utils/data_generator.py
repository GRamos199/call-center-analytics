"""
Data generation utility.
Generates synthetic call center data for analytics testing.
"""

from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

# Configuration
AGENTS = [
    {"agent_id": 101, "agent_name": "Alice Johnson", "department": "Sales"},
    {"agent_id": 102, "agent_name": "Bob Smith", "department": "Sales"},
    {"agent_id": 103, "agent_name": "Carol White", "department": "Support"},
    {"agent_id": 104, "agent_name": "David Brown", "department": "Sales"},
    {"agent_id": 105, "agent_name": "Emma Davis", "department": "Support"},
    {"agent_id": 106, "agent_name": "Frank Miller", "department": "Support"},
]

CHANNELS = ["Phone", "Email", "Chat", "WhatsApp"]

COSTS = {
    "hourly_rate": 45.50,
    "cost_per_call": 2.50,
    "cost_per_email": 1.00,
    "cost_per_chat": 0.75,
    "cost_per_whatsapp": 0.50,
}


def get_mondays(start_date: str, num_weeks: int) -> list:
    """Get list of Monday dates for weekly data."""
    start = pd.to_datetime(start_date)
    # Adjust to the nearest Monday
    days_until_monday = (7 - start.weekday()) % 7
    if start.weekday() != 0:
        start = start + timedelta(days=days_until_monday)

    return [start + timedelta(weeks=i) for i in range(num_weeks)]


def get_months(start_date: str, num_months: int) -> list:
    """Get list of first day of month dates for monthly data."""
    start = pd.to_datetime(start_date).replace(day=1)
    months = []
    for i in range(num_months):
        month = start.month + i
        year = start.year + (month - 1) // 12
        month = ((month - 1) % 12) + 1
        months.append(pd.Timestamp(year=year, month=month, day=1))
    return months


# =============================================================================
# WEEKLY DATA GENERATORS
# =============================================================================


def generate_weekly_overall(
    start_date: str = "2025-01-06", num_weeks: int = 52
) -> pd.DataFrame:
    """Generate weekly overall metrics."""
    weeks = get_mondays(start_date, num_weeks)

    data = []
    for week in weeks:
        total_calls = np.random.randint(800, 1200)
        total_emails = np.random.randint(300, 500)
        total_chats = np.random.randint(400, 600)
        total_whatsapp = np.random.randint(200, 400)

        total_interactions = total_calls + total_emails + total_chats + total_whatsapp

        avg_handle_time = np.random.uniform(12, 18)
        avg_wait_time = np.random.uniform(1, 5)
        first_call_resolution = np.random.uniform(0.70, 0.90)
        customer_satisfaction = np.random.uniform(3.5, 4.8)

        total_cost = (
            total_calls * COSTS["cost_per_call"]
            + total_emails * COSTS["cost_per_email"]
            + total_chats * COSTS["cost_per_chat"]
            + total_whatsapp * COSTS["cost_per_whatsapp"]
            + len(AGENTS) * COSTS["hourly_rate"] * 40  # 40 hours per week
        )

        data.append(
            {
                "week_start": week.date(),
                "total_calls": total_calls,
                "total_emails": total_emails,
                "total_chats": total_chats,
                "total_whatsapp": total_whatsapp,
                "total_interactions": total_interactions,
                "avg_handle_time_minutes": round(avg_handle_time, 2),
                "avg_wait_time_minutes": round(avg_wait_time, 2),
                "first_call_resolution_rate": round(first_call_resolution, 4),
                "customer_satisfaction_score": round(customer_satisfaction, 2),
                "total_cost": round(total_cost, 2),
                "cost_per_interaction": round(total_cost / total_interactions, 2),
            }
        )

    return pd.DataFrame(data)


def generate_weekly_agent(
    start_date: str = "2025-01-06", num_weeks: int = 52
) -> pd.DataFrame:
    """Generate weekly agent performance metrics."""
    weeks = get_mondays(start_date, num_weeks)

    data = []
    for week in weeks:
        for agent in AGENTS:
            calls_handled = np.random.randint(100, 200)
            emails_handled = np.random.randint(40, 80)
            chats_handled = np.random.randint(60, 100)
            whatsapp_handled = np.random.randint(30, 60)

            total_handled = (
                calls_handled + emails_handled + chats_handled + whatsapp_handled
            )

            avg_handle_time = np.random.uniform(10, 20)
            resolution_rate = np.random.uniform(0.65, 0.95)
            satisfaction_score = np.random.uniform(3.2, 5.0)
            hours_worked = np.random.uniform(35, 45)

            total_cost = hours_worked * COSTS["hourly_rate"]

            data.append(
                {
                    "week_start": week.date(),
                    "agent_id": agent["agent_id"],
                    "agent_name": agent["agent_name"],
                    "department": agent["department"],
                    "calls_handled": calls_handled,
                    "emails_handled": emails_handled,
                    "chats_handled": chats_handled,
                    "whatsapp_handled": whatsapp_handled,
                    "total_interactions": total_handled,
                    "avg_handle_time_minutes": round(avg_handle_time, 2),
                    "resolution_rate": round(resolution_rate, 4),
                    "customer_satisfaction_score": round(satisfaction_score, 2),
                    "hours_worked": round(hours_worked, 2),
                    "total_cost": round(total_cost, 2),
                    "cost_per_interaction": round(total_cost / total_handled, 2),
                }
            )

    return pd.DataFrame(data)


def generate_weekly_channel(
    start_date: str = "2025-01-06", num_weeks: int = 52
) -> pd.DataFrame:
    """Generate weekly channel metrics."""
    weeks = get_mondays(start_date, num_weeks)

    channel_config = {
        "Phone": {
            "volume_range": (800, 1200),
            "handle_time": (12, 18),
            "cost_key": "cost_per_call",
        },
        "Email": {
            "volume_range": (300, 500),
            "handle_time": (8, 15),
            "cost_key": "cost_per_email",
        },
        "Chat": {
            "volume_range": (400, 600),
            "handle_time": (6, 12),
            "cost_key": "cost_per_chat",
        },
        "WhatsApp": {
            "volume_range": (200, 400),
            "handle_time": (5, 10),
            "cost_key": "cost_per_whatsapp",
        },
    }

    data = []
    for week in weeks:
        for channel, config in channel_config.items():
            volume = np.random.randint(*config["volume_range"])
            avg_handle_time = np.random.uniform(*config["handle_time"])
            resolution_rate = np.random.uniform(0.68, 0.92)
            satisfaction = np.random.uniform(3.4, 4.9)

            cost_per_unit = COSTS[config["cost_key"]]
            total_cost = volume * cost_per_unit

            data.append(
                {
                    "week_start": week.date(),
                    "channel": channel,
                    "total_interactions": volume,
                    "avg_handle_time_minutes": round(avg_handle_time, 2),
                    "resolution_rate": round(resolution_rate, 4),
                    "customer_satisfaction_score": round(satisfaction, 2),
                    "total_cost": round(total_cost, 2),
                    "cost_per_interaction": round(cost_per_unit, 2),
                }
            )

    return pd.DataFrame(data)


def generate_weekly_calls(
    start_date: str = "2025-01-06", num_weeks: int = 52
) -> pd.DataFrame:
    """Generate detailed weekly call data."""
    weeks = get_mondays(start_date, num_weeks)

    data = []
    call_id = 1

    for week in weeks:
        # Generate calls for each day of the week
        for day_offset in range(7):
            current_date = week + timedelta(days=day_offset)

            # Fewer calls on weekends
            if day_offset >= 5:
                num_calls = np.random.randint(20, 50)
            else:
                num_calls = np.random.randint(100, 180)

            for _ in range(num_calls):
                agent = np.random.choice(AGENTS)
                channel = np.random.choice(CHANNELS, p=[0.45, 0.20, 0.20, 0.15])

                hour = np.random.randint(8, 20)
                minute = np.random.randint(0, 60)

                duration = np.random.normal(15, 5)
                duration = max(1, min(60, duration))

                wait_time = np.random.exponential(3)
                wait_time = min(wait_time, 20)

                resolved = np.random.random() < 0.78
                satisfaction = (
                    np.random.randint(1, 6) if resolved else np.random.randint(1, 4)
                )

                data.append(
                    {
                        "call_id": call_id,
                        "date": current_date.date(),
                        "week_start": week.date(),
                        "hour": hour,
                        "agent_id": agent["agent_id"],
                        "agent_name": agent["agent_name"],
                        "channel": channel,
                        "duration_minutes": round(duration, 2),
                        "wait_time_minutes": round(wait_time, 2),
                        "resolved": resolved,
                        "customer_satisfaction": satisfaction,
                    }
                )
                call_id += 1

    return pd.DataFrame(data)


# =============================================================================
# MONTHLY DATA GENERATORS
# =============================================================================


def generate_monthly_overall(
    start_date: str = "2025-01-01", num_months: int = 12
) -> pd.DataFrame:
    """Generate monthly overall metrics."""
    months = get_months(start_date, num_months)

    data = []
    for month in months:
        total_calls = np.random.randint(3500, 5000)
        total_emails = np.random.randint(1200, 2000)
        total_chats = np.random.randint(1600, 2400)
        total_whatsapp = np.random.randint(800, 1600)

        total_interactions = total_calls + total_emails + total_chats + total_whatsapp

        avg_handle_time = np.random.uniform(12, 18)
        avg_wait_time = np.random.uniform(1.5, 4.5)
        first_call_resolution = np.random.uniform(0.72, 0.88)
        customer_satisfaction = np.random.uniform(3.6, 4.7)

        total_cost = (
            total_calls * COSTS["cost_per_call"]
            + total_emails * COSTS["cost_per_email"]
            + total_chats * COSTS["cost_per_chat"]
            + total_whatsapp * COSTS["cost_per_whatsapp"]
            + len(AGENTS) * COSTS["hourly_rate"] * 40 * 4  # ~4 weeks per month
        )

        data.append(
            {
                "month": month.date(),
                "month_name": month.strftime("%B %Y"),
                "total_calls": total_calls,
                "total_emails": total_emails,
                "total_chats": total_chats,
                "total_whatsapp": total_whatsapp,
                "total_interactions": total_interactions,
                "avg_handle_time_minutes": round(avg_handle_time, 2),
                "avg_wait_time_minutes": round(avg_wait_time, 2),
                "first_call_resolution_rate": round(first_call_resolution, 4),
                "customer_satisfaction_score": round(customer_satisfaction, 2),
                "total_cost": round(total_cost, 2),
                "cost_per_interaction": round(total_cost / total_interactions, 2),
            }
        )

    return pd.DataFrame(data)


def generate_monthly_agent(
    start_date: str = "2025-01-01", num_months: int = 12
) -> pd.DataFrame:
    """Generate monthly agent performance metrics."""
    months = get_months(start_date, num_months)

    data = []
    for month in months:
        for agent in AGENTS:
            calls_handled = np.random.randint(400, 800)
            emails_handled = np.random.randint(160, 320)
            chats_handled = np.random.randint(240, 400)
            whatsapp_handled = np.random.randint(120, 240)

            total_handled = (
                calls_handled + emails_handled + chats_handled + whatsapp_handled
            )

            avg_handle_time = np.random.uniform(10, 20)
            resolution_rate = np.random.uniform(0.65, 0.95)
            satisfaction_score = np.random.uniform(3.2, 5.0)
            hours_worked = np.random.uniform(140, 180)

            total_cost = hours_worked * COSTS["hourly_rate"]

            data.append(
                {
                    "month": month.date(),
                    "month_name": month.strftime("%B %Y"),
                    "agent_id": agent["agent_id"],
                    "agent_name": agent["agent_name"],
                    "department": agent["department"],
                    "calls_handled": calls_handled,
                    "emails_handled": emails_handled,
                    "chats_handled": chats_handled,
                    "whatsapp_handled": whatsapp_handled,
                    "total_interactions": total_handled,
                    "avg_handle_time_minutes": round(avg_handle_time, 2),
                    "resolution_rate": round(resolution_rate, 4),
                    "customer_satisfaction_score": round(satisfaction_score, 2),
                    "hours_worked": round(hours_worked, 2),
                    "total_cost": round(total_cost, 2),
                    "cost_per_interaction": round(total_cost / total_handled, 2),
                }
            )

    return pd.DataFrame(data)


def generate_monthly_channel(
    start_date: str = "2025-01-01", num_months: int = 12
) -> pd.DataFrame:
    """Generate monthly channel metrics."""
    months = get_months(start_date, num_months)

    channel_config = {
        "Phone": {
            "volume_range": (3500, 5000),
            "handle_time": (12, 18),
            "cost_key": "cost_per_call",
        },
        "Email": {
            "volume_range": (1200, 2000),
            "handle_time": (8, 15),
            "cost_key": "cost_per_email",
        },
        "Chat": {
            "volume_range": (1600, 2400),
            "handle_time": (6, 12),
            "cost_key": "cost_per_chat",
        },
        "WhatsApp": {
            "volume_range": (800, 1600),
            "handle_time": (5, 10),
            "cost_key": "cost_per_whatsapp",
        },
    }

    data = []
    for month in months:
        for channel, config in channel_config.items():
            volume = np.random.randint(*config["volume_range"])
            avg_handle_time = np.random.uniform(*config["handle_time"])
            resolution_rate = np.random.uniform(0.68, 0.92)
            satisfaction = np.random.uniform(3.4, 4.9)

            cost_per_unit = COSTS[config["cost_key"]]
            total_cost = volume * cost_per_unit

            data.append(
                {
                    "month": month.date(),
                    "month_name": month.strftime("%B %Y"),
                    "channel": channel,
                    "total_interactions": volume,
                    "avg_handle_time_minutes": round(avg_handle_time, 2),
                    "resolution_rate": round(resolution_rate, 4),
                    "customer_satisfaction_score": round(satisfaction, 2),
                    "total_cost": round(total_cost, 2),
                    "cost_per_interaction": round(cost_per_unit, 2),
                }
            )

    return pd.DataFrame(data)


def generate_monthly_calls(
    start_date: str = "2025-01-01", num_months: int = 12
) -> pd.DataFrame:
    """Generate detailed monthly aggregated call data."""
    months = get_months(start_date, num_months)

    data = []
    call_id = 1

    for month in months:
        # Get number of days in month
        if month.month == 12:
            next_month = month.replace(year=month.year + 1, month=1)
        else:
            next_month = month.replace(month=month.month + 1)
        days_in_month = (next_month - month).days

        for day in range(days_in_month):
            current_date = month + timedelta(days=day)
            weekday = current_date.weekday()

            # Fewer calls on weekends
            if weekday >= 5:
                num_calls = np.random.randint(20, 50)
            else:
                num_calls = np.random.randint(100, 180)

            for _ in range(num_calls):
                agent = np.random.choice(AGENTS)
                channel = np.random.choice(CHANNELS, p=[0.45, 0.20, 0.20, 0.15])

                hour = np.random.randint(8, 20)
                minute = np.random.randint(0, 60)

                duration = np.random.normal(15, 5)
                duration = max(1, min(60, duration))

                wait_time = np.random.exponential(3)
                wait_time = min(wait_time, 20)

                resolved = np.random.random() < 0.78
                satisfaction = (
                    np.random.randint(1, 6) if resolved else np.random.randint(1, 4)
                )

                data.append(
                    {
                        "call_id": call_id,
                        "date": current_date.date(),
                        "month": month.date(),
                        "month_name": month.strftime("%B %Y"),
                        "hour": hour,
                        "agent_id": agent["agent_id"],
                        "agent_name": agent["agent_name"],
                        "channel": channel,
                        "duration_minutes": round(duration, 2),
                        "wait_time_minutes": round(wait_time, 2),
                        "resolved": resolved,
                        "customer_satisfaction": satisfaction,
                    }
                )
                call_id += 1

    return pd.DataFrame(data)


# =============================================================================
# MAIN GENERATION FUNCTIONS
# =============================================================================


def generate_weekly_data(output_dir: str = "analytics/data/weekly"):
    """Generate all weekly data files."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print("Generating weekly data...")

    # Overall metrics
    overall_df = generate_weekly_overall()
    overall_df.to_csv(output_path / "overall.csv", index=False)
    print(f"  Created weekly/overall.csv with {len(overall_df)} records")

    # Agent metrics
    agent_df = generate_weekly_agent()
    agent_df.to_csv(output_path / "agent.csv", index=False)
    print(f"  Created weekly/agent.csv with {len(agent_df)} records")

    # Channel metrics
    channel_df = generate_weekly_channel()
    channel_df.to_csv(output_path / "channel.csv", index=False)
    print(f"  Created weekly/channel.csv with {len(channel_df)} records")

    # Detailed calls
    calls_df = generate_weekly_calls()
    calls_df.to_csv(output_path / "calls.csv", index=False)
    print(f"  Created weekly/calls.csv with {len(calls_df)} records")

    print("Weekly data generation complete!\n")


def generate_monthly_data(output_dir: str = "analytics/data/monthly"):
    """Generate all monthly data files."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print("Generating monthly data...")

    # Overall metrics
    overall_df = generate_monthly_overall()
    overall_df.to_csv(output_path / "overall.csv", index=False)
    print(f"  Created monthly/overall.csv with {len(overall_df)} records")

    # Agent metrics
    agent_df = generate_monthly_agent()
    agent_df.to_csv(output_path / "agent.csv", index=False)
    print(f"  Created monthly/agent.csv with {len(agent_df)} records")

    # Channel metrics
    channel_df = generate_monthly_channel()
    channel_df.to_csv(output_path / "channel.csv", index=False)
    print(f"  Created monthly/channel.csv with {len(channel_df)} records")

    # Detailed calls
    calls_df = generate_monthly_calls()
    calls_df.to_csv(output_path / "calls.csv", index=False)
    print(f"  Created monthly/calls.csv with {len(calls_df)} records")

    print("Monthly data generation complete!\n")


def generate_all_data(base_dir: str = "analytics/data"):
    """Generate all synthetic data files for both weekly and monthly."""
    print("=" * 50)
    print("Call Center Analytics - Data Generation")
    print("=" * 50 + "\n")

    generate_weekly_data(f"{base_dir}/weekly")
    generate_monthly_data(f"{base_dir}/monthly")

    print("=" * 50)
    print("All data generation complete!")
    print("=" * 50)


if __name__ == "__main__":
    generate_all_data()
