#!/usr/bin/env python3
"""
Cohort Analysis for SaaS Metrics
Generates retention cohort matrices and visualizations.

Usage:
    python cohort_analysis.py --revenue revenue.csv --customers customers.csv --output cohorts.xlsx
"""

import argparse
import json
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, Any, Tuple
from pathlib import Path


def load_data(revenue_path: str, customers_path: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Load revenue and customer data files."""
    revenue_df = pd.read_csv(revenue_path)
    revenue_df['date'] = pd.to_datetime(revenue_df['date'])

    customers_df = pd.read_csv(customers_path)
    customers_df['created_date'] = pd.to_datetime(customers_df['created_date'])
    if 'churned_date' in customers_df.columns:
        customers_df['churned_date'] = pd.to_datetime(customers_df['churned_date'])

    return revenue_df, customers_df


def create_cohort_column(df: pd.DataFrame, date_col: str = 'created_date') -> pd.DataFrame:
    """Add cohort column based on signup month."""
    df = df.copy()
    df['cohort'] = df[date_col].dt.to_period('M')
    return df


def build_retention_matrix(customers_df: pd.DataFrame, revenue_df: pd.DataFrame) -> pd.DataFrame:
    """Build customer retention cohort matrix."""
    customers_df = create_cohort_column(customers_df)

    # Get all periods
    all_periods = sorted(revenue_df['date'].dt.to_period('M').unique())
    cohorts = sorted(customers_df['cohort'].unique())

    # Build matrix
    matrix_data = []

    for cohort in cohorts:
        cohort_customers = customers_df[customers_df['cohort'] == cohort]['customer_id'].tolist()
        cohort_size = len(cohort_customers)

        row = {'cohort': str(cohort), 'cohort_size': cohort_size}

        for i, period in enumerate(all_periods):
            if period >= cohort:
                month_num = (period.year - cohort.year) * 12 + (period.month - cohort.month)

                # Count active customers in this period
                period_revenue = revenue_df[
                    (revenue_df['date'].dt.to_period('M') == period) &
                    (revenue_df['customer_id'].isin(cohort_customers)) &
                    (revenue_df['mrr'] > 0)
                ]
                active_count = period_revenue['customer_id'].nunique()

                retention_pct = (active_count / cohort_size * 100) if cohort_size > 0 else 0
                row[f'M{month_num}'] = round(retention_pct, 1)

        matrix_data.append(row)

    return pd.DataFrame(matrix_data)


def build_revenue_retention_matrix(customers_df: pd.DataFrame, revenue_df: pd.DataFrame) -> pd.DataFrame:
    """Build revenue retention (NRR) cohort matrix."""
    customers_df = create_cohort_column(customers_df)

    all_periods = sorted(revenue_df['date'].dt.to_period('M').unique())
    cohorts = sorted(customers_df['cohort'].unique())

    matrix_data = []

    for cohort in cohorts:
        cohort_customers = customers_df[customers_df['cohort'] == cohort]['customer_id'].tolist()

        # Get initial MRR for cohort
        initial_revenue = revenue_df[
            (revenue_df['date'].dt.to_period('M') == cohort) &
            (revenue_df['customer_id'].isin(cohort_customers))
        ]['mrr'].sum()

        row = {'cohort': str(cohort), 'initial_mrr': initial_revenue}

        for period in all_periods:
            if period >= cohort:
                month_num = (period.year - cohort.year) * 12 + (period.month - cohort.month)

                period_revenue = revenue_df[
                    (revenue_df['date'].dt.to_period('M') == period) &
                    (revenue_df['customer_id'].isin(cohort_customers))
                ]['mrr'].sum()

                nrr_pct = (period_revenue / initial_revenue * 100) if initial_revenue > 0 else 0
                row[f'M{month_num}'] = round(nrr_pct, 1)

        matrix_data.append(row)

    return pd.DataFrame(matrix_data)


def calculate_cohort_metrics(retention_matrix: pd.DataFrame, revenue_matrix: pd.DataFrame) -> Dict[str, Any]:
    """Calculate aggregate cohort metrics."""
    metrics = {}

    # Get month columns
    month_cols = [c for c in retention_matrix.columns if c.startswith('M')]

    if not month_cols:
        return {'error': 'No cohort periods found'}

    # Average retention by month
    avg_retention = {}
    for col in month_cols:
        values = retention_matrix[col].dropna()
        if len(values) > 0:
            avg_retention[col] = round(values.mean(), 1)
    metrics['avg_retention_by_month'] = avg_retention

    # Average NRR by month
    avg_nrr = {}
    month_cols_rev = [c for c in revenue_matrix.columns if c.startswith('M')]
    for col in month_cols_rev:
        values = revenue_matrix[col].dropna()
        if len(values) > 0:
            avg_nrr[col] = round(values.mean(), 1)
    metrics['avg_nrr_by_month'] = avg_nrr

    # 12-month metrics (if available)
    if 'M12' in avg_retention:
        metrics['avg_12mo_retention'] = avg_retention['M12']
    if 'M12' in avg_nrr:
        metrics['avg_12mo_nrr'] = avg_nrr['M12']

    # Cohort-level summary
    metrics['total_cohorts'] = len(retention_matrix)
    metrics['oldest_cohort'] = retention_matrix['cohort'].iloc[0] if len(retention_matrix) > 0 else None
    metrics['newest_cohort'] = retention_matrix['cohort'].iloc[-1] if len(retention_matrix) > 0 else None

    return metrics


def generate_flags(metrics: Dict[str, Any]) -> list:
    """Generate warning flags based on cohort analysis."""
    flags = []

    # Check 3-month retention
    avg_retention = metrics.get('avg_retention_by_month', {})
    if 'M3' in avg_retention:
        m3_retention = avg_retention['M3']
        if m3_retention < 70:
            flags.append({
                'severity': 'high',
                'metric': '3mo_retention',
                'value': m3_retention,
                'message': f'3-month retention at {m3_retention}% - early churn problem'
            })
        elif m3_retention < 85:
            flags.append({
                'severity': 'medium',
                'metric': '3mo_retention',
                'value': m3_retention,
                'message': f'3-month retention at {m3_retention}% - watch onboarding'
            })

    # Check NRR trends
    avg_nrr = metrics.get('avg_nrr_by_month', {})
    if 'M6' in avg_nrr:
        m6_nrr = avg_nrr['M6']
        if m6_nrr < 90:
            flags.append({
                'severity': 'high',
                'metric': '6mo_nrr',
                'value': m6_nrr,
                'message': f'6-month NRR at {m6_nrr}% - revenue contraction'
            })

    return flags


def export_to_excel(retention_matrix: pd.DataFrame, revenue_matrix: pd.DataFrame,
                    metrics: Dict[str, Any], output_path: str):
    """Export cohort analysis to Excel workbook."""
    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        # Retention matrix
        retention_matrix.to_excel(writer, sheet_name='Logo Retention', index=False)

        # Revenue retention matrix
        revenue_matrix.to_excel(writer, sheet_name='Revenue Retention', index=False)

        # Metrics summary
        metrics_df = pd.DataFrame([
            {'metric': k, 'value': str(v)}
            for k, v in metrics.items()
            if not isinstance(v, dict)
        ])
        metrics_df.to_excel(writer, sheet_name='Metrics Summary', index=False)

        # Format worksheets
        workbook = writer.book

        # Conditional formatting for retention
        for sheet_name in ['Logo Retention', 'Revenue Retention']:
            worksheet = writer.sheets[sheet_name]

            # Green for high retention, red for low
            green_format = workbook.add_format({'bg_color': '#C6EFCE'})
            yellow_format = workbook.add_format({'bg_color': '#FFEB9C'})
            red_format = workbook.add_format({'bg_color': '#FFC7CE'})


def main():
    parser = argparse.ArgumentParser(description='Generate cohort retention analysis')
    parser.add_argument('--revenue', required=True, help='Revenue CSV file')
    parser.add_argument('--customers', required=True, help='Customers CSV file')
    parser.add_argument('--output', default='cohorts.xlsx', help='Output Excel file')
    parser.add_argument('--json', action='store_true', help='Also output JSON metrics')

    args = parser.parse_args()

    # Load data
    print(f"Loading data from {args.revenue} and {args.customers}...")
    revenue_df, customers_df = load_data(args.revenue, args.customers)

    print(f"Found {len(customers_df)} customers and {len(revenue_df)} revenue records")

    # Build matrices
    print("Building retention matrices...")
    retention_matrix = build_retention_matrix(customers_df, revenue_df)
    revenue_matrix = build_revenue_retention_matrix(customers_df, revenue_df)

    # Calculate metrics
    metrics = calculate_cohort_metrics(retention_matrix, revenue_matrix)
    flags = generate_flags(metrics)
    metrics['flags'] = flags
    metrics['generated_at'] = datetime.now().isoformat()

    # Export
    print(f"Exporting to {args.output}...")
    export_to_excel(retention_matrix, revenue_matrix, metrics, args.output)

    if args.json:
        json_path = args.output.replace('.xlsx', '.json')
        with open(json_path, 'w') as f:
            json.dump({
                'metrics': metrics,
                'retention_matrix': retention_matrix.to_dict('records'),
                'revenue_matrix': revenue_matrix.to_dict('records')
            }, f, indent=2, default=str)
        print(f"JSON exported to {json_path}")

    # Summary output
    print("\n=== COHORT ANALYSIS SUMMARY ===")
    print(f"Cohorts analyzed: {metrics.get('total_cohorts', 0)}")
    print(f"Period: {metrics.get('oldest_cohort')} to {metrics.get('newest_cohort')}")

    avg_retention = metrics.get('avg_retention_by_month', {})
    if 'M1' in avg_retention:
        print(f"Avg M1 Retention: {avg_retention['M1']}%")
    if 'M3' in avg_retention:
        print(f"Avg M3 Retention: {avg_retention['M3']}%")

    if flags:
        print("\n=== FLAGS ===")
        for flag in flags:
            severity = flag['severity'].upper()
            print(f"[{severity}] {flag['message']}")

    print(f"\nOutput saved to {args.output}")


if __name__ == '__main__':
    main()
