---
name: data-room
description: Secure data room management using Egnyte MCP for VC due diligence. Use when accessing investor data rooms, searching for deal documents, analyzing uploaded financials, reviewing contracts, conducting due diligence document review, querying knowledge bases, or managing portfolio company documents. Triggers on "data room", "Egnyte", "find documents", "search deal folder", "contract review", "due diligence documents", "knowledge base query".
---

# Data Room Skill

Secure data room management using Egnyte Remote MCP Server for Crowley Capital due diligence workflows.

## Connection Setup

### Egnyte MCP Server URL
```
https://mcp-server.egnyte.com/mcp
```

### Prerequisites
- Egnyte Essential, Elite, or Ultimate plan (Gen 4)
- OR Platform Enterprise with Co-Pilot add-on (Gen 3)
- OAuth 2.0 authentication

## Core Capabilities

### 1. Search & Discovery

**Basic Search:**
```python
# Search for files by keyword
search(query="financials 2024", folder_path="/Due Diligence/TechCorp")
```

**Advanced Search with Filters:**
```python
# Advanced search with metadata, date, file type
advanced_search(
    query="revenue",
    folder_path="/Due Diligence/TechCorp",
    file_types=["pdf", "xlsx"],
    date_range="2024-01-01:2024-12-31",
    metadata_filters={"deal_stage": "Series A"}
)
```

### 2. Document Analysis

**Ask Questions About Documents:**
```python
# Query specific document content
ask_document(
    file_id="FILE_ID",
    question="What are the termination conditions?"
)
```

**Generate Summaries:**
```python
# AI-powered document summary
summarize_document(file_id="FILE_ID")
```

**Fetch Full Content:**
```python
# Get complete document content
fetch_document(file_id="FILE_ID")
```

### 3. Copilot Integration

**Query with Context:**
```python
# Ask questions across multiple documents
ask_copilot(
    question="What is the revenue growth trend?",
    context_path="/Due Diligence/TechCorp/Financials"
)
```

### 4. Knowledge Base Queries

**Query Curated Collections:**
```python
# Search knowledge bases
query_knowledge_base(
    kb_id="KNOWLEDGE_BASE_ID",
    query="cap table structure"
)
```

## VC Due Diligence Workflows

### Contract Review

1. **Locate Contracts:**
   ```
   advanced_search(
       query="contract agreement",
       folder_path="/Due Diligence/[COMPANY]/Legal",
       file_types=["pdf"]
   )
   ```

2. **Extract Key Terms:**
   ```
   ask_document(file_id, "What are the payment terms?")
   ask_document(file_id, "What is the liability cap?")
   ask_document(file_id, "What are the termination conditions?")
   ```

3. **Compare Across Documents:**
   Use Copilot to identify common terms and variations.

### Financial Due Diligence

1. **Find Financial Documents:**
   ```
   advanced_search(
       query="P&L income statement",
       folder_path="/Due Diligence/[COMPANY]/Financials",
       date_range="2023-01-01:2024-12-31"
   )
   ```

2. **Extract Key Metrics:**
   ```
   ask_document(file_id, "What is the total revenue?")
   ask_document(file_id, "What is the gross margin?")
   ask_document(file_id, "What are the major expense categories?")
   ```

3. **Generate Summary:**
   ```
   summarize_document(file_id)
   ```

### Cap Table Analysis

1. **Locate Cap Table:**
   ```
   search(query="cap table", folder_path="/Due Diligence/[COMPANY]")
   ```

2. **Extract Ownership Details:**
   ```
   ask_document(file_id, "What is the current ownership breakdown?")
   ask_document(file_id, "What is the option pool size?")
   ask_document(file_id, "Are there any liquidation preferences?")
   ```

### Customer Reference Materials

1. **Find Customer Data:**
   ```
   advanced_search(
       query="customer list CRM",
       folder_path="/Due Diligence/[COMPANY]/Customers"
   )
   ```

2. **Analyze Concentration:**
   ```
   ask_document(file_id, "Who are the top 10 customers by revenue?")
   ask_document(file_id, "What percentage of revenue comes from the largest customer?")
   ```

## Folder Structure Best Practices

Recommended data room organization for deals:

```
/Due Diligence/
└── [Company Name]/
    ├── Financials/
    │   ├── P&L/
    │   ├── Balance Sheet/
    │   ├── Cash Flow/
    │   └── Projections/
    ├── Legal/
    │   ├── Contracts/
    │   ├── IP/
    │   └── Corporate/
    ├── Cap Table/
    ├── Customers/
    │   ├── CRM Export/
    │   └── References/
    ├── Product/
    │   ├── Roadmap/
    │   └── Tech Architecture/
    ├── Team/
    │   ├── Org Chart/
    │   └── Key Bios/
    └── Diligence Notes/
```

## Security & Permissions

- All access respects Egnyte permissions
- Claude can only access files user has permission to view
- Governed by organizational policies
- Audit logs maintained by Egnyte

## Tips for Effective Use

1. **Be Specific:** Include folder paths and date ranges
   - ❌ "Find the contract"
   - ✅ "Search for PDF contracts in /Legal/Vendor from 2024"

2. **Use Natural Language:** ask_document understands conversational queries
   - "What are the payment terms?"
   - "Summarize the main risks"

3. **Leverage Knowledge Bases:** For frequently accessed policies

4. **Use Filters:** Narrow results with metadata, dates, file types

## Integration with Other Skills

### With saas-metrics:
1. Fetch financial documents from data room
2. Parse into metrics calculation
3. Generate analysis

### With risk-framework:
1. Extract evidence from documents
2. Score each risk category
3. Generate scorecard with citations

### With data-room-templates:
1. Pull data from Egnyte documents
2. Populate memo templates
3. Generate final deliverables

## References

- `references/folder-templates.md` — Standard folder structures
- `references/search-patterns.md` — Common search queries
- `references/extraction-prompts.md` — Document question templates
