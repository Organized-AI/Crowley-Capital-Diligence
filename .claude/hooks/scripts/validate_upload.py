#!/usr/bin/env python3
"""
File Upload Validator Hook
Validates and categorizes files uploaded to the data room.

Usage:
    python validate_upload.py <filepath>
"""

import sys
import os
import json
import pandas as pd
from pathlib import Path
from datetime import datetime


def detect_file_type(filepath: str) -> dict:
    """Detect file type and validate structure."""
    path = Path(filepath)
    suffix = path.suffix.lower()

    result = {
        'filename': path.name,
        'filepath': str(path),
        'suffix': suffix,
        'valid': False,
        'category': 'unknown',
        'columns': [],
        'row_count': 0,
        'errors': []
    }

    if suffix not in ['.csv', '.xlsx', '.xls']:
        result['errors'].append(f'Unsupported file type: {suffix}')
        return result

    try:
        if suffix == '.csv':
            df = pd.read_csv(filepath)
        else:
            df = pd.read_excel(filepath)

        result['columns'] = list(df.columns)
        result['row_count'] = len(df)
        result['valid'] = True

    except Exception as e:
        result['errors'].append(f'Failed to parse file: {str(e)}')
        return result

    return result


def categorize_file(result: dict) -> str:
    """Categorize file based on column names."""
    columns_lower = [c.lower() for c in result['columns']]

    # Financial indicators
    financial_keywords = ['revenue', 'expense', 'cost', 'profit', 'margin', 'cogs',
                         'opex', 'ebitda', 'burn', 'cash', 'balance']
    if any(kw in ' '.join(columns_lower) for kw in financial_keywords):
        return 'financials'

    # Cap table indicators
    captable_keywords = ['shares', 'holder', 'shareholder', 'equity', 'ownership',
                        'preferred', 'common', 'options', 'vesting']
    if any(kw in ' '.join(columns_lower) for kw in captable_keywords):
        return 'captable'

    # Customer indicators
    customer_keywords = ['customer', 'client', 'account', 'churn', 'segment',
                        'created_date', 'signup']
    if any(kw in ' '.join(columns_lower) for kw in customer_keywords):
        return 'customers'

    # Revenue/MRR indicators
    revenue_keywords = ['mrr', 'arr', 'subscription', 'monthly', 'recurring']
    if any(kw in ' '.join(columns_lower) for kw in revenue_keywords):
        return 'revenue'

    return 'unknown'


def log_intake(result: dict, category: str, log_path: str):
    """Log file intake to intake-log.md."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    log_entry = f"""
## {timestamp} - {result['filename']}

- **Category**: {category}
- **Rows**: {result['row_count']}
- **Columns**: {', '.join(result['columns'][:5])}{'...' if len(result['columns']) > 5 else ''}
- **Status**: {'Valid' if result['valid'] else 'Invalid'}

"""

    if result['errors']:
        log_entry += f"- **Errors**: {', '.join(result['errors'])}\n"

    # Append to log
    with open(log_path, 'a') as f:
        f.write(log_entry)


def suggest_next_step(category: str) -> str:
    """Suggest next analysis step based on category."""
    suggestions = {
        'financials': 'Run `/diligence analyze --financials` to analyze financial data',
        'captable': 'Run `/diligence captable --model` to parse and model cap table',
        'customers': 'Run `/diligence analyze --customers` to analyze customer data',
        'revenue': 'Run `/diligence analyze --metrics` to calculate SaaS metrics',
        'unknown': 'Review file contents to determine appropriate analysis'
    }
    return suggestions.get(category, suggestions['unknown'])


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_upload.py <filepath>")
        sys.exit(1)

    filepath = sys.argv[1]

    if not os.path.exists(filepath):
        print(json.dumps({'error': f'File not found: {filepath}'}))
        sys.exit(1)

    # Validate and detect
    result = detect_file_type(filepath)

    if result['valid']:
        # Categorize
        category = categorize_file(result)
        result['category'] = category

        # Log intake
        log_path = 'data-room/intake-log.md'
        if os.path.exists(os.path.dirname(log_path)):
            log_intake(result, category, log_path)

        # Suggest next step
        result['next_step'] = suggest_next_step(category)

    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
