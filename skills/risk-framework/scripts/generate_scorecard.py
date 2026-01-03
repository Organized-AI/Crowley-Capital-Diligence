#!/usr/bin/env python3
"""
Risk Scorecard Generator
Generates 11-risks scorecard from analysis outputs.

Usage:
    python generate_scorecard.py --analysis-dir data-room/analysis/ --output data-room/output/risk-scorecard.md
"""

import argparse
import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class RiskScore:
    """Individual risk score."""
    risk_id: int
    name: str
    score: float
    weight: float
    evidence: List[str]
    concerns: List[str]


# Risk definitions with weights
RISKS = [
    {'id': 1, 'name': 'Market Timing', 'weight': 0.05,
     'question': 'Is the market ready now?'},
    {'id': 2, 'name': 'Business Model', 'weight': 0.12,
     'question': 'Can this make money sustainably?'},
    {'id': 3, 'name': 'Market Adoption', 'weight': 0.10,
     'question': 'Will customers actually buy?'},
    {'id': 4, 'name': 'Market Size', 'weight': 0.12,
     'question': 'Is the opportunity big enough?'},
    {'id': 5, 'name': 'Execution', 'weight': 0.10,
     'question': 'Can the team ship and scale?'},
    {'id': 6, 'name': 'Technology', 'weight': 0.08,
     'question': 'Is there defensible tech advantage?'},
    {'id': 7, 'name': 'Capitalization', 'weight': 0.08,
     'question': 'Is funding sufficient and efficient?'},
    {'id': 8, 'name': 'Competition', 'weight': 0.08,
     'question': 'Can they win against alternatives?'},
    {'id': 9, 'name': 'Team', 'weight': 0.15,
     'question': 'Are these the right people?'},
    {'id': 10, 'name': 'Regulatory/Legal', 'weight': 0.05,
     'question': 'Are there compliance landmines?'},
    {'id': 11, 'name': 'Exit Potential', 'weight': 0.07,
     'question': 'Can this return the fund?'}
]


def load_analysis_data(analysis_dir: str) -> Dict[str, Any]:
    """Load all analysis JSON files."""
    data = {}

    json_files = ['metrics.json', 'financial-summary.json', 'parsed_captable.json',
                  'customer-analysis.json', 'round_model.json']

    for filename in json_files:
        filepath = os.path.join(analysis_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                key = filename.replace('.json', '').replace('-', '_')
                data[key] = json.load(f)

    # Load flags
    flags_path = os.path.join(analysis_dir, 'flags.md')
    if os.path.exists(flags_path):
        with open(flags_path, 'r') as f:
            data['flags_content'] = f.read()

    return data


def score_business_model(data: Dict[str, Any]) -> RiskScore:
    """Score business model risk based on unit economics."""
    evidence = []
    concerns = []
    score = 6.0  # Default neutral

    metrics = data.get('metrics', {})

    # LTV:CAC
    ltv_cac = metrics.get('ltv_cac_ratio', 0)
    if ltv_cac >= 4:
        score += 1.5
        evidence.append(f"Strong LTV:CAC of {ltv_cac:.1f}x")
    elif ltv_cac >= 3:
        score += 0.5
        evidence.append(f"Healthy LTV:CAC of {ltv_cac:.1f}x")
    elif ltv_cac > 0:
        score -= 1.5
        concerns.append(f"Weak LTV:CAC of {ltv_cac:.1f}x")

    # Gross margin
    gross_margin = metrics.get('gross_margin', 0)
    if gross_margin >= 75:
        score += 1
        evidence.append(f"SaaS-grade margins at {gross_margin:.0f}%")
    elif gross_margin >= 60:
        evidence.append(f"Acceptable margins at {gross_margin:.0f}%")
    elif gross_margin > 0:
        score -= 1
        concerns.append(f"Below-average margins at {gross_margin:.0f}%")

    # NRR
    nrr = metrics.get('net_revenue_retention', 100)
    if nrr >= 120:
        score += 1
        evidence.append(f"Excellent NRR of {nrr:.0f}%")
    elif nrr >= 110:
        score += 0.5
        evidence.append(f"Good NRR of {nrr:.0f}%")
    elif nrr < 100:
        score -= 1.5
        concerns.append(f"Shrinking customer base with NRR of {nrr:.0f}%")

    score = max(1, min(10, score))

    return RiskScore(
        risk_id=2,
        name='Business Model',
        score=round(score, 1),
        weight=0.12,
        evidence=evidence,
        concerns=concerns
    )


def score_capitalization(data: Dict[str, Any]) -> RiskScore:
    """Score capitalization risk."""
    evidence = []
    concerns = []
    score = 6.0

    metrics = data.get('metrics', {})

    # Runway
    runway = metrics.get('runway_months', 0)
    if runway >= 24:
        score += 1.5
        evidence.append(f"Strong runway of {runway:.0f} months")
    elif runway >= 18:
        score += 0.5
        evidence.append(f"Adequate runway of {runway:.0f} months")
    elif runway >= 12:
        concerns.append(f"Limited runway of {runway:.0f} months")
    elif runway > 0:
        score -= 2
        concerns.append(f"Critical runway of only {runway:.0f} months")

    # Burn multiple
    burn_multiple = metrics.get('burn_multiple', 0)
    if burn_multiple > 0 and burn_multiple <= 1:
        score += 1.5
        evidence.append(f"Efficient growth with {burn_multiple:.1f}x burn multiple")
    elif burn_multiple <= 1.5:
        score += 0.5
        evidence.append(f"Reasonable burn multiple of {burn_multiple:.1f}x")
    elif burn_multiple <= 2.5:
        concerns.append(f"High burn multiple of {burn_multiple:.1f}x")
    elif burn_multiple > 2.5:
        score -= 1.5
        concerns.append(f"Inefficient growth with {burn_multiple:.1f}x burn multiple")

    score = max(1, min(10, score))

    return RiskScore(
        risk_id=7,
        name='Capitalization',
        score=round(score, 1),
        weight=0.08,
        evidence=evidence,
        concerns=concerns
    )


def score_market_adoption(data: Dict[str, Any]) -> RiskScore:
    """Score market adoption risk."""
    evidence = []
    concerns = []
    score = 6.0

    metrics = data.get('metrics', {})

    # MRR growth
    mrr_growth = metrics.get('mrr_growth_mom', 0)
    if mrr_growth >= 15:
        score += 2
        evidence.append(f"Exceptional MoM growth of {mrr_growth:.0f}%")
    elif mrr_growth >= 10:
        score += 1
        evidence.append(f"Strong MoM growth of {mrr_growth:.0f}%")
    elif mrr_growth >= 5:
        evidence.append(f"Moderate MoM growth of {mrr_growth:.0f}%")
    elif mrr_growth > 0:
        score -= 1
        concerns.append(f"Slow MoM growth of {mrr_growth:.0f}%")
    else:
        score -= 2
        concerns.append("Flat or declining growth")

    # Churn
    churn = metrics.get('gross_churn_rate', 0)
    if churn <= 1:
        score += 1
        evidence.append(f"Excellent retention with {churn:.1f}% churn")
    elif churn <= 2:
        evidence.append(f"Good retention with {churn:.1f}% churn")
    elif churn <= 5:
        concerns.append(f"Elevated churn at {churn:.1f}%")
    elif churn > 5:
        score -= 1.5
        concerns.append(f"High churn at {churn:.1f}%")

    score = max(1, min(10, score))

    return RiskScore(
        risk_id=3,
        name='Market Adoption',
        score=round(score, 1),
        weight=0.10,
        evidence=evidence,
        concerns=concerns
    )


def generate_default_scores() -> List[RiskScore]:
    """Generate default scores for risks without data."""
    defaults = []
    for risk in RISKS:
        if risk['id'] not in [2, 3, 7]:  # Skip ones we calculate
            defaults.append(RiskScore(
                risk_id=risk['id'],
                name=risk['name'],
                score=6.0,
                weight=risk['weight'],
                evidence=['Requires manual assessment'],
                concerns=[]
            ))
    return defaults


def calculate_weighted_score(scores: List[RiskScore]) -> float:
    """Calculate weighted overall score."""
    total = sum(s.score * s.weight for s in scores)
    return round(total, 2)


def check_veto_rules(scores: List[RiskScore]) -> Optional[str]:
    """Check if any veto rules are triggered."""
    for score in scores:
        if score.score == 1:
            return f"VETO: {score.name} scored 1 - critical failure"
        if score.name == 'Team' and score.score < 3:
            return f"VETO: Team score of {score.score} below minimum threshold"
        if score.name == 'Market Size' and score.score < 4:
            return f"VETO: Market Size score of {score.score} below minimum threshold"
        if score.name == 'Business Model' and score.score < 3:
            return f"VETO: Business Model score of {score.score} below minimum threshold"
    return None


def get_recommendation(weighted_score: float, veto: Optional[str]) -> str:
    """Get investment recommendation."""
    if veto:
        return "PASS"

    if weighted_score >= 8.0:
        return "STRONG CONVICTION — Lead the round"
    elif weighted_score >= 7.0:
        return "POSITIVE — Participate in round"
    elif weighted_score >= 6.0:
        return "CAUTIOUS POSITIVE — Need risk mitigation"
    elif weighted_score >= 5.0:
        return "PASS — But monitor"
    else:
        return "CLEAR PASS"


def generate_scorecard_markdown(
    scores: List[RiskScore],
    weighted_score: float,
    recommendation: str,
    veto: Optional[str]
) -> str:
    """Generate markdown scorecard."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    md = f"""# Risk Scorecard

**Generated**: {timestamp}
**Overall Score**: {weighted_score:.1f} / 10.0
**Recommendation**: {recommendation}

"""

    if veto:
        md += f"""## ⛔ Veto Triggered

{veto}

---

"""

    md += """## Scores by Risk

| # | Risk | Score | Weight | Weighted |
|---|------|-------|--------|----------|
"""

    for score in sorted(scores, key=lambda x: x.risk_id):
        weighted = score.score * score.weight
        bar = '█' * int(score.score) + '░' * (10 - int(score.score))
        md += f"| {score.risk_id} | {score.name} | {score.score:.1f} {bar} | {score.weight*100:.0f}% | {weighted:.2f} |\n"

    md += f"\n**Weighted Total**: {weighted_score:.1f}\n\n"

    # Strengths
    md += "## Top Strengths\n\n"
    all_evidence = []
    for score in scores:
        for e in score.evidence:
            if 'manual' not in e.lower():
                all_evidence.append((score.score, e))
    for _, e in sorted(all_evidence, reverse=True)[:5]:
        md += f"- {e}\n"

    # Concerns
    md += "\n## Key Concerns\n\n"
    all_concerns = []
    for score in scores:
        for c in score.concerns:
            all_concerns.append((10 - score.score, c))
    for _, c in sorted(all_concerns, reverse=True)[:5]:
        md += f"- {c}\n"

    md += """
---

## Scoring Guide

| Score | Rating |
|-------|--------|
| 9-10 | Exceptional |
| 7-8 | Strong |
| 5-6 | Acceptable |
| 3-4 | Concerning |
| 1-2 | Critical |

---
*Crowley Capital — Austin, TX*
"""

    return md


def main():
    parser = argparse.ArgumentParser(description='Generate 11-risks scorecard')
    parser.add_argument('--analysis-dir', default='data-room/analysis/',
                        help='Directory containing analysis outputs')
    parser.add_argument('--output', default='data-room/output/risk-scorecard.md',
                        help='Output scorecard path')

    args = parser.parse_args()

    # Load data
    print(f"Loading analysis from {args.analysis_dir}...")
    data = load_analysis_data(args.analysis_dir)

    # Calculate scores
    print("Calculating risk scores...")
    scores = []

    # Calculated scores
    scores.append(score_business_model(data))
    scores.append(score_capitalization(data))
    scores.append(score_market_adoption(data))

    # Default scores for remaining risks
    scores.extend(generate_default_scores())

    # Calculate weighted score
    weighted_score = calculate_weighted_score(scores)

    # Check veto rules
    veto = check_veto_rules(scores)

    # Get recommendation
    recommendation = get_recommendation(weighted_score, veto)

    # Generate markdown
    md = generate_scorecard_markdown(scores, weighted_score, recommendation, veto)

    # Write output
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, 'w') as f:
        f.write(md)

    print(f"\n=== RISK ASSESSMENT ===")
    print(f"Overall Score: {weighted_score:.1f}/10")
    print(f"Recommendation: {recommendation}")
    if veto:
        print(f"Veto: {veto}")
    print(f"\nScorecard saved to {args.output}")


if __name__ == '__main__':
    main()
