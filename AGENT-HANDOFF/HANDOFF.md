# Agent Handoff Document

## Project: Crowley Capital Diligence Tool

### Quick Context

Internal VC due diligence automation system for Crowley Capital. Uses Claude Code with subagents, skills, and hooks to transform startup data into professional data room packages.

### Key Files to Read

1. `CLAUDE.md` — Project overview and quick start
2. `ARCHITECTURE/system-design.md` — Technical architecture
3. `skills/*/SKILL.md` — Individual skill documentation
4. `QUICK-REFERENCE.md` — Commands and metrics cheat sheet

### Current State

| Component | Status |
|-----------|--------|
| Skills (10) | ✅ Defined |
| Subagents (5) | ✅ Designed |
| Hooks (4) | ✅ Designed |
| Phase Prompts | ✅ Ready |
| Core Scripts | ⏳ Phase 1 |
| Full Integration | ⏳ Phase 2-4 |

### Skills Implemented

| Skill | Purpose | Status |
|-------|---------|--------|
| saas-metrics | LTV, CAC, NRR, churn | ✅ SKILL.md + scripts |
| cap-table-modeling | Dilution, waterfalls | ✅ SKILL.md |
| risk-framework | 11-risks scoring | ✅ SKILL.md |
| data-room-templates | Memos, dashboards | ✅ SKILL.md |
| austin-market | Regional context | ✅ SKILL.md |
| data-audit | Meta Ads analysis | ✅ SKILL.md |
| data-room | Egnyte integration | ✅ SKILL.md + references |
| contract-review | Legal document review | ✅ SKILL.md + references |
| business-fin-analyst | P&L, burn, financials | ✅ SKILL.md + scripts |
| phased-planning | Implementation planning | ✅ SKILL.md |

### MCP Integrations

| MCP | Purpose | Status |
|-----|---------|--------|
| Egnyte | Data room access | Ready to connect |
| Pipeboard Meta | Ad account auditing | Ready to connect |
| Stape | CAPI assessment | Ready to connect |

### Next Steps

1. **Run Phase 0** — Foundation setup (verify structure)
2. **Run Phase 1** — Implement core Python scripts
3. **Run Phase 2** — Subagent orchestration
4. **Run Phase 3** — Risk assessment engine
5. **Run Phase 4** — Polish and testing

### How to Continue

```bash
# Navigate to project
cd "/Users/supabowl/Library/Mobile Documents/com~apple~CloudDocs/BHT Promo iCloud/Organized AI/Windsurf/Crowley Capital Diligence"

# Open phase prompt and run
claude --dangerously-skip-permissions
# Paste contents of PLANNING/phase-X.md
```

### Key Decisions Made

1. **Native Claude Code** over MCP servers — More maintainable
2. **Tunguz 11-Risks** framework — Industry standard
3. **Austin Market** focus — Crowley Capital's territory
4. **Egnyte Integration** — Secure data room access
5. **Contract Review** — Legal diligence automation
6. **Business Financial Analyst** — CSV/Excel processing
7. **Phased Planning** — Structured implementation
8. **Phased Implementation** — Testable increments

### Dependencies

```
pandas>=2.0.0
numpy>=1.24.0
openpyxl>=3.1.0
plotly>=5.14.0
tabulate>=0.9.0
```

### Contact

Project Owner: Jordaaan
Partner: Jake Crowley (Crowley Capital)
