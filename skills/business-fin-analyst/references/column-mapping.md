# Standard Column Mappings

## Revenue Columns

| Standard Name | Common Variants |
|---------------|-----------------|
| `revenue` | Revenue, Total Revenue, Net Revenue, Sales |
| `mrr` | MRR, Monthly Recurring Revenue |
| `arr` | ARR, Annual Recurring Revenue |
| `new_mrr` | New MRR, New Revenue, New Sales |
| `expansion_mrr` | Expansion MRR, Upsell, Expansion Revenue |
| `churned_mrr` | Churned MRR, Churn, Lost Revenue |

## Expense Columns

| Standard Name | Common Variants |
|---------------|-----------------|
| `cogs` | COGS, Cost of Goods Sold, Cost of Revenue |
| `opex` | OpEx, Operating Expenses, Total Expenses |
| `sales_marketing` | S&M, Sales & Marketing, Sales and Marketing |
| `research_development` | R&D, Research & Development |
| `general_admin` | G&A, General & Administrative |
| `payroll` | Payroll, Salaries, Wages, Compensation |

## Cash Columns

| Standard Name | Common Variants |
|---------------|-----------------|
| `cash` | Cash, Cash Balance, Bank Balance |
| `burn` | Burn, Net Burn, Monthly Burn, Cash Burn |
| `runway` | Runway, Months Runway |

## Customer Columns

| Standard Name | Common Variants |
|---------------|-----------------|
| `customers` | Customers, Customer Count, Total Customers |
| `new_customers` | New Customers, Acquired, Acquisitions |
| `churned_customers` | Churned, Lost Customers, Churn |
| `arpu` | ARPU, Average Revenue Per User |
| `acv` | ACV, Average Contract Value |

## Date Columns

| Standard Name | Common Variants |
|---------------|-----------------|
| `date` | Date, Month, Period |
| `month` | Month, Month End, Period End |
| `quarter` | Quarter, Q, Qtr |
| `year` | Year, Fiscal Year, FY |

## Normalization Rules

1. Convert to lowercase
2. Replace spaces with underscores
3. Remove special characters
4. Strip leading/trailing whitespace

```python
def normalize_column(col: str) -> str:
    return col.lower().strip().replace(' ', '_').replace('&', 'and')
```
