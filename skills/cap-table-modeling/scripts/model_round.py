#!/usr/bin/env python3
"""
Round Modeling for Cap Table
Models new investment rounds and their dilutive impact.

Usage:
    python model_round.py --captable captable.json --round-size 5000000 --pre-money 20000000 --output round_model.json
"""

import argparse
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict, field


@dataclass
class RoundTerms:
    """Investment round terms."""
    round_name: str
    investment_amount: float
    pre_money_valuation: float
    post_money_valuation: float = 0.0
    price_per_share: float = 0.0
    new_shares_issued: int = 0
    option_pool_increase: float = 0.0
    liquidation_preference: float = 1.0
    participating: bool = False
    participation_cap: float = 0.0
    anti_dilution: str = 'broad_weighted_average'
    pro_rata_rights: bool = True


@dataclass
class DilutionImpact:
    """Dilution impact for a holder."""
    holder_name: str
    holder_type: str
    pre_round_shares: int
    pre_round_pct: float
    post_round_shares: int
    post_round_pct: float
    dilution_pct: float


@dataclass
class RoundModel:
    """Complete round model output."""
    round_terms: RoundTerms
    pre_money_cap_table: Dict[str, Any]
    post_money_cap_table: Dict[str, Any]
    dilution_impacts: List[DilutionImpact]
    new_investor_ownership: float
    option_pool_post: float


def load_cap_table(path: str) -> Dict[str, Any]:
    """Load parsed cap table JSON."""
    with open(path, 'r') as f:
        return json.load(f)


def calculate_option_pool_shuffle(
    pre_money: float,
    investment: float,
    current_pool_pct: float,
    target_pool_pct: float,
    fully_diluted_shares: int
) -> Dict[str, Any]:
    """Calculate option pool expansion (shuffle) before round."""
    if target_pool_pct <= current_pool_pct:
        return {
            'pool_increase_shares': 0,
            'pool_increase_pct': 0,
            'effective_pre_money': pre_money
        }

    # Option pool shuffle happens pre-money
    additional_pool_pct = target_pool_pct - current_pool_pct

    # New shares for pool expansion
    pool_increase_shares = int(fully_diluted_shares * (additional_pool_pct / 100))

    # Effective pre-money is reduced by pool expansion
    effective_pre_money = pre_money * (1 - additional_pool_pct / 100)

    return {
        'pool_increase_shares': pool_increase_shares,
        'pool_increase_pct': additional_pool_pct,
        'effective_pre_money': effective_pre_money
    }


def model_round(
    cap_table: Dict[str, Any],
    investment: float,
    pre_money: float,
    round_name: str = 'Series A',
    target_option_pool: float = 0.0,
    liquidation_pref: float = 1.0,
    participating: bool = False
) -> RoundModel:
    """Model a new investment round."""

    cap_data = cap_table.get('cap_table', cap_table)
    current_shares = cap_data['fully_diluted_shares']
    current_pool_pct = cap_data.get('option_pool_pct', 0)
    holders = cap_data.get('holders', [])

    # Handle option pool shuffle if needed
    pool_shuffle = calculate_option_pool_shuffle(
        pre_money=pre_money,
        investment=investment,
        current_pool_pct=current_pool_pct,
        target_pool_pct=target_option_pool,
        fully_diluted_shares=current_shares
    )

    # Calculate shares after pool expansion
    shares_after_pool = current_shares + pool_shuffle['pool_increase_shares']

    # Calculate post-money and price per share
    post_money = pre_money + investment
    price_per_share = pre_money / shares_after_pool

    # Calculate new shares for investor
    new_shares = int(investment / price_per_share)

    # Total shares after round
    total_shares_post = shares_after_pool + new_shares

    # Calculate new investor ownership
    new_investor_pct = (new_shares / total_shares_post) * 100

    # Build round terms
    round_terms = RoundTerms(
        round_name=round_name,
        investment_amount=investment,
        pre_money_valuation=pre_money,
        post_money_valuation=post_money,
        price_per_share=price_per_share,
        new_shares_issued=new_shares,
        option_pool_increase=pool_shuffle['pool_increase_pct'],
        liquidation_preference=liquidation_pref,
        participating=participating
    )

    # Calculate dilution impacts
    dilution_impacts = []
    for holder in holders:
        pre_shares = holder['shares']
        pre_pct = holder['ownership_pct']

        # Shares don't change, but percentage does
        post_pct = (pre_shares / total_shares_post) * 100
        dilution = pre_pct - post_pct

        impact = DilutionImpact(
            holder_name=holder['name'],
            holder_type=holder['holder_type'],
            pre_round_shares=pre_shares,
            pre_round_pct=round(pre_pct, 2),
            post_round_shares=pre_shares,
            post_round_pct=round(post_pct, 2),
            dilution_pct=round(dilution, 2)
        )
        dilution_impacts.append(impact)

    # Build post-money cap table
    post_holders = []
    for holder in holders:
        post_holder = holder.copy()
        post_holder['ownership_pct'] = round((holder['shares'] / total_shares_post) * 100, 2)
        post_holder['fully_diluted_pct'] = post_holder['ownership_pct']
        post_holders.append(post_holder)

    # Add new investor
    new_investor = {
        'name': f'{round_name} Investor',
        'holder_type': 'investor',
        'share_class': f'preferred_{round_name.lower().replace(" ", "_")}',
        'shares': new_shares,
        'price_per_share': price_per_share,
        'invested': investment,
        'ownership_pct': round(new_investor_pct, 2),
        'fully_diluted_pct': round(new_investor_pct, 2)
    }
    post_holders.append(new_investor)

    # Option pool post-round
    pool_shares = cap_data.get('option_pool_shares', 0) + pool_shuffle['pool_increase_shares']
    option_pool_post = (pool_shares / total_shares_post) * 100

    post_cap_table = {
        'total_shares_outstanding': total_shares_post,
        'fully_diluted_shares': total_shares_post,
        'option_pool_shares': pool_shares,
        'option_pool_pct': round(option_pool_post, 2),
        'holders': post_holders
    }

    return RoundModel(
        round_terms=round_terms,
        pre_money_cap_table=cap_data,
        post_money_cap_table=post_cap_table,
        dilution_impacts=dilution_impacts,
        new_investor_ownership=round(new_investor_pct, 2),
        option_pool_post=round(option_pool_post, 2)
    )


def format_summary(model: RoundModel) -> str:
    """Format round model as summary text."""
    terms = model.round_terms

    summary = f"""
=== {terms.round_name} ROUND MODEL ===

Investment: ${terms.investment_amount:,.0f}
Pre-Money: ${terms.pre_money_valuation:,.0f}
Post-Money: ${terms.post_money_valuation:,.0f}
Price/Share: ${terms.price_per_share:.4f}
New Shares: {terms.new_shares_issued:,}

New Investor Ownership: {model.new_investor_ownership:.1f}%
Option Pool Post-Round: {model.option_pool_post:.1f}%

=== DILUTION IMPACT ===

"""
    for impact in sorted(model.dilution_impacts, key=lambda x: -x.pre_round_pct):
        summary += f"{impact.holder_name} ({impact.holder_type})\n"
        summary += f"  {impact.pre_round_pct:.1f}% -> {impact.post_round_pct:.1f}% "
        summary += f"(diluted {impact.dilution_pct:.1f}%)\n"

    return summary


def main():
    parser = argparse.ArgumentParser(description='Model investment round')
    parser.add_argument('--captable', required=True, help='Parsed cap table JSON')
    parser.add_argument('--round-size', type=float, required=True, help='Investment amount')
    parser.add_argument('--pre-money', type=float, required=True, help='Pre-money valuation')
    parser.add_argument('--round-name', default='Series A', help='Round name')
    parser.add_argument('--option-pool', type=float, default=0, help='Target option pool %')
    parser.add_argument('--liq-pref', type=float, default=1.0, help='Liquidation preference')
    parser.add_argument('--participating', action='store_true', help='Participating preferred')
    parser.add_argument('--output', default='round_model.json', help='Output file')

    args = parser.parse_args()

    # Load cap table
    print(f"Loading cap table from {args.captable}...")
    cap_table = load_cap_table(args.captable)

    # Model round
    print(f"Modeling {args.round_name}...")
    model = model_round(
        cap_table=cap_table,
        investment=args.round_size,
        pre_money=args.pre_money,
        round_name=args.round_name,
        target_option_pool=args.option_pool,
        liquidation_pref=args.liq_pref,
        participating=args.participating
    )

    # Output
    output = {
        'round_terms': asdict(model.round_terms),
        'new_investor_ownership': model.new_investor_ownership,
        'option_pool_post': model.option_pool_post,
        'dilution_impacts': [asdict(d) for d in model.dilution_impacts],
        'post_money_cap_table': model.post_money_cap_table,
        'modeled_at': datetime.now().isoformat()
    }

    with open(args.output, 'w') as f:
        json.dump(output, f, indent=2, default=str)

    # Print summary
    print(format_summary(model))
    print(f"Output saved to {args.output}")


if __name__ == '__main__':
    main()
