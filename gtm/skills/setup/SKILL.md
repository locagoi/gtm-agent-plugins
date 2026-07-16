---
name: setup
description: Use FIRST, right after installing the gtm plugin, to connect Claude Code to a GTM Automation workspace. Guides the agent through installing the `gtm` CLI, logging in with the workspace MCP key, and validating the connection with `gtm whoami` + `gtm tools`. Run this before gtm-operate or build-gtm-workflow.
allowed-tools: Bash, Read
---

# Set up the gtm connection to a GTM Automation workspace

This skill gets a freshly installed `gtm` plugin from "installed" to "connected and verified".
Do the three steps in order. Stop and ask the user for anything you don't have — never guess a key.

**Prerequisites (confirm before you start):**
- The user has a **GTM Automation workspace** on the **Growth plan or higher** (MCP access is plan-gated).
- The user has their **workspace MCP key**. It comes from the app: **Erweiterungen / Extensions -> MCP**. It is per-workspace and secret — the user pastes it; you never print it in full.
- Node 18+ is available (the CLI needs it).

There are two surfaces this plugin sets up, and they share the same key and the same `/api/mcp/<key>` endpoint:
1. **The `gtm` CLI** — for shell-driven operating (this skill installs + logs it in).
2. **The bundled MCP connection** — Claude Code prompts for the same workspace MCP key when the plugin is enabled (the `workspace_mcp_key` config), and connects the `gtm` MCP server automatically. If you were already prompted for that key at install time, the MCP tools are live and you only need the CLI for shell recipes.

## Step 1 — Install the `gtm` CLI

Install the published package globally (Node 18+ required):

```bash
npm i -g gtm-goat-cli
```

This puts the `gtm` binary on your PATH. Verify it's reachable:

```bash
gtm --help               # command groups + global flags
```

> The npm package is `gtm-goat-cli`; the command it installs is `gtm`.

**Fallback (build from source):** if you can't install from npm (e.g. offline, or you want a local dev build),
the CLI source lives in the main GTM Automation repo under `cli/` (full reference: `cli/README.md`):

```bash
# from a checkout of the main GTM Automation repo
cd cli
npm install
npm run build            # compiles to dist/, produces the `gtm` bin
npm link                 # puts `gtm` on your PATH
# …or run without linking: node dist/index.js --help
```

## Step 2 — Log in with the workspace MCP key

Ask the user to paste their workspace MCP key (from Erweiterungen/Extensions -> MCP). Then:

```bash
gtm login --key <workspace MCP key> --url https://app.cegtec.net
```

- The key is stored in `~/.gtm/config.json` (chmod 0600). Only a masked form is ever printed.
- Credentials resolve in this order: `--key`/`--url` flags -> `GTM_API_KEY`/`GTM_BASE_URL` env -> `~/.gtm/config.json`.
- For a non-prod host, pass a different `--url` (e.g. `--url http://localhost:3000`).

## Step 3 — Validate the connection

```bash
gtm whoami               # verifies the key + shows the workspace — spends NO credits
gtm tools                # lists every tool available on THIS workspace (name + description)
gtm tools --json         # machine-readable, for the agent
```

- `gtm whoami` returning the workspace name = the CLI is connected.
- `gtm tools` returning a non-empty list = the workspace endpoint is reachable and the key is valid.

**Read the exit code if anything fails** — the CLI maps failures precisely:
`0` ok · `2` usage · `3` no/unreadable creds · `4` bad key (401) · `5` plan-gated, needs Growth+ (403) · `6` rate-limited (429) · `7` network · `8` tool ran but returned an error.
Exit `4` -> re-check the key. Exit `5` -> the workspace is not on Growth+ (or MCP is off); tell the user. Exit `7` -> check the `--url`/network.

## Done — what next

Once `gtm whoami` and `gtm tools` succeed, you are connected. Then:
- To **operate** the workspace (read tables/Wissen, source, enrich, run columns, spend safely) -> the **gtm-operate** skill.
- To **build a repeatable play** as a table (create table -> module columns -> cascade -> save as template) -> the **build-gtm-workflow** skill.

**Guardrails carry over from the moment you connect:** paid (`ai`/`enrichment`) live runs require `--max-credits`; always `--mode dry_run` first; no auto-retries; outreach sends are gated; every call is scoped to this one workspace. See gtm-operate for the full list.
