#!/usr/bin/env python3
"""
Diligence Report Generator
Compiles analysis files into professional PDF with Mermaid visualizations.

Usage: python generate_report.py --company "Company Name" --data-room ./data-room --output report.pdf
"""

import json
import os
import argparse
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    PageBreak, KeepTogether, Flowable
)
from reportlab.pdfgen import canvas

# Crowley Capital Brand Colors
CROWLEY_NAVY = HexColor('#1a365d')
CROWLEY_GOLD = HexColor('#d69e2e')
CROWLEY_LIGHT = HexColor('#f7fafc')
CROWLEY_GREEN = HexColor('#38a169')
CROWLEY_RED = HexColor('#e53e3e')
CROWLEY_GRAY = HexColor('#718096')


class DiligenceReport:
    """Generate comprehensive diligence PDF report."""
    
    def __init__(self, company_name: str, data_room_path: str):
        self.company_name = company_name
        self.data_room = Path(data_room_path)
        self.styles = self._create_styles()
        self.data = self._load_data()
        self.charts = {}
    
    def _create_styles(self) -> Dict[str, ParagraphStyle]:
        """Create custom paragraph styles."""
        base = getSampleStyleSheet()
        
        styles = {
            'title': ParagraphStyle(
                'CustomTitle',
                parent=base['Title'],
                fontSize=28,
                textColor=CROWLEY_NAVY,
                spaceAfter=30,
                alignment=TA_CENTER
            ),
            'subtitle': ParagraphStyle(
                'CustomSubtitle',
                parent=base['Normal'],
                fontSize=14,
                textColor=CROWLEY_GRAY,
                alignment=TA_CENTER,
                spaceAfter=20
            ),
            'heading1': ParagraphStyle(
                'CustomH1',
                parent=base['Heading1'],
                fontSize=18,
                textColor=CROWLEY_NAVY,
                spaceBefore=20,
                spaceAfter=12,
                borderColor=CROWLEY_GOLD,
                borderWidth=2,
                borderPadding=5
            ),
            'heading2': ParagraphStyle(
                'CustomH2',
                parent=base['Heading2'],
                fontSize=14,
                textColor=CROWLEY_NAVY,
                spaceBefore=15,
                spaceAfter=8
            ),
            'body': ParagraphStyle(
                'CustomBody',
                parent=base['Normal'],
                fontSize=10,
                textColor=black,
                spaceAfter=8,
                leading=14
            ),
            'metric_value': ParagraphStyle(
                'MetricValue',
                parent=base['Normal'],
                fontSize=24,
                textColor=CROWLEY_NAVY,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            ),
            'metric_label': ParagraphStyle(
                'MetricLabel',
                parent=base['Normal'],
                fontSize=9,
                textColor=CROWLEY_GRAY,
                alignment=TA_CENTER
            ),
            'footer': ParagraphStyle(
                'Footer',
                parent=base['Normal'],
                fontSize=8,
                textColor=CROWLEY_GRAY,
                alignment=TA_CENTER
            )
        }
        return styles
    
    def _load_data(self) -> Dict[str, Any]:
        """Load all analysis data from data room."""
        data = {
            'metrics': {},
            'cap_table': {},
            'risks': {},
            'flags': [],
            'memo': ''
        }
        
        # Load metrics
        metrics_path = self.data_room / 'analysis' / 'metrics.json'
        if metrics_path.exists():
            with open(metrics_path) as f:
                data['metrics'] = json.load(f)
        
        # Load cap table
        captable_path = self.data_room / 'analysis' / 'parsed_captable.json'
        if captable_path.exists():
            with open(captable_path) as f:
                data['cap_table'] = json.load(f)
        
        # Load risk scorecard
        risk_path = self.data_room / 'output' / 'risk-scorecard.md'
        if risk_path.exists():
            data['risks'] = self._parse_risk_scorecard(risk_path)
        
        # Load flags
        flags_path = self.data_room / 'analysis' / 'flags.md'
        if flags_path.exists():
            with open(flags_path) as f:
                data['flags'] = f.read()
        
        # Load investment memo
        memo_path = self.data_room / 'output' / 'investment-memo.md'
        if memo_path.exists():
            with open(memo_path) as f:
                data['memo'] = f.read()
        
        return data
    
    def _parse_risk_scorecard(self, path: Path) -> Dict[str, Any]:
        """Parse risk scorecard markdown into structured data."""
        risks = {'scores': {}, 'composite': 0, 'level': 'UNKNOWN'}
        
        with open(path) as f:
            content = f.read()
        
        # Parse risk scores (simplified - expand as needed)
        risk_categories = [
            'Market', 'Product', 'Team', 'Financial', 'Competition',
            'Timing', 'Regulatory', 'Customer', 'Technology', 'Legal', 'Execution'
        ]
        
        for category in risk_categories:
            # Look for score patterns
            import re
            pattern = rf'{category}[^\d]*(\d+(?:\.\d+)?)/10'
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                risks['scores'][category] = float(match.group(1))
        
        # Calculate composite
        if risks['scores']:
            risks['composite'] = sum(risks['scores'].values()) / len(risks['scores'])
            if risks['composite'] >= 8:
                risks['level'] = 'LOW'
            elif risks['composite'] >= 6:
                risks['level'] = 'MODERATE'
            else:
                risks['level'] = 'HIGH'
        
        return risks
    
    def _generate_mermaid_chart(self, mermaid_code: str, filename: str) -> Optional[str]:
        """Generate chart image from Mermaid code using CLI."""
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False) as f:
                f.write(mermaid_code)
                mmd_path = f.name
            
            output_path = tempfile.mktemp(suffix='.png')
            
            # Try mmdc (mermaid-cli) if available
            result = subprocess.run(
                ['mmdc', '-i', mmd_path, '-o', output_path, '-b', 'transparent'],
                capture_output=True,
                timeout=30
            )
            
            if result.returncode == 0 and os.path.exists(output_path):
                return output_path
            
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        return None
    
    def _create_metric_box(self, value: str, label: str, status: str = 'neutral') -> Table:
        """Create a metric display box."""
        color_map = {
            'good': CROWLEY_GREEN,
            'bad': CROWLEY_RED,
            'neutral': CROWLEY_NAVY
        }
        
        data = [
            [Paragraph(value, self.styles['metric_value'])],
            [Paragraph(label, self.styles['metric_label'])]
        ]
        
        table = Table(data, colWidths=[1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), CROWLEY_LIGHT),
            ('BOX', (0, 0), (-1, -1), 2, color_map.get(status, CROWLEY_NAVY)),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        return table
    
    def _create_risk_bar(self, category: str, score: float) -> List:
        """Create a risk score bar visualization."""
        filled = int(score)
        empty = 10 - filled
        
        bar = '█' * filled + '░' * empty
        status = '🟢' if score >= 7 else ('🟡' if score >= 5 else '🔴')
        
        return [category, bar, f'{score:.1f}/10', status]
    
    def _build_cover_page(self) -> List:
        """Build cover page elements."""
        elements = []
        
        elements.append(Spacer(1, 2*inch))
        elements.append(Paragraph(self.company_name, self.styles['title']))
        elements.append(Paragraph('Due Diligence Report', self.styles['subtitle']))
        elements.append(Spacer(1, 0.5*inch))
        elements.append(Paragraph(
            f'Prepared by Crowley Capital',
            self.styles['subtitle']
        ))
        elements.append(Paragraph(
            datetime.now().strftime('%B %Y'),
            self.styles['subtitle']
        ))
        elements.append(Spacer(1, 2*inch))
        elements.append(Paragraph(
            'CONFIDENTIAL - FOR INTERNAL USE ONLY',
            self.styles['footer']
        ))
        elements.append(PageBreak())
        
        return elements
    
    def _build_executive_summary(self) -> List:
        """Build executive summary section."""
        elements = []
        
        elements.append(Paragraph('Executive Summary', self.styles['heading1']))
        
        # Key metrics row
        metrics = self.data.get('metrics', {})
        
        metric_boxes = []
        if 'arr' in metrics:
            metric_boxes.append(self._create_metric_box(
                f"${metrics['arr']/1000000:.1f}M",
                'ARR',
                'good' if metrics['arr'] > 1000000 else 'neutral'
            ))
        if 'growth_rate' in metrics:
            metric_boxes.append(self._create_metric_box(
                f"{metrics['growth_rate']*100:.0f}%",
                'YoY Growth',
                'good' if metrics['growth_rate'] > 1 else 'neutral'
            ))
        if 'burn_rate' in metrics:
            metric_boxes.append(self._create_metric_box(
                f"${metrics['burn_rate']/1000:.0f}K",
                'Monthly Burn',
                'good' if metrics['burn_rate'] < 200000 else 'bad'
            ))
        if 'runway_months' in metrics:
            metric_boxes.append(self._create_metric_box(
                f"{metrics['runway_months']:.0f} mo",
                'Runway',
                'good' if metrics['runway_months'] > 12 else 'bad'
            ))
        
        if metric_boxes:
            metrics_table = Table([metric_boxes], colWidths=[1.7*inch] * len(metric_boxes))
            metrics_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            elements.append(metrics_table)
            elements.append(Spacer(1, 0.3*inch))
        
        # Risk summary
        risks = self.data.get('risks', {})
        if risks.get('composite'):
            elements.append(Paragraph(
                f"<b>Risk Score:</b> {risks['composite']:.1f}/10 ({risks['level']} RISK)",
                self.styles['body']
            ))
        
        elements.append(Spacer(1, 0.2*inch))
        elements.append(PageBreak())
        
        return elements
    
    def _build_metrics_section(self) -> List:
        """Build detailed metrics section."""
        elements = []
        
        elements.append(Paragraph('Financial Metrics', self.styles['heading1']))
        
        metrics = self.data.get('metrics', {})
        
        # Unit economics table
        unit_econ_data = [
            ['Metric', 'Value', 'Benchmark', 'Status'],
        ]
        
        if 'ltv' in metrics:
            status = '🟢' if metrics['ltv'] > 30000 else '🟡'
            unit_econ_data.append(['LTV', f"${metrics['ltv']:,.0f}", '$30,000', status])
        
        if 'cac' in metrics:
            status = '🟢' if metrics['cac'] < 15000 else '🔴'
            unit_econ_data.append(['CAC', f"${metrics['cac']:,.0f}", '$15,000', status])
        
        if 'ltv' in metrics and 'cac' in metrics and metrics['cac'] > 0:
            ltv_cac = metrics['ltv'] / metrics['cac']
            status = '🟢' if ltv_cac > 3 else '🔴'
            unit_econ_data.append(['LTV:CAC', f"{ltv_cac:.2f}x", '3.0x', status])
        
        if 'nrr' in metrics:
            status = '🟢' if metrics['nrr'] > 110 else '🟡'
            unit_econ_data.append(['Net Retention', f"{metrics['nrr']:.0f}%", '110%', status])
        
        if 'gross_margin' in metrics:
            status = '🟢' if metrics['gross_margin'] > 70 else '🟡'
            unit_econ_data.append(['Gross Margin', f"{metrics['gross_margin']:.0f}%", '70%', status])
        
        if len(unit_econ_data) > 1:
            unit_table = Table(unit_econ_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 0.8*inch])
            unit_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), CROWLEY_NAVY),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 0.5, CROWLEY_GRAY),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, CROWLEY_LIGHT]),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            elements.append(unit_table)
        
        elements.append(Spacer(1, 0.3*inch))
        elements.append(PageBreak())
        
        return elements
    
    def _build_risk_section(self) -> List:
        """Build risk assessment section."""
        elements = []
        
        elements.append(Paragraph('Risk Assessment', self.styles['heading1']))
        elements.append(Paragraph(
            'Based on Tunguz 11-Risks Framework',
            self.styles['body']
        ))
        elements.append(Spacer(1, 0.2*inch))
        
        risks = self.data.get('risks', {})
        scores = risks.get('scores', {})
        
        if scores:
            risk_data = [['Category', 'Score Bar', 'Score', 'Status']]
            
            for category, score in sorted(scores.items(), key=lambda x: -x[1]):
                risk_data.append(self._create_risk_bar(category, score))
            
            risk_table = Table(risk_data, colWidths=[1.5*inch, 3*inch, 0.8*inch, 0.6*inch])
            risk_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), CROWLEY_NAVY),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (1, 1), (1, -1), 'Courier'),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (2, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 0.5, CROWLEY_GRAY),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, CROWLEY_LIGHT]),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            elements.append(risk_table)
            
            elements.append(Spacer(1, 0.3*inch))
            
            # Composite score
            composite = risks.get('composite', 0)
            level = risks.get('level', 'UNKNOWN')
            elements.append(Paragraph(
                f"<b>Composite Risk Score: {composite:.1f}/10</b> — {level} RISK",
                self.styles['heading2']
            ))
        
        elements.append(PageBreak())
        
        return elements
    
    def _build_cap_table_section(self) -> List:
        """Build cap table section."""
        elements = []
        
        elements.append(Paragraph('Capitalization Summary', self.styles['heading1']))
        
        cap_table = self.data.get('cap_table', {})
        
        if cap_table.get('stakeholders'):
            # Ownership table
            ownership_data = [['Stakeholder', 'Shares', 'Ownership %', 'Type']]
            
            for sh in cap_table['stakeholders'][:10]:  # Top 10
                ownership_data.append([
                    sh.get('name', 'Unknown'),
                    f"{sh.get('shares', 0):,}",
                    f"{sh.get('ownership_pct', 0):.1f}%",
                    sh.get('type', 'Common')
                ])
            
            ownership_table = Table(ownership_data, colWidths=[2.5*inch, 1.5*inch, 1.2*inch, 1.2*inch])
            ownership_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), CROWLEY_NAVY),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('GRID', (0, 0), (-1, -1), 0.5, CROWLEY_GRAY),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, CROWLEY_LIGHT]),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            elements.append(ownership_table)
        
        # Summary stats
        if cap_table.get('summary'):
            summary = cap_table['summary']
            elements.append(Spacer(1, 0.2*inch))
            elements.append(Paragraph(
                f"<b>Fully Diluted Shares:</b> {summary.get('fully_diluted', 0):,}",
                self.styles['body']
            ))
            elements.append(Paragraph(
                f"<b>Option Pool:</b> {summary.get('option_pool_pct', 0):.1f}% ({summary.get('option_pool_available', 0):,} available)",
                self.styles['body']
            ))
        
        elements.append(PageBreak())
        
        return elements
    
    def generate(self, output_path: str, format: str = 'executive'):
        """Generate the complete PDF report."""
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        story = []
        
        # Cover page
        story.extend(self._build_cover_page())
        
        # Executive summary
        story.extend(self._build_executive_summary())
        
        # Metrics section
        story.extend(self._build_metrics_section())
        
        # Cap table section
        story.extend(self._build_cap_table_section())
        
        # Risk assessment
        story.extend(self._build_risk_section())
        
        # Footer with page numbers
        def add_page_number(canvas, doc):
            canvas.saveState()
            canvas.setFont('Helvetica', 8)
            canvas.setFillColor(CROWLEY_GRAY)
            page_num = canvas.getPageNumber()
            text = f"Crowley Capital | {self.company_name} | Page {page_num}"
            canvas.drawCentredString(letter[0]/2, 0.5*inch, text)
            canvas.restoreState()
        
        # Build PDF
        doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
        
        return output_path


def main():
    parser = argparse.ArgumentParser(description='Generate Diligence Report PDF')
    parser.add_argument('--company', required=True, help='Company name')
    parser.add_argument('--data-room', required=True, help='Path to data room directory')
    parser.add_argument('--output', required=True, help='Output PDF path')
    parser.add_argument('--format', choices=['executive', 'detailed', 'ic'], 
                       default='executive', help='Report format')
    
    args = parser.parse_args()
    
    report = DiligenceReport(args.company, args.data_room)
    output = report.generate(args.output, args.format)
    
    print(f"Report generated: {output}")


if __name__ == '__main__':
    main()
