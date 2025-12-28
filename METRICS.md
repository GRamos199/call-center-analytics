# Business Metrics Documentation

## Overview

This document describes all business metrics calculated and displayed in the Call Center Analytics Dashboard, aligned with the Cost and Productivity Analytics user story.

## Core Metrics

### 1. Cost per Agent

**Definition**: Total operational cost attributed to a single agent during a period.

**Formula**:
```
Cost per Agent = Hours Worked × Hourly Rate
```

**Calculation**:
- Hours Worked = Sum of all call durations (in minutes) / 60
- Hourly Rate = Average hourly rate from costs configuration

**Business Value**:
- Identifies cost-efficient agents
- Helps optimize staffing decisions
- Basis for agent performance reviews
- Capacity planning

**Data Source**: calls.csv + costs.csv

**Example**:
- Alice worked 30 hours
- Hourly rate = $45.50
- Cost per Agent = 30 × $45.50 = **$1,365**

---

### 2. Cost per Client

**Definition**: Total operational cost allocated to service a specific client.

**Formula**:
```
Cost per Client = Total Hours Spent on Client × Hourly Rate
```

**Calculation**:
- Hours per Client = Sum of call durations for that client / 60
- Hourly Rate = Average hourly rate from costs configuration

**Business Value**:
- Understand customer profitability
- Identify high-cost clients
- Price service appropriately
- Optimize client portfolio

**Data Source**: calls.csv + costs.csv

**Example**:
- Client #201 had 10 hours of support
- Hourly rate = $45.50
- Cost per Client = 10 × $45.50 = **$455**

---

### 3. Total Calls

**Definition**: Total number of calls handled in a period.

**Formula**:
```
Total Calls = COUNT(call_id) in date range
```

**Business Value**:
- Measures operational volume
- Indicates demand levels
- Baseline for other metrics
- Capacity assessment

**Trend Indicator**: ↑ (more calls = higher volume)

**Data Source**: calls.csv

---

### 4. Average Call Duration

**Definition**: Mean duration of calls in a period (in minutes).

**Formula**:
```
Average Duration = SUM(duration_minutes) / COUNT(call_id)
```

**Business Value**:
- Quality indicator
- Efficiency measure
- Identifies process bottlenecks
- Training needs assessment

**Interpretation**:
- Lower duration = Higher efficiency (if quality maintained)
- Higher duration = More complex issues or thoroughness

**Data Source**: calls.csv

---

### 5. Active Agents

**Definition**: Number of unique agents who handled calls in a period.

**Formula**:
```
Active Agents = COUNT(DISTINCT agent_id)
```

**Business Value**:
- Staffing level indicator
- Capacity planning
- Resource allocation
- Identifies coverage gaps

**Data Source**: calls.csv

---

### 6. Unique Clients

**Definition**: Number of different clients served in a period.

**Formula**:
```
Unique Clients = COUNT(DISTINCT client_id)
```

**Business Value**:
- Customer reach indicator
- Market penetration
- Diversification measurement
- Risk assessment

**Data Source**: calls.csv

---

### 7. Calls per Agent

**Definition**: Average number of calls handled by each agent in a period.

**Formula**:
```
Calls per Agent = Total Calls / Active Agents
```

**Business Value**:
- Productivity measure
- Workload distribution
- Performance benchmark
- Identifies high performers

**Example**:
- Total Calls = 587
- Active Agents = 6
- Calls per Agent = 587 / 6 = **97.83 calls**

---

### 8. Hours Worked

**Definition**: Total hours an agent spent on calls in a period.

**Formula**:
```
Hours Worked = SUM(duration_minutes) / 60 per agent
```

**Business Value**:
- Utilization tracking
- Workload assessment
- Payroll calculation basis
- Efficiency analysis

**Data Source**: calls.csv

---

## Delta Metrics (Period-over-Period Comparison)

Each metric is compared to the previous period:

### Delta Value
```
Delta = Current Period Value - Previous Period Value
```

### Delta Percentage
```
Delta % = (Delta / Previous Period Value) × 100
```

### Trend Direction
- **Up** (↑): Current > Previous (positive in most cases)
- **Down** (↓): Current < Previous (negative in most cases)
- **Flat** (→): Current = Previous

**Example**:
```
Current Period Total Calls: 587
Previous Period Total Calls: 520
Delta: 587 - 520 = +67 calls
Delta %: (67 / 520) × 100 = +12.88%
Trend: UP ↑
```

---

## Aggregation Levels

### Daily Metrics
Metrics calculated for each day:
- Date
- Total Calls
- Total Duration (minutes)
- Average Duration
- Active Agents
- Unique Clients
- Daily Cost

### Weekly Metrics
Aggregation of daily metrics for a 7-day period:
- Week starting date
- All daily metrics summed
- Deltas vs previous week

### Monthly Metrics
Aggregation of daily metrics for a calendar month:
- Month and year
- All daily metrics summed
- Deltas vs previous month

---

## Cost Breakdown

### Operational Costs

From `costs.csv`:

| Cost Type | Amount | Description |
|-----------|--------|-------------|
| Hourly Rate | $45.50 | Direct agent labor cost |
| Equipment per Agent | $500/year | Equipment amortized cost |
| Infrastructure | $2,500/month | Facilities, systems, overhead |
| Management | $3,000/month | Supervisory and admin costs |

### Total Cost Calculation
```
Total Cost = Variable Costs + Fixed Costs
           = (Hours × Hourly Rate) + Infrastructure + Management
```

**Example** (Monthly):
- Hours: 1,000
- Variable Cost: 1,000 × $45.50 = $45,500
- Infrastructure: $2,500
- Management: $3,000
- **Total: $51,000/month**

---

## Key Performance Indicators (KPIs)

### Productivity Indicators

1. **Calls per Agent per Hour**
   - Formula: Calls / Hours Worked per Agent
   - Target: >6 calls/hour
   - Efficiency measure

2. **Average Handle Time (AHT)**
   - Formula: Total Duration / Total Calls
   - Target: <20 minutes
   - Quality vs speed balance

3. **Agent Utilization**
   - Formula: Hours Worked / Available Hours
   - Target: 75-85%
   - Prevents burnout while maximizing use

### Cost Indicators

1. **Cost per Call**
   - Formula: Total Cost / Total Calls
   - Helps optimize pricing
   - Efficiency tracking

2. **Cost per Hour**
   - Formula: Total Cost / Total Hours
   - Compares to hourly rate ($45.50)
   - Includes overhead allocation

3. **Revenue per Call** (When implemented)
   - Formula: Revenue Generated / Calls
   - Profitability measure

### Quality Indicators (Future)

1. **Customer Satisfaction (CSAT)**
   - Post-call survey scores
   - Target: >4/5

2. **First Call Resolution (FCR)**
   - % of calls resolved without escalation
   - Target: >80%

3. **Average Handling Time by Complexity**
   - Tracking by call type
   - Identifies training needs

---

## Data Validation Rules

### Calls Data
- call_id must be unique
- duration_minutes > 0
- start_time < end_time
- date must be valid
- agent_id and client_id must exist in reference tables

### Agents Data
- agent_id must be unique
- agent_name must not be empty
- department must be valid (Sales, Support, etc.)
- hire_date must be valid

### Costs Data
- cost_type must be predefined
- amount must be > 0
- currency must be valid (USD)

---

## Benchmarking

### Industry Standards (Call Centers)

| Metric | Low | Average | High |
|--------|-----|---------|------|
| AHT (minutes) | 25+ | 10-20 | <10 |
| Calls/Agent/Day | <50 | 50-100 | 100+ |
| Utilization | <60% | 75-85% | >90% |
| Cost/Call | >$5 | $2-5 | <$2 |

### Comparison
Compare your metrics against these benchmarks to identify improvement areas.

---

## Future Enhancements

1. **Forecast Metrics**: Predict next period performance
2. **Anomaly Detection**: Alert on unusual patterns
3. **Customer Lifetime Value**: Track individual client profitability
4. **Agent Segmentation**: Group by performance levels
5. **Seasonal Trends**: Identify patterns by season
6. **Predictive Analytics**: Churn prediction, demand forecasting

---

## References

- **Cost Analysis**: From costs.csv configuration
- **Productivity Data**: From calls.csv records
- **Agent Information**: From agents.csv roster
- **Date Handling**: Python datetime utilities
- **Calculations**: Pandas aggregation functions
