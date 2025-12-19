"""
Planning Tools - Positioning, Messaging, and Launch Planning.

These tools create strategic deliverables for PMM work.
"""

from langchain_core.tools import tool
from typing import Optional


@tool
def create_positioning_statement(
    target_customer: str,
    problem: str,
    product_name: str,
    category: str,
    key_benefit: str,
    competitive_alternative: str,
    differentiator: str,
) -> str:
    """
    Create a positioning statement using the classic framework.

    This is a HUMAN-APPROVAL-REQUIRED tool. The positioning statement
    will be presented for review before being finalized.

    Args:
        target_customer: Who the product is for
        problem: The problem or need they have
        product_name: Name of the product
        category: Product category
        key_benefit: Primary reason to buy
        competitive_alternative: What they'd use instead
        differentiator: What makes this unique

    Returns:
        Formatted positioning statement with variations
    """
    return f"""
## Positioning Statement

### Classic Format

For **{target_customer}**
Who **{problem}**
**{product_name}** is a **{category}**
That **{key_benefit}**
Unlike **{competitive_alternative}**
Our product **{differentiator}**

---

### One-Liner Version
"{product_name}: {key_benefit} for {target_customer}"

### Elevator Pitch (30 seconds)
"{product_name} helps {target_customer} {key_benefit}. Unlike {competitive_alternative}, we {differentiator}. Companies like [example customers] use us to [specific outcome]."

### Internal Alignment Version
"We win when {target_customer} chooses us over {competitive_alternative} because {differentiator}. Our key proof point is [evidence]."

---

### Validation Checklist
- [ ] Would target customer self-identify?
- [ ] Is the category understood?
- [ ] Is the benefit compelling?
- [ ] Is the differentiator defensible?
- [ ] Can we prove the claims?

### Next Steps
1. Test with 5 target customers
2. Create messaging hierarchy from positioning
3. Develop proof points for each claim
4. Align sales and marketing on language

---
**REQUIRES HUMAN APPROVAL BEFORE FINALIZING**
"""


@tool
def create_messaging_matrix(
    positioning: str,
    audience_segments: str,
    value_propositions: str,
) -> str:
    """
    Create a messaging matrix mapping audiences to messages.

    This is a HUMAN-APPROVAL-REQUIRED tool.

    Args:
        positioning: The approved positioning statement
        audience_segments: Different audience segments to message
        value_propositions: Key value props to include

    Returns:
        Comprehensive messaging matrix
    """
    return f"""
## Messaging Matrix

### Based on Positioning
{positioning}

---

### Primary Message Hierarchy

**Headline (5 words or less)**
[Compelling headline here]

**Subhead (One sentence)**
[Supporting statement that adds context]

**Body (2-3 sentences)**
[Expansion of value with proof point]

---

### Segment-Specific Messaging

| Segment | Pain Point | Value Prop | Proof Point | CTA |
|---------|------------|------------|-------------|-----|
| {audience_segments.split(',')[0] if ',' in audience_segments else 'Segment 1'} | [Their pain] | [Our value] | [Evidence] | [Action] |
| Segment 2 | [Their pain] | [Our value] | [Evidence] | [Action] |
| Segment 3 | [Their pain] | [Our value] | [Evidence] | [Action] |

---

### Message by Funnel Stage

**Awareness (What is this?)**
- Headline: [Attention-grabbing]
- Focus: Problem recognition

**Consideration (Why this?)**
- Headline: [Differentiation-focused]
- Focus: Competitive comparison

**Decision (Why now?)**
- Headline: [Urgency-creating]
- Focus: Risk reduction, proof

---

### Proof Points Library

| Claim | Evidence Type | Specific Proof |
|-------|--------------|----------------|
| [Claim 1] | [Stat/Quote/Case Study] | [Specific evidence] |
| [Claim 2] | [Stat/Quote/Case Study] | [Specific evidence] |
| [Claim 3] | [Stat/Quote/Case Study] | [Specific evidence] |

---

### Words We Use / Words We Avoid

| Use | Avoid | Why |
|-----|-------|-----|
| [Word] | [Word] | [Reason] |
| [Word] | [Word] | [Reason] |

---
**REQUIRES HUMAN APPROVAL BEFORE FINALIZING**
"""


@tool
def create_battlecard(
    competitor: str,
    our_positioning: str,
    their_positioning: str,
    our_strengths: str,
    their_strengths: str,
) -> str:
    """
    Create a competitive battlecard for sales enablement.

    Args:
        competitor: Name of the competitor
        our_positioning: Our positioning statement
        their_positioning: Their positioning
        our_strengths: Where we win
        their_strengths: Where they're strong

    Returns:
        Sales-ready competitive battlecard
    """
    return f"""
## Competitive Battlecard: vs {competitor}

### Quick Win (30-Second Pitch)
"When evaluating {competitor}, here's what matters: [key differentiator]. Unlike them, we [unique value]. Companies like [customer] chose us because [reason]."

---

### Competitive Overview

| Dimension | Us | {competitor} |
|-----------|----|----|
| Target Market | [Our ICP] | [Their ICP] |
| Core Strength | [What we do best] | [What they do best] |
| Pricing Model | [Our model] | [Their model] |
| Key Differentiator | [Our unique value] | [Their unique value] |

---

### Where We Win

{our_strengths}

**Proof Points:**
- [Specific evidence 1]
- [Specific evidence 2]
- [Customer quote]

---

### Where They're Strong (Handle With Care)

{their_strengths}

**How to Handle:**
- [Reframe 1]
- [Acknowledge and pivot]
- [Turn into our advantage]

---

### Common Objections & Rebuttals

| Objection | Rebuttal |
|-----------|----------|
| "They're the market leader" | [Response] |
| "They have more features" | [Response] |
| "We already use them" | [Response] |

---

### Landmines to Set

Questions to ask early that favor us:
1. "[Question that surfaces competitor weakness]"
2. "[Question about our differentiator]"
3. "[Question about their typical pain point]"

---

### Discovery Questions

- "How are you handling [problem we solve] today?"
- "What's working? What's frustrating?"
- "What would success look like?"
- "Who else are you evaluating?"

---

### Competitive Traps to Avoid

- Don't [thing that backfires]
- Never [thing that helps competitor]
- Watch out for [common mistake]

---

### Win Story

**Customer:** [Name/Type]
**Situation:** Evaluated us vs {competitor}
**Why They Chose Us:** [Key reason]
**Quote:** "[Compelling quote]"
**Result:** [Outcome/metric]
"""


@tool
def create_launch_plan(
    product_name: str,
    launch_date: str,
    launch_tier: str,
    target_audience: str,
    key_messages: str,
) -> str:
    """
    Create a go-to-market launch plan.

    This is a HUMAN-APPROVAL-REQUIRED tool.

    Args:
        product_name: What we're launching
        launch_date: Target launch date
        launch_tier: Launch tier (1=Major, 2=Medium, 3=Minor)
        target_audience: Who this is for
        key_messages: Core messaging for launch

    Returns:
        Comprehensive launch plan with timeline
    """
    return f"""
## Launch Plan: {product_name}

### Launch Overview
- **Launch Date:** {launch_date}
- **Launch Tier:** {launch_tier}
- **Target Audience:** {target_audience}

---

### Key Messages
{key_messages}

---

### Launch Timeline

**T-4 Weeks: Preparation**
- [ ] Messaging finalized and approved
- [ ] Sales enablement created
- [ ] Support trained
- [ ] Press/analyst briefings scheduled

**T-2 Weeks: Internal Readiness**
- [ ] All hands announcement
- [ ] Demo environment ready
- [ ] Email sequences built
- [ ] Social content scheduled

**T-1 Week: Final Prep**
- [ ] Website updates staged
- [ ] Press release drafted
- [ ] Customer reference lined up
- [ ] Contingency plan reviewed

**Launch Day**
- [ ] Website live
- [ ] Email sent
- [ ] Social posted
- [ ] Press release out
- [ ] Sales notified

**T+1 Week: Momentum**
- [ ] Monitor coverage
- [ ] Social engagement
- [ ] Sales follow-up
- [ ] Customer feedback

---

### Channel Activation

| Channel | Content | Owner | Date |
|---------|---------|-------|------|
| Website | Landing page, feature page | [Owner] | [Date] |
| Email | Launch announcement | [Owner] | [Date] |
| Social | Thread, posts | [Owner] | [Date] |
| Press | Release, briefings | [Owner] | [Date] |
| Sales | Enablement, demo | [Owner] | [Date] |
| Product | In-app announcement | [Owner] | [Date] |

---

### Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Website traffic | +X% | Google Analytics |
| Sign-ups | X new | Product metrics |
| Press mentions | X articles | Coverage tracking |
| Social engagement | X impressions | Social analytics |

---

### Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | H/M/L | H/M/L | [Plan] |
| [Risk 2] | H/M/L | H/M/L | [Plan] |

---
**REQUIRES HUMAN APPROVAL BEFORE FINALIZING**
"""


@tool
def create_checklist(
    task_type: str,
    context: str,
) -> str:
    """
    Create a PMM checklist for common workflows.

    Args:
        task_type: Type of checklist (launch, positioning, competitive, messaging)
        context: Specific context for the checklist

    Returns:
        Detailed checklist for the task
    """
    checklists = {
        "launch": """
## Launch Checklist

### Messaging & Positioning
- [ ] Positioning statement finalized
- [ ] Key messages defined
- [ ] Elevator pitch drafted
- [ ] FAQ created

### Content & Assets
- [ ] Website pages created/updated
- [ ] Blog post drafted
- [ ] Social content ready
- [ ] Email sequences built
- [ ] Press release written

### Sales Enablement
- [ ] Sales deck updated
- [ ] Battlecards created
- [ ] Demo script ready
- [ ] Pricing & packaging clear
- [ ] Objection handling documented

### Internal Alignment
- [ ] All hands presented
- [ ] Support trained
- [ ] Success team briefed
- [ ] Engineering aligned on messaging

### External Prep
- [ ] Analyst briefings scheduled
- [ ] Press briefings scheduled
- [ ] Customer reference confirmed
- [ ] Partner communications sent
""",
        "positioning": """
## Positioning Checklist

### Research Complete
- [ ] Customer interviews (5+)
- [ ] Competitive analysis done
- [ ] Market trends reviewed
- [ ] Win/loss analysis current

### Framework Applied
- [ ] Target customer defined (ICP)
- [ ] Problem/need articulated
- [ ] Category established
- [ ] Key benefit clear
- [ ] Differentiator defensible

### Validation Done
- [ ] Tested with customers
- [ ] Sales team reviewed
- [ ] Leadership aligned
- [ ] Proof points identified

### Activation Ready
- [ ] Messaging derived from positioning
- [ ] Website reflects positioning
- [ ] Sales trained on positioning
- [ ] Consistent across channels
""",
        "competitive": """
## Competitive Analysis Checklist

### Intelligence Gathered
- [ ] Product capabilities mapped
- [ ] Pricing researched
- [ ] Messaging analyzed
- [ ] Reviews mined
- [ ] Team/hiring tracked
- [ ] Recent announcements reviewed

### Analysis Complete
- [ ] Strengths identified
- [ ] Weaknesses documented
- [ ] Differentiation clear
- [ ] Risk areas flagged

### Deliverables Created
- [ ] Battlecard drafted
- [ ] Comparison page ready
- [ ] Sales objection guide
- [ ] Win story documented
""",
        "messaging": """
## Messaging Checklist

### Foundation Set
- [ ] Positioning approved
- [ ] Audience segments defined
- [ ] Value props ranked
- [ ] Proof points gathered

### Hierarchy Created
- [ ] Headline (5 words)
- [ ] Subhead (1 sentence)
- [ ] Body copy (2-3 sentences)
- [ ] Supporting messages

### Variations Done
- [ ] By audience segment
- [ ] By funnel stage
- [ ] By channel

### Validation Complete
- [ ] Customer tested
- [ ] A/B test planned
- [ ] Legal reviewed (if needed)
"""
    }

    return checklists.get(task_type.lower(), f"""
## Custom Checklist: {task_type}

### Context
{context}

### Items
- [ ] Item 1
- [ ] Item 2
- [ ] Item 3
- [ ] Item 4
- [ ] Item 5

### Notes
Add specific items based on context.
""")
