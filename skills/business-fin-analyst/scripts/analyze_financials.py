#!/usr/bin/env python3
"""
Financial Analysis Script for VC Due Diligence
Usage: python analyze_financials.py <filepath> [--output json|md]
"""

import pandas as pd
import numpy as np
import json
import sys
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

def load_data(filepath: str) -> pd.DataFrame:
    """Load financial data from CSV or Excel."""
    path = Path(filepath)
    if path.suffix == '.csv':
        df = pd.read_csv(filepath)
    elif path.suffix in ['.xlsx', '.xls']:
        df = pd.read_excel(filepath)
    else:
        raise ValueError(f"Unsupported file type: {path.suffix}")
    
    # Normalize columns
    df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')
    
    # Parse dates
    for col in df.columns:
        if any(x in col for x in ['date', 'month', 'period']):
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    return df


def find_column(df: pd.DataFrame, keywords: list) -> Optional[str]:
    """Find column matching keywords."""
    for col in df.columns:
        if any(kw in col for kw in keywords):
            return col
    return None


def analyze_revenue(df: pd.DataFrame) -> Dict[str, Any]:
    """Analyze revenue metrics."""
    rev_col = find_column(df, ['revenue', 'mrr', 'arr', 'sales'])
    if not rev_col:
        return {"error": "No revenue column found"}
    
    values = df[rev_col].dropna()
    
    results = {
        "column": rev_col,
        "total": float(values.sum()),
        "average": float(values.mean()),
        "latest": float(values.iloc[-1]) if len(values) > 0 else 0,
        "first": float(values.iloc[0]) if len(values) > 0 else 0,
        "periods": len(values)
    }
    
    if len(values) > 1:
        results["mom_growth_pct"] = float(values.pct_change().mean() * 100)
        results["total_growth_pct"] = float((results["latest"] / results["first"] - 1) * 100)
        results["cagr"] = float(((results["latest"] / results["first"]) ** (12 / len(values)) - 1) * 100)
    
    return results


def analyze_expenses(df: pd.DataFrame) -> Dict[str, Any]:
    """Analyze expense metrics."""
    expense_cols = [c for c in df.columns if any(x in c for x in ['expense', 'cost', 'opex', 'cogs'])]
    
    if not expense_cols:
        return {"error": "No expense columns found"}
    
    results = {"columns": expense_cols, "breakdown": {}}
    
    total_expenses = 0
    for col in expense_cols:
        col_total = float(df[col].sum())
        results["breakdown"][col] = col_total
        total_expenses += col_total
    
    results["total"] = total_expenses
    results["average_monthly"] = total_expenses / len(df) if len(df) > 0 else 0
    
    return results


def analyze_burn(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate burn rate and runway."""
    rev_col = find_column(df, ['revenue', 'mrr', 'sales'])
    expense_col = find_column(df, ['expense', 'opex', 'cost'])
    cash_col = find_column(df, ['cash', 'balance', 'bank'])
    
    results = {}
    
    if rev_col:
        results["avg_monthly_revenue"] = float(df[rev_col].mean())
    
    if expense_col:
        results["avg_monthly_expense"] = float(df[expense_col].mean())
    
    if rev_col and expense_col:
        net_burn = df[expense_col].mean() - df[rev_col].mean()
        results["net_burn"] = float(net_burn)
        results["status"] = "burning" if net_burn > 0 else "cash_flow_positive"
    
    if cash_col:
        current_cash = float(df[cash_col].iloc[-1])
        results["current_cash"] = current_cash
        
        if "net_burn" in results and results["net_burn"] > 0:
            results["runway_months"] = current_cash / results["net_burn"]
    
    return results


def analyze_margins(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate margin metrics."""
    rev_col = find_column(df, ['revenue', 'sales'])
    cogs_col = find_column(df, ['cogs', 'cost_of_goods', 'cost_of_revenue'])
    opex_col = find_column(df, ['opex', 'operating_expense'])
    
    results = {}
    
    if rev_col and cogs_col:
        gross_profit = df[rev_col].sum() - df[cogs_col].sum()
        results["gross_margin_pct"] = float((gross_profit / df[rev_col].sum()) * 100)
    
    if rev_col and opex_col:
        operating_income = df[rev_col].sum() - df[opex_col].sum()
        results["operating_margin_pct"] = float((operating_income / df[rev_col].sum()) * 100)
    
    return results


def validate_data(df: pd.DataFrame) -> list:
    """Check data quality."""
    issues = []
    
    # Null checks
    for col in df.columns:
        null_count = df[col].isnull().sum()
        if null_count > 0:
            pct = (null_count / len(df)) * 100
            issues.append({
                "type": "null_values",
                "column": col,
                "count": int(null_count),
                "percentage": float(pct),
                "severity": "warning" if pct < 10 else "error"
            })
    
    # Negative revenue check
    rev_col = find_column(df, ['revenue', 'mrr'])
    if rev_col and (df[rev_col] < 0).any():
        issues.append({
            "type": "negative_values",
            "column": rev_col,
            "severity": "error"
        })
    
    return issues


def generate_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """Generate complete analysis summary."""
    return {
        "metadata": {
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": list(df.columns),
            "analyzed_at": datetime.now().isoformat()
        },
        "revenue": analyze_revenue(df),
        "expenses": analyze_expenses(df),
        "burn": analyze_burn(df),
        "margins": analyze_margins(df),
        "data_quality": validate_data(df)
    }


def format_markdown(summary: Dict[str, Any]) -> str:
    """Format summary as markdown."""
    rev = summary.get("revenue", {})
    burn = summary.get("burn", {})
    margins = summary.get("margins", {})
    quality = summary.get("data_quality", [])
    
    md = f"""# Financial Analysis Summary

**Generated:** {summary['metadata']['analyzed_at']}
**Data:** {summary['metadata']['rows']} periods, {summary['metadata']['columns']} columns

---

## Revenue

| Metric | Value |
|--------|-------|
| Total Revenue | ${rev.get('total', 0):,.0f} |
| Latest Period | ${rev.get('latest', 0):,.0f} |
| Average Monthly | ${rev.get('average', 0):,.0f} |
| MoM Growth | {rev.get('mom_growth_pct', 0):.1f}% |
| Total Growth | {rev.get('total_growth_pct', 0):.1f}% |

## Burn & Runway

| Metric | Value |
|--------|-------|
| Net Burn | ${burn.get('net_burn', 0):,.0f}/mo |
| Current Cash | ${burn.get('current_cash', 0):,.0f} |
| Runway | {burn.get('runway_months', 0):.1f} months |
| Status | {burn.get('status', 'unknown')} |

## Margins

| Metric | Value |
|--------|-------|
| Gross Margin | {margins.get('gross_margin_pct', 0):.1f}% |
| Operating Margin | {margins.get('operating_margin_pct', 0):.1f}% |

## Data Quality

"""
    
    if not quality:
        md += "✅ No data quality issues detected\n"
    else:
        for issue in quality:
            icon = "🔴" if issue.get("severity") == "error" else "⚠️"
            md += f"- {icon} {issue.get('type')}: {issue.get('column')} ({issue.get('count', '')} values)\n"
    
    return md


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_financials.py <filepath> [--output json|md]")
        sys.exit(1)
    
    filepath = sys.argv[1]
    output_format = "json"
    
    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output_format = sys.argv[idx + 1]
    
    try:
        df = load_data(filepath)
        summary = generate_summary(df)
        
        if output_format == "md":
            print(format_markdown(summary))
        else:
            print(json.dumps(summary, indent=2, default=str))
    
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)
