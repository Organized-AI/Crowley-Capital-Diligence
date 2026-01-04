---
name: data-room
description: Accesses investor data rooms via Egnyte MCP for VC due diligence. Searches documents, extracts content, and queries knowledge bases. Use when reviewing deal documents, searching for financials/contracts/cap tables, or analyzing uploaded files. Triggers on "data room", "Egnyte", "find documents", "search deal folder", "due diligence documents".
---

# Data Room Skill (Egnyte MCP)

Secure document access for Crowley Capital due diligence.

## MCP Server

```
https://mcp-server.egnyte.com/mcp
```

Requires: Egnyte Essential/Elite/Ultimate (Gen 4) or Platform Enterprise with Co-Pilot

## Core Operations

### Search

```python
# Basic search
search(query="financials 2024", folder_path="/Due Diligence/TechCorp")

# Advanced with filters
advanced_search(
    query="revenue",
    folder_path="/Due Diligence/TechCorp",
    file_types=["pdf", "xlsx"],
    date_range="2024-01-01:2024-12-31"
)
```

### Document Analysis

```python
# Ask questions
ask_document(file_id="FILE_ID", question="What are the termination conditions?")

# Get summary
summarize_document(file_id="FILE_ID")

# Fetch full content
fetch_document(file_id="FILE_ID")
```

### Copilot Queries

```python
ask_copilot(
    question="What is the revenue growth trend?",
    context_path="/Due Diligence/TechCorp/Financials"
)
```

## Diligence Workflows

### Financial Review
1. `advanced_search(query="P&L income statement", folder_path=".../Financials")`
2. `ask_document(file_id, "What is the total revenue?")`
3. `summarize_document(file_id)`

### Contract Review
1. `search(query="contract agreement", folder_path=".../Legal")`
2. `ask_document(file_id, "What are the payment terms?")`
3. `ask_document(file_id, "What is the liability cap?")`

### Cap Table Review
1. `search(query="cap table", folder_path="...")`
2. `ask_document(file_id, "What is the ownership breakdown?")`
3. `ask_document(file_id, "What are the liquidation preferences?")`

## Folder Structure

```
/Due Diligence/[Company]/
├── Financials/     # P&L, Balance Sheet, Projections
├── Legal/          # Contracts, IP, Corporate docs
├── Cap Table/      # Ownership, option pool
├── Customers/      # CRM export, references
├── Product/        # Roadmap, architecture
└── Team/           # Org chart, bios
```

## Tips

- Include folder paths: `search(folder_path="/Due Diligence/TechCorp/Legal")`
- Use file type filters: `file_types=["pdf", "xlsx"]`
- Ask specific questions: "What are the payment terms?" not "Tell me about the contract"

## Security

- All access respects Egnyte permissions
- Audit logs maintained by Egnyte
- Only accessible files are visible

## References

- [references/folder-templates.md](references/folder-templates.md) — Standard structures
- [references/extraction-prompts.md](references/extraction-prompts.md) — Question templates
