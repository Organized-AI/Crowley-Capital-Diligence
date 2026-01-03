#!/usr/bin/env python3
"""
Cap Table Parser
Parses cap table exports from Carta, Pulley, or standard CSV format.

Usage:
    python parse_captable.py --input captable.csv --output parsed_captable.json
"""

import argparse
import json
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict, field


@dataclass
class ShareClass:
    """Represents a share class."""
    name: str
    share_type: str  # common, preferred, options
    authorized: int = 0
    issued: int = 0
    outstanding: int = 0
    price_per_share: float = 0.0
    liquidation_preference: float = 1.0
    participating: bool = False
    conversion_ratio: float = 1.0
    seniority: int = 0


@dataclass
class Holder:
    """Represents a cap table holder."""
    name: str
    holder_type: str  # founder, investor, employee, pool
    share_class: str
    shares: int
    price_per_share: float
    invested: float
    ownership_pct: float
    fully_diluted_pct: float = 0.0
    vesting_start: Optional[str] = None
    vesting_end: Optional[str] = None
    vested_shares: int = 0


@dataclass
class CapTable:
    """Complete cap table representation."""
    company_name: str
    as_of_date: str
    total_shares_authorized: int
    total_shares_outstanding: int
    fully_diluted_shares: int
    share_classes: List[ShareClass] = field(default_factory=list)
    holders: List[Holder] = field(default_factory=list)
    option_pool_shares: int = 0
    option_pool_pct: float = 0.0


def detect_format(df: pd.DataFrame) -> str:
    """Detect cap table format (Carta, Pulley, generic)."""
    columns_lower = [c.lower() for c in df.columns]

    # Carta format detection
    if 'security type' in columns_lower or 'certificate' in columns_lower:
        return 'carta'

    # Pulley format detection
    if 'grant type' in columns_lower or 'stakeholder' in columns_lower:
        return 'pulley'

    # Generic CSV
    return 'generic'


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names to standard format."""
    df = df.copy()
    df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')

    # Standard column mappings
    column_map = {
        'stakeholder': 'holder',
        'shareholder': 'holder',
        'name': 'holder',
        'security_type': 'share_class',
        'class': 'share_class',
        'type': 'holder_type',
        'quantity': 'shares',
        'share_count': 'shares',
        'number_of_shares': 'shares',
        'cost_basis': 'invested',
        'investment': 'invested',
        'amount_invested': 'invested',
        'pps': 'price_per_share',
        'share_price': 'price_per_share',
        'ownership': 'ownership_pct',
        'percent': 'ownership_pct',
        '%': 'ownership_pct'
    }

    df = df.rename(columns={k: v for k, v in column_map.items() if k in df.columns})
    return df


def infer_holder_type(holder_name: str, share_class: str) -> str:
    """Infer holder type from name and share class."""
    holder_lower = holder_name.lower()
    class_lower = share_class.lower() if share_class else ''

    if 'founder' in holder_lower:
        return 'founder'
    if 'pool' in holder_lower or 'esop' in holder_lower or 'option' in holder_lower:
        return 'pool'
    if any(x in holder_lower for x in ['ventures', 'capital', 'partners', 'fund', 'investor']):
        return 'investor'
    if 'preferred' in class_lower:
        return 'investor'
    if 'common' in class_lower and 'employee' in holder_lower:
        return 'employee'

    return 'other'


def parse_generic_captable(df: pd.DataFrame) -> CapTable:
    """Parse generic CSV cap table format."""
    df = normalize_columns(df)

    # Calculate totals
    total_shares = df['shares'].sum() if 'shares' in df.columns else 0

    # Parse holders
    holders = []
    for _, row in df.iterrows():
        holder_name = str(row.get('holder', 'Unknown'))
        share_class = str(row.get('share_class', 'common'))
        shares = int(row.get('shares', 0))
        price = float(row.get('price_per_share', 0))
        invested = float(row.get('invested', 0))

        # Infer holder type if not provided
        holder_type = row.get('holder_type', infer_holder_type(holder_name, share_class))

        # Calculate ownership
        ownership = float(row.get('ownership_pct', 0))
        if ownership == 0 and total_shares > 0:
            ownership = (shares / total_shares) * 100

        holder = Holder(
            name=holder_name,
            holder_type=str(holder_type),
            share_class=share_class,
            shares=shares,
            price_per_share=price,
            invested=invested,
            ownership_pct=round(ownership, 2),
            fully_diluted_pct=round(ownership, 2)
        )
        holders.append(holder)

    # Identify share classes
    share_class_names = df['share_class'].unique() if 'share_class' in df.columns else ['common']
    share_classes = []
    for class_name in share_class_names:
        class_df = df[df['share_class'] == class_name] if 'share_class' in df.columns else df
        class_shares = class_df['shares'].sum()

        share_type = 'common'
        if 'preferred' in str(class_name).lower():
            share_type = 'preferred'
        elif 'option' in str(class_name).lower():
            share_type = 'options'

        sc = ShareClass(
            name=str(class_name),
            share_type=share_type,
            issued=int(class_shares),
            outstanding=int(class_shares)
        )
        share_classes.append(sc)

    # Calculate option pool
    pool_holders = [h for h in holders if h.holder_type == 'pool']
    option_pool_shares = sum(h.shares for h in pool_holders)
    option_pool_pct = (option_pool_shares / total_shares * 100) if total_shares > 0 else 0

    return CapTable(
        company_name='Unknown',
        as_of_date=datetime.now().strftime('%Y-%m-%d'),
        total_shares_authorized=int(total_shares),
        total_shares_outstanding=int(total_shares),
        fully_diluted_shares=int(total_shares),
        share_classes=share_classes,
        holders=holders,
        option_pool_shares=int(option_pool_shares),
        option_pool_pct=round(option_pool_pct, 2)
    )


def generate_summary(cap_table: CapTable) -> Dict[str, Any]:
    """Generate summary statistics from cap table."""
    summary = {
        'total_shares': cap_table.total_shares_outstanding,
        'fully_diluted': cap_table.fully_diluted_shares,
        'option_pool_pct': cap_table.option_pool_pct,
        'share_class_count': len(cap_table.share_classes),
        'holder_count': len(cap_table.holders)
    }

    # Ownership by type
    ownership_by_type = {}
    for holder in cap_table.holders:
        if holder.holder_type not in ownership_by_type:
            ownership_by_type[holder.holder_type] = 0
        ownership_by_type[holder.holder_type] += holder.ownership_pct
    summary['ownership_by_type'] = ownership_by_type

    # Total invested
    total_invested = sum(h.invested for h in cap_table.holders)
    summary['total_invested'] = total_invested

    # Implied valuation (if we have price per share for preferred)
    preferred_holders = [h for h in cap_table.holders if 'preferred' in h.share_class.lower()]
    if preferred_holders:
        latest_price = max(h.price_per_share for h in preferred_holders)
        if latest_price > 0:
            summary['implied_valuation'] = latest_price * cap_table.fully_diluted_shares

    return summary


def main():
    parser = argparse.ArgumentParser(description='Parse cap table CSV/Excel files')
    parser.add_argument('--input', required=True, help='Input cap table file')
    parser.add_argument('--output', default='parsed_captable.json', help='Output JSON file')
    parser.add_argument('--format', choices=['carta', 'pulley', 'generic', 'auto'],
                        default='auto', help='Input format')

    args = parser.parse_args()

    # Load file
    print(f"Loading cap table from {args.input}...")
    if args.input.endswith('.xlsx') or args.input.endswith('.xls'):
        df = pd.read_excel(args.input)
    else:
        df = pd.read_csv(args.input)

    print(f"Found {len(df)} rows, {len(df.columns)} columns")

    # Detect format
    if args.format == 'auto':
        detected_format = detect_format(df)
        print(f"Detected format: {detected_format}")
    else:
        detected_format = args.format

    # Parse based on format
    cap_table = parse_generic_captable(df)

    # Generate summary
    summary = generate_summary(cap_table)

    # Output
    output = {
        'cap_table': {
            'company_name': cap_table.company_name,
            'as_of_date': cap_table.as_of_date,
            'total_shares_authorized': cap_table.total_shares_authorized,
            'total_shares_outstanding': cap_table.total_shares_outstanding,
            'fully_diluted_shares': cap_table.fully_diluted_shares,
            'option_pool_shares': cap_table.option_pool_shares,
            'option_pool_pct': cap_table.option_pool_pct,
            'share_classes': [asdict(sc) for sc in cap_table.share_classes],
            'holders': [asdict(h) for h in cap_table.holders]
        },
        'summary': summary,
        'parsed_at': datetime.now().isoformat()
    }

    with open(args.output, 'w') as f:
        json.dump(output, f, indent=2, default=str)

    # Print summary
    print("\n=== CAP TABLE SUMMARY ===")
    print(f"Total Shares: {cap_table.total_shares_outstanding:,}")
    print(f"Holders: {len(cap_table.holders)}")
    print(f"Share Classes: {len(cap_table.share_classes)}")
    print(f"Option Pool: {cap_table.option_pool_pct:.1f}%")
    print(f"\nOwnership by Type:")
    for holder_type, pct in summary['ownership_by_type'].items():
        print(f"  {holder_type}: {pct:.1f}%")
    print(f"\nTotal Invested: ${summary['total_invested']:,.0f}")
    if 'implied_valuation' in summary:
        print(f"Implied Valuation: ${summary['implied_valuation']:,.0f}")

    print(f"\nOutput saved to {args.output}")


if __name__ == '__main__':
    main()
