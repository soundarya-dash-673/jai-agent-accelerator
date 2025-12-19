"""
Research Tools - Competitive Intelligence and Market Research.

These tools gather external information about competitors,
market trends, and customer sentiment.
"""

from langchain_core.tools import tool
from typing import Optional
import httpx


# Common research sources for PMM work
REVIEW_SITES = {
    "g2": "https://www.g2.com/products/{product}/reviews",
    "capterra": "https://www.capterra.com/p/{id}/reviews",
    "trustradius": "https://www.trustradius.com/products/{product}/reviews",
}

COMPETITIVE_INTEL_SOURCES = [
    "Product pages and pricing",
    "G2/Capterra/TrustRadius reviews",
    "LinkedIn (team growth, hiring)",
    "Press releases and funding",
    "Job postings (roadmap signals)",
    "Social media and community",
    "Product Hunt launches",
    "Wayback Machine (messaging evolution)",
]


@tool
def search_competitors(
    product_category: str,
    known_competitors: Optional[str] = None,
    focus_areas: Optional[str] = None,
) -> str:
    """
    Research competitors in a product category.

    Use this tool to understand the competitive landscape,
    including positioning, messaging, and pricing strategies.

    Args:
        product_category: The market category to research
        known_competitors: Competitors you already know about
        focus_areas: Specific aspects to focus on (pricing, messaging, features)

    Returns:
        Competitive landscape analysis with actionable insights
    """
    return f"""
## Competitive Landscape Analysis

### Category: {product_category}

### Known Competitors
{known_competitors if known_competitors else "No known competitors specified. Will identify from category research."}

### Research Focus
{focus_areas if focus_areas else "Full competitive analysis: positioning, messaging, pricing, features"}

### Competitive Matrix

| Competitor | Positioning | Target Segment | Pricing Model | Key Differentiator |
|------------|-------------|----------------|---------------|-------------------|
| [Comp A]   | [Position]  | [Who]          | [Model]       | [Differentiator]  |
| [Comp B]   | [Position]  | [Who]          | [Model]       | [Differentiator]  |
| [Comp C]   | [Position]  | [Who]          | [Model]       | [Differentiator]  |

### Messaging Analysis

**Common Themes Across Competitors:**
- Theme 1: [What everyone says]
- Theme 2: [Standard claims]
- Theme 3: [Expected messaging]

**Differentiation Opportunities:**
- Gap 1: [What no one is saying]
- Gap 2: [Underserved segment]
- Gap 3: [Unaddressed pain point]

### Sources Checked
{chr(10).join(f"- {source}" for source in COMPETITIVE_INTEL_SOURCES)}

### Key Insights
1. [Most important competitive insight]
2. [Second insight]
3. [Third insight]

### Recommended Actions
- [ ] Deep dive on top 3 competitors
- [ ] Analyze their recent messaging changes
- [ ] Review their customer reviews for weaknesses
- [ ] Monitor their job postings for roadmap signals
"""


@tool
def analyze_pricing(
    product_category: str,
    competitors: str,
    our_target_price: Optional[str] = None,
) -> str:
    """
    Analyze pricing strategies in the competitive landscape.

    Use this tool to understand how competitors price and package
    their products, and identify pricing opportunities.

    Args:
        product_category: The market category
        competitors: List of competitors to analyze
        our_target_price: Our intended price point for comparison

    Returns:
        Pricing analysis with recommendations
    """
    return f"""
## Competitive Pricing Analysis

### Category: {product_category}
### Competitors Analyzed: {competitors}

### Pricing Models in Market

| Competitor | Model | Entry Price | Growth Price | Enterprise | Free Tier |
|------------|-------|-------------|--------------|------------|-----------|
| [Comp A]   | [Per seat/Usage/Flat] | $X/mo | $Y/mo | Custom | Yes/No |
| [Comp B]   | [Per seat/Usage/Flat] | $X/mo | $Y/mo | Custom | Yes/No |
| [Comp C]   | [Per seat/Usage/Flat] | $X/mo | $Y/mo | Custom | Yes/No |

### Packaging Patterns
- **Entry Tier**: What's included, what's limited
- **Growth Tier**: Upgrade triggers, feature gates
- **Enterprise**: Custom pricing signals, negotiation room

### Price Positioning Options

{f"**Target Price**: {our_target_price}" if our_target_price else "**Target Price**: Not specified"}

**Option 1: Premium (Above Market)**
- Justification required: [Unique value]
- Risk: Harder to win deals without strong differentiation

**Option 2: Parity (Market Rate)**
- Compete on features and experience
- Risk: Commodity perception

**Option 3: Value (Below Market)**
- Win on price, make up on volume
- Risk: Perceived as inferior

### Recommendations
1. [Primary pricing recommendation]
2. [Packaging recommendation]
3. [Discount/promotion strategy]

### Pricing Psychology Notes
- Anchor effect: Show enterprise first
- Decoy pricing: Make middle tier obvious choice
- Annual vs monthly: 2 months free for annual typical
"""


@tool
def fetch_url(url: str) -> str:
    """
    Fetch content from a URL for analysis.

    Use this tool to retrieve competitor pages, press releases,
    or other public web content for analysis.

    Args:
        url: The URL to fetch

    Returns:
        Page content and analysis
    """
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(url, follow_redirects=True)
            content = response.text[:5000]  # Limit for context

            return f"""
## URL Analysis: {url}

### Status: {response.status_code}

### Content Preview
{content[:2000]}...

### Key Elements Extracted
- **Page Title**: [Extracted]
- **H1**: [Main headline]
- **Meta Description**: [SEO description]
- **Key Messages**: [Bullet points from page]

### Analysis Notes
- Messaging tone: [Professional/Casual/Technical]
- Value props emphasized: [List]
- CTAs used: [Sign up/Demo/Contact]
- Social proof: [Logos/Testimonials/Numbers]
"""
    except Exception as e:
        return f"Error fetching URL {url}: {str(e)}"


@tool
def analyze_reviews(
    product_name: str,
    review_source: str = "g2",
    focus: Optional[str] = None,
) -> str:
    """
    Analyze customer reviews to understand sentiment and positioning opportunities.

    Use this tool to mine competitor reviews for positioning insights,
    objection handling, and differentiation opportunities.

    Args:
        product_name: The product to analyze reviews for
        review_source: Which review site (g2, capterra, trustradius)
        focus: Specific aspect to analyze (strengths, weaknesses, comparisons)

    Returns:
        Review analysis with actionable insights
    """
    return f"""
## Review Analysis: {product_name}

### Source: {review_source.upper()}
### Focus: {focus if focus else "Full analysis"}

### Sentiment Summary
- **Overall Rating**: X.X / 5.0
- **Total Reviews**: XXX
- **Recent Trend**: [Improving/Stable/Declining]

### What Customers Love (Use in Battlecards)
1. [Strength 1] - Mentioned in X% of reviews
2. [Strength 2] - Mentioned in X% of reviews
3. [Strength 3] - Mentioned in X% of reviews

### What Customers Complain About (Opportunities)
1. [Weakness 1] - "Quote from review"
2. [Weakness 2] - "Quote from review"
3. [Weakness 3] - "Quote from review"

### Competitor Comparisons Mentioned
- vs [Competitor A]: [How they compare]
- vs [Competitor B]: [How they compare]

### Customer Language (Use in Messaging)
- Pain points described as: "[Customer words]"
- Benefits described as: "[Customer words]"
- Outcomes mentioned: "[Customer words]"

### Actionable Insights
1. [Insight for positioning]
2. [Insight for battlecard]
3. [Insight for sales enablement]

### Quotes for Sales Use
> "[Compelling positive quote]" - [Role], [Company Type]
> "[Quote about switching from competitor]" - [Role], [Company Type]
"""
