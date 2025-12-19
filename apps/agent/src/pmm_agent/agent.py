"""
PMM Deep Agent Factory.

Creates configurable PMM agents with different capability modes.
"""

from typing import Literal

from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent

from .prompts import (
    MAIN_SYSTEM_PROMPT,
    COMPETITIVE_ANALYST_PROMPT,
    MESSAGING_SPECIALIST_PROMPT,
    LAUNCH_COORDINATOR_PROMPT,
)
from .tools import (
    INTAKE_TOOLS,
    RESEARCH_TOOLS,
    PLANNING_TOOLS,
    RISK_TOOLS,
    ALL_TOOLS,
    HUMAN_APPROVAL_TOOLS,
)


AgentMode = Literal["full", "intake", "research", "planning", "risk"]


def create_pmm_agent(
    mode: AgentMode = "full",
    model_name: str = "claude-sonnet-4-20250514",
    with_subagents: bool = True,
):
    """
    Create a PMM agent with the specified capabilities.

    Args:
        mode: Operating mode determining available tools
            - "full": All tools available
            - "intake": Product analysis and requirements only
            - "research": Competitive intelligence and market research
            - "planning": Positioning, messaging, and launch planning
            - "risk": Risk assessment and validation
        model_name: Claude model to use
        with_subagents: Whether to include specialist subagents

    Returns:
        Configured LangGraph agent
    """
    # Select tools based on mode
    tools = []
    if mode == "full":
        tools = ALL_TOOLS
    elif mode == "intake":
        tools = INTAKE_TOOLS
    elif mode == "research":
        tools = RESEARCH_TOOLS + INTAKE_TOOLS  # Research needs intake context
    elif mode == "planning":
        tools = PLANNING_TOOLS + INTAKE_TOOLS
    elif mode == "risk":
        tools = RISK_TOOLS + RESEARCH_TOOLS

    # Initialize model
    llm = ChatAnthropic(
        model_name=model_name,
        max_tokens=8192,
    )

    # Create base agent
    agent = create_react_agent(
        model=llm,
        tools=tools,
        state_modifier=MAIN_SYSTEM_PROMPT,
    )

    return agent


def create_competitive_analyst():
    """Create a specialist agent for competitive intelligence."""
    llm = ChatAnthropic(model_name="claude-sonnet-4-20250514", max_tokens=4096)
    return create_react_agent(
        model=llm,
        tools=RESEARCH_TOOLS,
        state_modifier=COMPETITIVE_ANALYST_PROMPT,
    )


def create_messaging_specialist():
    """Create a specialist agent for messaging work."""
    llm = ChatAnthropic(model_name="claude-sonnet-4-20250514", max_tokens=4096)
    return create_react_agent(
        model=llm,
        tools=PLANNING_TOOLS,
        state_modifier=MESSAGING_SPECIALIST_PROMPT,
    )


def create_launch_coordinator():
    """Create a specialist agent for launch planning."""
    llm = ChatAnthropic(model_name="claude-sonnet-4-20250514", max_tokens=4096)
    return create_react_agent(
        model=llm,
        tools=PLANNING_TOOLS + RISK_TOOLS,
        state_modifier=LAUNCH_COORDINATOR_PROMPT,
    )


# Convenience exports
agent = create_pmm_agent()
