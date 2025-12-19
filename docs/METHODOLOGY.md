# The Mixture of Experts Methodology

> How we build AI agents that actually work in production.

---

## Core Philosophy

Most AI agents fail because they try to do everything with one monolithic prompt. The result? Generic outputs, hallucinations, and frustrated users.

**Mixture of Experts (MoE)** takes a different approach: decompose complex domains into specialized sub-agents that collaborate on tasks—each expert handling what they do best.

This isn't theory. It's the pattern behind every successful production agent we've built.

---

## The Five Principles

### 1. Domain Decomposition

Break complex domains into discrete expertise areas. A PMM agent doesn't try to "do marketing"—it has separate experts for:
- Competitive intelligence
- Positioning strategy
- Messaging development
- Launch coordination
- Risk assessment

Each expert has focused knowledge, specific tools, and clear output formats.

### 2. Semantic Grounding

Ground agent behavior in established frameworks from domain experts. Don't invent new methodologies—encode proven ones.

When our positioning expert works, it uses April Dunford's framework. When assessing product-market fit, it applies Ash Maurya's constraints-as-features lens. When planning experiments, it thinks in Eric Ries's Build-Measure-Learn loops.

The AI doesn't guess what good looks like. It knows because we've encoded what the best practitioners do.

### 3. Human-in-the-Loop

Critical decisions require human judgment. The agent proposes, the human disposes.

Our agents explicitly surface:
- Strategic recommendations (before finalizing)
- Risk assessments (before proceeding)
- Assumptions (before acting on them)
- Confidence levels (so you know when to dig deeper)

This isn't about AI limitation—it's about building trust and catching edge cases.

### 4. Eval-Driven Development

Every output should be measurable. "Good enough" isn't good enough.

We build agents with observability from day one:
- Token usage tracking
- Latency monitoring
- Output quality scoring
- User feedback loops

If you can't measure it, you can't improve it.

### 5. Iterative Refinement

Start rough, improve through feedback. The first version of any agent is wrong—the question is how fast you can make it right.

Our workflow:
1. Build MVP agent (working, not perfect)
2. Deploy to real users (learn what breaks)
3. Analyze failure modes (understand why)
4. Refine and redeploy (ship improvements)
5. Repeat forever (agents are never "done")

---

## Standing on the Shoulders of Giants

The intelligence in our agents isn't invented—it's inherited. We've encoded insights from practitioners who've shaped how we think about products, markets, and AI.

| Giant | Key Insight | Applied When |
|-------|-------------|--------------|
| **Geoffrey Moore** | The Chasm exists—early adopters ≠ mainstream | Targeting market segments, crossing from early adopters |
| **Clay Christensen** | Jobs to Be Done trump demographics | Understanding what customers actually hire products for |
| **April Dunford** | Positioning is competitive context, not aspiration | Creating positioning statements, defining market category |
| **Marty Cagan** | Discovery over delivery—validate before building | Prioritizing customer research, validating assumptions |
| **Ash Maurya** | Constraints are features—embrace the box | Scoping MVPs, focusing on what matters most |
| **Eric Ries** | Build-Measure-Learn is the scientific method for startups | Planning experiments, iterating on feedback |
| **swyx** | Evals are the new tests—measure AI quality | Building evaluation frameworks, assessing output quality |
| **Harrison Chase** | Tools extend capability—agents need actions | Designing tool suites, orchestrating agent actions |
| **Anthropic Team** | Human-AI collaboration beats pure automation | Surfacing decisions, building trust loops |
| **Rahul & Alex** | Observability matters—you can't fix what you can't see | Debugging agents, monitoring production systems |

---

## How This Translates to Code

### Agent Architecture

```python
# Domain-specific expert agents
EXPERTS = {
    "competitive_analyst": CompetitiveAnalystExpert,
    "positioning_strategist": PositioningExpert,
    "messaging_specialist": MessagingExpert,
    "launch_coordinator": LaunchExpert,
    "risk_assessor": RiskExpert,
}

# Router determines which expert handles the task
def route_to_expert(task: Task) -> Expert:
    """Route based on task type, not keyword matching."""
    return EXPERTS[classify_task(task)]
```

### Tool Design

Each expert has access to domain-specific tools:

```python
# Competitive Analyst tools
competitive_tools = [
    search_competitors,      # Find and analyze competitors
    fetch_competitor_page,   # Pull competitor messaging
    analyze_reviews,         # Mine G2/Capterra feedback
    track_competitive_moves, # Monitor announcements
]

# Positioning Strategist tools
positioning_tools = [
    create_positioning_statement,  # Dunford framework
    map_competitive_alternatives,  # What customers use instead
    identify_unique_attributes,    # What we have they don't
    define_target_market,          # Who cares most
]
```

### Output Formats

Every expert produces structured, consistent output:

```python
class PositioningStatement(BaseModel):
    """April Dunford's positioning framework."""
    target_customer: str
    problem_or_opportunity: str
    product_category: str
    key_benefit: str
    competitive_alternative: str
    key_differentiator: str
```

---

## Why This Works

### vs. Monolithic Prompts

| Monolithic | Mixture of Experts |
|------------|-------------------|
| One prompt tries to do everything | Specialized experts collaborate |
| Generic outputs | Domain-specific depth |
| Hard to debug | Clear failure attribution |
| Difficult to improve | Iterative expert refinement |

### vs. RAG-Only Approaches

| RAG-Only | MoE + RAG |
|----------|-----------|
| Retrieves information | Retrieves AND reasons |
| Passive knowledge | Active problem-solving |
| No workflow intelligence | Structured decision-making |
| Context window limited | Expert-specific context |

### vs. Fine-Tuning

| Fine-Tuning | MoE with Prompt Engineering |
|-------------|----------------------------|
| Expensive to iterate | Cheap to modify |
| Black box changes | Transparent behavior |
| Model-specific | Model-agnostic |
| Slow feedback loop | Fast iteration |

---

## Getting Started

### 1. Identify Your Experts

What are the 3-5 core expertise areas in your domain? For PMM, we identified:
- Intake & Discovery
- Research & Intelligence
- Strategy & Frameworks
- Execution & Delivery
- Validation & Refinement

### 2. Ground in Frameworks

What established methodologies do experts in your domain use? Find the "Giants" whose work you can encode:
- Books that define the field
- Practitioners with proven track records
- Frameworks that practitioners actually use

### 3. Design Your Tools

What actions does each expert need to take? Design tools that:
- Do one thing well
- Return structured output
- Handle errors gracefully
- Log for observability

### 4. Define Output Formats

How should each expert communicate? Create consistent formats for:
- Analysis outputs
- Recommendations
- Deliverables
- Handoffs between experts

### 5. Build Feedback Loops

How will you know if it's working? Implement:
- User feedback collection
- Output quality metrics
- Error tracking
- Usage analytics

---

## Further Reading

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/) — Multi-agent orchestration
- [Obviously Awesome](https://www.aprildunford.com/obviously-awesome) — April Dunford's positioning framework
- [Running Lean](https://leanstack.com/books/running-lean) — Ash Maurya's systematic approach
- [Inspired](https://www.svpg.com/books/inspired-how-to-create-tech-products-customers-love-2nd-edition/) — Marty Cagan on product discovery
- [The Lean Startup](http://theleanstartup.com/) — Eric Ries on Build-Measure-Learn
- [Crossing the Chasm](https://www.harpercollins.com/products/crossing-the-chasm-3rd-edition-geoffrey-a-moore) — Geoffrey Moore on technology adoption
- [Competing Against Luck](https://www.christenseninstitute.org/books/competing-against-luck/) — Clay Christensen on Jobs to Be Done

---

## About This Methodology

Developed by Jai Bhagat through 2+ years of teaching AI agent development to non-technical practitioners. Battle-tested with QEDC validation and refined through hundreds of prototype-to-production deployments.

This isn't academic theory—it's the pattern we use every day.

[Learn more at chaiwithjai.com](https://chaiwithjai.com)
