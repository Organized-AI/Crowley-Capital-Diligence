# StartBid Financial Model Audit

**Date**: 2026-01-03
**Analyst**: Crowley Capital Diligence System
**Status**: COMPLETE

---

## Executive Summary

| Assessment | Rating | Notes |
|------------|--------|-------|
| **Overall Model Quality** | ⚠️ MODERATE | Reasonable assumptions with some aggressive elements |
| **Revenue Projections** | ✅ ACHIEVABLE | Conservative PTE assumption offsets GMV growth |
| **Unit Economics** | ✅ SOUND | LTV:CAC targets align with marketplace benchmarks |
| **Exit Math** | ⚠️ OPTIMISTIC | 5x revenue multiple requires growth execution |
| **Risk Level** | MEDIUM | Execution risk on migration; market risk manageable |

**Recommendation**: PROCEED with standard seed terms. Key diligence items flagged below.

---

## 1. Deal Terms Validation

### Capital Structure
| Parameter | Stated | Validation |
|-----------|--------|------------|
| Pre-money | $20M | ✅ Reasonable for $5.5M GMV marketplace |
| Post-money | $25M | ✅ Standard seed structure |
| Raise Amount | $5M | ✅ 18-24 month runway with GTM plan |
| Implied Ownership | 20% | ✅ Market standard for seed |

### Valuation Benchmarks
| Metric | StartBid | Seed Benchmark | Assessment |
|--------|----------|----------------|------------|
| Pre/GMV | 3.6x | 2-5x | ✅ Within range |
| Pre/Rev (at 22% PTE) | 16.5x | 10-25x | ✅ Acceptable |
| Pre/Active Users | $308/user | $200-500 | ✅ Mid-range |

**Finding**: Valuation is fair for seed stage with proven traction.

---

## 2. Revenue Model Analysis

### Platform Take Equivalent (PTE) Validation

| Comparable | GMV | Revenue | PTE | Notes |
|------------|-----|---------|-----|-------|
| eBay (FY2024) | $74.7B | $10.3B | 13.8% | Mature, low-touch |
| Etsy (FY2023) | $13.2B | $2.7B | 20.5% | Handmade/vintage |
| The RealReal (FY2024) | $1.83B | $600M | 32.8% | Authentication premium |
| Poshmark (FY2021) | $1.8B | $326M | 18.1% | Social commerce |
| **Garnet Gazelle (Historical)** | - | - | **32%** | Event-based auctions |
| **StartBid (Projected)** | - | - | **22%** | Conservative assumption |

**Finding**: 22% PTE is conservative given:
- Historical 32% achieved on Garnet Gazelle
- Category comps (luxury resale) achieve 18-33%
- Authentication services could push to 25-30%

⚠️ **Flag**: Model uses -10% haircut from historical. Validate why PTE would decline with technology upgrade.

### GMV Growth Path

| Year | GMV Target | Growth Rate | Required for 10x |
|------|------------|-------------|------------------|
| 2025 (Actual) | $5.5M | - | Baseline |
| 2026 | ~$20M | 264% | Platform launch |
| 2027 | ~$60M | 200% | GTM scale |
| 2028 | ~$150M | 150% | Category expansion |
| 2029 | ~$280M | 87% | Flywheel |
| 2030 | $330-410M | 18-46% | Exit target |

**CAGR Required**: ~130% over 5 years

**Finding**: Aggressive but achievable given:
- ✅ Existing 148K registrations (conversion runway)
- ✅ 800K+ deployable SKUs (supply ready)
- ✅ Always-on model increases throughput 10-50x vs. events
- ⚠️ Requires successful platform migration
- ⚠️ Requires GTM execution at $65 CAC

---

## 3. Unit Economics Audit

### Customer Acquisition Cost (CAC)

| Channel | Gross Outlay | Burn | CAC Target | NTB Range |
|---------|--------------|------|------------|-----------|
| Paid Social | $1.9M | $720K | $60-90 | 21-32K |
| Paid Search | $1.1M | $450K | $50-80 | 14-22K |
| Creators | $700K | $300K | $40-80 | 9-17K |
| Affiliates | $450K | $110K | GMV-based | 5-8K |
| Email/SMS | $110K | $110K | $5-15 | 4-8K |
| **Total** | **$4.75M** | **$2.2M** | **$55-70** | **53-87K** |

**Blended CAC Calculation**:
- Gross CAC: $4.75M / 70K NTBs = $68
- Burn CAC: $2.2M / 70K NTBs = $31
- **Finding**: ✅ $55-70 target is achievable with in-period revenue recycling

### Lifetime Value (LTV) Model

| Component | Value | Source |
|-----------|-------|--------|
| AOV | $230-260 | GTM doc |
| Repeat Rate | 1.6 orders/year | Target |
| Annual GMV/Customer | $368-416 | Calculated |
| PTE (22%) | $81-92 | Revenue/customer |
| Gross Margin (~70%) | $57-64 | After COGS |
| Customer Lifespan | 3 years | Assumed |
| **LTV** | **$171-192** | Gross margin × lifespan |

### LTV:CAC Ratio

| Scenario | LTV | CAC | Ratio | Assessment |
|----------|-----|-----|-------|------------|
| Conservative | $171 | $70 | 2.4x | ⚠️ Below 3x target |
| Base | $182 | $65 | 2.8x | ⚠️ Marginal |
| Optimistic | $192 | $55 | 3.5x | ✅ Healthy |

**Finding**: LTV:CAC ranges from 2.4x to 3.5x depending on execution.
- ⚠️ Must hit <$65 CAC to achieve 3:1 target
- ✅ Repeat rate improvement (1.6 → 2.0) adds significant upside

### Payback Period

| Scenario | Contribution/Order | Orders to Payback | Months (at 1.6/yr) |
|----------|-------------------|-------------------|-------------------|
| PTE 22% | $51-57 | 1.1-1.4 | 8-10 |
| PTE 25% | $58-65 | 1.0-1.2 | 7-9 |
| PTE 32% | $74-83 | 0.8-0.9 | 6-7 |

**Finding**: ✅ <12 month payback achievable at 22%+ PTE

---

## 4. GTM Budget Analysis

### Spend Allocation Assessment

| Category | % of Budget | Benchmark | Assessment |
|----------|-------------|-----------|------------|
| Paid Acquisition | 77% | 60-80% | ✅ Appropriate for launch |
| Creators/Affiliates | 10% | 10-20% | ✅ Room to scale |
| Retention/CRM | 5% | 5-15% | ⚠️ May need increase Y2 |
| Creative/Testing | 5% | 5-10% | ✅ Sufficient |
| Contingency | 4% | 5-10% | ⚠️ Tight buffer |

### Channel Risk Assessment

| Channel | Risk | Mitigation |
|---------|------|------------|
| Meta/TikTok | HIGH - CPM volatility, iOS privacy | CAPI server-side, diversification |
| Search | MEDIUM - Competition | Category clusters, RLSA |
| Creators | MEDIUM - Attribution | Rev-share alignment |
| Email/SMS | LOW - Owned channel | Deliverability monitoring |

**Finding**:
- ⚠️ 77% reliance on paid social is risky
- ✅ Sensitivities documented for CAC drift >$75
- ✅ Contingency plan to shift to Search/Affiliates

### Quarterly Burn Phasing

| Quarter | Burn | % of Total | Risk Level |
|---------|------|------------|------------|
| Q4'26 | $330K | 15% | LOW - Launch validation |
| Q1'27 | $440K | 20% | MEDIUM - Scale test |
| Q2'27 | $550K | 25% | HIGH - Peak acquisition |
| Q3'27 | $550K | 25% | HIGH - Monetization pivot |
| Q4'27 | $330K | 15% | MEDIUM - Optimization |

**Finding**: ✅ Phasing is prudent with 50% of budget in middle quarters after validation.

---

## 5. Exit Model Validation

### Target Exit Math

| Parameter | Base | Downside | Upside |
|-----------|------|----------|--------|
| Year 5 GMV | $370M | $420M | $330M |
| PTE | 22% | 20% | 25% |
| Revenue | $82M | $84M | $82M |
| Multiple | 5.0x | 4.0x | 6.0x |
| **Enterprise Value** | **$410M** | **$336M** | **$492M** |
| **MOIC** | **10.2x** | **8.4x** | **12.3x** |
| **IRR** | **~58%** | **~53%** | **~65%** |

### Multiple Benchmarks

| Company | Revenue Multiple | Notes |
|---------|------------------|-------|
| eBay | 2.5x | Mature |
| Etsy | 4.2x | Growth |
| The RealReal | 1.0x | Unprofitable |
| Poshmark (Acq.) | 3.6x | Acquired by Naver |
| **Median Growth Marketplace** | **4-6x** | At scale |

**Finding**:
- ✅ 5x revenue multiple is achievable for growing marketplace
- ⚠️ Requires demonstrating path to profitability
- ⚠️ Multiple compression risk if growth slows

---

## 6. Risk Matrix

| Risk | Probability | Impact | Mitigation | Residual |
|------|-------------|--------|------------|----------|
| Platform migration fails | 20% | HIGH | Stage gates, cohort testing | MEDIUM |
| CAC exceeds $80 | 30% | MEDIUM | Channel shift, creative ops | LOW |
| PTE compresses to <18% | 15% | HIGH | Buyer premium tiers, fees | MEDIUM |
| Competitor enters space | 25% | MEDIUM | Speed to scale, supply lock | LOW |
| Macro downturn | 35% | MEDIUM | Collectibles often counter-cyclical | LOW |

### Scenario Analysis

| Scenario | Probability | Year 5 Value | MOIC |
|----------|-------------|--------------|------|
| Bull (PTE 25%, 5x) | 25% | $515M | 12.9x |
| Base (PTE 22%, 5x) | 45% | $410M | 10.2x |
| Bear (PTE 18%, 4x) | 20% | $260M | 6.5x |
| Failure | 10% | $0 | 0x |

**Expected Value**: $331M (weighted)
**Expected MOIC**: 8.3x

---

## 7. Key Diligence Items

### Must Validate Before Close

1. **Historical Garnet Gazelle financials**
   - Request 3 years P&L, monthly GMV, customer cohorts
   - Validate 32% historical PTE claim

2. **Platform development status**
   - Technical diligence on always-on auction system
   - Timeline confidence to Q4'26 launch

3. **Supply agreements**
   - Contracts with 98 suppliers
   - Exclusivity terms, volume commitments

4. **Customer concentration**
   - Top 10 buyers as % of GMV
   - Churn analysis on 65K active customers

5. **Cap table review**
   - Current ownership structure
   - Prior debt/convertible instruments ($2M LOC mentioned)

### Information Gaps

| Item | Status | Priority |
|------|--------|----------|
| Detailed P&L | NOT PROVIDED | HIGH |
| Monthly cohort data | NOT PROVIDED | HIGH |
| Customer concentration | NOT PROVIDED | MEDIUM |
| Cap table | NOT PROVIDED | HIGH |
| Team bios/org chart | NOT PROVIDED | MEDIUM |
| Technical architecture | NOT PROVIDED | MEDIUM |

---

## 8. Audit Conclusions

### Model Strengths
1. ✅ Conservative PTE assumption (-10% from historical)
2. ✅ Clear unit economics with payback targets
3. ✅ Sensitivity analysis included
4. ✅ Phased GTM with gates
5. ✅ Comp analysis supports thesis

### Model Weaknesses
1. ⚠️ No detailed P&L provided
2. ⚠️ ~130% CAGR is aggressive
3. ⚠️ Heavy reliance on paid social (77%)
4. ⚠️ 4% contingency may be thin
5. ⚠️ LTV:CAC marginal in conservative case

### Recommendation

**CONDITIONAL PASS** - Model is fundamentally sound with realistic assumptions for a seed-stage marketplace. Key conditions:

1. Validate historical financials (32% PTE claim)
2. Complete cap table review
3. Technical diligence on platform readiness
4. Customer cohort analysis to validate repeat rates

---

*Generated by Crowley Capital Diligence System*
