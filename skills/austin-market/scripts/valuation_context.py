#!/usr/bin/env python3
"""
Austin Valuation Context
Provides Austin-specific valuation benchmarks and comparisons.

Usage:
    python valuation_context.py --arr 1000000 --stage seed --output valuation_context.json
"""

import argparse
import json
from datetime import datetime
from typing import Dict, Any


# Austin valuation benchmarks (pre-money, in millions)
AUSTIN_BENCHMARKS = {
    'seed': {
        'low': 6_000_000,
        'median': 10_000_000,
        'high': 15_000_000,
        'bay_area_median': 15_000_000
    },
    'series_a': {
        'low': 15_000_000,
        'median': 30_000_000,
        'high': 50_000_000,
        'bay_area_median': 45_000_000
    },
    'series_b': {
        'low': 50_000_000,
        'median': 90_000_000,
        'high': 150_000_000,
        'bay_area_median': 130_000_000
    }
}

# Sectors that command Bay Area parity
PREMIUM_SECTORS = [
    'Enterprise SaaS',
    'Fintech/Payments',
    'Cybersecurity',
    'E-commerce/D2C',
    'AI/ML Infrastructure'
]

# ARR multiples by growth rate
ARR_MULTIPLES = {
    'hypergrowth': {'threshold': 100, 'multiple_low': 15, 'multiple_high': 30},
    'high_growth': {'threshold': 50, 'multiple_low': 10, 'multiple_high': 20},
    'growth': {'threshold': 25, 'multiple_low': 6, 'multiple_high': 12},
    'moderate': {'threshold': 10, 'multiple_low': 4, 'multiple_high': 8},
    'slow': {'threshold': 0, 'multiple_low': 2, 'multiple_high': 5}
}


def get_growth_category(yoy_growth: float) -> str:
    """Determine growth category based on YoY growth rate."""
    for category, config in ARR_MULTIPLES.items():
        if yoy_growth >= config['threshold']:
            return category
    return 'slow'


def calculate_arr_valuation(arr: float, yoy_growth: float) -> Dict[str, float]:
    """Calculate implied valuation based on ARR and growth."""
    category = get_growth_category(yoy_growth)
    multiples = ARR_MULTIPLES[category]

    return {
        'arr': arr,
        'yoy_growth': yoy_growth,
        'growth_category': category,
        'multiple_low': multiples['multiple_low'],
        'multiple_high': multiples['multiple_high'],
        'valuation_low': arr * multiples['multiple_low'],
        'valuation_high': arr * multiples['multiple_high'],
        'valuation_mid': arr * (multiples['multiple_low'] + multiples['multiple_high']) / 2
    }


def compare_to_benchmarks(valuation: float, stage: str) -> Dict[str, Any]:
    """Compare valuation to Austin and Bay Area benchmarks."""
    benchmarks = AUSTIN_BENCHMARKS.get(stage, AUSTIN_BENCHMARKS['seed'])

    return {
        'stage': stage,
        'valuation': valuation,
        'austin_low': benchmarks['low'],
        'austin_median': benchmarks['median'],
        'austin_high': benchmarks['high'],
        'bay_area_median': benchmarks['bay_area_median'],
        'vs_austin_median': (valuation / benchmarks['median'] - 1) * 100,
        'vs_bay_area': (valuation / benchmarks['bay_area_median'] - 1) * 100,
        'austin_discount': (1 - benchmarks['median'] / benchmarks['bay_area_median']) * 100,
        'position': 'below_median' if valuation < benchmarks['median'] else
                   'at_median' if valuation < benchmarks['high'] else 'above_median'
    }


def generate_context_report(
    arr: float,
    stage: str,
    yoy_growth: float = 0,
    sector: str = None,
    proposed_valuation: float = None
) -> Dict[str, Any]:
    """Generate complete Austin context report."""

    # Calculate ARR-based valuation
    arr_valuation = calculate_arr_valuation(arr, yoy_growth)

    # Use proposed or mid-range valuation
    valuation = proposed_valuation or arr_valuation['valuation_mid']

    # Compare to benchmarks
    benchmark_comparison = compare_to_benchmarks(valuation, stage)

    # Check if sector commands premium
    sector_premium = sector in PREMIUM_SECTORS if sector else False

    report = {
        'timestamp': datetime.now().isoformat(),
        'inputs': {
            'arr': arr,
            'stage': stage,
            'yoy_growth': yoy_growth,
            'sector': sector,
            'proposed_valuation': proposed_valuation
        },
        'arr_analysis': arr_valuation,
        'benchmark_comparison': benchmark_comparison,
        'sector_premium': sector_premium,
        'recommendations': []
    }

    # Generate recommendations
    if benchmark_comparison['position'] == 'above_median':
        if sector_premium:
            report['recommendations'].append(
                f"Valuation above Austin median but sector ({sector}) commands premium pricing"
            )
        else:
            report['recommendations'].append(
                "Valuation above Austin median - may face pushback from local investors"
            )

    if benchmark_comparison['vs_bay_area'] < -30:
        report['recommendations'].append(
            "Significant Austin discount vs Bay Area - attractive for Austin-based funds"
        )

    if arr_valuation['growth_category'] in ['hypergrowth', 'high_growth']:
        report['recommendations'].append(
            f"Strong growth ({yoy_growth}% YoY) justifies premium multiple"
        )

    return report


def format_report_text(report: Dict[str, Any]) -> str:
    """Format report as readable text."""
    arr = report['inputs']['arr']
    stage = report['inputs']['stage']
    comparison = report['benchmark_comparison']
    arr_analysis = report['arr_analysis']

    text = f"""
=== AUSTIN VALUATION CONTEXT ===

ARR: ${arr:,.0f}
Stage: {stage.replace('_', ' ').title()}
Growth Category: {arr_analysis['growth_category'].replace('_', ' ').title()}

ARR-Based Valuation Range:
  Low:  ${arr_analysis['valuation_low']:,.0f} ({arr_analysis['multiple_low']}x ARR)
  High: ${arr_analysis['valuation_high']:,.0f} ({arr_analysis['multiple_high']}x ARR)

Benchmark Comparison:
  Austin Median:   ${comparison['austin_median']:,.0f}
  Bay Area Median: ${comparison['bay_area_median']:,.0f}
  Austin Discount: {comparison['austin_discount']:.0f}%

Position: {comparison['position'].replace('_', ' ').title()}

Recommendations:
"""
    for rec in report['recommendations']:
        text += f"  • {rec}\n"

    return text


def main():
    parser = argparse.ArgumentParser(description='Austin valuation context analysis')
    parser.add_argument('--arr', type=float, required=True, help='Current ARR')
    parser.add_argument('--stage', choices=['seed', 'series_a', 'series_b'],
                        required=True, help='Funding stage')
    parser.add_argument('--growth', type=float, default=0, help='YoY growth rate %')
    parser.add_argument('--sector', help='Company sector')
    parser.add_argument('--valuation', type=float, help='Proposed valuation')
    parser.add_argument('--output', help='Output JSON file')

    args = parser.parse_args()

    # Generate report
    report = generate_context_report(
        arr=args.arr,
        stage=args.stage,
        yoy_growth=args.growth,
        sector=args.sector,
        proposed_valuation=args.valuation
    )

    # Print text report
    print(format_report_text(report))

    # Save JSON if requested
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\nJSON saved to {args.output}")


if __name__ == '__main__':
    main()
