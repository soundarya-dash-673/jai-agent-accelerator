# Jai's Agent Accelerator

> **From prototype to production in 48 hours.**

A battle-tested framework for building, deploying, and iterating on AI agents—created by an agent engineer who's spent 2 years teaching non-technical people to ship AI that works.

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start)
[![Powered by LangChain](https://img.shields.io/badge/Powered%20by-LangChain-blue)](https://langchain.com)

---

## The Story

I've taught hundreds of PMs, designers, and founders to build AI agents. Not toy demos—real systems that run in production.

The pattern is always the same:
1. **Day 1:** "I made a ChatGPT wrapper!"
2. **Day 3:** "Why is the output so generic?"
3. **Day 7:** "How do I make it remember context?"
4. **Day 14:** "How do I know if it's actually good?"
5. **Day 30:** "Why can't I deploy this anywhere?"

This repo solves all of that. It's the system I use to prototype and productionize every agent I build—battle-tested with Claude Code, LangChain, and Netlify.

**My credentials:**
- Professional Agent Engineer (LLM observability & evaluations via LangChain)
- 2 years teaching AI to non-technical people
- QEDC-validated methodology for real business outcomes
- Life's research documented at [pm-ai-lab.netlify.app](https://pm-ai-lab.netlify.app)

---

## What You Get

### The Framework

```
jai-agent-accelerator/
├── apps/
│   ├── agent/                    # Python backend (LangChain + FastAPI)
│   │   └── src/pmm_agent/
│   │       ├── agent.py          # Agent factory with 5 operating modes
│   │       ├── prompts.py        # MoE methodology + 10 Giants framework
│   │       ├── server.py         # Production-ready FastAPI
│   │       └── tools/            # 15+ domain-specific tools
│   │           ├── intake.py     # Product analysis
│   │           ├── research.py   # Competitive intelligence
│   │           ├── planning.py   # Positioning & messaging
│   │           └── risk.py       # Validation & risk assessment
│   └── web/                      # React frontend (Vite + Tailwind)
├── config/
│   └── domains/
│       └── pmm.json              # Domain configuration
├── docs/
│   ├── DEPLOYMENT.md             # Step-by-step deployment guides
│   ├── CUSTOMIZATION.md          # How to adapt for your domain
│   └── METHODOLOGY.md            # The Mixture of Experts approach
└── docker-compose.yml            # One-command local setup
```

### The Methodology: Mixture of Experts

Instead of one monolithic prompt trying to do everything, we decompose expertise into specialized sub-agents that work together.

**Core Principles:**
1. **DOMAIN DECOMPOSITION** — Break complex domains into specialized sub-experts
2. **SEMANTIC GROUNDING** — Ground agent behavior in established frameworks
3. **HUMAN-IN-THE-LOOP** — Critical decisions require human approval
4. **EVAL-DRIVEN** — Every output should be measurable and improvable
5. **ITERATIVE REFINEMENT** — Start rough, improve through feedback loops

### Standing on the Shoulders of Giants

The agent's intelligence is semantically grounded in the work of 10 practitioners who've shaped how we think about products, markets, and AI:

| Giant | Key Insight | Applied When |
|-------|-------------|--------------|
| Geoffrey Moore | The Chasm exists | Targeting segments |
| Clay Christensen | Jobs to Be Done | Understanding needs |
| April Dunford | Positioning is foundation | Before messaging |
| Marty Cagan | Discovery over delivery | Validating assumptions |
| Ash Maurya | Constraints are features | Prioritizing scope |
| Eric Ries | Build-Measure-Learn | Planning experiments |
| swyx | Evals are the new tests | Assessing quality |
| Harrison Chase | Tools extend capability | Orchestrating actions |
| Anthropic Team | Human-AI collaboration | Surfacing decisions |
| Rahul & Alex | Observability matters | Debugging outcomes |

---

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Anthropic API key

### Local Development (5 minutes)

```bash
# Clone the repo
git clone https://github.com/chai-with-jai/jai-agent-accelerator.git
cd jai-agent-accelerator

# Backend setup
cd apps/agent
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .

# Set your API key
export ANTHROPIC_API_KEY=sk-ant-...

# Start the agent
python -m uvicorn pmm_agent.server:app --host 0.0.0.0 --port 8123
```

In a new terminal:

```bash
# Frontend setup
cd apps/web
npm install
npm run dev
```

Open [http://localhost:3003](http://localhost:3003) — you're running a production-grade agent.

---

## Deployment Guide

### Option 1: Netlify + LangChain (Recommended)

This is the deployment pattern I use for all my agents. It's fast, cheap, and scales.

#### Step 1: Prepare Your Repository

Create a `netlify.toml` in the root:

```toml
[build]
  command = "cd apps/web && npm install && npm run build"
  publish = "apps/web/dist"

[functions]
  directory = "apps/agent/netlify/functions"

[[redirects]]
  from = "/api/*"
  to = "/.netlify/functions/:splat"
  status = 200
```

#### Step 2: Create the Netlify Function

Create `apps/agent/netlify/functions/agent.py`:

```python
from pmm_agent.server import app
from mangum import Mangum

handler = Mangum(app)
```

#### Step 3: Deploy

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login and deploy
netlify login
netlify init
netlify env:set ANTHROPIC_API_KEY sk-ant-...
netlify deploy --prod
```

Your agent is now live at `https://your-site.netlify.app`

#### Step 4: Verify

```bash
curl https://your-site.netlify.app/api/health
# → {"status": "ok", "agent": "jai-agent-accelerator"}
```

### Option 2: Vercel (Coming Soon)

Vercel deployment guide is in development. Pattern:
- Backend: Vercel Serverless Functions (Python runtime)
- Frontend: Vercel (zero-config for Vite)

### Option 3: Docker (Self-Hosted)

```bash
docker-compose up --build
# Backend: http://localhost:8123
# Frontend: http://localhost:3003
```

### Option 4: Railway

```bash
npm i -g @railway/cli
railway login
railway init
railway up
```

---

## Agent Modes

| Mode | Tools Available | Use Case |
|------|-----------------|----------|
| `full` | All 15+ tools | Complete PMM workflow |
| `intake` | Product analysis | Understanding product |
| `research` | Competitive intel | Market analysis |
| `planning` | Positioning/messaging | Strategic deliverables |
| `risk` | Validation | Risk assessment |

```python
from pmm_agent import create_pmm_agent

# Full capability agent
agent = create_pmm_agent(mode="full")

# Specialized research agent
research_agent = create_pmm_agent(mode="research")
```

---

## Tools Reference

### Intake Tools
- `analyze_product` — Extract product details and value props
- `extract_value_props` — Identify benefits and proof points
- `identify_icp` — Define ideal customer profile

### Research Tools
- `search_competitors` — Find and analyze competitors
- `analyze_pricing` — Competitive pricing research
- `fetch_url` — Retrieve web content
- `analyze_reviews` — Mine customer feedback

### Planning Tools
- `create_positioning_statement` — Dunford framework positioning
- `create_messaging_matrix` — Audience-specific messaging
- `create_battlecard` — Sales enablement
- `create_launch_plan` — GTM timeline
- `create_checklist` — PMM workflow checklists

### Risk Tools
- `assess_market_risks` — Risk matrix and mitigation
- `validate_positioning` — Customer validation framework
- `identify_gaps` — Gap analysis and action plan

---

## Customization

### Adding Your Own Domain

1. **Copy the config template:**
```bash
cp config/domains/pmm.json config/domains/your-domain.json
```

2. **Update the domain configuration**

3. **Create domain-specific tools** in `tools/your_domain.py`

4. **Update the prompts** to reflect your domain expertise

See `docs/CUSTOMIZATION.md` for the full guide.

---

## API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/chat` | POST | Send message, get response |
| `/chat/stream` | POST | Streaming response |
| `/sessions/{id}` | DELETE | Clear session |

---

## Pricing & Support

This is a premium product sold on [LemonSqueezy](https://lemonsqueezy.com).

| Tier | Price | Includes |
|------|-------|----------|
| **Starter** | $497 | Source code + docs + 30 days email support |
| **Pro** | $997 | + Self-paced video modules + Office hours access |
| **Team** | $1,997 | + 3 seats + Private Slack channel |

### What's Included

**Starter ($497):**
- Complete source code (MIT licensed for your use)
- Masterful documentation
- Deployment guides (Netlify, Vercel, Docker, Railway)
- 30 days email support
- Lifetime updates

**Pro ($997):**
Everything in Starter, plus:
- Self-paced video modules
- Monthly office hours access
- Priority email support

**Team ($1,997):**
Everything in Pro, plus:
- 3 team seats
- Private Slack channel
- 1 hour onboarding call

### Cohort Course

Want hands-on learning? Join my **cohort-based course starting January 27, 2025**.

4 weeks, 4 live sessions, working agent at the end.

[Learn more →](https://chaiwithjai.com/course)

---

## FAQ

**Who is this for?**
PMs, designers, and founders who want to build AI that actually works.

**Do I need to code?**
You should be comfortable reading Python and terminal commands.

**What about OpenAI?**
Uses Claude, but patterns work with any model.

**How much does it cost to run?**
$30-50/month in API costs at typical usage.

**Refund policy?**
30-day money-back guarantee.

---

## Author

**Jai Bhagat** — Agent Engineer & Educator

- LLM Observability & Evaluations (via LangChain)
- Prototype → Production Framework (Claude Code + Netlify)
- 2 Years Teaching AI to Non-Technical People
- QEDC-Validated Methodology

[chaiwithjai.com](https://chaiwithjai.com)

---

## License

MIT License — see [LICENSE](LICENSE)

---

Built with [LangChain](https://langchain.com), [Claude](https://anthropic.com), and [Netlify](https://netlify.com)
