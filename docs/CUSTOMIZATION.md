# Customization Guide

> Adapt this template for your domain in 4 steps.

The PMM agent is just one instantiation of the Mixture of Experts pattern. This guide shows you how to create your own domain-specific agent.

---

## Overview

Customization involves four areas:

| Area | File(s) | Purpose |
|------|---------|---------|
| **Domain Config** | `config/domains/*.json` | Define domain, experts, tools |
| **Prompts** | `prompts.py` | Encode domain expertise |
| **Tools** | `tools/*.py` | Create domain-specific actions |
| **Frontend** | `App.tsx` | Update quick actions |

---

## Step 1: Create Domain Configuration

Create a new domain config at `config/domains/your-domain.json`:

```json
{
  "domain": "sales-enablement",
  "name": "Sales Enablement Agent",
  "description": "AI agent for sales training and enablement",

  "experts": [
    {
      "id": "training_specialist",
      "name": "Training Specialist",
      "focus": "Sales training content and methodology"
    },
    {
      "id": "content_curator",
      "name": "Content Curator",
      "focus": "Organizing and surfacing sales collateral"
    },
    {
      "id": "performance_analyst",
      "name": "Performance Analyst",
      "focus": "Analyzing sales metrics and identifying gaps"
    },
    {
      "id": "onboarding_coordinator",
      "name": "Onboarding Coordinator",
      "focus": "New rep ramp programs"
    }
  ],

  "tools": {
    "intake": ["analyze_deal", "extract_objections", "identify_stakeholders"],
    "research": ["search_playbooks", "find_case_studies", "analyze_competitors"],
    "planning": ["create_training_plan", "build_battlecard", "design_onboarding"],
    "risk": ["assess_deal_risk", "identify_skill_gaps", "flag_churn_signals"]
  },

  "frameworks": [
    {
      "name": "MEDDIC",
      "applied_when": "Qualifying enterprise deals"
    },
    {
      "name": "Challenger Sale",
      "applied_when": "Teaching reps to lead with insights"
    },
    {
      "name": "SPIN Selling",
      "applied_when": "Discovery and needs analysis"
    }
  ],

  "quick_actions": [
    {
      "label": "Analyze a Deal",
      "message": "Help me analyze this deal and identify risks",
      "icon": "target"
    },
    {
      "label": "Create Training",
      "message": "Create a training module for handling objections",
      "icon": "book"
    },
    {
      "label": "Build Battlecard",
      "message": "Build a competitive battlecard for our main competitor",
      "icon": "shield"
    }
  ]
}
```

---

## Step 2: Create Domain Prompts

### Main System Prompt

Create your domain's main prompt in `prompts.py`. Follow this structure:

```python
YOUR_DOMAIN_SYSTEM_PROMPT = """
# [Domain] Intelligence Agent

You are a [role description]—a deep agent that [core value proposition].

## Your Philosophy

**[Principle 1]**
[Explanation of why this matters]

**[Principle 2]**
[Explanation of why this matters]

**[Principle 3]**
[Explanation of why this matters]

## Your Workflow

### Phase 1: [Intake Phase Name]
Before anything else, understand the full context:
- [Key question 1]
- [Key question 2]
- [Key question 3]

Use `[tool_name]` to [purpose].
Surface unknowns early with clarifying questions.

### Phase 2: [Research Phase Name]
Gather external context:
- [Research area 1]
- [Research area 2]
- [Research area 3]

Use `[tool_name]` and `[tool_name]` to build intelligence.

### Phase 3: [Strategy Phase Name]
Create the strategic foundation:
- [Deliverable 1]
- [Deliverable 2]
- [Deliverable 3]

Get human approval before finalizing strategic documents.

### Phase 4: [Execution Phase Name]
Turn strategy into deliverables:
- [Output 1]
- [Output 2]
- [Output 3]

## Your Outputs

When producing documents, follow these formats:

### [Output Type 1]
```
[Template structure]
```

### [Output Type 2]
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| ... | ... | ... |

## [Domain] Knowledge

### [Framework Category 1]
- **[Framework Name]**: [Brief description]
- **[Framework Name]**: [Brief description]

### [Best Practices Category]
- [Practice 1]
- [Practice 2]
- [Practice 3]

## Anti-Patterns to Avoid

**DON'T**:
- [Common mistake 1]
- [Common mistake 2]
- [Common mistake 3]

**DO**:
- [Best practice 1]
- [Best practice 2]
- [Best practice 3]

## Communication Style

You're a strategic partner, not an order-taker. You:
- Ask probing questions before jumping to solutions
- Challenge assumptions respectfully
- Provide options with trade-offs
- Flag risks early
"""
```

### Expert Prompts

Create specialized prompts for each expert:

```python
TRAINING_SPECIALIST_PROMPT = """
You are a sales training specialist focused on building high-performance sales teams.

## Your Expertise
- Adult learning principles
- Sales methodology training (MEDDIC, Challenger, SPIN)
- Role-play and simulation design
- Knowledge retention techniques

## Your Approach
1. Assess current skill levels
2. Identify specific gaps
3. Design targeted interventions
4. Measure learning outcomes

## Output Format
Always structure training content as:
- Learning objective (what they'll be able to do)
- Key concepts (what they need to know)
- Practice activity (how they'll apply it)
- Assessment (how we'll measure success)
"""

CONTENT_CURATOR_PROMPT = """
You are a sales content curator who ensures reps have the right content at the right time.

## Your Expertise
- Content organization and taxonomy
- Search and discovery optimization
- Content effectiveness measurement
- Sales stage alignment

## Your Approach
1. Understand the selling situation
2. Surface relevant content
3. Provide context for usage
4. Track what works
"""
```

---

## Step 3: Create Domain Tools

### Tool Structure

Create tools in `tools/your_domain.py`:

```python
"""
Sales Enablement Tools.

Domain-specific tools for sales training and enablement workflows.
"""

from langchain_core.tools import tool
from pydantic import BaseModel, Field
from typing import Optional, List


class DealAnalysis(BaseModel):
    """Structured deal analysis output."""
    deal_name: str
    stage: str
    risks: List[str]
    next_actions: List[str]
    confidence_score: float


@tool
def analyze_deal(
    deal_description: str,
    current_stage: Optional[str] = None,
    key_stakeholders: Optional[List[str]] = None,
) -> DealAnalysis:
    """
    Analyze a sales deal using MEDDIC qualification framework.

    Use this when a user wants to understand deal health, identify
    risks, or determine next best actions.

    Args:
        deal_description: Description of the deal and current status
        current_stage: Current sales stage (discovery, demo, negotiation, etc.)
        key_stakeholders: List of known stakeholders

    Returns:
        Structured deal analysis with risks and recommendations
    """
    # Implementation here
    pass


@tool
def create_training_module(
    topic: str,
    target_audience: str,
    duration_minutes: int = 30,
    methodology: Optional[str] = None,
) -> dict:
    """
    Create a sales training module with learning objectives and activities.

    Use this when building new training content or refreshing existing
    training materials.

    Args:
        topic: The skill or knowledge area to train on
        target_audience: Who this training is for (new reps, managers, etc.)
        duration_minutes: Target length of the training
        methodology: Optional sales methodology to incorporate

    Returns:
        Complete training module with objectives, content, and assessments
    """
    # Implementation here
    pass


@tool
def search_playbooks(
    query: str,
    stage: Optional[str] = None,
    persona: Optional[str] = None,
) -> List[dict]:
    """
    Search internal sales playbooks and content library.

    Use this to find relevant sales collateral, talk tracks,
    or competitive materials.

    Args:
        query: What content are you looking for
        stage: Filter by sales stage
        persona: Filter by buyer persona

    Returns:
        List of relevant playbook entries with links
    """
    # Implementation here
    pass


# Export tools for agent
SALES_ENABLEMENT_TOOLS = [
    analyze_deal,
    create_training_module,
    search_playbooks,
]
```

### Tool Design Principles

1. **Clear Purpose**: Each tool does one thing well
2. **Typed Inputs**: Use Pydantic models for complex inputs
3. **Structured Outputs**: Return typed objects, not raw strings
4. **Good Docstrings**: The agent uses these to decide when to call tools
5. **Sensible Defaults**: Make common cases easy

---

## Step 4: Update Frontend

### Quick Actions

Update `apps/web/src/App.tsx` with your domain's quick actions:

```tsx
const QUICK_ACTIONS = [
  {
    label: "Analyze a Deal",
    message: "Help me analyze this deal and identify risks. Here's the context: [paste deal info]",
    icon: "🎯",
  },
  {
    label: "Create Training",
    message: "Create a 30-minute training module on handling pricing objections for new AEs",
    icon: "📚",
  },
  {
    label: "Find Content",
    message: "I need a case study for a healthcare prospect in the evaluation stage",
    icon: "🔍",
  },
  {
    label: "Build Battlecard",
    message: "Create a competitive battlecard comparing us to [competitor name]",
    icon: "⚔️",
  },
];
```

### Branding

Update the header and metadata:

```tsx
// In App.tsx
<header className="header">
  <h1>Sales Enablement Agent</h1>
  <p>AI-powered sales training and content</p>
</header>
```

```html
<!-- In index.html -->
<title>Sales Enablement Agent</title>
<meta name="description" content="AI agent for sales training and enablement" />
```

---

## Example: Converting PMM → Sales Enablement

### Before (PMM)

```python
# prompts.py
MAIN_SYSTEM_PROMPT = """
# Product Marketing Intelligence Agent

You are a veteran Product Marketing Manager's right hand...
"""

# tools/planning.py
@tool
def create_positioning_statement(...):
    """Create a positioning statement using Dunford framework."""
```

### After (Sales Enablement)

```python
# prompts.py
MAIN_SYSTEM_PROMPT = """
# Sales Enablement Intelligence Agent

You are a veteran Sales Enablement leader's right hand...
"""

# tools/training.py
@tool
def create_training_module(...):
    """Create a training module using adult learning principles."""
```

---

## Domain Ideas

This template works for any domain with:
- Clear expertise areas (→ experts)
- Established frameworks (→ encoded knowledge)
- Repeatable workflows (→ phases)
- Specific deliverables (→ tools)

### Example Domains

| Domain | Experts | Key Frameworks |
|--------|---------|----------------|
| **Sales Enablement** | Training, Content, Performance | MEDDIC, Challenger, SPIN |
| **Customer Success** | Onboarding, Health, Expansion | Outcomes-based, Health scoring |
| **Content Marketing** | Strategy, SEO, Distribution | Content pillars, AIDA |
| **HR/People Ops** | Recruiting, Onboarding, Performance | Competency models, OKRs |
| **Legal Ops** | Contract, Compliance, IP | Matter management, Risk assessment |
| **Finance** | FP&A, Treasury, Reporting | DCF, Scenario planning |

---

## Testing Your Customization

### 1. Local Testing

```bash
# Run the agent locally
cd apps/agent
python -m uvicorn pmm_agent.server:app --reload

# Test a tool directly
python -c "from pmm_agent.tools.your_domain import your_tool; print(your_tool('test'))"
```

### 2. Prompt Testing

Test your prompts with different scenarios:

```python
# test_prompts.py
scenarios = [
    "Basic request in domain",
    "Edge case requiring clarification",
    "Request outside domain scope",
    "Complex multi-step workflow",
]

for scenario in scenarios:
    response = agent.invoke({"message": scenario})
    print(f"Scenario: {scenario}")
    print(f"Response: {response}")
    print("---")
```

### 3. Tool Testing

Verify tools work correctly:

```python
# test_tools.py
from pmm_agent.tools.your_domain import TOOLS

for tool in TOOLS:
    print(f"Tool: {tool.name}")
    print(f"Description: {tool.description}")
    print(f"Schema: {tool.args_schema.schema()}")
    print("---")
```

---

## Common Customization Patterns

### Adding Data Sources

Connect to internal APIs or databases:

```python
@tool
def search_internal_wiki(query: str) -> List[dict]:
    """Search internal documentation."""
    # Connect to Notion, Confluence, etc.
    response = notion_client.search(query)
    return format_results(response)
```

### Adding External Intelligence

Integrate external data sources:

```python
@tool
def get_company_info(company_name: str) -> dict:
    """Get company information from external sources."""
    # Use Clearbit, LinkedIn, etc.
    data = clearbit.company(company_name)
    return format_company_data(data)
```

### Adding Human-in-the-Loop

For sensitive operations:

```python
@tool
def create_contract_draft(terms: dict) -> dict:
    """Create a contract draft for human review."""
    draft = generate_draft(terms)
    return {
        "draft": draft,
        "status": "PENDING_REVIEW",
        "message": "Please review this draft before sending to the customer.",
    }
```

---

## Need Help?

- **Discord**: Get help from the community
- **Office Hours**: Pro/Team tiers get direct access
- **Course**: Deep dive in the cohort course (starts 1/27)

---

[Back to README](../README.md) | [Deployment Guide](DEPLOYMENT.md) | [Methodology](METHODOLOGY.md)
