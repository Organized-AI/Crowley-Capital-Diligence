# Analysis Functions Reference

## Data Loading

```python
import pandas as pd

def load_financial_data(filepath: str) -> pd.DataFrame:
    """Load and normalize financial data."""
    if filepath.endswith('.csv'):
        df = pd.read_csv(filepath)
    else:
        df = pd.read_excel(filepath)

    # Normalize column names
    df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')

    # Parse dates if present
    date_cols = [c for c in df.columns if 'date' in c or 'month' in c]
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')

    return df
```

## Revenue Analysis

```python
def analyze_revenue(df: pd.DataFrame) -> dict:
    """Calculate key revenue metrics."""
    rev_col = next((c for c in df.columns if 'revenue' in c or 'mrr' in c), None)
    if not rev_col:
        return {"error": "No revenue column found"}

    return {
        'total_revenue': df[rev_col].sum(),
        'avg_monthly': df[rev_col].mean(),
        'latest_month': df[rev_col].iloc[-1],
        'mom_growth': df[rev_col].pct_change().mean() * 100,
    }
```

## Burn Rate Analysis

```python
def analyze_burn(df: pd.DataFrame) -> dict:
    """Calculate burn rate and runway."""
    expense_col = next((c for c in df.columns if 'expense' in c or 'opex' in c), None)
    cash_col = next((c for c in df.columns if 'cash' in c or 'balance' in c), None)
    revenue_col = next((c for c in df.columns if 'revenue' in c), None)

    results = {}

    if expense_col and revenue_col:
        results['net_burn'] = df[expense_col].mean() - df[revenue_col].mean()
        results['burn_status'] = 'burning' if results['net_burn'] > 0 else 'profitable'

    if cash_col and results.get('net_burn', 0) > 0:
        current_cash = df[cash_col].iloc[-1]
        results['runway_months'] = current_cash / results['net_burn']

    return results
```

## Margin Analysis

```python
def analyze_margins(df: pd.DataFrame) -> dict:
    """Calculate margin metrics."""
    rev = next((c for c in df.columns if 'revenue' in c), None)
    cogs = next((c for c in df.columns if 'cogs' in c or 'cost_of' in c), None)

    results = {}
    if rev and cogs:
        gross_profit = df[rev] - df[cogs]
        results['gross_margin'] = (gross_profit.sum() / df[rev].sum()) * 100

    return results
```

## Data Quality Validation

```python
def validate_data(df: pd.DataFrame) -> list:
    """Check for data quality issues."""
    issues = []

    # Null check
    for col, count in df.isnull().sum().items():
        if count > 0:
            issues.append(f"Warning: {col} has {count} null values")

    # Negative revenue check
    rev_col = next((c for c in df.columns if 'revenue' in c), None)
    if rev_col and (df[rev_col] < 0).any():
        issues.append("Error: Negative revenue values found")

    return issues if issues else ["OK: No data quality issues"]
```

## Visualization Functions

```python
import plotly.express as px

def plot_revenue_trend(df, date_col, rev_col):
    return px.line(df, x=date_col, y=rev_col, title='Revenue Trend')

def plot_expense_breakdown(df, expense_cols):
    totals = {col: df[col].sum() for col in expense_cols}
    return px.pie(values=list(totals.values()), names=list(totals.keys()))

def plot_burn_runway(df, cash_col):
    return px.area(df, x='month', y=cash_col, title='Cash Position')
```
