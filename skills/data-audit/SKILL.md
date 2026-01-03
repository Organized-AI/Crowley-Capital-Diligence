---
name: data-audit
description: Comprehensive data auditing using Pipeboard Meta MCP and Stape MCP tools for portfolio company analysis. Use when conducting performance audits, analyzing ad account data, evaluating tracking infrastructure (Pixel/CAPI/Stape), creating audit reports for portfolio companies, assessing campaign performance, or generating architecture diagrams. Triggers on "audit Meta account", "analyze ad performance", "evaluate tracking setup", "CAPI recommendations", "Stape container", "generate audit report".
---

# Data Audit Skill

Systematic workflow for conducting comprehensive Meta Ads account audits for portfolio company diligence.

## VC Context

When evaluating SaaS companies, Meta Ads efficiency directly impacts:
- **CAC Calculation** — True customer acquisition cost
- **Growth Efficiency** — Burn multiple on paid channels
- **Attribution Accuracy** — iOS 14+ impact without CAPI can hide 30-40% of conversions

## Audit Workflow

### Phase 1: Data Collection

**Step 1: Account Discovery**
```python
# Get all accessible ad accounts
get_ad_accounts(access_token=None, user_id="me", limit=200)

# Select target account and get details
get_account_info(account_id="act_XXXXXXXXX")
```

**Step 2: Campaign Analysis**
```python
# Get campaigns with filters
get_campaigns(
    account_id="act_XXXXXXXXX",
    limit=50,
    status_filter="ACTIVE",
    objective_filter=""
)

# Get detailed campaign data
get_campaign_details(campaign_id="CAMPAIGN_ID")
```

**Step 3: Performance Insights**
```python
# Get insights with breakdowns
get_insights(
    object_id="act_XXXXXXXXX",
    time_range="last_30d",
    breakdown="",
    level="campaign",
    limit=25
)
```

### Phase 2: Analysis

**Key Metrics for VC Diligence:**
- Total spend and budget allocation
- Lead volume and CPL
- Purchase volume and cost per purchase
- CTR ranges
- Conversion events
- Top performers vs. underperformers

**Tracking Infrastructure Assessment:**
- Pixel implementation status
- CAPI deployment
- Event match quality scores
- iOS 14+ impact (30-40% loss without CAPI)

### Phase 3: Recommendations

**Priority HIGH: CAPI Implementation**
- Expected: +30-40% attribution recovery
- Impacts CAC calculation accuracy

**Priority MEDIUM: Revenue Tracking**
- Audit purchase paths
- Standardize value parameters
- Enable value-based bidding

## Tool Reference

### Pipeboard Meta MCP
- `get_ad_accounts`, `get_account_info`
- `get_campaigns`, `get_campaign_details`
- `get_adsets`, `get_adset_details`
- `get_ads`, `get_ad_details`, `get_ad_creatives`
- `get_insights`, `bulk_get_insights`

### Stape MCP
- `stape_container_crud`, `stape_container_power_ups`
- `stape_container_analytics`, `stape_container_statistics`

## References

- `references/audit_template.md` — Audit report template
- `references/capi_checklist.md` — CAPI implementation guide
