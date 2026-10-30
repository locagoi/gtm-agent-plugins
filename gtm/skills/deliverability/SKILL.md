---
name: deliverability
description: Use daily, or whenever replies drop, bounces rise or the user asks "do our mails still land in the inbox". Reads inbox and domain health (SPF, DMARC, DKIM), bounce and reply rates and seed-test placement, sorts every sending inbox into burned / untested / healthy on real data, and proposes the smallest reversible fix — pause, rest, swap, re-test. Every change to a live sending setup and every placement test is previewed and confirmed. Part of the closed loop (see closed-loop).
allowed-tools: Bash, Read, Grep, Glob
---

# Deliverability

Station 4 of the closed loop. Copy, targeting and timing are worth nothing if the mail lands
in spam — and a burned inbox gives no error. It keeps sending, the reply rate quietly falls,
and the campaign looks like a copy problem.

Obeys the rules in **`closed-loop`**: reading is free; pausing, swapping or re-testing waits
for a yes. The sending rules themselves (volume per inbox, links, tracking, validation) live
in **`outbound-playbook`** and **`sequences`**; this skill keeps an existing setup healthy.

## 1. Read (immediately)

- `get_deliverability_health` — per inbox: status, daily limit, warm-up; per campaign:
  bounce and reply rates; per domain: SPF, the DMARC policy, DKIM, with plain-sentence
  findings. Pass `window_days` to see volume over a window instead of a running total.
  **Read the timestamp** — the values come from the last monitoring run, not from now.
- `get_placement_report` — results of seed (placement) tests: inbox versus spam, per inbox.
- `list_senders` — which sender carries which inbox, its limit, its status.
- `get_sender_pool_health` — the LinkedIn side: connected accounts, invites and messages today.
- `get_campaign_stats` — sends, bounces and replies per campaign, including a connected
  outbound tool.

Judge an inbox on **real placement and bounce data**, not on a warm-up score. A warm-up score
can read perfect while cold mail lands in spam.

## 2. Sort every inbox

| State | Rule | Action to propose |
|---|---|---|
| **burned** | recent placement data with enough seeds behind it, spam share above your bar — or bounce rate above your stop bar | take it out of cold sending, rest it, re-test later |
| **untested** | no recent placement data | **hold** — never strip an inbox for missing data; schedule a test |
| **healthy** | recent data, below your bars | keep; may replace a burned one |
| **broken** | sender `error`, disconnected | reconnect first — a hard blocker, not a reputation problem |

Set the bars before you look (see `closed-loop` rule 4); `outbound-playbook` names published
reference points for bounce. A score backed by only a handful of seeds is "still collecting",
not a verdict.

Domain findings explain what the inbox list cannot: a missing or `none` DMARC policy, a
failing DKIM selector or a broken SPF record affects every inbox on that domain at once.

## 3. Propose the smallest reversible fix (gated)

One proposal per object: preview it, wait for an explicit yes, then execute and read back:

| Problem | Smallest fix |
|---|---|
| One inbox burned, others healthy | remove it from the cold rotation, keep the campaign running on the rest |
| All inboxes of a sequence burned | pause the sequence (`update_sequence`) or brake the playbook (`update_playbook` with `outreach_paused`) — a human adds fresh, warmed inboxes |
| Domain authentication finding | fix the DNS record; nothing in the workspace changes |
| No recent placement data | run a seed test (`create_placement_test`) — it sends real mail from your inboxes to the provider's seed addresses, so it is gated like any send |
| Bounce rate climbing | stop enrolling from the source that delivered the bad addresses; validate before import |

Guardrails:

- **Never empty a running campaign.** If removing burned inboxes would leave none, do not
  remove them silently — pause and flag that new inboxes are needed. That is a human task.
- **Never raise a sender's limit** to compensate for removed inboxes.
- Record before and after for every change, so it can be undone.
- Placement tests score over hours. Today's action rests on the last scored cycle; do not
  expect same-minute truth.

## Output

```
DELIVERABILITY — <workspace> — data as of <timestamp>

INBOX            DOMAIN        PLACEMENT (spam/seeds)   BOUNCE   STATE      PROPOSAL
<inbox>          <domain>      <x>/<n>                   <x> %    burned     rest + re-test
<inbox>          <domain>      —                         <x> %    untested   schedule test

DOMAINS     <finding per domain, in one line each>
CAN'T FIX   <sequences left without a healthy inbox — needs new inboxes>
```

Name the tool behind every number. A missing measurement is "not measured", never "clean".

## Make it a loop

The platform ships a deliverability-watch workflow; **`agents-loops-goals`** shows how to run
this check on a schedule. Reading and flagging can run unattended; changes to the live sending
setup keep their human gate.
