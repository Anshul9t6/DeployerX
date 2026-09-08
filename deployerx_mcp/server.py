"""DeployerX MCP server — stdio transport, run by the MCP client (e.g. Claude).

Reads only files inside this repository plus the FAQ text a caller passes in.
No network calls, no storage, no telemetry.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

try:
    from mcp.server.mcpserver import MCPServer as _Server  # MCP SDK 2.x
except ImportError:
    try:
        from mcp.server.fastmcp import FastMCP as _Server  # MCP SDK 1.x
    except ImportError:
        raise SystemExit(
            "The DeployerX MCP server needs the MCP SDK: pip install mcp\n"
            "(everything else in this repo stays stdlib-only)"
        )

from deployerx_mcp import tools

mcp = _Server(
    "deployerx",
    instructions=(
        "DeployerX is a field kit for deploying AI assistants with non-engineer "
        "operators (shops, clinics) in their language. Typical flow: "
        "list_playbooks/pick_playbook -> get_playbook -> locale_context for the "
        "operator's district -> build_system_prompt with the owner's real FAQ -> "
        "list_eval_cases + run_eval before any customer-facing use. "
        "Core rules the prompts and evals enforce: answer only from the owner's "
        "FAQ, never invent prices or discounts, escalate to the owner when "
        "unsure, and for clinics never diagnose, prescribe, or interpret reports."
    ),
)


@mcp.tool()
def list_playbooks() -> str:
    """List all DeployerX playbooks (deployment recipes) with when to use each.

    Call this first when the user wants to deploy an AI assistant for a shop,
    clinic, or local service and you need to see what recipes exist.
    """
    return tools.playbook_catalog()


@mcp.tool()
def pick_playbook(use_case: str, channel: str = "whatsapp") -> str:
    """Recommend a playbook for a use case and channel.

    use_case examples: shop_faq, retail, kirana, clinic, lab, diagnostic.
    channel is usually 'whatsapp'. Call when the user has described their
    business and you need the matching recipe.
    """
    return tools.choose_playbook(use_case, channel)


@mcp.tool()
def get_playbook(playbook_id: str) -> str:
    """Get a playbook's full guide: overview, when (not) to use it, the
    step-by-step deployment path (Path A needs no paid API), and cost bands.

    Call after pick_playbook, before walking the user through deployment.
    """
    return tools.playbook_guide(playbook_id)


@mcp.tool()
def list_locales(country: str = "") -> str:
    """List available locale packs. Without arguments: countries. With a
    country code (e.g. 'in'): its L2 regions and L3 districts.

    Call to find the right slugs before locale_context or build_system_prompt.
    """
    return tools.locale_catalog(country)


@mcp.tool()
def locale_context(country: str, l2: str = "", l3: str = "") -> str:
    """Get the merged local context for a place: the L0→L1→L2→L3 cascade and
    concatenated constraints (language mix, trust norms, local do/don'ts).

    Call with the operator's location (e.g. country='in', l2='rajasthan',
    l3='jaipur') before assembling any customer-facing prompt.
    """
    return tools.locale_context(country, l2, l3)


@mcp.tool()
def build_system_prompt(
    playbook_id: str,
    faq: str = "",
    country: str = "",
    l2: str = "",
    l3: str = "",
    language: str = "",
    faq_path: str = "",
) -> str:
    """Assemble the deployable system prompt: playbook prompt + the owner's
    FAQ + merged locale constraints. This is the exact assembly deploy.md
    describes doing by hand.

    Pass the owner's real FAQ via `faq` (pasted text) or `faq_path` (local
    .txt or Sheet CSV with question,answer). faq_path wins when both are set.
    If both are empty a marked SAMPLE FAQ is used — never deploy that.
    language picks prompts/system.<language>.md (e.g. 'hi', 'en').
    """
    return tools.system_prompt(playbook_id, faq, country, l2, l3, language, faq_path)


@mcp.tool()
def list_eval_cases(playbook_id: str) -> str:
    """List a playbook's eval cases: customer messages to test with and the
    expected behavior for each.

    Call before go-live: send each message to the assistant under test, then
    grade the replies with run_eval.
    """
    return tools.eval_cases(playbook_id)


@mcp.tool()
def run_eval(playbook_id: str, responses: dict[str, str]) -> str:
    """Grade replies against a playbook's eval suite and return a scorecard.

    `responses` maps case id (from list_eval_cases) to the assistant's reply.
    Checks are deterministic: no invented prices (currency amounts must be
    grounded in the FAQ), escalation to the owner when unsure, and forbidden
    content (e.g. prescriptions). A failing scorecard means the prompt or FAQ
    must be fixed before any customer-facing use.
    """
    return tools.eval_responses(playbook_id, responses)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
