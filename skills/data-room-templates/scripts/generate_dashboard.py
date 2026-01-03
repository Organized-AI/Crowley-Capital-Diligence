#!/usr/bin/env python3
"""
Metrics Dashboard Generator
Generates interactive HTML dashboard with Plotly charts.

Usage:
    python generate_dashboard.py --analysis-dir data-room/analysis/ --output data-room/output/metrics-dashboard.html
"""

import argparse
import json
import os
from datetime import datetime
from typing import Dict, Any

try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False


def load_analysis_data(analysis_dir: str) -> Dict[str, Any]:
    """Load all analysis JSON files."""
    data = {}

    json_files = ['metrics.json', 'parsed_captable.json', 'round_model.json',
                  'series_a_model.json']

    for filename in json_files:
        filepath = os.path.join(analysis_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                key = filename.replace('.json', '').replace('-', '_')
                data[key] = json.load(f)

    return data


def create_gauge_chart(value: float, title: str, ranges: list) -> str:
    """Create a gauge chart HTML snippet."""
    if not PLOTLY_AVAILABLE:
        return f"<div class='metric-card'><h3>{title}</h3><p class='metric-value'>{value:.1f}</p></div>"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title},
        gauge={
            'axis': {'range': [0, ranges[-1][1]]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': r[:2], 'color': r[2]} for r in ranges
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))

    fig.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20))
    return fig.to_html(full_html=False, include_plotlyjs=False)


def create_metric_cards(metrics: Dict[str, Any]) -> str:
    """Create metric cards HTML."""
    cards = []

    # Key metrics to display
    metric_config = [
        ('arr', 'ARR', '${:,.0f}'),
        ('mrr', 'MRR', '${:,.0f}'),
        ('mrr_growth_mom', 'MoM Growth', '{:.1f}%'),
        ('net_revenue_retention', 'NRR', '{:.0f}%'),
        ('ltv_cac_ratio', 'LTV:CAC', '{:.1f}x'),
        ('gross_margin', 'Gross Margin', '{:.0f}%'),
        ('burn_multiple', 'Burn Multiple', '{:.1f}x'),
        ('runway_months', 'Runway', '{:.0f} mo'),
    ]

    for key, label, fmt in metric_config:
        value = metrics.get(key, 0)
        formatted = fmt.format(value) if value else 'N/A'

        # Determine status color
        status_class = 'neutral'
        if key == 'ltv_cac_ratio':
            status_class = 'good' if value >= 3 else 'warning' if value >= 2 else 'bad'
        elif key == 'net_revenue_retention':
            status_class = 'good' if value >= 110 else 'warning' if value >= 100 else 'bad'
        elif key == 'burn_multiple':
            status_class = 'good' if value <= 1.5 else 'warning' if value <= 2.5 else 'bad'
        elif key == 'runway_months':
            status_class = 'good' if value >= 18 else 'warning' if value >= 12 else 'bad'
        elif key == 'mrr_growth_mom':
            status_class = 'good' if value >= 10 else 'warning' if value >= 5 else 'neutral'

        cards.append(f"""
        <div class="metric-card {status_class}">
            <h3>{label}</h3>
            <p class="metric-value">{formatted}</p>
        </div>
        """)

    return '\n'.join(cards)


def create_ownership_chart(captable: Dict[str, Any]) -> str:
    """Create ownership pie chart."""
    if not PLOTLY_AVAILABLE:
        return "<p>Plotly not available for charts</p>"

    summary = captable.get('summary', {})
    ownership = summary.get('ownership_by_type', {})

    if not ownership:
        return "<p>No ownership data available</p>"

    labels = list(ownership.keys())
    values = list(ownership.values())

    fig = go.Figure(data=[go.Pie(
        labels=[l.title() for l in labels],
        values=values,
        hole=0.4,
        marker_colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    )])

    fig.update_layout(
        title="Ownership Distribution",
        height=350,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    return fig.to_html(full_html=False, include_plotlyjs=False)


def generate_dashboard(data: Dict[str, Any]) -> str:
    """Generate complete HTML dashboard."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    metrics = data.get('metrics', {})
    captable = data.get('parsed_captable', {})

    # Generate components
    metric_cards = create_metric_cards(metrics)
    ownership_chart = create_ownership_chart(captable)

    # Flags section
    flags = metrics.get('flags', [])
    flags_html = ""
    for flag in flags:
        severity = flag.get('severity', 'medium')
        message = flag.get('message', '')
        icon = '🔴' if severity == 'high' else '🟡'
        flags_html += f"<li>{icon} {message}</li>"

    if not flags_html:
        flags_html = "<li>✅ No threshold violations</li>"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Metrics Dashboard - Crowley Capital</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        :root {{
            --primary: #1a365d;
            --secondary: #2d3748;
            --success: #48bb78;
            --warning: #ecc94b;
            --danger: #f56565;
            --light: #f7fafc;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: var(--light);
            color: var(--secondary);
            line-height: 1.6;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}

        header {{
            background: var(--primary);
            color: white;
            padding: 20px;
            margin-bottom: 30px;
        }}

        header h1 {{
            font-size: 24px;
            font-weight: 600;
        }}

        header p {{
            opacity: 0.8;
            font-size: 14px;
        }}

        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}

        .metric-card {{
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid var(--secondary);
        }}

        .metric-card.good {{
            border-left-color: var(--success);
        }}

        .metric-card.warning {{
            border-left-color: var(--warning);
        }}

        .metric-card.bad {{
            border-left-color: var(--danger);
        }}

        .metric-card h3 {{
            font-size: 14px;
            text-transform: uppercase;
            color: #718096;
            margin-bottom: 8px;
        }}

        .metric-value {{
            font-size: 28px;
            font-weight: 700;
            color: var(--primary);
        }}

        .section {{
            background: white;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}

        .section h2 {{
            font-size: 18px;
            margin-bottom: 16px;
            color: var(--primary);
        }}

        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 24px;
        }}

        .flags-list {{
            list-style: none;
        }}

        .flags-list li {{
            padding: 12px;
            border-bottom: 1px solid #e2e8f0;
        }}

        .flags-list li:last-child {{
            border-bottom: none;
        }}

        footer {{
            text-align: center;
            padding: 20px;
            color: #718096;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>Metrics Dashboard</h1>
            <p>Generated: {timestamp}</p>
        </div>
    </header>

    <div class="container">
        <div class="metrics-grid">
            {metric_cards}
        </div>

        <div class="section">
            <h2>Alerts & Flags</h2>
            <ul class="flags-list">
                {flags_html}
            </ul>
        </div>

        <div class="charts-grid">
            <div class="section">
                <h2>Ownership Distribution</h2>
                {ownership_chart}
            </div>
        </div>
    </div>

    <footer>
        <p>Crowley Capital — Austin, TX</p>
    </footer>
</body>
</html>
"""

    return html


def main():
    parser = argparse.ArgumentParser(description='Generate metrics dashboard')
    parser.add_argument('--analysis-dir', default='data-room/analysis/',
                        help='Directory containing analysis outputs')
    parser.add_argument('--output', default='data-room/output/metrics-dashboard.html',
                        help='Output dashboard path')

    args = parser.parse_args()

    # Load data
    print(f"Loading analysis from {args.analysis_dir}...")
    data = load_analysis_data(args.analysis_dir)

    # Generate dashboard
    print("Generating dashboard...")
    html = generate_dashboard(data)

    # Write output
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, 'w') as f:
        f.write(html)

    print(f"Dashboard saved to {args.output}")


if __name__ == '__main__':
    main()
