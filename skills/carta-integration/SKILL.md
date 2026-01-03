---
name: carta-integration
description: Carta API integration for real-time cap table data, portfolio holdings, fund performance metrics, and stakeholder information. Use when pulling cap table data from Carta, checking portfolio company ownership, analyzing fund performance (TVPI, DPI, IRR), or syncing investment data. Triggers on "Carta cap table", "portfolio holdings", "fund performance", "ownership data", "409A valuation", "equity data".
---

# Carta Integration Skill

Real-time equity data integration using Carta's Developer Platform APIs for Crowley Capital due diligence workflows.

## API Overview

Carta offers four core APIs:

| API | Purpose | Use Case for VC |
|-----|---------|-----------------|
| **Investor API** | Portfolio company data for institutional investors | Real-time cap table updates, ownership tracking |
| **Issuer API** | Company cap table and securities data | Due diligence on portfolio companies |
| **Portfolio API** | Individual holdings data | LP portfolio views |
| **Launch API** | New company onboarding | Post-investment setup |

## Authentication

### OAuth 2.0 Flows

**Authorization Code Flow** (User-based):
```
1. Redirect user to Carta authorization
2. User grants access
3. Receive authorization code
4. Exchange for access token
```

**Client Credentials Flow** (Service-based):
```python
import requests

def get_access_token(client_id: str, client_secret: str) -> str:
    """Get access token using client credentials."""
    response = requests.post(
        "https://api.carta.com/oauth/token",
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": "read_investor_capitalizationtables read_investor_investments"
        }
    )
    return response.json()["access_token"]
```

### API Base URLs

| Environment | Base URL |
|-------------|----------|
| Playground | `https://api.playground.carta.team/v1alpha1` |
| Production | `https://api.carta.com/v1alpha1` |

## Key Endpoints for VC Diligence

### Investor API

**List Firm Investments:**
```
GET /investors/firms/{firmId}/investments
```
Returns all portfolio company investments for the firm.

**Get Cap Table:**
```
GET /investors/firms/{firmId}/funds/{fundId}/investments/{companyId}/capitalizationTables/{capTableId}
```
Returns cap table at share class and stakeholder level.

**Get Fund Performance:**
```
GET /investors/firms/{firmId}/funds/{fundId}/performance
```
Returns TVPI, DPI, IRR, and other fund metrics.

**List Securities:**
```
GET /investors/firms/{firmId}/funds/{fundId}/investments/{companyId}/securities
```
Returns detailed security information.

### Issuer API

**Get Company Info:**
```
GET /issuers/{issuerId}
```

**Get Stakeholders:**
```
GET /issuers/{issuerId}/stakeholders
```

**Get Securities (Options, RSUs, etc.):**
```
GET /issuers/{issuerId}/optionGrants
GET /issuers/{issuerId}/rsus
GET /issuers/{issuerId}/certificates
```

**Get Valuations:**
```
GET /issuers/{issuerId}/valuations
```
Returns 409A valuations.

**Get Share Classes:**
```
GET /issuers/{issuerId}/shareClasses
```

## OAuth Scopes

### Investor Scopes (For Crowley Capital)
```
read_investor_capitalizationtables  # Cap table views
read_investor_investments           # Portfolio investments
read_investor_funds                 # Fund information
read_investor_fundperformance       # TVPI, DPI, IRR
read_investor_securities            # Security details
read_investor_stakeholdercapitalizationtable  # Stakeholder-level data
```

### Issuer Scopes (For Portfolio Companies)
```
read_issuer_info                    # Company details
read_issuer_securities              # Options, RSUs, certificates
read_issuer_stakeholders            # Stakeholder list
read_issuer_valuations              # 409A valuations
read_issuer_shareclasses            # Share class info
read_issuer_capitalizationtablesummary  # Summary cap table
```

## Data Extraction Functions

```python
import requests
from typing import Dict, List, Any

class CartaClient:
    """Carta API client for VC diligence."""
    
    def __init__(self, access_token: str, base_url: str = "https://api.carta.com/v1alpha1"):
        self.access_token = access_token
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {access_token}"}
    
    def get_firm_investments(self, firm_id: str) -> List[Dict]:
        """Get all portfolio company investments."""
        response = requests.get(
            f"{self.base_url}/investors/firms/{firm_id}/investments",
            headers=self.headers
        )
        return response.json()
    
    def get_cap_table(self, firm_id: str, fund_id: str, company_id: str, cap_table_id: str) -> Dict:
        """Get cap table for a portfolio company."""
        response = requests.get(
            f"{self.base_url}/investors/firms/{firm_id}/funds/{fund_id}/investments/{company_id}/capitalizationTables/{cap_table_id}",
            headers=self.headers
        )
        return response.json()
    
    def get_fund_performance(self, firm_id: str, fund_id: str) -> Dict:
        """Get fund performance metrics."""
        response = requests.get(
            f"{self.base_url}/investors/firms/{firm_id}/funds/{fund_id}/performance",
            headers=self.headers
        )
        return response.json()
    
    def get_valuations(self, issuer_id: str) -> List[Dict]:
        """Get 409A valuations for a company."""
        response = requests.get(
            f"{self.base_url}/issuers/{issuer_id}/valuations",
            headers=self.headers
        )
        return response.json()
```

## Integration with Diligence Workflow

### Cap Table Sync Flow

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Portfolio Co   │────▶│   Carta API     │────▶│  Diligence Tool │
│  (on Carta)     │     │   (Investor)    │     │  (Analysis)     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                │
                                ▼
                    ┌─────────────────────┐
                    │ cap-table-modeling  │
                    │ skill processes     │
                    │ extracted data      │
                    └─────────────────────┘
```

### Automated Data Pull

```python
def pull_portfolio_cap_tables(carta_client: CartaClient, firm_id: str) -> Dict[str, Any]:
    """Pull all portfolio company cap tables."""
    results = {}
    
    # Get all investments
    investments = carta_client.get_firm_investments(firm_id)
    
    for investment in investments:
        company_id = investment["companyId"]
        company_name = investment["companyName"]
        
        # Get cap table if available
        cap_tables = investment.get("capitalizationTables", [])
        if cap_tables:
            cap_table = carta_client.get_cap_table(
                firm_id, 
                investment["fundId"],
                company_id,
                cap_tables[0]["id"]
            )
            results[company_name] = {
                "cap_table": cap_table,
                "type": cap_table.get("type"),  # PRIMARY or PRO_FORMA
                "fully_diluted_shares": cap_table.get("fullyDilutedShares"),
                "stakeholders": cap_table.get("stakeholders", [])
            }
    
    return results
```

## Key Data Points for Diligence

### From Cap Table
- Fully diluted share count
- Ownership percentages by stakeholder
- Share class breakdown
- Option pool size and utilization
- Investor ownership vs founder ownership

### From Fund Performance
- TVPI (Total Value to Paid-In)
- DPI (Distributions to Paid-In)
- IRR (Internal Rate of Return)
- RVPI (Residual Value to Paid-In)

### From Valuations
- Latest 409A valuation
- Fair market value per share
- Valuation date
- Methodology used

## Rate Limits

| Environment | Rate Limit |
|-------------|------------|
| Playground | 100 requests/minute |
| Production | 1000 requests/minute |

## Environment Variables

```bash
# Carta API Credentials
CARTA_CLIENT_ID=your_client_id
CARTA_CLIENT_SECRET=your_client_secret
CARTA_FIRM_ID=your_firm_id

# Environment
CARTA_ENV=playground  # or production
```

## Setup Steps

1. **Register for Developer Portal**
   - Visit https://developers.app.carta.com/user/registration
   - Need invite code from Carta (or join waitlist)

2. **Create Playground App**
   - Set OAuth grant type
   - Select required scopes
   - Configure callback URLs

3. **Get API Credentials**
   - Save `client_id` and `client_secret` securely
   - Never expose in code

4. **Test in Playground**
   - Use playground base URL
   - Test with sample data

5. **Migrate to Production**
   - Contact Carta for production access
   - Update base URL and credentials

## Integration Points

### With cap-table-modeling Skill
- Pull real cap table data from Carta
- Model rounds with actual ownership
- Generate accurate waterfall analysis

### With saas-metrics Skill
- Use funding data for runway calculations
- Track valuation progression

### With risk-framework Skill
- Capitalization risk scoring
- Option pool health check

### With data-room Skill
- Store Carta exports in Egnyte
- Cross-reference with uploaded documents

## References

- `references/api-endpoints.md` — Complete endpoint reference
- `references/data-mapping.md` — Field mapping to diligence outputs
- `scripts/carta_client.py` — Python client implementation
- Carta Docs: https://docs.carta.com/carta/docs

## Contact

Developer Support: developers@carta.com
Partner Inquiries: partners@carta.com
