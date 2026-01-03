#!/usr/bin/env python3
"""
Data Room Packager
Complete packaging script for final data room export.

Usage:
    python package_dataroom.py --company "Example Corp" --output exports/
"""

import argparse
import json
import os
import shutil
import zipfile
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any


def collect_all_files(base_path: str) -> List[Dict[str, str]]:
    """Collect all files for export."""
    files = []

    # Analysis outputs
    analysis_dir = os.path.join(base_path, 'data-room', 'analysis')
    if os.path.exists(analysis_dir):
        for item in os.listdir(analysis_dir):
            item_path = os.path.join(analysis_dir, item)
            if os.path.isfile(item_path):
                files.append({
                    'source': item_path,
                    'dest': f'01-Analysis/{item}',
                    'category': 'Analysis'
                })

    # Output files (memos, scorecards)
    output_dir = os.path.join(base_path, 'data-room', 'output')
    if os.path.exists(output_dir):
        for item in os.listdir(output_dir):
            item_path = os.path.join(output_dir, item)
            if os.path.isfile(item_path):
                files.append({
                    'source': item_path,
                    'dest': f'02-Reports/{item}',
                    'category': 'Reports'
                })

    # Raw data (optional - for reference)
    raw_dir = os.path.join(base_path, 'data-room', 'raw')
    if os.path.exists(raw_dir):
        for subdir in ['financials', 'customers', 'captable']:
            subdir_path = os.path.join(raw_dir, subdir)
            if os.path.exists(subdir_path):
                for item in os.listdir(subdir_path):
                    item_path = os.path.join(subdir_path, item)
                    if os.path.isfile(item_path):
                        files.append({
                            'source': item_path,
                            'dest': f'03-Source-Data/{subdir}/{item}',
                            'category': 'Source Data'
                        })

    return files


def generate_readme(files: List[Dict], company: str) -> str:
    """Generate README for the data room package."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Group by category
    by_category = {}
    for f in files:
        cat = f['category']
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(f)

    readme = f"""# {company} - Due Diligence Package

**Generated**: {timestamp}
**Prepared by**: Crowley Capital

---

## Package Contents

"""

    for category in ['Analysis', 'Reports', 'Source Data']:
        if category in by_category:
            readme += f"### {category}\n\n"
            for f in sorted(by_category[category], key=lambda x: x['dest']):
                filename = os.path.basename(f['dest'])
                readme += f"- `{filename}`\n"
            readme += "\n"

    readme += """---

## File Descriptions

### Analysis Files
| File | Description |
|------|-------------|
| `metrics.json` | Calculated SaaS metrics (ARR, growth, retention) |
| `cohorts.xlsx` | Customer retention cohort analysis |
| `parsed_captable.json` | Parsed cap table structure |
| `round_model.json` | Investment round modeling |
| `waterfall.xlsx` | Exit waterfall scenarios |
| `flags.md` | Metric threshold violations |

### Report Files
| File | Description |
|------|-------------|
| `risk-scorecard.md` | 11-risks framework assessment |
| `investment-memo.md` | Partner meeting memo |
| `metrics-dashboard.html` | Interactive metrics dashboard |

---

## How to Use This Package

1. **Quick Overview**: Start with `investment-memo.md` for executive summary
2. **Risk Analysis**: Review `risk-scorecard.md` for detailed risk assessment
3. **Interactive View**: Open `metrics-dashboard.html` in a browser
4. **Deep Dive**: Examine individual analysis files for detailed data

---

## Contact

Crowley Capital
Austin, TX

---

*This package was generated automatically by the Crowley Capital Diligence Tool*
"""

    return readme


def create_package(
    base_path: str,
    company: str,
    output_dir: str
) -> Dict[str, Any]:
    """Create complete data room package."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_company = company.lower().replace(' ', '_').replace('.', '')

    # Collect files
    files = collect_all_files(base_path)

    if not files:
        return {
            'success': False,
            'error': 'No files found to package'
        }

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Create package folder
    package_name = f'{safe_company}_diligence_{timestamp}'
    package_folder = os.path.join(output_dir, package_name)
    os.makedirs(package_folder, exist_ok=True)

    # Copy files
    for f in files:
        dest_path = os.path.join(package_folder, f['dest'])
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        shutil.copy2(f['source'], dest_path)

    # Generate and save README
    readme = generate_readme(files, company)
    readme_path = os.path.join(package_folder, 'README.md')
    with open(readme_path, 'w') as f:
        f.write(readme)

    # Create ZIP
    zip_path = f'{package_folder}.zip'
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, filenames in os.walk(package_folder):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                arcname = os.path.relpath(file_path, package_folder)
                zipf.write(file_path, os.path.join(package_name, arcname))

    # Get ZIP size
    zip_size = os.path.getsize(zip_path)

    # Clean up folder (keep only ZIP)
    shutil.rmtree(package_folder)

    return {
        'success': True,
        'company': company,
        'package_name': package_name,
        'zip_path': zip_path,
        'zip_size_bytes': zip_size,
        'zip_size_mb': round(zip_size / 1024 / 1024, 2),
        'file_count': len(files),
        'categories': list(set(f['category'] for f in files)),
        'timestamp': timestamp
    }


def main():
    parser = argparse.ArgumentParser(description='Package data room for export')
    parser.add_argument('--company', default='Target Company', help='Company name')
    parser.add_argument('--output', default='data-room/exports/', help='Output directory')
    parser.add_argument('--base-path', default='.', help='Base project path')

    args = parser.parse_args()

    print(f"\n=== PACKAGING DATA ROOM ===")
    print(f"Company: {args.company}")
    print(f"Output: {args.output}")

    result = create_package(
        base_path=args.base_path,
        company=args.company,
        output_dir=args.output
    )

    if result['success']:
        print(f"\n✅ Package created successfully!")
        print(f"   Name: {result['package_name']}")
        print(f"   Location: {result['zip_path']}")
        print(f"   Size: {result['zip_size_mb']} MB")
        print(f"   Files: {result['file_count']}")
        print(f"   Categories: {', '.join(result['categories'])}")
    else:
        print(f"\n❌ Package failed: {result.get('error', 'Unknown error')}")

    # Output JSON result
    print(f"\n{json.dumps(result, indent=2)}")


if __name__ == '__main__':
    main()
