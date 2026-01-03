#!/usr/bin/env python3
"""
Metric Threshold Checker Hook
Checks calculated metrics against thresholds and flags violations.

Usage:
    python check_thresholds.py <metrics_json_path>
"""

import sys
import os
import json
from datetime import datetime
from typing import Dict, List, Any


# Threshold definitions
THRESHOLDS = {
    'ltv_cac_ratio': {
        'red': {'max': 2.0, 'message': 'LTV:CAC below 2.0 - Unit economics challenged'},
        'yellow': {'max': 3.0, 'message': 'LTV:CAC below 3.0 - Watch unit economics'}
    },
    'gross_churn_rate': {
        'red': {'min': 5.0, 'message': 'Monthly churn exceeds 5% - Product/market fit concern'},
        'yellow': {'min': 2.0, 'message': 'Monthly churn exceeds 2% - Monitor retention'}
    },
    'net_revenue_retention': {
        'red': {'max': 100, 'message': 'NRR below 100% - Customer base is shrinking'},
        'yellow': {'max': 110, 'message': 'NRR below 110% - Limited expansion revenue'}
    },
    'burn_multiple': {
        'red': {'min': 2.5, 'message': 'Burn multiple exceeds 2.5x - Inefficient growth'},
        'yellow': {'min': 1.5, 'message': 'Burn multiple exceeds 1.5x - Watch efficiency'}
    },
    'runway_months': {
        'red': {'max': 12, 'message': 'Runway under 12 months - Financing pressure'},
        'yellow': {'max': 18, 'message': 'Runway under 18 months - Plan next raise'}
    },
    'top_customer_concentration': {
        'red': {'min': 30, 'message': 'Top customer >30% of revenue - High concentration risk'},
        'yellow': {'min': 20, 'message': 'Top customer >20% of revenue - Monitor concentration'}
    },
    'gross_margin': {
        'red': {'max': 50, 'message': 'Gross margin below 50% - Not true SaaS margins'},
        'yellow': {'max': 70, 'message': 'Gross margin below 70% - Below SaaS benchmark'}
    }
}


def check_threshold(metric_name: str, value: float) -> List[Dict[str, Any]]:
    """Check a single metric against thresholds."""
    flags = []

    if metric_name not in THRESHOLDS:
        return flags

    thresholds = THRESHOLDS[metric_name]

    # Check red threshold first (more severe)
    if 'red' in thresholds:
        red = thresholds['red']
        triggered = False
        if 'max' in red and value < red['max']:
            triggered = True
        if 'min' in red and value > red['min']:
            triggered = True

        if triggered:
            flags.append({
                'severity': 'red',
                'metric': metric_name,
                'value': value,
                'message': f"🔴 {red['message']}"
            })
            return flags  # Don't add yellow if red is triggered

    # Check yellow threshold
    if 'yellow' in thresholds:
        yellow = thresholds['yellow']
        triggered = False
        if 'max' in yellow and value < yellow['max']:
            triggered = True
        if 'min' in yellow and value > yellow['min']:
            triggered = True

        if triggered:
            flags.append({
                'severity': 'yellow',
                'metric': metric_name,
                'value': value,
                'message': f"🟡 {yellow['message']}"
            })

    return flags


def check_all_thresholds(metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Check all metrics against thresholds."""
    all_flags = []

    for metric_name in THRESHOLDS.keys():
        if metric_name in metrics:
            value = metrics[metric_name]
            if isinstance(value, (int, float)):
                flags = check_threshold(metric_name, value)
                all_flags.extend(flags)

    return all_flags


def write_flags_file(flags: List[Dict[str, Any]], output_path: str):
    """Write flags to markdown file."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    content = f"""# Metric Threshold Flags

**Generated**: {timestamp}

## Summary

- **Red Flags**: {len([f for f in flags if f['severity'] == 'red'])}
- **Yellow Flags**: {len([f for f in flags if f['severity'] == 'yellow'])}

## Flags

"""

    if not flags:
        content += "✅ No threshold violations detected.\n"
    else:
        # Red flags first
        red_flags = [f for f in flags if f['severity'] == 'red']
        if red_flags:
            content += "### Critical (Red)\n\n"
            for flag in red_flags:
                content += f"- {flag['message']} (current: {flag['value']:.2f})\n"
            content += "\n"

        # Yellow flags
        yellow_flags = [f for f in flags if f['severity'] == 'yellow']
        if yellow_flags:
            content += "### Warning (Yellow)\n\n"
            for flag in yellow_flags:
                content += f"- {flag['message']} (current: {flag['value']:.2f})\n"
            content += "\n"

    with open(output_path, 'w') as f:
        f.write(content)


def main():
    if len(sys.argv) < 2:
        print("Usage: python check_thresholds.py <metrics_json_path>")
        sys.exit(1)

    metrics_path = sys.argv[1]

    if not os.path.exists(metrics_path):
        print(json.dumps({'error': f'Metrics file not found: {metrics_path}'}))
        sys.exit(1)

    # Load metrics
    with open(metrics_path, 'r') as f:
        metrics = json.load(f)

    # Check thresholds
    flags = check_all_thresholds(metrics)

    # Write flags file
    output_dir = os.path.dirname(metrics_path)
    flags_path = os.path.join(output_dir, 'flags.md')
    write_flags_file(flags, flags_path)

    # Output result
    result = {
        'metrics_file': metrics_path,
        'flags_file': flags_path,
        'red_count': len([f for f in flags if f['severity'] == 'red']),
        'yellow_count': len([f for f in flags if f['severity'] == 'yellow']),
        'flags': flags
    }

    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
