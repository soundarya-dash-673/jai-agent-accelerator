"""
Risk Tools - Market Risk Assessment and Validation.

These tools help identify and mitigate risks in positioning,
messaging, and go-to-market strategy.
"""

from langchain_core.tools import tool
from typing import Optional


@tool
def assess_market_risks(
    positioning: str,
    target_market: str,
    competitive_context: str,
    launch_timeline: Optional[str] = None,
) -> str:
    """
    Assess market risks for positioning and GTM strategy.

    Use this tool to surface potential problems before they
    become launch-day disasters.

    Args:
        positioning: Current positioning statement
        target_market: Target market and ICP
        competitive_context: Competitive landscape
        launch_timeline: Planned launch timing if applicable

    Returns:
        Risk assessment with mitigation strategies
    """
    return f"""
## Market Risk Assessment

### Context
- **Positioning:** {positioning[:200]}...
- **Target Market:** {target_market}
- **Timeline:** {launch_timeline if launch_timeline else "Not specified"}

---

### Risk Matrix

| Risk | Likelihood | Impact | Score | Mitigation |
|------|------------|--------|-------|------------|
| **Competitive Response** | H/M/L | H/M/L | X/9 | [Action] |
| **Market Timing** | H/M/L | H/M/L | X/9 | [Action] |
| **Message Resonance** | H/M/L | H/M/L | X/9 | [Action] |
| **Proof Point Gaps** | H/M/L | H/M/L | X/9 | [Action] |
| **Internal Alignment** | H/M/L | H/M/L | X/9 | [Action] |
| **Channel Saturation** | H/M/L | H/M/L | X/9 | [Action] |

---

### Competitive Risks

**Threat Assessment:**
{competitive_context}

**Potential Responses:**
1. [Competitor A might do X]
2. [Competitor B might do Y]
3. [New entrant risk]

**Counter-Strategies:**
- [Preemptive action 1]
- [Defensive measure 2]
- [Offensive opportunity 3]

---

### Positioning Risks

**Assumptions Being Made:**
1. [Assumption about market]
2. [Assumption about customer]
3. [Assumption about differentiation]

**What Could Invalidate Them:**
1. [Scenario that breaks assumption 1]
2. [Scenario that breaks assumption 2]
3. [Scenario that breaks assumption 3]

**Validation Plan:**
- [ ] Customer interview validation
- [ ] Competitive monitoring setup
- [ ] Market signal tracking

---

### Message Risks

**Potential Objections:**
1. "[Objection 1]" - Risk Level: H/M/L
2. "[Objection 2]" - Risk Level: H/M/L
3. "[Objection 3]" - Risk Level: H/M/L

**Proof Point Gaps:**
- Claim: [X] - Evidence: [Missing/Weak/Strong]
- Claim: [Y] - Evidence: [Missing/Weak/Strong]

---

### Timing Risks

**External Factors:**
- [ ] Competitor launches in same window
- [ ] Market event conflicts
- [ ] Economic conditions
- [ ] Industry calendar (conferences, quarters)

**Internal Factors:**
- [ ] Resource availability
- [ ] Cross-functional alignment
- [ ] Product readiness
- [ ] Sales capacity

---

### Recommended Actions

**Immediate (This Week):**
1. [High-priority risk mitigation]
2. [Validation action]

**Before Launch:**
1. [Risk reduction step]
2. [Contingency planning]

**Ongoing:**
1. [Monitoring setup]
2. [Response playbook]
"""


@tool
def validate_positioning(
    positioning: str,
    validation_method: str,
    results: Optional[str] = None,
) -> str:
    """
    Validate positioning with customers or market data.

    Use this tool to structure positioning validation
    and interpret results.

    Args:
        positioning: The positioning to validate
        validation_method: How we're validating (interviews, surveys, A/B test)
        results: Results if validation has been done

    Returns:
        Validation framework and interpretation
    """
    return f"""
## Positioning Validation

### Positioning Under Test
{positioning}

### Validation Method: {validation_method.upper()}

---

### Validation Framework

**Key Questions to Answer:**
1. Does the target customer self-identify?
2. Does the problem resonate as urgent?
3. Is the category understood?
4. Is the benefit compelling?
5. Is the differentiator believable?
6. Would they take action?

---

### Interview Protocol (If Using Interviews)

**Screening Questions:**
- Role: [Target role]
- Company: [Target company type]
- Pain: [Relevant experience with problem]

**Core Questions:**
1. "How would you describe [problem space] challenges?"
2. "What solutions have you tried?"
3. [Show positioning] "What's your reaction?"
4. "What would make you skeptical?"
5. "How does this compare to [competitor]?"
6. "What would you need to see to believe this?"

**Signals to Watch:**
- Verbal: Enthusiasm, skepticism, confusion
- Non-verbal: Leaning in, nodding, frowning
- Follow-up: Questions they ask

---

### Results Interpretation
{results if results else "Results not yet available. Complete validation and add results."}

**Score Card:**

| Dimension | Score (1-5) | Notes |
|-----------|-------------|-------|
| Self-identification | X | [Notes] |
| Problem urgency | X | [Notes] |
| Category clarity | X | [Notes] |
| Benefit appeal | X | [Notes] |
| Differentiator credibility | X | [Notes] |
| Action intent | X | [Notes] |

**Overall Validation:** [PASS / ITERATE / FAIL]

---

### Recommended Iterations

**If Failing on Self-Identification:**
- Narrow or expand target definition
- Use different language for "who"

**If Failing on Problem:**
- Research deeper customer pain points
- Find more urgent trigger

**If Failing on Differentiator:**
- Find stronger proof points
- Identify more defensible unique value
"""


@tool
def identify_gaps(
    current_state: str,
    desired_state: str,
    resources_available: Optional[str] = None,
) -> str:
    """
    Identify gaps between current and desired positioning/messaging state.

    Use this tool to create a clear action plan for PMM improvements.

    Args:
        current_state: Where we are now
        desired_state: Where we want to be
        resources_available: What we have to work with

    Returns:
        Gap analysis with prioritized action plan
    """
    return f"""
## Gap Analysis

### Current State
{current_state}

### Desired State
{desired_state}

---

### Gap Identification

| Area | Current | Desired | Gap Size | Priority |
|------|---------|---------|----------|----------|
| **Positioning** | [Current] | [Desired] | S/M/L | H/M/L |
| **Messaging** | [Current] | [Desired] | S/M/L | H/M/L |
| **Proof Points** | [Current] | [Desired] | S/M/L | H/M/L |
| **Sales Enablement** | [Current] | [Desired] | S/M/L | H/M/L |
| **Competitive Intel** | [Current] | [Desired] | S/M/L | H/M/L |
| **Customer Research** | [Current] | [Desired] | S/M/L | H/M/L |

---

### Resource Assessment
{resources_available if resources_available else "Resources not specified. Assuming standard PMM capacity."}

**Available:**
- [ ] Time: [Hours/weeks available]
- [ ] Budget: [For research, content, etc.]
- [ ] Tools: [Existing tools and data]
- [ ] Support: [Cross-functional help]

---

### Prioritized Action Plan

**Quick Wins (1-2 weeks):**
1. [Action with immediate impact]
2. [Low-effort, high-value]

**Medium-Term (1 month):**
1. [Significant improvement]
2. [Requires some investment]

**Strategic (3+ months):**
1. [Major initiative]
2. [Foundational improvement]

---

### Success Metrics

| Gap | Metric | Current | Target | By When |
|-----|--------|---------|--------|---------|
| [Gap 1] | [Metric] | [Now] | [Goal] | [Date] |
| [Gap 2] | [Metric] | [Now] | [Goal] | [Date] |

---

### Dependencies & Blockers

**Dependencies:**
- [What needs to happen first]
- [Who needs to be involved]
- [What resources are needed]

**Potential Blockers:**
- [Blocker 1] - Mitigation: [Action]
- [Blocker 2] - Mitigation: [Action]

---

### Recommendation

Based on the gap analysis, the recommended path forward is:

1. **Start with:** [Highest priority gap]
2. **Then focus on:** [Second priority]
3. **Defer:** [Lower priority items]

**Rationale:** [Why this prioritization makes sense]
"""
