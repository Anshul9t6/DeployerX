# DeployerX MCP server

Plug the DeployerX field kit into Claude (Desktop, Code) or any
[MCP](https://modelcontextprotocol.io) client. An AI assistant can then pick
a playbook, pull the locale cascade for a district, assemble the deployable
system prompt from the owner's real FAQ, and grade replies with the eval
suite — the same flow `deploy.md` describes doing by hand.

MCP (Model Context Protocol) is an open standard, MIT-licensed, created by
Anthropic and adopted across the industry. This server is ~100 lines of
wiring around code that already exists in this repo.

## What data it uses

- **Repo files only:** the playbooks, locale packs, prompts, and eval cases
  in this repository — nothing else.
- **Plus whatever the caller passes in:** e.g. the shop owner's FAQ text via
  `build_system_prompt`. It is used to assemble the prompt and returned;
  never stored.
- **Runs locally over stdio.** The MCP client starts this process on your
  machine. The server makes **no network calls**, keeps **no state**, and
  has **no telemetry**. The AI model runs in the client (e.g. Claude), so
  API keys and model access belong to the client — this server needs none.

## Setup

```bash
pip install mcp    # the only dependency; the rest of the repo stays stdlib-only
```

**Claude Desktop** — add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "deployerx": {
      "command": "python3",
      "args": ["/absolute/path/to/DeployerX/deployerx_mcp/server.py"]
    }
  }
}
```

**Claude Code:**

```bash
claude mcp add deployerx -- python3 /absolute/path/to/DeployerX/deployerx_mcp/server.py
```

(If `mcp` is installed in a virtualenv, point `command` at that venv's
`python3` instead.)

## Tools

| Tool | What it does |
|------|--------------|
| `list_playbooks` | Catalog of deployment recipes |
| `pick_playbook` | use case + channel → recommended playbook |
| `get_playbook` | Full guide: when (not) to use, deploy steps, cost bands |
| `list_locales` | Countries, or a country's L2/L3 tree |
| `locale_context` | Merged L0→L1→L2→L3 constraints for a place |
| `build_system_prompt` | Playbook prompt + owner FAQ + locale cascade, ready to deploy |
| `list_eval_cases` | Test messages + expected behavior for a playbook |
| `run_eval` | Grade replies → deterministic scorecard (invented prices, escalation, forbidden content) |

## Example

> **User:** Set up a WhatsApp FAQ assistant for my guest house in Varanasi.
>
> **Claude** calls `pick_playbook("shop_faq")` → `get_playbook` →
> `locale_context("in", "uttar-pradesh", "varanasi")` (which carries rules
> like *never invent ritual/religious facts*) → asks the user for their real
> FAQ → `build_system_prompt(...)` → `list_eval_cases` + `run_eval` to check
> the assembled assistant before handing it over.

The contract still applies: evals must pass, and customer-facing use starts
with human approval (see the playbook's `deploy.md`).
