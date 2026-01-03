# Metrics Definitions

## Unit Economics

### LTV (Lifetime Value)
```
LTV = (ARPU × Gross Margin) / Monthly Churn Rate
```
DCF-adjusted version includes discount rate.

### CAC (Customer Acquisition Cost)
```
CAC = (Sales + Marketing Spend) / New Customers Acquired
```
Fully-loaded includes all S&M headcount.

### LTV:CAC Ratio
```
LTV:CAC = LTV / CAC
```
Target: > 3.0x

### CAC Payback
```
CAC Payback (months) = CAC / (ARPU × Gross Margin)
```
Target: < 18 months

## Retention

### Gross Churn
```
Gross Churn = Churned MRR / Starting MRR
```
Target: < 2% monthly

### Net Revenue Retention (NRR)
```
NRR = (Starting MRR + Expansion - Churn) / Starting MRR
```
Target: > 110%

### Quick Ratio
```
Quick Ratio = (New MRR + Expansion) / (Churn + Contraction)
```
Target: > 4

## Efficiency

### Burn Multiple
```
Burn Multiple = Net Burn / Net New ARR
```
Target: < 1.5x

### Gross Margin
```
Gross Margin = (Revenue - COGS) / Revenue
```
Target: > 70% for SaaS

## Thresholds

| Metric | Good | Watch | Risk |
|--------|------|-------|------|
| LTV:CAC | >3.0 | 2.0-3.0 | <2.0 |
| Gross Churn | <2% | 2-5% | >5% |
| NRR | >110% | 100-110% | <100% |
| Burn Multiple | <1.5 | 1.5-2.5 | >2.5 |
| Runway | >18mo | 12-18mo | <12mo |
| Gross Margin | >70% | 60-70% | <60% |
