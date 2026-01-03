---
name: business-fin-analyst
description: Analyzes CSV/Excel files for financial due diligence, generates summary statistics, answers common financial analysis questions, and creates visualizations using Python and pandas. Use when processing P&L statements, balance sheets, cash flow data, revenue models, or any financial spreadsheet requiring analysis. Triggers on "analyze financials", "P&L analysis", "revenue breakdown", "burn rate", "financial model", "visualize metrics".
---

# Business Financial Analyst Skill

Financial data analysis for VC due diligence using Python, pandas, and visualization libraries.

## Capabilities

- Parse and clean financial CSV/Excel files
- Generate summary statistics and KPIs
- Answer common diligence questions programmatically
- Create visualizations (charts, trends, comparisons)
- Validate data quality and flag anomalies

## Workflow

### Phase 1: Data Ingestion

**Supported Formats:**
- CSV (`.csv`)
- Excel (`.xlsx`, `.xls`)
- Google Sheets (via export)

**Common File Types:**
```python
FILE_PATTERNS = {
    "p&l": ["income", "profit", "loss", "p&l", "pnl"],
    "balance_sheet": ["balance", "assets", "liabilities"],
    "cash_flow": ["cash", "flow", "burn"],
    "revenue": ["revenue", "sales", "mrr", "arr"],
    "customers": ["customers", "cohort", "churn"],
    "cap_table": ["cap", "equity", "shares", "ownership"]
}
```

**Data Loading:**
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
    date_cols = [c for c in df.columns if 'date' in c or 'month' in c or 'period' in c]
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    
    return df
```

### Phase 2: Analysis Functions

**Revenue Analysis:**
```python
def analyze_revenue(df: pd.DataFrame) -> dict:
    """Calculate key revenue metrics."""
    results = {}
    
    # Find revenue column
    rev_col = next((c for c in df.columns if 'revenue' in c or 'mrr' in c), None)
    if not rev_col:
        return {"error": "No revenue column found"}
    
    results['total_revenue'] = df[rev_col].sum()
    results['avg_monthly'] = df[rev_col].mean()
    results['latest_month'] = df[rev_col].iloc[-1]
    results['first_month'] = df[rev_col].iloc[0]
    
    # Growth
    if len(df) > 1:
        results['mom_growth'] = (df[rev_col].pct_change().mean() * 100)
        results['total_growth'] = ((results['latest_month'] / results['first_month']) - 1) * 100
    
    return results
```

**Burn Rate Analysis:**
```python
def analyze_burn(df: pd.DataFrame) -> dict:
    """Calculate burn rate and runway."""
    results = {}
    
    # Find expense and cash columns
    expense_col = next((c for c in df.columns if 'expense' in c or 'cost' in c or 'opex' in c), None)
    cash_col = next((c for c in df.columns if 'cash' in c or 'balance' in c), None)
    revenue_col = next((c for c in df.columns if 'revenue' in c), None)
    
    if expense_col:
        results['avg_monthly_expense'] = df[expense_col].mean()
    
    if expense_col and revenue_col:
        results['net_burn'] = df[expense_col].mean() - df[revenue_col].mean()
        if results['net_burn'] > 0:
            results['burn_status'] = 'burning'
        else:
            results['burn_status'] = 'profitable'
    
    if cash_col and 'net_burn' in results and results['net_burn'] > 0:
        current_cash = df[cash_col].iloc[-1]
        results['runway_months'] = current_cash / results['net_burn']
    
    return results
```

**Margin Analysis:**
```python
def analyze_margins(df: pd.DataFrame) -> dict:
    """Calculate margin metrics."""
    results = {}
    
    rev = next((c for c in df.columns if 'revenue' in c), None)
    cogs = next((c for c in df.columns if 'cogs' in c or 'cost_of' in c), None)
    opex = next((c for c in df.columns if 'opex' in c or 'operating' in c), None)
    
    if rev and cogs:
        gross_profit = df[rev] - df[cogs]
        results['gross_margin'] = (gross_profit.sum() / df[rev].sum()) * 100
    
    if rev and opex:
        operating_income = df[rev] - df[opex]
        results['operating_margin'] = (operating_income.sum() / df[rev].sum()) * 100
    
    return results
```

### Phase 3: Visualization

**Revenue Trend Chart:**
```python
import plotly.express as px

def plot_revenue_trend(df: pd.DataFrame, date_col: str, rev_col: str):
    """Create revenue trend visualization."""
    fig = px.line(
        df, x=date_col, y=rev_col,
        title='Monthly Revenue Trend',
        labels={rev_col: 'Revenue ($)', date_col: 'Month'}
    )
    fig.update_layout(template='plotly_white')
    return fig
```

**Expense Breakdown:**
```python
def plot_expense_breakdown(df: pd.DataFrame, expense_cols: list):
    """Create expense category breakdown."""
    totals = {col: df[col].sum() for col in expense_cols}
    fig = px.pie(
        values=list(totals.values()),
        names=list(totals.keys()),
        title='Expense Breakdown'
    )
    return fig
```

**Burn Rate Chart:**
```python
def plot_burn_runway(df: pd.DataFrame, cash_col: str, burn_col: str):
    """Visualize cash runway projection."""
    fig = px.area(
        df, x='month', y=cash_col,
        title='Cash Position & Projected Runway'
    )
    return fig
```

### Phase 4: Report Generation

**Summary Report:**
```python
def generate_financial_summary(df: pd.DataFrame) -> str:
    """Generate markdown summary report."""
    revenue = analyze_revenue(df)
    burn = analyze_burn(df)
    margins = analyze_margins(df)
    
    report = f"""
## Financial Summary

### Revenue
- **Total Revenue:** ${revenue.get('total_revenue', 0):,.0f}
- **Latest Month:** ${revenue.get('latest_month', 0):,.0f}
- **MoM Growth:** {revenue.get('mom_growth', 0):.1f}%

### Burn & Runway
- **Net Burn:** ${burn.get('net_burn', 0):,.0f}/month
- **Runway:** {burn.get('runway_months', 0):.1f} months
- **Status:** {burn.get('burn_status', 'unknown')}

### Margins
- **Gross Margin:** {margins.get('gross_margin', 0):.1f}%
- **Operating Margin:** {margins.get('operating_margin', 0):.1f}%
"""
    return report
```

## Common Diligence Questions

| Question | Function | Output |
|----------|----------|--------|
| "What's the revenue trend?" | `analyze_revenue()` | Growth rates, totals |
| "What's the burn rate?" | `analyze_burn()` | Monthly burn, runway |
| "What are the margins?" | `analyze_margins()` | Gross, operating margins |
| "Show me the expense breakdown" | `plot_expense_breakdown()` | Pie chart |
| "Visualize revenue growth" | `plot_revenue_trend()` | Line chart |

## Data Quality Checks

```python
def validate_data(df: pd.DataFrame) -> list:
    """Check for data quality issues."""
    issues = []
    
    # Check for nulls
    null_counts = df.isnull().sum()
    for col, count in null_counts.items():
        if count > 0:
            issues.append(f"⚠️ {col}: {count} null values")
    
    # Check for negative values in revenue
    rev_col = next((c for c in df.columns if 'revenue' in c), None)
    if rev_col and (df[rev_col] < 0).any():
        issues.append(f"🔴 Negative revenue values found")
    
    # Check date continuity
    date_col = next((c for c in df.columns if 'date' in c or 'month' in c), None)
    if date_col:
        df_sorted = df.sort_values(date_col)
        gaps = df_sorted[date_col].diff().dt.days
        if (gaps > 35).any():  # More than ~1 month gap
            issues.append(f"⚠️ Date gaps detected in {date_col}")
    
    return issues if issues else ["✅ No data quality issues found"]
```

## Integration

### With saas-metrics Skill
```python
# Use business-fin-analyst for raw data processing
df = load_financial_data("revenue.csv")
revenue_data = analyze_revenue(df)

# Pass to saas-metrics for advanced calculations
# LTV, CAC, NRR calculations use cleaned data
```

### With data-room Skill
```python
# Fetch financial docs from Egnyte
fetch_document(file_id="FINANCIALS_ID")

# Process with business-fin-analyst
df = load_financial_data("downloaded_file.xlsx")
summary = generate_financial_summary(df)
```

## Dependencies

```
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.14.0
openpyxl>=3.1.0
```

## References

- `references/column-mapping.md` — Standard column name mappings
- `references/analysis-templates.md` — Common analysis patterns
- `scripts/analyze_financials.py` — Main analysis script
- `scripts/visualize.py` — Visualization utilities
