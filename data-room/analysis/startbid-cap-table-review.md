# StartBid Cap Table Review & Dilution Analysis

**Date**: 2026-01-03
**Analyst**: Crowley Capital Diligence System
**Status**: COMPLETE (Based on Available Data)

---

## Executive Summary

| Assessment | Rating | Notes |
|------------|--------|-------|
| **Cap Table Clarity** | ⚠️ LIMITED | Cap table not provided; modeled from deal terms |
| **Dilution Path** | ✅ REASONABLE | Standard seed-to-exit dilution trajectory |
| **Founder Alignment** | ⚠️ VALIDATE | Need to confirm founder ownership post-round |
| **Option Pool** | ⚠️ ASSUMPTION | Standard 15% pool assumed |

**Key Action**: Request actual cap table and 409A valuation before closing.

---

## 1. Current Round Structure

### Deal Terms (Stated)

| Parameter | Value |
|-----------|-------|
| Pre-money Valuation | $20,000,000 |
| Investment Amount | $5,000,000 |
| Post-money Valuation | $25,000,000 |
| New Investor Ownership | 20.0% |
| Capital Structure | 50% Equity / 50% Debt |

### Capital Breakdown

| Source | Amount | Notes |
|--------|--------|-------|
| Equity | $2,500,000 | Primary shares |
| Debt | $2,500,000 | LOC/loan facility |
| **Total Raise** | **$5,000,000** | |

⚠️ **Note**: Documents mention $2M to pay off existing LOC. Validate existing debt obligations.

---

## 2. Modeled Cap Table (Pre-Round)

*Based on typical seed-stage structure. VALIDATE WITH ACTUAL DATA.*

### Assumed Pre-Round Ownership

| Shareholder | Shares | % Ownership | Notes |
|-------------|--------|-------------|-------|
| Founder(s) | 6,000,000 | 60.0% | Assumed 2-3 founders |
| Early Team/Advisors | 1,000,000 | 10.0% | Vested options/grants |
| Option Pool (Unallocated) | 1,500,000 | 15.0% | Standard pre-seed pool |
| Prior Investors (F&F/Angels) | 1,500,000 | 15.0% | Assumed prior raise |
| **Total Pre-Round** | **10,000,000** | **100.0%** | |

### Post-Round Ownership (This Round)

| Shareholder | Shares | % Ownership | Change |
|-------------|--------|-------------|--------|
| Founder(s) | 6,000,000 | 48.0% | -12.0% |
| Early Team/Advisors | 1,000,000 | 8.0% | -2.0% |
| Option Pool (Unallocated) | 1,500,000 | 12.0% | -3.0% |
| Prior Investors | 1,500,000 | 12.0% | -3.0% |
| **New Seed Investors** | **2,500,000** | **20.0%** | +20.0% |
| **Total Post-Round** | **12,500,000** | **100.0%** | |

### Share Price Calculation

| Metric | Value |
|--------|-------|
| Post-money Valuation | $25,000,000 |
| Total Shares Outstanding | 12,500,000 |
| **Price Per Share** | **$2.00** |

---

## 3. Dilution Scenario Modeling

### Path to Exit (5-Year Model)

Assuming standard VC financing trajectory:

| Round | Timing | Raise | Pre-$ | Post-$ | New % | Cumulative Dilution |
|-------|--------|-------|-------|--------|-------|---------------------|
| Seed (Current) | 2026 | $5M | $20M | $25M | 20% | 20% |
| Series A | 2027 | $15M | $60M | $75M | 20% | 36% |
| Series B | 2029 | $40M | $200M | $240M | 17% | 47% |
| Exit | 2030 | - | $410M | - | - | - |

### Founder Dilution Path

| Stage | Founder % | Value of Stake | Notes |
|-------|-----------|----------------|-------|
| Pre-Seed | 60.0% | $12M | Starting position |
| Post-Seed | 48.0% | $12M | Flat value, new $ |
| Post-Series A | 38.4% | $23M | Value increase |
| Post-Series B | 31.9% | $64M | Significant appreciation |
| At Exit | 31.9% | **$131M** | At $410M exit |

### Investor Return Analysis (Seed Round)

| Scenario | Exit Value | Seed % | Seed Return | MOIC |
|----------|------------|--------|-------------|------|
| Bear | $260M | 20.0% | $52M | 10.4x |
| Base | $410M | 20.0% | $82M | 16.4x |
| Bull | $515M | 20.0% | $103M | 20.6x |

⚠️ **Note**: Assumes no pro-rata in follow-on rounds. Pro-rata could improve returns.

---

## 4. Option Pool Analysis

### Current Pool Assumption

| Parameter | Value |
|-----------|-------|
| Option Pool Size | 15% (1,500,000 shares) |
| Assumed Allocated | 10% (1,000,000 shares) |
| Available for Grants | 5% (500,000 shares) |

### Pool Adequacy Assessment

| Role | Typical Grant | Shares | Pool Impact |
|------|---------------|--------|-------------|
| VP Engineering | 1.0-2.0% | 125K-250K | -1.5% |
| VP Marketing | 0.75-1.5% | 94K-188K | -1.1% |
| VP Sales | 0.75-1.5% | 94K-188K | -1.1% |
| Senior Engineers (4) | 0.25% each | 125K | -1.0% |
| **Total Key Hires** | **3.75-6.0%** | **438K-751K** | **-4.7%** |

**Finding**:
- ⚠️ 5% available pool may be tight for scaling team
- ✅ Likely will expand pool at Series A (standard)
- Recommend confirming pool size and vesting schedules

### Vesting Schedule (Standard)

| Parameter | Standard |
|-----------|----------|
| Total Vesting | 4 years |
| Cliff | 1 year (25%) |
| Monthly Vesting | Remaining 36 months |
| Acceleration | Single/Double trigger |

---

## 5. Debt Analysis

### Existing Debt Obligations

From documents:
- $2M of raise allocated to "pay off existing LOC and loans"

| Debt Type | Amount | Status | Risk |
|-----------|--------|--------|------|
| Line of Credit | ~$2M | To be retired | LOW (paid at close) |
| Other Loans | TBD | VALIDATE | UNKNOWN |

### New Debt Terms (if venture debt)

| Parameter | Typical Seed Debt | Notes |
|-----------|-------------------|-------|
| Interest Rate | 10-14% | Validate actual terms |
| Term | 24-36 months | |
| Warrants | 10-20% coverage | DILUTIVE |
| Covenants | Minimal at seed | |

⚠️ **Flag**: $2.5M debt component of raise needs term clarification:
- Is this venture debt with warrants?
- What's the interest rate?
- What are repayment terms?

### Debt Service Impact

From CSV data:
| Year | Debt Service | Coverage Ratio |
|------|--------------|----------------|
| Year 1 | $2,900,000 | 9.51x |
| Year 2 | $900,000 | 56.95x |
| Year 3 | $3,175,000 | 27.05x |
| Year 4 | $2,950,000 | 39.62x |
| Year 5 | $0 | N/A |

**Finding**: ✅ Debt service coverage ratios are healthy

---

## 6. Waterfall Analysis

### Liquidation Preference Scenarios

Assuming 1x non-participating preferred:

| Exit Value | Preferred Return | Common Split | Seed Gets | Founders Get |
|------------|------------------|--------------|-----------|--------------|
| $10M | $5M | $5M × 48% | $5.0M | $2.4M |
| $25M | $5M | $20M × 48% | $5.0M | $9.6M |
| $50M | $5M | Convert → 20% | $10.0M | $24.0M |
| $100M | $5M | Convert → 20% | $20.0M | $48.0M |
| $250M | $5M | Convert → 20% | $50.0M | $120.0M |
| $410M | $5M | Convert → 20% | $82.0M | $197.0M |

**Conversion Point**: ~$25M (Preferred converts when value exceeds 1x)

### With Participating Preferred (Validate Terms)

| Exit Value | Preferred Gets | Common Gets | Total Seed | Total Founders |
|------------|----------------|-------------|------------|----------------|
| $25M | $5M + 20% × $20M | 80% × $20M | $9.0M | $7.7M |
| $100M | $5M + 20% × $95M | 80% × $95M | $24.0M | $36.5M |

⚠️ **Recommendation**: Confirm preference structure is 1x non-participating (standard for seed).

---

## 7. Governance & Control

### Assumed Board Composition

| Seat | Holder | Control |
|------|--------|---------|
| Seat 1 | Founder/CEO | Common |
| Seat 2 | Founder/COO | Common |
| Seat 3 | Lead Seed Investor | Preferred |
| Seat 4 | Independent | Mutual consent |
| Seat 5 | Observer (optional) | No vote |

### Protective Provisions (Standard)

Preferred typically has consent rights over:
- [ ] Sale of company
- [ ] New equity issuance (above certain threshold)
- [ ] Debt above threshold
- [ ] Change to preferred rights
- [ ] Change in board size
- [ ] Related party transactions

### Information Rights

| Right | Standard Seed |
|-------|---------------|
| Monthly financials | ✅ |
| Annual audit | ✅ |
| Board materials | ✅ |
| Observer rights | Optional |

---

## 8. Red Flags & Diligence Items

### Must Validate

| Item | Status | Priority | Risk if Not Validated |
|------|--------|----------|----------------------|
| Actual cap table | NOT PROVIDED | **CRITICAL** | Unknown dilution |
| Existing debt terms | PARTIAL | **HIGH** | Hidden obligations |
| Prior investor rights | NOT PROVIDED | **HIGH** | Pro-rata, preferences |
| Founder vesting | NOT PROVIDED | **MEDIUM** | Key man risk |
| Option grants | NOT PROVIDED | **MEDIUM** | Pool depletion |
| 409A valuation | NOT PROVIDED | **MEDIUM** | Tax/accounting issues |

### Potential Issues

1. **$2M LOC paydown** - Ensure clean debt at close
2. **Debt component** - Clarify if $2.5M is venture debt with warrants
3. **Prior raise** - Any convertible notes that convert?
4. **Founder concentration** - Is 60% held by one or multiple founders?

---

## 9. Pro-Forma Cap Table Request

To complete analysis, request:

```
STARTBID CAP TABLE REQUEST

1. Current shareholders (names, shares, %)
2. Option pool (size, allocated, available)
3. Outstanding debt/convertibles
4. 409A valuation date and PPS
5. Prior round terms (if any)
6. Founder vesting schedules
7. Advisor grants and terms
8. Any warrants outstanding
```

---

## 10. Summary Findings

### Dilution Assessment

| Metric | Value | Assessment |
|--------|-------|------------|
| Seed Dilution | 20% | ✅ Standard |
| Expected A Dilution | 20% | ✅ Typical |
| Path to Exit Dilution | ~47% | ✅ Normal trajectory |
| Founder % at Exit | ~32% | ✅ Aligned incentives |

### Investment Considerations

**Positive Factors**:
1. ✅ Standard seed structure
2. ✅ Reasonable dilution path
3. ✅ Strong founder alignment at exit
4. ✅ Healthy debt coverage (if projections hold)

**Concerns**:
1. ⚠️ Cap table not provided
2. ⚠️ Debt structure unclear ($2.5M component)
3. ⚠️ Prior investor terms unknown
4. ⚠️ Option pool status unknown

### Recommendation

**CONDITIONAL PASS** - Structure appears standard pending validation of:
1. Actual cap table documentation
2. Debt terms and covenants
3. Prior investor rights
4. Founder vesting status

---

*Generated by Crowley Capital Diligence System*
*Note: Analysis based on deal terms provided. Actual cap table required for final assessment.*
