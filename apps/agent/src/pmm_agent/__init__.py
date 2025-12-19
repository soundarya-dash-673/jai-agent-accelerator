"""
PMM Deep Agent - Product Marketing Intelligence.

Turn market chaos into messaging clarity.
"""

from .agent import create_pmm_agent
from .prompts import MAIN_SYSTEM_PROMPT

__all__ = ["create_pmm_agent", "MAIN_SYSTEM_PROMPT"]
__version__ = "0.1.0"
