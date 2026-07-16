# GTM Automation — Claude Code plugins

A Claude Code **plugin marketplace** that connects your agent to a **GTM Automation** workspace.
Install it and your Claude Code gets the **`gtm` CLI**, the **operating + build skills**, and a **wired MCP connection**
to your own workspace — so your agent can build and run GTM plays (sourcing, enrichment, qualification,
copy, enrollment) directly against your data.

Brand: **GTM Automation / cegtec**. CLI: **`gtm`**. Endpoint: `https://app.cegtec.net/api/mcp/<your-key>`.

## What you get

The marketplace `gtm-plugins` ships one plugin, `gtm`, which bundles:

- **`gtm-operate`** skill — the agent operating guide: the object model, the CLI-vs-MCP choice, exact
  commands/tool names/args, copyable recipes, and the spend/send guardrails.
- **`build-gtm-workflow`** skill — build a repeatable play as a workspace table (create table -> module
  columns -> cascade -> save as template) and replay it deterministically.
- **`setup`** skill — a guided first-run: install the CLI, log in with your workspace MCP key, and validate.
- **A wired MCP connection** — the `gtm` MCP server, pointed at your workspace endpoint. Claude Code prompts
  for your workspace MCP key when the plugin is enabled and stores it in secure storage (never in a plain file).

## Prerequisites

1. A **GTM Automation workspace** on the **Growth plan or higher** (MCP access is plan-gated).
2. Your **workspace MCP key** — see below.
3. **Node 18+** (for the `gtm` CLI).

### Get your workspace MCP key

In the app (`https://app.cegtec.net`): **Erweiterungen / Extensions -> MCP**. Copy the key for your workspace.
It is per-workspace and secret — treat it like a password. You paste it at setup; it is never committed anywhere.

## Install

In Claude Code:

```
/plugin marketplace add locagoi/gtm-agent-plugins
/plugin install gtm@gtm-plugins
```

When the plugin is enabled, Claude Code prompts for your **workspace MCP key** (`workspace_mcp_key`). Paste it —
it is stored in secure storage and used to connect the `gtm` MCP server at
`https://app.cegtec.net/api/mcp/<your-key>`. No key is ever hardcoded in this repo.

> The repo is private during rollout. If `/plugin marketplace add` can't reach it, make sure your GitHub
> account has access to `locagoi/gtm-agent-plugins`.

## First run

Ask your agent to run the **setup** skill (or say "set up gtm"). It will:

1. Install the `gtm` CLI (`npm i -g gtm-goat-cli`; or build from the CLI source at the main repo's `cli/` —
   see `cli/README.md`).
2. `gtm login --key <workspace MCP key> --url https://app.cegtec.net`
3. Validate with `gtm whoami` (no credits spent) and `gtm tools`.

After that, **your agent knows the product** via the `gtm-operate` skill — it can read your tables and Wissen,
source and enrich rows, run columns within a credit cap, and build plays with `build-gtm-workflow`.

## The `gtm` CLI

The CLI speaks MCP over HTTP to your workspace's `/api/mcp/<key>` endpoint — no SDK, no extra backend.

- **Install:** `npm i -g gtm-goat-cli` (Node 18+). The npm package is `gtm-goat-cli`; the command is `gtm`.
- **Fallback (build from source):** in the main GTM Automation repo under `cli/`
  (`npm install && npm run build && npm link`). Full reference: the main repo's `cli/README.md`.

Common commands:

```bash
gtm tools                                   # every tool on this workspace
gtm tables list                             # every table
gtm table schema                            # data model + Wissen assets
gtm column run <table> <column> --mode dry_run          # FREE cost preview
gtm column run <table> <column> --max-credits 25        # live paid run (hard cap)
gtm wissen list --kind icp
gtm call <tool> --input '{...}' --json      # any tool, JSON in/out
```

## Guardrails (built in)

- **Paid runs need a budget** — a live `ai`/`enrichment` run without `--max-credits` is refused; `--mode dry_run` first.
- **No auto-retries** — a re-run is a deliberate act.
- **Outreach sends are gated** — send categories are refused at run time; propose, don't fire.
- **Single workspace** — every call is scoped to the workspace behind your key; there is no cross-workspace access.

## Layout

```
.claude-plugin/marketplace.json     # marketplace "gtm-plugins" -> plugin "gtm" (source ./gtm)
gtm/
  .claude-plugin/plugin.json        # plugin manifest + MCP server + userConfig (workspace_mcp_key)
  skills/
    setup/SKILL.md                  # guided first-run
    gtm-operate/SKILL.md            # operate the workspace
    build-gtm-workflow/SKILL.md     # build a play as a table
```

## Support

info@cegtec.net · https://app.cegtec.net
