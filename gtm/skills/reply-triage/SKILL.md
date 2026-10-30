---
name: reply-triage
description: Use when the user wants to work the reply inbox or check for new responses — surface inbound replies, read the whole thread, classify each one (positive, question, objection, referral, not interested, opt-out, out of office), draft answers, and hold every send for a per-reply yes. Opt-outs are suppressed, never answered with a pitch. Never auto-sends. Part of the closed loop (see closed-loop); the station where outreach turns into conversations.
allowed-tools: Bash, Read, Grep, Glob
---

# Reply triage

Station 3 of the closed loop. Every reply is either a conversation about to start or a person
asking to be left alone, and both need a decision fast. Default posture: **surface, draft,
hold for approval.**

Obeys the rules in **`closed-loop`**: drafting is free, sending waits for a yes per reply.

## Inputs

- Nothing → replies of the last 7 days that still need a decision.
- A sequence, playbook or lead → just those.

## 1. Surface (read immediately)

- `list_replies` — inbound replies and drafts waiting for a decision.
- `mailbox_list` / `mailbox_thread` — the full email thread in a connected mailbox.
- `get_lead_thread` — the conversation history of one lead across channels.
- `get_lead_intelligence` — who the person is, the company, any open deal, earlier contact.

**Read the whole thread before classifying.** A reply marked as not handled is not
necessarily unanswered — someone may have answered from the mailbox directly. An answer
written without the thread contradicts what was already said.

If an expected reply is missing, `list_runs` with `source: "webhook"` shows inbound events
that failed to settle — that is where a lost reply usually is.

## 2. Classify

| Class | Means | Next |
|---|---|---|
| `positive` | interest, asks for a call or the material | draft a reply — fast |
| `question` | wants to know something first | draft an answer to exactly that question |
| `objection` | a reason not to, but still talking | draft a short answer to the objection, no pressure |
| `referral` | "not me — talk to X" | draft a thank-you and the handover to X |
| `not-interested` | a clear no | no sales reply; mark the lead (step 4) |
| `opt-out` | asks to stop | **suppress, never pitch** (step 4) |
| `out-of-office` | auto-reply | no draft; note the return date |
| `other` | anything else | surface to the user |

On LinkedIn, accepting an invitation or a one-word reaction to it is not a positive reply.
Count only real answers.

## 3. Draft (free — nothing is sent)

- `draft_reply` — returns draft text for a lead's inbound message. Text only; it queues and
  sends nothing.
- `mailbox_draft_reply` — writes a draft into the real mailbox thread; a human edits and
  sends it there. Never sends.
- `queue_reply_draft` — puts a draft into the workspace's approval queue. Never sends.

Rules for every draft:

- Answer what the person actually wrote. One message, one point, one easy next step.
- Match their language and register. If they wrote in a different language than the
  campaign, ask the user which language to answer in before drafting.
- No claims you cannot prove, no numbers that are not in your Wissen, no internal tool or
  vendor names.
- A positive reply wants the next step, not the pitch again.

## 4. Decide and send (gated, one reply at a time)

Present each draft as:

```
<lead> · <company> · <class>
  they wrote:  "<snippet>"
  draft:       "<proposed answer>"
  → send / edit / skip?
```

- **send** → `edit_and_send_reply` with the approved text. This is the step that sends.
- **edit** → revise, present again, wait again.
- **skip** → nothing happens.

Never send without an explicit yes for that reply. Several replies under one confirmation
only when the user explicitly says "send all of these".

Opt-out and not-interested (also gated — confirm, then act):

- `update_lead` with `status: "unsubscribed"` or `"not_interested"` — stops every running
  outreach for that lead.
- `add_blacklist` — suppress by email, domain, phone or LinkedIn URL when the person or
  company must never be contacted again.

## Output

Triage table first, then the drafts:

```
LEAD            CHANNEL    CLASS          NEEDS A REPLY?   AGE
<name>          email      positive       yes              2h
<name>          linkedin   opt-out        no — suppress    1d
```

Report what was sent, what was suppressed and what is still open — never a draft as if it
had been sent.

## Make it a loop

The platform ships a reply-triage workflow; **`agents-loops-goals`** shows how to run triage on
every reply event. Keep the send gate: an agent may classify and draft on its own, a human
approves what goes out.
