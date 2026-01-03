#!/usr/bin/env python3
"""
Investment Memo Generator
Generates partner meeting investment memo from analysis outputs.

Usage:
    python generate_memo.py --analysis-dir data-room/analysis/ --output data-room/output/investment-memo.md
"""

import argparse
import json
import os
from datetime import datetime
from typing import Dict, Any


def load_analysis_data(analysis_dir: str) -> Dict[str, Any]:
    """Load all analysis JSON files."""
    data = {}

    json_files = ['metrics.json', 'financial-summary.json', 'parsed_captable.json',
                  'customer-analysis.json', 'round_model.json', 'series_a_model.json']

    for filename in json_files:
        filepath = os.path.join(analysis_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                key = filename.replace('.json', '').replace('-', '_').replace('series_a_model', 'round_model')
                data[key] = json.load(f)

    return data


def format_currency(value: float) -> str:
    """Format number as currency."""
    if value >= 1_000_000:
        return f"${value/1_000_000:.1f}M"
    elif value >= 1_000:
        return f"${value/1_000:.0f}K"
    else:
        return f"${value:.0f}"


def generate_memo(data: Dict[str, Any], company_name: str = "Target Company") -> str:
    """Generate investment memo markdown."""
    timestamp = datetime.now().strftime('%Y-%m-%d')

    metrics = data.get('metrics', {})
    captable = data.get('parsed_captable', {}).get('cap_table', {})
    round_model = data.get('round_model', {})
    summary = data.get('parsed_captable', {}).get('summary', {})

    # Extract key metrics
    arr = metrics.get('arr', 0)
    mrr = metrics.get('mrr', 0)
    mrr_growth = metrics.get('mrr_growth_mom', 0)
    nrr = metrics.get('net_revenue_retention', 100)
    ltv_cac = metrics.get('ltv_cac_ratio', 0)
    gross_margin = metrics.get('gross_margin', 0)
    runway = metrics.get('runway_months', 0)
    burn_multiple = metrics.get('burn_multiple', 0)

    # Round terms
    round_terms = round_model.get('round_terms', {})
    investment = round_terms.get('investment_amount', 0)
    pre_money = round_terms.get('pre_money_valuation', 0)
    post_money = round_terms.get('post_money_valuation', 0)

    md = f"""# Investment Memo: {company_name}

**Date**: {timestamp}
**Prepared by**: Crowley Capital Diligence Tool
**Status**: Draft for Partner Review

---

## Executive Summary

**Opportunity**: [Company description - requires manual input]

**Investment Thesis**:
1. [Key thesis point 1]
2. [Key thesis point 2]
3. [Key thesis point 3]

**Recommendation**: [See risk scorecard for recommendation]

---

## Deal Terms

| Term | Value |
|------|-------|
| Round | {round_terms.get('round_name', 'Series A')} |
| Investment | {format_currency(investment)} |
| Pre-Money | {format_currency(pre_money)} |
| Post-Money | {format_currency(post_money)} |
| Our Ownership | {round_model.get('new_investor_ownership', 0):.1f}% |

---

## Key Metrics

### Revenue & Growth

| Metric | Value | Benchmark | Status |
|--------|-------|-----------|--------|
| ARR | {format_currency(arr)} | — | — |
| MRR | {format_currency(mrr)} | — | — |
| MoM Growth | {mrr_growth:.1f}% | >10% | {'✅' if mrr_growth >= 10 else '⚠️' if mrr_growth >= 5 else '❌'} |

### Unit Economics

| Metric | Value | Benchmark | Status |
|--------|-------|-----------|--------|
| LTV:CAC | {ltv_cac:.1f}x | >3x | {'✅' if ltv_cac >= 3 else '⚠️' if ltv_cac >= 2 else '❌'} |
| Gross Margin | {gross_margin:.0f}% | >70% | {'✅' if gross_margin >= 70 else '⚠️' if gross_margin >= 50 else '❌'} |
| NRR | {nrr:.0f}% | >110% | {'✅' if nrr >= 110 else '⚠️' if nrr >= 100 else '❌'} |

### Efficiency

| Metric | Value | Benchmark | Status |
|--------|-------|-----------|--------|
| Burn Multiple | {burn_multiple:.1f}x | <1.5x | {'✅' if burn_multiple <= 1.5 else '⚠️' if burn_multiple <= 2.5 else '❌'} |
| Runway | {runway:.0f} months | >18mo | {'✅' if runway >= 18 else '⚠️' if runway >= 12 else '❌'} |

---

## Cap Table Summary

| Holder Type | Ownership |
|-------------|-----------|
"""

    ownership_by_type = summary.get('ownership_by_type', {})
    for holder_type, pct in sorted(ownership_by_type.items(), key=lambda x: -x[1]):
        md += f"| {holder_type.title()} | {pct:.1f}% |\n"

    md += f"""
**Option Pool**: {captable.get('option_pool_pct', 0):.1f}%
**Total Invested to Date**: {format_currency(summary.get('total_invested', 0))}

---

## Market Opportunity

### TAM/SAM/SOM
[Requires manual input]

### Competitive Landscape
[Requires manual input]

---

## Team

### Leadership
[Requires manual input]

### Key Hires Needed
[Requires manual input]

---

## Risks & Mitigations

### Key Risks
"""

    # Add flags if available
    flags = metrics.get('flags', [])
    if flags:
        for flag in flags:
            md += f"- {flag.get('message', 'Unknown flag')}\n"
    else:
        md += "- [See risk scorecard for detailed assessment]\n"

    md += """
### Proposed Mitigations
1. [Mitigation 1]
2. [Mitigation 2]
3. [Mitigation 3]

---

## Due Diligence Checklist

- [ ] Financial audit complete
- [ ] Customer references (5+ calls)
- [ ] Technical review
- [ ] Legal review (contracts, IP)
- [ ] Background checks
- [ ] Cap table verification

---

## Next Steps

1. Partner discussion
2. Founder meeting
3. Customer references
4. Term sheet negotiation

---

## Appendices

- A: Financial Model
- B: Cohort Analysis
- C: Cap Table Detail
- D: Risk Scorecard

---
*Crowley Capital — Austin, TX*
"""

    return md


def main():
    parser = argparse.ArgumentParser(description='Generate investment memo')
    parser.add_argument('--analysis-dir', default='data-room/analysis/',
                        help='Directory containing analysis outputs')
    parser.add_argument('--output', default='data-room/output/investment-memo.md',
                        help='Output memo path')
    parser.add_argument('--company', default='Target Company',
                        help='Company name')

    args = parser.parse_args()

    # Load data
    print(f"Loading analysis from {args.analysis_dir}...")
    data = load_analysis_data(args.analysis_dir)

    # Generate memo
    print("Generating investment memo...")
    md = generate_memo(data, args.company)

    # Write output
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, 'w') as f:
        f.write(md)

    print(f"Investment memo saved to {args.output}")


if __name__ == '__main__':
    main()
