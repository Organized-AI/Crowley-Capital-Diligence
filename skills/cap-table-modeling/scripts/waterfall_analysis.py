#!/usr/bin/env python3
"""
Waterfall Analysis for Exit Scenarios
Models exit proceeds distribution across different valuations.

Usage:
    python waterfall_analysis.py --captable captable.json --exits 10000000,50000000,100000000 --output waterfall.xlsx
"""

import argparse
import json
import pandas as pd
from datetime import datetime
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass, asdict
import xlsxwriter


@dataclass
class ShareClass:
    """Share class with liquidation terms."""
    name: str
    share_type: str
    shares: int
    price_per_share: float
    liquidation_preference: float
    participating: bool
    participation_cap: float
    seniority: int
    total_invested: float = 0.0


@dataclass
class HolderProceeds:
    """Exit proceeds for a holder."""
    holder_name: str
    holder_type: str
    share_class: str
    shares: int
    invested: float
    proceeds: float
    roi: float
    proceeds_pct: float


@dataclass
class ExitScenario:
    """Complete exit scenario analysis."""
    exit_value: float
    holders_proceeds: List[HolderProceeds]
    share_class_proceeds: Dict[str, float]
    total_distributed: float
    remaining: float


def load_cap_table(path: str) -> Dict[str, Any]:
    """Load parsed cap table JSON or round model JSON."""
    with open(path, 'r') as f:
        data = json.load(f)

    # Handle round model output
    if 'post_money_cap_table' in data:
        return data['post_money_cap_table']

    # Handle parsed cap table
    if 'cap_table' in data:
        return data['cap_table']

    return data


def extract_share_classes(cap_table: Dict[str, Any]) -> List[ShareClass]:
    """Extract share classes with their terms from cap table."""
    holders = cap_table.get('holders', [])
    classes = {}

    for holder in holders:
        class_name = holder.get('share_class', 'common')
        if class_name not in classes:
            # Determine share type and seniority
            share_type = 'common'
            seniority = 0
            liq_pref = 0.0
            participating = False

            if 'preferred' in class_name.lower():
                share_type = 'preferred'
                seniority = 1  # Base preferred seniority
                liq_pref = 1.0  # 1x default

                # Series hierarchy (higher letter = more senior)
                if 'series_b' in class_name.lower() or 'series b' in class_name.lower():
                    seniority = 2
                elif 'series_c' in class_name.lower() or 'series c' in class_name.lower():
                    seniority = 3
                elif 'series_d' in class_name.lower() or 'series d' in class_name.lower():
                    seniority = 4

            classes[class_name] = ShareClass(
                name=class_name,
                share_type=share_type,
                shares=0,
                price_per_share=holder.get('price_per_share', 0),
                liquidation_preference=liq_pref,
                participating=participating,
                participation_cap=0,
                seniority=seniority
            )

        classes[class_name].shares += holder.get('shares', 0)
        classes[class_name].total_invested += holder.get('invested', 0)

    return list(classes.values())


def calculate_waterfall(
    cap_table: Dict[str, Any],
    exit_value: float
) -> ExitScenario:
    """Calculate exit proceeds waterfall."""
    holders = cap_table.get('holders', [])
    share_classes = extract_share_classes(cap_table)
    total_shares = cap_table.get('fully_diluted_shares', cap_table.get('total_shares_outstanding', 0))

    remaining = exit_value
    holder_proceeds = {h['name']: 0.0 for h in holders}
    class_proceeds = {sc.name: 0.0 for sc in share_classes}

    # Sort share classes by seniority (highest first)
    sorted_classes = sorted(share_classes, key=lambda x: -x.seniority)

    # Step 1: Pay liquidation preferences (senior to junior)
    for share_class in sorted_classes:
        if share_class.share_type != 'preferred':
            continue

        # Calculate liquidation preference amount
        liq_amount = share_class.total_invested * share_class.liquidation_preference

        # Pay up to available
        payment = min(liq_amount, remaining)
        remaining -= payment

        # Distribute to holders in this class
        for holder in holders:
            if holder.get('share_class') == share_class.name:
                holder_pct = holder.get('shares', 0) / share_class.shares if share_class.shares > 0 else 0
                holder_payment = payment * holder_pct
                holder_proceeds[holder['name']] += holder_payment
                class_proceeds[share_class.name] += holder_payment

    # Step 2: Distribute remaining pro-rata to all shareholders
    if remaining > 0:
        # For non-participating preferred, they choose between liq pref or conversion
        # For simplicity, we assume conversion if remaining/share > price paid
        for holder in holders:
            holder_shares = holder.get('shares', 0)
            pro_rata_pct = holder_shares / total_shares if total_shares > 0 else 0
            pro_rata_amount = remaining * pro_rata_pct
            holder_proceeds[holder['name']] += pro_rata_amount
            class_proceeds[holder.get('share_class', 'common')] += pro_rata_amount

        remaining = 0

    # Build holder proceeds list
    proceeds_list = []
    for holder in holders:
        proceeds = holder_proceeds[holder['name']]
        invested = holder.get('invested', 0)
        roi = (proceeds / invested - 1) if invested > 0 else 0

        hp = HolderProceeds(
            holder_name=holder['name'],
            holder_type=holder.get('holder_type', 'other'),
            share_class=holder.get('share_class', 'common'),
            shares=holder.get('shares', 0),
            invested=invested,
            proceeds=round(proceeds, 2),
            roi=round(roi, 2),
            proceeds_pct=round(proceeds / exit_value * 100, 2) if exit_value > 0 else 0
        )
        proceeds_list.append(hp)

    return ExitScenario(
        exit_value=exit_value,
        holders_proceeds=proceeds_list,
        share_class_proceeds=class_proceeds,
        total_distributed=exit_value - remaining,
        remaining=remaining
    )


def generate_waterfall_scenarios(
    cap_table: Dict[str, Any],
    exit_values: List[float]
) -> List[ExitScenario]:
    """Generate waterfall analysis for multiple exit scenarios."""
    return [calculate_waterfall(cap_table, ev) for ev in exit_values]


def export_to_excel(
    scenarios: List[ExitScenario],
    output_path: str
):
    """Export waterfall analysis to Excel."""
    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        workbook = writer.book

        # Format definitions
        money_format = workbook.add_format({'num_format': '$#,##0'})
        pct_format = workbook.add_format({'num_format': '0.0%'})
        header_format = workbook.add_format({'bold': True, 'bg_color': '#4472C4', 'font_color': 'white'})

        # Summary sheet
        summary_data = []
        for scenario in scenarios:
            row = {'Exit Value': scenario.exit_value}
            for hp in scenario.holders_proceeds:
                row[hp.holder_name] = hp.proceeds
            summary_data.append(row)

        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        # Format summary sheet
        worksheet = writer.sheets['Summary']
        for col_num in range(len(summary_df.columns)):
            worksheet.set_column(col_num, col_num, 15, money_format)

        # Detailed sheets for each scenario
        for i, scenario in enumerate(scenarios):
            sheet_name = f"Exit ${int(scenario.exit_value/1000000)}M"

            detail_data = []
            for hp in sorted(scenario.holders_proceeds, key=lambda x: -x.proceeds):
                detail_data.append({
                    'Holder': hp.holder_name,
                    'Type': hp.holder_type,
                    'Share Class': hp.share_class,
                    'Shares': hp.shares,
                    'Invested': hp.invested,
                    'Proceeds': hp.proceeds,
                    'ROI': hp.roi,
                    '% of Exit': hp.proceeds_pct / 100
                })

            detail_df = pd.DataFrame(detail_data)
            detail_df.to_excel(writer, sheet_name=sheet_name, index=False)

        # ROI comparison sheet
        roi_data = []
        for scenario in scenarios:
            row = {'Exit Value': scenario.exit_value}
            for hp in scenario.holders_proceeds:
                row[f"{hp.holder_name} ROI"] = hp.roi
            roi_data.append(row)

        roi_df = pd.DataFrame(roi_data)
        roi_df.to_excel(writer, sheet_name='ROI Comparison', index=False)


def main():
    parser = argparse.ArgumentParser(description='Generate exit waterfall analysis')
    parser.add_argument('--captable', required=True, help='Cap table or round model JSON')
    parser.add_argument('--exits', required=True,
                        help='Comma-separated exit values (e.g., 10000000,50000000,100000000)')
    parser.add_argument('--output', default='waterfall.xlsx', help='Output Excel file')
    parser.add_argument('--json', action='store_true', help='Also output JSON')

    args = parser.parse_args()

    # Parse exit values
    exit_values = [float(x.strip()) for x in args.exits.split(',')]

    # Load cap table
    print(f"Loading cap table from {args.captable}...")
    cap_table = load_cap_table(args.captable)

    # Generate scenarios
    print(f"Analyzing {len(exit_values)} exit scenarios...")
    scenarios = generate_waterfall_scenarios(cap_table, exit_values)

    # Export to Excel
    print(f"Exporting to {args.output}...")
    export_to_excel(scenarios, args.output)

    # Optional JSON output
    if args.json:
        json_path = args.output.replace('.xlsx', '.json')
        json_output = {
            'scenarios': [
                {
                    'exit_value': s.exit_value,
                    'holders_proceeds': [asdict(hp) for hp in s.holders_proceeds],
                    'share_class_proceeds': s.share_class_proceeds,
                    'total_distributed': s.total_distributed
                }
                for s in scenarios
            ],
            'generated_at': datetime.now().isoformat()
        }
        with open(json_path, 'w') as f:
            json.dump(json_output, f, indent=2)
        print(f"JSON saved to {json_path}")

    # Print summary
    print("\n=== WATERFALL SUMMARY ===\n")
    for scenario in scenarios:
        print(f"Exit: ${scenario.exit_value:,.0f}")
        print("-" * 50)
        for hp in sorted(scenario.holders_proceeds, key=lambda x: -x.proceeds)[:5]:
            roi_str = f"{hp.roi:.1f}x" if hp.roi >= 0 else "N/A"
            print(f"  {hp.holder_name}: ${hp.proceeds:,.0f} ({hp.proceeds_pct:.1f}%) ROI: {roi_str}")
        print()

    print(f"Output saved to {args.output}")


if __name__ == '__main__':
    main()
