"""DeployerX MCP server — plug the field kit into Claude or any MCP client.

The server exposes the repo's existing knowledge as tools: playbook catalog
and selection, the locale cascade, deployable system-prompt assembly, and
the eval scorecard. It reads only files inside this repository plus whatever
FAQ text the caller passes in; it runs locally over stdio and makes no
network calls of its own.

Run:  python3 deployerx_mcp/server.py   (or: python3 -m deployerx_mcp)
Needs the MCP SDK: pip install mcp
"""
