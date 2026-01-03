# Investor Matcher Skill

AI-powered startup-investor matching using hybrid scoring algorithm.

## Overview

This skill matches startups/founders with appropriate investors from the Phalanx database using a 40/40/20 hybrid scoring algorithm combining semantic similarity, rule-based matching, and stage alignment.

## Algorithm

```
┌─────────────────────────────────────────────────────────────────┐
│                    HYBRID MATCHING ENGINE                        │
├─────────────────────────────────────────────────────────────────┤
│  SEMANTIC (40%)     RULE-BASED (40%)      STAGE (20%)           │
│  ───────────────    ────────────────      ───────────           │
│  • pgvector cosine  • Industry (37.5%)    • Exact match (1.0)   │
│  • OpenAI ada-002   • Check size (37.5%)  • Adjacent (0.5)      │
│  • 1536-dim vectors • Geography (12.5%)   • Mismatch (0.0)      │
│                     • Completeness (12.5%)                       │
└─────────────────────────────────────────────────────────────────┘
```

## Data Sources

### Investor Database
- **Location**: `data-room/raw/investors/phalanx-investors.csv`
- **Fields**:
  - Investor name, Website, Global HQ
  - Countries of investment
  - Stage of investment (1-6 scale)
  - Investment thesis
  - Investor type
  - First cheque minimum/maximum

### Stage Mapping

| CSV Stage | Normalized Stage |
|-----------|------------------|
| 1. Idea or Patent | Pre-Seed |
| 2. Prototype | Pre-Seed |
| 3. Early Revenue | Seed |
| 4. Scaling | Series A |
| 5. Growth | Series B+ |
| 6. Pre-IPO | Series B+ |

## Usage

### Match a Startup to Investors

```typescript
import { scoreMatchCandidates, rankMatches } from './src/matching';

// Score all investor candidates
const candidates = scoreMatchCandidates(startupProfile, investors);

// Get top matches
const topMatches = rankMatches(candidates, 0.5, 10); // minScore, limit
```

### Score Breakdown Example

```json
{
  "total_score": 0.78,
  "quality_tier": "Good",
  "semantic": {
    "score": 0.85,
    "weight": 0.40,
    "contribution": 0.34,
    "reasoning": "Strong alignment in investment thesis"
  },
  "rule": {
    "score": 0.75,
    "weight": 0.40,
    "contribution": 0.30,
    "breakdown": {
      "industry_match": { "score": 1.0, "reasoning": "Exact: Fintech" },
      "check_size": { "score": 0.8, "reasoning": "80% overlap" },
      "geography": { "score": 1.0, "reasoning": "Match: USA" },
      "completeness": { "score": 0.5, "reasoning": "50% complete" }
    }
  },
  "stage": {
    "score": 0.70,
    "weight": 0.20,
    "contribution": 0.14,
    "reasoning": "Adjacent stage: Seed ↔ Series A"
  }
}
```

## Quality Tiers

| Tier | Score Range | Description |
|------|-------------|-------------|
| Excellent | 0.90+ | Exceptional fit across all dimensions |
| Good | 0.75-0.89 | Strong match with minor gaps |
| Fair | 0.50-0.74 | Moderate fit, worth exploring |
| Poor | <0.50 | Weak match, low priority |

## Integration with Diligence

### Workflow

1. **Input**: Startup profile from data room
2. **Extraction**: Parse financials, industry, stage, geography
3. **Matching**: Run hybrid algorithm against investor database
4. **Output**: Ranked investor recommendations with reasoning

### Commands

```bash
# Find matching investors for a startup
/diligence investors match <startup-file>

# Filter by geography
/diligence investors match <startup-file> --geo USA

# Filter by stage
/diligence investors match <startup-file> --stage Seed
```

## Source Files

| File | Purpose |
|------|---------|
| `src/types.ts` | Type definitions, constants |
| `src/matching.ts` | Hybrid scoring algorithm |
| `src/embeddings.ts` | OpenAI embedding pipeline |
| `src/supabase.ts` | Database operations |
| `references/SCORING-RUBRIC.md` | Detailed scoring documentation |

## Dependencies

- OpenAI API (ada-002 embeddings)
- Supabase + pgvector (optional, for persistence)

## Origin

Ported from [phalanx-matcher](../../../phalanx-matcher) project.
