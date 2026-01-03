# Carta API Endpoints Reference

## Base URLs

| Environment | URL |
|-------------|-----|
| **Playground** | `https://api.playground.carta.team` |
| **Production** | `https://api.carta.com` |

---

## Investor API (For VC Firms)

### Firms

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1alpha1/investors/firms` | GET | List all firms |
| `/v1alpha1/investors/firms/{firmId}` | GET | Get firm details |

### Funds

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1alpha1/investors/firms/{firmId}/funds` | GET | List funds in firm |
| `/v1alpha1/investors/firms/{firmId}/funds/{fundId}` | GET | Get fund details |
| `/v1alpha1/investors/firms/{firmId}/funds/{fundId}/performance` | GET | Get fund performance (TVPI, DPI, IRR) |
| `/v1alpha1/investors/firms/{firmId}/funds/{fundId}/cashBalances` | GET | Get fund cash balances |

### Investments

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1alpha1/investors/firms/{firmId}/investments` | GET | List all investments |
| `/v1alpha1/investors/firms/{firmId}/funds/{fundId}/investments` | GET | List fund investments |
| `/v1alpha1/investors/firms/{firmId}/funds/{fundId}/investments/{companyId}` | GET | Get investment details |

### Cap Tables

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1alpha1/investors/firms/{firmId}/funds/{fundId}/investments/{companyId}/capitalizationTables` | GET | List cap tables |
| `/v1alpha1/investors/firms/{firmId}/funds/{fundId}/investments/{companyId}/capitalizationTables/{capTableId}` | GET | Get cap table details |

### Securities

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1alpha1/investors/firms/{firmId}/funds/{fundId}/investments/{companyId}/securities` | GET | List securities |

---

## Issuer API (For Portfolio Companies)

### Company Info

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1alpha1/issuers/{issuerId}` | GET | Get company details |
| `/v1alpha1/issuers/{issuerId}/shareClasses` | GET | List share classes |

### Stakeholders

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1alpha1/issuers/{issuerId}/stakeholders` | GET | List all stakeholders |
| `/v1alpha1/issuers/{issuerId}/stakeholders/{stakeholderId}` | GET | Get stakeholder details |

### Securities

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1alpha1/issuers/{issuerId}/optionGrants` | GET | List option grants |
| `/v1alpha1/issuers/{issuerId}/optionGrants/{optionGrantId}` | GET | Get option grant details |
| `/v1alpha1/issuers/{issuerId}/rsus` | GET | List RSUs |
| `/v1alpha1/issuers/{issuerId}/rsas` | GET | List RSAs |
| `/v1alpha1/issuers/{issuerId}/certificates` | GET | List stock certificates |

### Valuations

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1alpha1/issuers/{issuerId}/valuations` | GET | List 409A valuations |
| `/v1alpha1/issuers/{issuerId}/valuations/{valuationId}` | GET | Get valuation details |

### Cap Table Summary

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1alpha1/issuers/{issuerId}/capitalizationTableSummary` | GET | Get summary cap table |
| `/v1alpha1/issuers/{issuerId}/stakeholderCapitalizationTable` | GET | Get stakeholder-level cap table |

---

## Portfolio API (For Individual Holdings)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1alpha1/portfolios/{portfolioId}` | GET | Get portfolio info |
| `/v1alpha1/portfolios/{portfolioId}/securities` | GET | List portfolio securities |
| `/v1alpha1/portfolios/{portfolioId}/issuers/{issuerId}/securityTransactions` | GET | List security transactions |
| `/v1alpha1/portfolios/{portfolioId}/issuers/{issuerId}/valuations` | GET | List issuer valuations |

---

## Launch API (For Onboarding)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1alpha1/draftIssuers` | POST | Create draft issuer |
| `/v1alpha1/draftIssuers/{draftIssuerId}` | GET | Get draft issuer |
| `/v1alpha1/draftIssuers/{draftIssuerId}` | PATCH | Update draft issuer |

---

## Response Data Fields (Key)

### Cap Table Response
```json
{
  "id": "string",
  "type": "PRIMARY | PRO_FORMA",
  "fullyDilutedShares": 10000000,
  "issuedShares": 8000000,
  "stakeholders": [
    {
      "id": "string",
      "name": "string",
      "category": "FOUNDER | INVESTOR | EMPLOYEE",
      "fullyDilutedShares": 2500000,
      "ownershipPercentage": 25.0
    }
  ],
  "shareClasses": [
    {
      "id": "string",
      "name": "Series A Preferred",
      "fullyDilutedShares": 3000000
    }
  ]
}
```

### Fund Performance Response
```json
{
  "fundId": "string",
  "asOfDate": "2025-01-01",
  "tvpi": 2.5,
  "dpi": 0.8,
  "rvpi": 1.7,
  "netIrr": 0.25,
  "totalContributions": 50000000,
  "totalDistributions": 40000000,
  "nav": 85000000
}
```

### Valuation Response
```json
{
  "id": "string",
  "issuerId": "string",
  "valuationDate": "2024-12-01",
  "fairMarketValuePerShare": 1.50,
  "commonStockPrice": 1.50,
  "preferredStockPrice": 2.25,
  "methodology": "409A",
  "status": "FINAL"
}
```

---

## Rate Limits

| Environment | Limit |
|-------------|-------|
| Playground | 100 requests/minute |
| Production | 1000 requests/minute |

---

## Error Codes

| Code | Meaning |
|------|---------|
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Invalid/expired token |
| 403 | Forbidden - Insufficient scope or permissions |
| 404 | Not Found - Resource doesn't exist |
| 429 | Too Many Requests - Rate limited |
| 500 | Internal Server Error |

### Common 403 Reasons
- `INSUFFICIENT_SCOPE` - App doesn't have required scope
- `MISSING_INTERNAL_PERMISSION` - User role changed, no longer has access
