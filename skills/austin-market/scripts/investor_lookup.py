#!/usr/bin/env python3
"""
Austin Investor Lookup
Identifies potential co-investors based on deal characteristics.

Usage:
    python investor_lookup.py --stage series_a --sector "Enterprise SaaS" --size 5000000
"""

import argparse
import json
from datetime import datetime
from typing import Dict, Any, List


# Austin investor database
AUSTIN_INVESTORS = {
    'seed': [
        {
            'name': 'Capital Factory',
            'check_size': '$100K - $1M',
            'focus': ['B2B SaaS', 'Consumer Tech', 'Hardware'],
            'notes': 'Austin HQ accelerator, very active at seed'
        },
        {
            'name': 'ATX Venture Partners',
            'check_size': '$500K - $5M',
            'focus': ['Enterprise SaaS', 'Fintech', 'Healthcare'],
            'notes': 'Austin-focused, operator backgrounds'
        },
        {
            'name': 'Silverton Partners',
            'check_size': '$500K - $3M',
            'focus': ['B2B Software', 'Consumer', 'Healthcare'],
            'notes': 'Long-standing Austin presence'
        },
        {
            'name': 'Ecliptic Capital',
            'check_size': '$250K - $1M',
            'focus': ['SaaS', 'Marketplaces', 'Fintech'],
            'notes': 'Seed specialist, quick decisions'
        }
    ],
    'series_a': [
        {
            'name': 'LiveOak Venture Partners',
            'check_size': '$2M - $10M',
            'focus': ['Enterprise Software', 'SaaS', 'Cloud'],
            'notes': 'Lead Series A in Austin, strong board members'
        },
        {
            'name': 'S3 Ventures',
            'check_size': '$1M - $15M',
            'focus': ['B2B SaaS', 'Infrastructure', 'Security'],
            'notes': 'Texas-focused, can lead or follow'
        },
        {
            'name': 'Next Coast Ventures',
            'check_size': '$3M - $15M',
            'focus': ['Enterprise SaaS', 'Fintech', 'Healthcare IT'],
            'notes': 'Ex-operators, hands-on support'
        },
        {
            'name': 'Silverton Partners',
            'check_size': '$3M - $10M',
            'focus': ['B2B Software', 'Consumer', 'Healthcare'],
            'notes': 'Can lead Series A, strong network'
        }
    ],
    'series_b': [
        {
            'name': 'Vista Equity Partners',
            'check_size': '$50M+',
            'focus': ['Enterprise Software', 'SaaS'],
            'notes': 'Austin HQ, growth/buyout focus'
        },
        {
            'name': 'Thoma Bravo',
            'check_size': '$50M+',
            'focus': ['Software', 'Security', 'Fintech'],
            'notes': 'Austin office, very active'
        },
        {
            'name': 'Tritium Partners',
            'check_size': '$10M - $30M',
            'focus': ['Software', 'Tech Services'],
            'notes': 'Austin-based growth equity'
        },
        {
            'name': 'S3 Ventures',
            'check_size': '$10M - $20M',
            'focus': ['B2B SaaS', 'Infrastructure'],
            'notes': 'Can participate in larger rounds'
        }
    ]
}

# Sector specialists
SECTOR_SPECIALISTS = {
    'fintech': ['ATX Venture Partners', 'Next Coast Ventures', 'Thoma Bravo'],
    'cybersecurity': ['S3 Ventures', 'Thoma Bravo', 'Vista Equity Partners'],
    'healthcare': ['Next Coast Ventures', 'Silverton Partners', 'ATX Venture Partners'],
    'enterprise_saas': ['LiveOak Venture Partners', 'S3 Ventures', 'Vista Equity Partners'],
    'consumer': ['Silverton Partners', 'Capital Factory']
}


def normalize_sector(sector: str) -> str:
    """Normalize sector name for matching."""
    sector_lower = sector.lower().replace(' ', '_').replace('/', '_')

    mappings = {
        'enterprise_saas': 'enterprise_saas',
        'b2b_saas': 'enterprise_saas',
        'saas': 'enterprise_saas',
        'fintech': 'fintech',
        'payments': 'fintech',
        'cybersecurity': 'cybersecurity',
        'security': 'cybersecurity',
        'healthcare': 'healthcare',
        'healthtech': 'healthcare',
        'consumer': 'consumer',
        'd2c': 'consumer'
    }

    return mappings.get(sector_lower, 'enterprise_saas')


def find_investors(
    stage: str,
    sector: str = None,
    check_size: float = None
) -> List[Dict[str, Any]]:
    """Find matching investors."""
    stage_investors = AUSTIN_INVESTORS.get(stage, [])

    # Score each investor
    scored = []
    normalized_sector = normalize_sector(sector) if sector else None

    for investor in stage_investors:
        score = 50  # Base score

        # Sector match
        if sector:
            investor_focus = [f.lower() for f in investor['focus']]
            if any(sector.lower() in f for f in investor_focus):
                score += 30

            # Check sector specialists
            if normalized_sector in SECTOR_SPECIALISTS:
                if investor['name'] in SECTOR_SPECIALISTS[normalized_sector]:
                    score += 20

        scored.append({
            **investor,
            'match_score': score
        })

    # Sort by score
    scored.sort(key=lambda x: -x['match_score'])

    return scored


def generate_investor_report(
    stage: str,
    sector: str = None,
    check_size: float = None
) -> Dict[str, Any]:
    """Generate investor lookup report."""

    investors = find_investors(stage, sector, check_size)

    report = {
        'timestamp': datetime.now().isoformat(),
        'search_criteria': {
            'stage': stage,
            'sector': sector,
            'check_size': check_size
        },
        'investors': investors,
        'top_recommendations': investors[:3],
        'total_found': len(investors)
    }

    return report


def format_report_text(report: Dict[str, Any]) -> str:
    """Format report as readable text."""
    criteria = report['search_criteria']

    text = f"""
=== AUSTIN INVESTOR LOOKUP ===

Search Criteria:
  Stage: {criteria['stage'].replace('_', ' ').title()}
  Sector: {criteria['sector'] or 'Any'}

Recommended Investors:
"""

    for i, investor in enumerate(report['investors'], 1):
        text += f"""
{i}. {investor['name']}
   Check Size: {investor['check_size']}
   Focus: {', '.join(investor['focus'])}
   Notes: {investor['notes']}
"""

    return text


def main():
    parser = argparse.ArgumentParser(description='Austin investor lookup')
    parser.add_argument('--stage', choices=['seed', 'series_a', 'series_b'],
                        required=True, help='Funding stage')
    parser.add_argument('--sector', help='Company sector')
    parser.add_argument('--size', type=float, help='Target check size')
    parser.add_argument('--output', help='Output JSON file')

    args = parser.parse_args()

    # Generate report
    report = generate_investor_report(
        stage=args.stage,
        sector=args.sector,
        check_size=args.size
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
