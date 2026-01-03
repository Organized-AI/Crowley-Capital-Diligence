#!/usr/bin/env python3
"""
Mermaid Chart Generator for Diligence Reports
Generates chart definitions for use with Mermaid Chart MCP.
"""

from typing import Dict, List, Any
import json


def generate_ownership_pie(cap_table: Dict[str, Any]) -> str:
    """Generate ownership pie chart Mermaid code."""
    stakeholders = cap_table.get('stakeholders', [])
    
    if not stakeholders:
        return ""
    
    # Group by category
    categories = {}
    for sh in stakeholders:
        cat = sh.get('category', 'Other')
        pct = sh.get('ownership_pct', 0)
        categories[cat] = categories.get(cat, 0) + pct
    
    lines = ['pie showData', '    title "Ownership Structure"']
    for cat, pct in sorted(categories.items(), key=lambda x: -x[1]):
        if pct > 0:
            lines.append(f'    "{cat}" : {pct:.1f}')
    
    return '\n'.join(lines)


def generate_revenue_chart(metrics: Dict[str, Any]) -> str:
    """Generate revenue growth bar chart."""
    monthly_revenue = metrics.get('monthly_revenue', [])
    
    if not monthly_revenue:
        return ""
    
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Use last 6 months
    recent = monthly_revenue[-6:] if len(monthly_revenue) >= 6 else monthly_revenue
    labels = months[:len(recent)]
    
    max_val = max(recent) if recent else 100
    
    lines = [
        'xychart-beta',
        '    title "Monthly Revenue Trend"',
        f'    x-axis [{", ".join(labels)}]',
        f'    y-axis "Revenue ($K)" 0 --> {int(max_val/1000 * 1.2)}',
        f'    bar [{", ".join(str(int(v/1000)) for v in recent)}]',
        f'    line [{", ".join(str(int(v/1000)) for v in recent)}]'
    ]
    
    return '\n'.join(lines)


def generate_risk_radar(risks: Dict[str, float]) -> str:
    """Generate risk scores as styled pie chart (radar alternative)."""
    if not risks:
        return ""
    
    lines = [
        '%%{init: {"theme": "base"}}%%',
        'pie showData',
        '    title "Risk Profile Scores"'
    ]
    
    for category, score in sorted(risks.items(), key=lambda x: -x[1]):
        lines.append(f'    "{category}" : {score:.1f}')
    
    return '\n'.join(lines)


def generate_funding_flow(funding_history: List[Dict]) -> str:
    """Generate funding history flowchart."""
    if not funding_history:
        return ""
    
    lines = ['flowchart LR', '    subgraph Funding History']
    
    prev_id = None
    for i, round_data in enumerate(funding_history):
        round_name = round_data.get('name', f'Round {i+1}')
        amount = round_data.get('amount', 0)
        node_id = f'R{i}'
        
        amount_str = f"${amount/1000000:.1f}M" if amount >= 1000000 else f"${amount/1000:.0f}K"
        lines.append(f'    {node_id}[{round_name}<br/>{amount_str}]')
        
        if prev_id:
            lines.append(f'    {prev_id} --> {node_id}')
        
        prev_id = node_id
    
    lines.append('    end')
    
    return '\n'.join(lines)


def generate_unit_economics_flow(metrics: Dict[str, Any]) -> str:
    """Generate unit economics visualization."""
    ltv = metrics.get('ltv', 0)
    cac = metrics.get('cac', 0)
    ltv_cac = ltv / cac if cac > 0 else 0
    
    lines = [
        'flowchart LR',
        '    subgraph Acquisition',
        f'    A[Marketing] --> B[Sales]',
        f'    B --> C[CAC<br/>${cac/1000:.0f}K]',
        '    end',
        '',
        '    subgraph Value',
        f'    D[Customer LTV<br/>${ltv/1000:.0f}K]',
        '    end',
        '',
        f'    C --> E{{LTV:CAC<br/>{ltv_cac:.1f}x}}',
        '    D --> E',
        ''
    ]
    
    # Style based on ratio
    if ltv_cac >= 3:
        lines.append('    style E fill:#38a169,color:#fff')
    elif ltv_cac >= 2:
        lines.append('    style E fill:#d69e2e,color:#fff')
    else:
        lines.append('    style E fill:#e53e3e,color:#fff')
    
    return '\n'.join(lines)


def generate_cohort_heatmap(cohorts: List[Dict]) -> str:
    """Generate cohort retention visualization as table-like diagram."""
    if not cohorts:
        return ""
    
    # This would be better as an actual heatmap image
    # For Mermaid, we'll create a simplified version
    lines = [
        'flowchart TB',
        '    subgraph Cohort Retention',
    ]
    
    for i, cohort in enumerate(cohorts[:6]):
        month = cohort.get('month', f'M{i+1}')
        retention = cohort.get('retention_pct', 100)
        
        color = '#38a169' if retention >= 80 else ('#d69e2e' if retention >= 60 else '#e53e3e')
        lines.append(f'    C{i}[{month}: {retention:.0f}%]')
        lines.append(f'    style C{i} fill:{color},color:#fff')
    
    lines.append('    end')
    
    return '\n'.join(lines)


def generate_burn_runway_chart(metrics: Dict[str, Any]) -> str:
    """Generate burn and runway visualization."""
    burn = metrics.get('burn_rate', 0)
    cash = metrics.get('cash_balance', 0)
    runway = metrics.get('runway_months', 0)
    
    lines = [
        'flowchart LR',
        f'    A[Cash Balance<br/>${cash/1000000:.1f}M] --> B[Monthly Burn<br/>${burn/1000:.0f}K]',
        f'    B --> C[Runway<br/>{runway:.0f} months]',
    ]
    
    # Color based on runway
    if runway >= 18:
        lines.append('    style C fill:#38a169,color:#fff')
    elif runway >= 12:
        lines.append('    style C fill:#d69e2e,color:#fff')
    else:
        lines.append('    style C fill:#e53e3e,color:#fff')
    
    return '\n'.join(lines)


def generate_all_charts(data: Dict[str, Any]) -> Dict[str, str]:
    """Generate all Mermaid charts for a diligence report."""
    charts = {}
    
    # Cap table charts
    if data.get('cap_table'):
        charts['ownership_pie'] = generate_ownership_pie(data['cap_table'])
    
    # Metrics charts
    if data.get('metrics'):
        charts['revenue_trend'] = generate_revenue_chart(data['metrics'])
        charts['unit_economics'] = generate_unit_economics_flow(data['metrics'])
        charts['burn_runway'] = generate_burn_runway_chart(data['metrics'])
    
    # Risk charts
    if data.get('risks', {}).get('scores'):
        charts['risk_radar'] = generate_risk_radar(data['risks']['scores'])
    
    # Funding history
    if data.get('funding_history'):
        charts['funding_flow'] = generate_funding_flow(data['funding_history'])
    
    # Cohort charts
    if data.get('cohorts'):
        charts['cohort_retention'] = generate_cohort_heatmap(data['cohorts'])
    
    return charts


# Example Mermaid templates for common visualizations
CHART_TEMPLATES = {
    'ownership_pie': '''pie showData
    title "Cap Table - Fully Diluted"
    "Founders" : {founders_pct}
    "Series A" : {series_a_pct}
    "Seed" : {seed_pct}
    "Option Pool" : {pool_pct}
    "Other" : {other_pct}''',
    
    'risk_scorecard': '''flowchart TB
    subgraph Risk Assessment
    M[Market: {market}/10]
    P[Product: {product}/10]
    T[Team: {team}/10]
    F[Financial: {financial}/10]
    C[Competition: {competition}/10]
    end
    
    M --> S[Composite: {composite}/10]
    P --> S
    T --> S
    F --> S
    C --> S
    
    style S fill:{composite_color},color:#fff''',
    
    'funding_timeline': '''gantt
    title Funding History
    dateFormat YYYY-MM
    section Rounds
    {round_entries}''',
    
    'revenue_growth': '''xychart-beta
    title "Monthly Revenue ($K)"
    x-axis [{months}]
    y-axis "Revenue" 0 --> {max_revenue}
    bar [{revenue_values}]
    line [{revenue_values}]''',
}


if __name__ == '__main__':
    # Example usage
    sample_data = {
        'metrics': {
            'ltv': 45000,
            'cac': 12000,
            'burn_rate': 180000,
            'cash_balance': 2500000,
            'runway_months': 14,
            'monthly_revenue': [100000, 120000, 140000, 165000, 190000, 220000]
        },
        'cap_table': {
            'stakeholders': [
                {'category': 'Founders', 'ownership_pct': 45},
                {'category': 'Series A', 'ownership_pct': 25},
                {'category': 'Seed', 'ownership_pct': 15},
                {'category': 'Option Pool', 'ownership_pct': 15},
            ]
        },
        'risks': {
            'scores': {
                'Market': 8,
                'Product': 7,
                'Team': 9,
                'Financial': 6,
                'Competition': 7
            }
        }
    }
    
    charts = generate_all_charts(sample_data)
    
    for name, code in charts.items():
        print(f"\n=== {name} ===")
        print(code)
