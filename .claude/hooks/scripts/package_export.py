#!/usr/bin/env python3
"""
Data Room Export Packager Hook
Packages all analysis outputs into a timestamped ZIP archive.

Usage:
    python package_export.py [--output-dir <path>]
"""

import sys
import os
import json
import shutil
import zipfile
from datetime import datetime
from pathlib import Path
from typing import List, Dict


def collect_files(base_path: str) -> List[Dict[str, str]]:
    """Collect all files to include in export."""
    files = []

    # Analysis outputs
    analysis_dir = os.path.join(base_path, 'data-room', 'analysis')
    if os.path.exists(analysis_dir):
        for item in os.listdir(analysis_dir):
            item_path = os.path.join(analysis_dir, item)
            if os.path.isfile(item_path):
                files.append({
                    'source': item_path,
                    'dest': f'analysis/{item}',
                    'category': 'analysis'
                })

    # Output files (memos, scorecards)
    output_dir = os.path.join(base_path, 'data-room', 'output')
    if os.path.exists(output_dir):
        for item in os.listdir(output_dir):
            item_path = os.path.join(output_dir, item)
            if os.path.isfile(item_path):
                files.append({
                    'source': item_path,
                    'dest': f'output/{item}',
                    'category': 'output'
                })

    return files


def generate_toc(files: List[Dict[str, str]]) -> str:
    """Generate table of contents markdown."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    toc = f"""# Crowley Capital Diligence Package

**Generated**: {timestamp}

## Contents

"""

    # Group by category
    by_category = {}
    for f in files:
        cat = f['category']
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(f)

    for category, cat_files in sorted(by_category.items()):
        toc += f"### {category.title()}\n\n"
        for f in sorted(cat_files, key=lambda x: x['dest']):
            toc += f"- [{os.path.basename(f['dest'])}]({f['dest']})\n"
        toc += "\n"

    toc += """---

## File Descriptions

### Analysis Files
- `metrics.json` — Calculated SaaS metrics
- `cohorts.xlsx` — Retention cohort matrices
- `parsed_captable.json` — Parsed cap table data
- `round_model.json` — Investment round modeling
- `waterfall.xlsx` — Exit waterfall scenarios
- `financial-summary.json` — Financial analysis

### Output Files
- `risk-scorecard.md` — 11-risks assessment
- `investment-memo.md` — Partner meeting memo
- `key-questions.md` — Founder discussion guide
- `metrics-dashboard.html` — Interactive metrics dashboard

---
*Crowley Capital — Austin, TX*
"""

    return toc


def create_export(base_path: str, output_dir: str = None) -> Dict[str, str]:
    """Create export package."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Determine output directory
    if output_dir is None:
        output_dir = os.path.join(base_path, 'data-room', 'exports')

    os.makedirs(output_dir, exist_ok=True)

    # Collect files
    files = collect_files(base_path)

    if not files:
        return {
            'success': False,
            'error': 'No files found to export'
        }

    # Create export folder
    export_name = f'diligence_export_{timestamp}'
    export_folder = os.path.join(output_dir, export_name)
    os.makedirs(export_folder, exist_ok=True)

    # Copy files
    for f in files:
        dest_path = os.path.join(export_folder, f['dest'])
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        shutil.copy2(f['source'], dest_path)

    # Generate and save TOC
    toc = generate_toc(files)
    toc_path = os.path.join(export_folder, 'README.md')
    with open(toc_path, 'w') as f:
        f.write(toc)

    # Create ZIP
    zip_path = f'{export_folder}.zip'
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, filenames in os.walk(export_folder):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                arcname = os.path.relpath(file_path, export_folder)
                zipf.write(file_path, arcname)

    # Clean up folder (keep only ZIP)
    shutil.rmtree(export_folder)

    return {
        'success': True,
        'export_name': export_name,
        'zip_path': zip_path,
        'file_count': len(files),
        'timestamp': timestamp
    }


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Package data room export')
    parser.add_argument('--output-dir', help='Output directory for export')
    parser.add_argument('--base-path', default='.', help='Base project path')

    args = parser.parse_args()

    result = create_export(args.base_path, args.output_dir)

    if result['success']:
        print(f"\n=== EXPORT COMPLETE ===")
        print(f"Package: {result['export_name']}")
        print(f"Location: {result['zip_path']}")
        print(f"Files: {result['file_count']}")
    else:
        print(f"\nExport failed: {result.get('error', 'Unknown error')}")

    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
