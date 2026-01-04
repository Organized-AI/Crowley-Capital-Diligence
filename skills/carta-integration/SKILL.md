---
name: carta-integration
description: Integrates with Carta API for real-time cap table data, portfolio holdings, fund performance (TVPI/DPI/IRR), and 409A valuations. Use when pulling cap tables from Carta, checking ownership data, analyzing fund performance, or syncing investment data. Triggers on "Carta cap table", "portfolio holdings", "fund performance", "409A valuation", "equity data from Carta".
---

# Carta Integration Skill

Real-time equity data from Carta Developer Platform for VC diligence.

## Quick Start

```python
from scripts.carta_client import CartaClient

client = CartaClient(access_token, firm_id=CARTA_FIRM_ID)

# Get all portfolio investments
investments = client.get_firm_investments()

# Get cap table for specific company
cap_table = client.get_cap_table(fund_id, company_id, cap_table_id)

# Get fund performance
performance = client.get_fund_performance(fund_id)
```

## Key Endpoints

| Endpoint | Returns |
|----------|---------|
| `GET /investors/firms/{firmId}/investments` | All portfolio companies |
| `GET /.../capitalizationTables/{id}` | Cap table by stakeholder |
| `GET /.../funds/{fundId}/performance` | TVPI, DPI, IRR |
| `GET /issuers/{id}/valuations` | 409A valuations |

## Data Extracted

**Cap Table:**
- Fully diluted share count
- Ownership % by stakeholder
- Share class breakdown
- Option pool utilization

**Fund Performance:**
- TVPI, DPI, RVPI
- IRR
- Investment value

**Valuations:**
- 409A FMV per share
- Valuation date

## Authentication

OAuth 2.0 with scopes:
```
read_investor_capitalizationtables
read_investor_investments
read_investor_fundperformance
read_issuer_valuations
```

## Environment

```bash
CARTA_CLIENT_ID=your_client_id
CARTA_CLIENT_SECRET=your_client_secret
CARTA_FIRM_ID=your_firm_id
CARTA_ENV=playground  # or production
```

| Env | Base URL | Rate Limit |
|-----|----------|------------|
| Playground | `api.playground.carta.team/v1alpha1` | 100/min |
| Production | `api.carta.com/v1alpha1` | 1000/min |

## Integration

| Skill | Data Flow |
|-------|-----------|
| cap-table-modeling | Real cap table → model rounds |
| risk-framework | Capitalization scoring |
| diligence-report | Ownership charts |

## References

- [references/api-endpoints.md](references/api-endpoints.md) — Full endpoint reference
- [scripts/carta_client.py](scripts/carta_client.py) — Python client
- Carta Docs: https://docs.carta.com/carta/docs
