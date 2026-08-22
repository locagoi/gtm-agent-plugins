# GTM Automation — Claude Code plugins

**The complete outbound setup guide, as a Claude Code plugin.** Install it and your agent
knows how to take a GTM Automation workspace from empty to a live, sending campaign in one
session — and, just as importantly, *what to build*: the ICP, the cadence, the copy rules and
the limits that decide whether outbound produces meetings or burns domains.

Free to install and free to read. The method inside is the same one used to run campaigns
across every workspace on the platform.

Brand: **GTM Automation / cegtec**. CLI: **`gtm`**. Endpoint: `https://app.cegtec.net/api/mcp/<your-key>`.

---

## What this actually gives you

Built by hand, a customer outbound playbook is a two-to-four week engagement: discovery call,
CRM analysis, ICP workshop, persona mapping, value props, sequence writing, QA. The plugin is
that process — same stages, same quality bars — executed by your agent against your own
workspace.

**Nine stages, one session:**

```
0  Connect and orient          →  a verified connection, a read model
1  Intake interview            →  answers you did not invent
2  Wissen assets               →  ICP · persona · offer · proof · angle · signals
3  Playbook                    →  the strategy, bound and pinned
4  Senders & channel           →  one channel, verified, within limits
5  The table                   →  source → qualify → enrich → copy
6  The sequence                →  the touch plan the lead experiences
7  The enroll column           →  the one handoff that sends
8  First bounded run           →  20 rows read by a human
9  Measure and rebuild         →  the loop that compounds
```

Start at **`gtm-quickstart`** and it walks you through all nine.

## The skills

| Skill | What it is |
|---|---|
| **`setup`** | Guided first run: install the CLI, log in with your workspace key, validate. |
| **`gtm-quickstart`** | **Start here.** The nine stages above, with a checkpoint at the end of each. Includes `intake.md` — the discovery questions the build actually consumes. |
| **`outbound-playbook`** | *What* to build: ICP breadth, channel choice, cadence, copy rules, volume, what to measure. Includes `benchmarks.md` — the numbers every rule rests on. |
| **`draft-gtm-play`** | The strategy layer, asset by asset: ICP → persona → offer → proof → angle → signals, with the quality bars. |
| **`build-gtm-workflow`** | Build a play as a table: columns, output schemas, gates, cascade, template. Includes `three-table-play.md` — the canonical accounts → people → outreach layout. |
| **`sequences`** | The touch plan: seven step kinds, cadence, slots, senders, enrollment, stop rules. Includes `copy-patterns.md` — per-channel copy structure and the pre-send check. |
| **`plays`** | **Nine ready-to-run motions**, each with its sources, columns, gates and tool calls: local business outreach · own-post engagers · keyword signals · job openings · inbound qualification · website visitors · lost-deal reactivation · CRM blacklist sync · CRM mining. |
| **`agents-loops-goals`** | Make the workspace run itself: missions as goals, agents with scoped tool allowlists, and the loops (scheduled sources, signal watches, event triggers, the `await_rows` return edge, approval gates). Includes what a dry run really simulates. |
| **`gtm-handoffs`** | How the pieces connect — and the connections that do **not** exist. Read before wiring a motion end to end. |
| **`gtm-operate`** | Day-to-day operating: read, source, enrich, run columns, spend safely. |

Plus **a wired MCP connection** — the `gtm` MCP server pointed at your workspace. Claude Code
prompts for your key when the plugin is enabled and stores it in secure storage, never in a
file.

## Nine plays, ready to run

Name the motion and the agent builds it — no "which tool does that?" round trip:

| Play | Starts from |
|---|---|
| **Local business outreach** | Maps → qualify → find the owner → validate email → sequence |
| **Own-post engagers** | your LinkedIn posts → everyone who reacted → warm LinkedIn sequence |
| **Keyword / competitor signals** | public discussion of the problem → who engaged → quote them |
| **Job openings** | Indeed discovery, plus a standing watch on your accounts' career pages |
| **Inbound lead qualification** | a webhook → qualified in seconds → routed, or a Feed card |
| **Website visitor outreach** | de-anonymisation tool → webhook → email + LinkedIn in 48 h |
| **Lost deal reactivation** | the CRM graveyard → what changed → a message that names the old reason |
| **CRM blacklist reconciliation** | the guard that stops outbound shadowing an open deal |
| **CRM mining for the ICP** | won deals → the ICP, written as Wissen → the free lookalike source |

Plus **ten installable platform workflows** — reply-to-meeting, reply triage, lead routing,
meeting→CRM, post-engagers, CRM auto-enrich, deliverability watch and three signal-to-outreach
reactions — which the agent installs rather than rebuilds. And **nineteen house plays as
structured data** via `get_play(id)`, including `full_gtm_chain`: the whole path from the
customer's own data to a scaled winner, in ten callable modules.

Every play carries the cost gate that matters: contact enrichment costs up to 25 credits a row
against 2 for qualification, so qualification always runs first and the expensive column is
gated on its verdict.

## Some of what is inside

A sample of the rules, each with its evidence in `benchmarks.md`:

- **Narrow beats broad by ~2×.** Playbooks naming ≤ 5 regions reply at roughly twice the rate
  of those naming more.
- **Rebuild the message before adding contacts.** The largest improvements observed come from
  rebuilding the copy on the *same* audience — several times the reply rate, at lower volume.
- **15 cold emails per inbox per day.** Scale by adding inboxes, never by raising volume.
  Thirty inboxes × fifteen = 450 clean sends a day.
- **No links and no tracking in a cold body.** The single largest deliverability lever, and
  the one that feels most like a lost conversion.
- **Validate before import.** 0.4 % versus 7.7 % bounce on identical infrastructure — a factor
  of 19.
- **Five touches, days 1 → 4 → 9 → 16 → 25**, each carrying a new angle. A reply pauses every
  channel.
- **A signal is hot for 3–7 days.** After ~28 it is cold, and a late approach does more damage
  than silence.
- **Check your sequence has steps.** A sequence with no steps is one of the most common build
  faults there is — wired, believed live, sending nothing, erroring never.

Platform findings are directional patterns aggregated across all workspaces, reported as
ratios only — no per-customer figures, no campaign volumes, nothing attributable to any
customer. Operator figures come from cegtec's published practice at
[cegtec.net/academy](https://www.cegtec.net/academy). Neither is a promise — they are
reference points to argue with.

## Prerequisites

1. A **GTM Automation workspace** on the **Starter plan or higher** (MCP access is plan-gated;
   only a trial workspace is refused).
2. Your **workspace MCP key** — in the app (`https://app.cegtec.net`): **Erweiterungen /
   Extensions → MCP**. Per workspace and secret; treat it like a password.
3. **Node 18+** for the `gtm` CLI.

No workspace yet? The skills are still worth reading — `outbound-playbook`,
`sequences/copy-patterns.md` and `benchmarks.md` are method, not product documentation.

## Install

```
/plugin marketplace add locagoi/gtm-agent-plugins
/plugin install gtm@gtm-plugins
```

Claude Code prompts for your **workspace MCP key** (`workspace_mcp_key`) when the plugin is
enabled. It is stored in secure storage and used to connect the `gtm` MCP server at
`https://app.cegtec.net/api/mcp/<your-key>`. No key is ever hardcoded in this repo.

Then say **"set up gtm"** and your agent runs the `setup` skill, or **"build my first
campaign"** for `gtm-quickstart`.

## The `gtm` CLI

Speaks MCP over HTTP to your workspace endpoint — no SDK, no extra backend.

- **Install:** `npm i -g gtm-goat-cli` (Node 18+). Package `gtm-goat-cli`, command `gtm`.
- **Reference:** `gtm --help`, and `gtm <command> --help` per command.

```bash
gtm whoami                                              # verify the key, spends nothing
gtm tools                                               # the curated core on this workspace
gtm table schema                                        # data model + Wissen assets
gtm column run <table> <column> --mode dry_run          # FREE cost preview
gtm column run <table> <column> --max-credits 25        # live paid run, hard cap
gtm call <tool> --input '{...}' --json                  # any tool, JSON in/out
```

**On the tool list:** `gtm tools` shows a curated core of ~70 verbs. The rest of the
catalogue is still callable by name — only the listing is trimmed. `find_tools` returns the
names; `gtm call <name>` runs them.

## Guardrails, built in

- **Paid runs need a budget** — a live `ai`/`enrichment` run without `--max-credits` is
  refused; `--mode dry_run` first.
- **No auto-retries** — a re-run is a deliberate act.
- **The enroll column is terminal** — last column, sends only in its own run, `auto_run`
  rejected.
- **Sends pass the gates** — unsubscribe and blacklist checked deny-only, fail closed.
- **Single workspace** — every call is scoped to the workspace behind your key. There is no
  cross-workspace access.

## Layout

```
.claude-plugin/marketplace.json     # marketplace "gtm-plugins" → plugin "gtm"
gtm/
  .claude-plugin/plugin.json        # manifest + MCP server + userConfig (workspace_mcp_key)
  skills/
    setup/SKILL.md                  # connect and validate
    gtm-quickstart/SKILL.md         # ← start here: zero to live campaign
                   intake.md        #   the discovery questions
    outbound-playbook/SKILL.md      # what to build, and why
                     benchmarks.md  #   the numbers behind every rule
    draft-gtm-play/SKILL.md         # strategy, asset by asset
    build-gtm-workflow/SKILL.md     # build a play as a table
                      three-table-play.md   # accounts → people → outreach
    sequences/SKILL.md              # the touch plan
             copy-patterns.md       #   per-channel copy structure
    agents-loops-goals/SKILL.md     # goals, agents, and the loops that keep running
    plays/SKILL.md                  # the source + module catalogue, and how to run a play
         local-business-outreach.md · own-post-engagers.md · keyword-signals.md
         job-openings.md · inbound-qualification.md · web-visitor-outreach.md
         lost-deal-reactivation.md · crm-blacklist-sync.md · crm-mining.md
    outbound-playbook/learnings.md  # cross-workspace patterns, each with its confound named
    gtm-operate/SKILL.md            # day-to-day operating
    gtm-handoffs/SKILL.md           # how the pieces connect
```

## Support

info@cegtec.net · https://app.cegtec.net · [Academy](https://www.cegtec.net/academy) ·
[Docs](https://www.cegtec.net/gtm-goat/docs/)
