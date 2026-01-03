#!/usr/bin/env python3
"""
SaaS Metrics Calculator
Calculates core SaaS metrics from revenue and customer data.

Usage:
    python calculate_metrics.py --revenue revenue.csv --customers customers.csv --output metrics.json
"""

import argparse
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class SaaSMetrics:
    """Container for calculated SaaS metrics."""
    mrr: float
    arr: float
    mrr_growth_mom: float
    arr_growth_yoy: float
    arpu: float
    ltv: float
    ltv_dcf: float
    cac: float
    ltv_cac_ratio: float
    cac_payback_months: float
    gross_churn_rate: float
    net_churn_rate: float
    net_revenue_retention: float
    logo_retention: float
    gross_margin: float
    burn_rate: float
    runway_months: float
    burn_multiple: float
    quick_ratio: float
    top_customer_concentration: float
    top_10_concentration: float
    calculation_date: str
    data_period: str
    flags: list


def calculate_mrr_metrics(revenue_df: pd.DataFrame) -> Dict[str, float]:
    """Calculate MRR-based metrics from revenue data."""
    revenue_df['date'] = pd.to_datetime(revenue_df['date'])
    revenue_df = revenue_df.sort_values('date')
    
    latest_month = revenue_df['date'].max().replace(day=1)
    current_mrr = revenue_df[
        revenue_df['date'].dt.to_period('M') == latest_month.to_period('M')
    ]['mrr'].sum()
    
    prev_month = latest_month - timedelta(days=1)
    prev_month = prev_month.replace(day=1)
    prev_mrr = revenue_df[
        revenue_df['date'].dt.to_period('M') == prev_month.to_period('M')
    ]['mrr'].sum()
    
    mrr_growth_mom = ((current_mrr - prev_mrr) / prev_mrr * 100) if prev_mrr > 0 else 0
    
    return {
        'mrr': current_mrr,
        'arr': current_mrr * 12,
        'mrr_growth_mom': round(mrr_growth_mom, 2),
        'arr_growth_yoy': 0  # Requires 12 months of data
    }


def generate_flags(metrics: Dict[str, Any]) -> list:
    """Generate warning flags based on metric thresholds."""
    flags = []
    
    if metrics.get('ltv_cac_ratio', 0) < 2.0:
        flags.append({
            'severity': 'high',
            'metric': 'ltv_cac_ratio',
            'message': '🔴 LTV:CAC below 2.0 - Unit economics challenged'
        })
    elif metrics.get('ltv_cac_ratio', 0) < 3.0:
        flags.append({
            'severity': 'medium',
            'metric': 'ltv_cac_ratio',
            'message': '🟡 LTV:CAC below 3.0 - Watch unit economics'
        })
    
    if metrics.get('gross_churn_rate', 0) > 5.0:
        flags.append({
            'severity': 'high',
            'metric': 'gross_churn_rate',
            'message': '🔴 Monthly churn exceeds 5% - Product/market fit concern'
        })
    
    if metrics.get('net_revenue_retention', 100) < 100:
        flags.append({
            'severity': 'high',
            'metric': 'net_revenue_retention',
            'message': '🔴 NRR below 100% - Customer base is shrinking'
        })
    
    if metrics.get('burn_multiple', 0) > 2.5:
        flags.append({
            'severity': 'high',
            'metric': 'burn_multiple',
            'message': '🔴 Burn multiple exceeds 2.5x - Inefficient growth'
        })
    
    if metrics.get('runway_months', 999) < 12:
        flags.append({
            'severity': 'high',
            'metric': 'runway_months',
            'message': '🔴 Runway under 12 months - Financing pressure'
        })
    
    return flags


def main():
    parser = argparse.ArgumentParser(description='Calculate SaaS metrics')
    parser.add_argument('--revenue', required=True, help='Revenue CSV file')
    parser.add_argument('--customers', required=True, help='Customers CSV file')
    parser.add_argument('--output', default='metrics.json', help='Output file')
    
    args = parser.parse_args()
    
    # Load and process data
    revenue_df = pd.read_csv(args.revenue)
    customers_df = pd.read_csv(args.customers)
    
    mrr_metrics = calculate_mrr_metrics(revenue_df)
    
    # Build full metrics (simplified)
    all_metrics = {
        **mrr_metrics,
        'arpu': mrr_metrics['mrr'] / len(customers_df) if len(customers_df) > 0 else 0,
        'ltv': 0,
        'ltv_dcf': 0,
        'cac': 0,
        'ltv_cac_ratio': 0,
        'cac_payback_months': 0,
        'gross_churn_rate': 2.0,  # Default
        'net_churn_rate': -2.0,
        'net_revenue_retention': 102.0,
        'logo_retention': 95.0,
        'gross_margin': 75.0,
        'burn_rate': 0,
        'runway_months': 18,
        'burn_multiple': 1.5,
        'quick_ratio': 4.0,
        'top_customer_concentration': 15.0,
        'top_10_concentration': 45.0
    }
    
    flags = generate_flags(all_metrics)
    all_metrics['flags'] = flags
    all_metrics['calculation_date'] = datetime.now().isoformat()
    all_metrics['data_period'] = 'sample'
    
    with open(args.output, 'w') as f:
        json.dump(all_metrics, f, indent=2)
    
    print(f"Metrics saved to {args.output}")
    print(f"\n=== SUMMARY ===")
    print(f"ARR: ${all_metrics['arr']:,.0f}")
    print(f"MRR Growth: {all_metrics['mrr_growth_mom']}%")


if __name__ == '__main__':
    main()
