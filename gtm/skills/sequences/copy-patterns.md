# Copy patterns per channel and step

A structure, not templates to paste. Every pattern below is a slot arrangement: the argument
order stays fixed, the fills come from the row.

## The five relevance proofs

Every cold message is trying to earn one of these, in this order. Get three and you get a
reply; get one and you get silence.

1. **Show me you know me** — the person, not the company field.
2. **Show me you know my business** — what they actually do, their USP, their product.
3. **Show me you know my challenges** — in *their* words, not marketing language.
4. **Show me you solved this for someone like me** — a comparable company, a number.
5. **Show me value first** — something useful with no commitment attached.

Message one usually carries 1, 3 and 4. That is enough.

## The five building blocks

Every step is assembled from these; the channel decides the dosage.

| Block | Job | Typical slot |
|---|---|---|
| **Signal** | show it is *now* | `{{cell.signal}}` |
| **Problem** | name the pain in their words | `{{cell.pain_point}}`, `{{cell.consequence}}` |
| **Proof** | make it credible | `{{cell.case_customer}}`, `{{cell.case_result}}` |
| **Value** | what changes for them | `{{cell.benefit}}`, `{{cell.quick_win}}` |
| **Courtesy** | acknowledge, give an exit | fixed text |

Email carries more blocks per message and a longer argument. LinkedIn carries fewer, shorter.
Same blocks, different dosage.

---

## The salutation is its own column

Two forms, and nothing in between:

| Form | Looks like | When |
|---|---|---|
| **Formal** (default in DACH B2B) | `Sehr geehrter Herr Meier` · `Sehr geehrte Frau Meier` | anyone you have not met, any decision maker, always unless told otherwise |
| **Informal** | `Hi Max` | startups, peers, and only when the customer says so |

Never mix them inside one sequence, and never fall back to something neutral when the gender
is unclear. "Guten Tag Max Meier" and "Hallo zusammen" both announce that a machine wrote the
line.

Build it as an **`ai` column**, not a formula. A formula cannot infer gender from a first
name, cannot handle an academic title, and cannot tell you when it does not know:

```bash
gtm call workspace_table_add_column --input '{
  "table": "Contacts", "key": "salutation", "kind": "ai",
  "config": {
    "prompt": "Erzeuge die Anrede-Zeile für einen deutschen B2B-Geschäftsbrief.\n\nVorname: {{lead.first_name}}\nNachname: {{lead.last_name}}\nTitel/Position: {{lead.title}}\n\nREGELN\n1. Form: SIE (formal). Ergebnis ist immer \"Sehr geehrter Herr <Nachname>\" oder \"Sehr geehrte Frau <Nachname>\".\n2. Akademischen Grad aufnehmen, wenn erkennbar: \"Sehr geehrter Herr Dr. Meier\".\n3. Geschlecht aus dem Vornamen ableiten. Wenn nicht eindeutig (z. B. Kim, Alex, Andrea, nur Initiale, nur Nachname): confidence unter 0.8 setzen und salutation leer lassen. NICHT raten.\n4. Keine Grußfloskel, kein Komma am Ende, kein Satzzeichen.\n5. Umlaute korrekt ausschreiben.",
    "output_schema": {
      "type": "object",
      "properties": {
        "salutation": { "type": "string" },
        "gender": { "type": "string", "enum": ["m", "f", "unknown"] },
        "confidence": { "type": "number" }
      },
      "required": ["salutation", "gender", "confidence"]
    }
  }
}' --json
```

Then **gate the send on it**: `run_condition` on the enroll column,
`salutation.confidence >= 0.8`. A row whose gender could not be determined does not get a
guessed greeting, it gets held back. That is a handful of rows you write by hand, against a
whole campaign that opens with the wrong gender.

For the informal variant, the same column with rule 1 replaced by: *Ergebnis ist immer
`Hi <Vorname>`*, plus a rule that strips titles.

In the template the greeting is then one slot and a comma:

```
{{cell.salutation}},

Ich sah {{cell.signal}}. Spielen {{cell.pain_point}} bei {{company.name}} aktuell eine Rolle?
```

## No dashes in outbound copy

An em dash or a hyphen used as a sentence connector is the clearest tell that a language model
wrote the line. Two short sentences say the same thing and read as human:

| Not this | This |
|---|---|
| `Ich sah X — spielt Y eine Rolle?` | `Ich sah X. Spielt Y eine Rolle?` |
| `Kurz nachgefasst — will es nicht liegen lassen.` | `Kurz nachgefasst. Ich wollte es nicht liegen lassen.` |
| `Verstehe — hat gerade keine Priorität.` | `Verstehe. Das hat gerade keine Priorität.` |

Put it in the generation prompt as a hard rule, not in your review habit: *keine Gedankenstriche,
keine Bindestriche als Satzverbinder. Zwei kurze Sätze statt einem verbundenen.* A rule you
apply to the template you read does not hold on the variants you did not.

Same family, same reason: no bullet lists in a cold email, no bold inside the body, no emoji.

---

## Email — three steps

### Step 1 · the opener · ≤ 80 words

| Section | Purpose | Pattern |
|---|---|---|
| Subject, ≤ 5 words | trigger pain or benefit | `{{cell.pain_point}} bei {{company.name}}?` |
| Hook, 1 sentence | prove relevance | `Ich sah {{cell.signal}}. Offenbar spielt {{cell.pain_point}} gerade eine Rolle.` |
| Value, 1 sentence | benefit with a number | `{{cell.case_customer}} senkte {{cell.pain_point}} um {{cell.case_result}}.` |
| Proof, 1 sentence | make it comparable | `Läuft bei {{company.employee_count}} MA in {{company.industry}}.` |
| CTA, 1 question | validate, do not sell | `Spielt das bei Ihnen ebenfalls eine Rolle?` |

Argument order: **signal → problem → solution → validation**.

The CTA validates rather than books. "Does this play a role for you?" gets answered; "do you
have 15 minutes Thursday?" gets deleted. The calendar link belongs in the *reply* — a cold
body carries no links at all.

### Step 2 · the follow-up · ≤ 50 words

| Section | Pattern |
|---|---|
| Reference | `Kurz nachgefasst. Ich wollte es nicht liegen lassen.` |
| **New** proof | `{{cell.case_customer}}: {{cell.benefit}} in {{cell.timeframe}}.` |
| CTA | one question, different from step 1 |

The proof must be **new**. Repeating message one with more urgency is the single most common
follow-up, and it performs worse than not sending.

### Step 3 · the break-up · ≤ 30 words

| Section | Pattern |
|---|---|
| Plain speech | `Offenbar hat {{cell.solution}} gerade keine Priorität. Alles gut.` |
| Opt-out | `Ich lasse das ruhen, außer Sie melden sich.` |
| Door open | `Bei Bedarf genügt eine Nachricht.` |

Understanding → respect → open door. No guilt, no "last chance". A clean break-up produces
more later replies than a pushy one produces now, and it keeps the opt-out rate under 2 %.

### Subject lines that work

```
{{cell.pain_point}} bei {{company.name}}?
{{company.name}}: {{cell.pain_point}} reduzieren
Wie {{cell.case_customer}} {{cell.pain_point}} löste
```

Under five words. No "quick question", no false familiarity, no `Re:` on a thread that never
existed.

---

## LinkedIn — four touches

| # | Step | Limit | Blocks |
|---|---|---|---|
| 1 | Connect | ≤ 50 chars, or **empty** | Signal |
| 2 | Opener (0–2 days after accept) | ≤ 150 chars | Signal + Problem |
| 3 | Follow-up (3–4 days later) | ≤ 250 chars | Problem + Proof + Value |
| 4 | Break-up (5–7 days later) | ≤ 100 chars | Courtesy + Value |

**Touch 1 — connect.** Empty is the strong default; it is accepted more often than a note
carrying a pitch. If you write one: `{{cell.signal}} fiel mir in Ihrem Feed auf. Verbinden
wir uns?`

**Touch 2 — opener.** Thanks → signal → validating question. Still no pitch.

> Danke fürs Annehmen, Herr {{lead.last_name}}. Ich sah {{cell.signal}}. Spielen
> {{cell.pain_point}} bei {{company.name}} aktuell eine Rolle?

**Touch 3 — follow-up.** The only step that pitches, and it pitches in four lines:

> Kurz und konkret, Herr {{lead.last_name}}:
> {{cell.consequence}}
> Ergebnis: {{cell.benefit}} bei {{cell.case_customer}}
> Für Sie: {{cell.quick_win}}
> 15 Minuten prüfen, ob das passt?

**Touch 4 — break-up.** `Verstehe, das hat gerade keine Priorität. Ich lasse das ruhen. Bei
Bedarf genügt eine Nachricht.`

**LinkedIn rules:** 300 characters is the ceiling for any touch — it is not a blog. Only
trigger on a signal younger than seven days. One variable per argument. Delete every
"synergy", "exciting" and "disruptive".

### LinkedIn KPI targets

| Metric | Target | If below |
|---|---|---|
| Connection acceptance | > 30 % | the profile or the note, not the sequence |
| Reply rate on the opener | > 10 % | signal quality or persona |
| Meeting rate off the follow-up | > 2 % | the offer, or the proof is not comparable |
| Opt-out rate | < 2 % | the break-up is too pushy |

All below target at once? The signal quality or the persona is wrong. Do not rewrite the
template — the template is rarely the problem.

---

## WhatsApp — two touches, maximum

The most intimate channel, and the least forgiving. Rules, not preferences:

- **2–3 sentences, under 300 characters.** It has to work on a lock screen.
- **A local hook** from the source data: the town, the trade, a visible detail.
- **No link in the first message.** Links trigger spam heuristics and cost trust.
- **An explicit opt-out**: "ein kurzes Nein genügt". This lowers complaints, and complaints
  are what cost you the number.
- **The offer comes in message two**, after a reaction — never in message one.
- **One follow-up after 3–4 days, then stop.** WhatsApp does not forgive persistence.

> {{cell.salutation}}, ich sehe, Sie betreiben {{company.name}} in {{company.city}}. Wir
> helfen {{cell.industry_short}} dabei, {{cell.quick_win}}. Wäre das interessant? Ein kurzes
> Nein genügt.

Two obligations run in parallel here and they are not the same: the platform's business
rules (violations cost the number, without warning) and data protection (a business mobile
number is personal data — you need a documented legal basis, transparent provenance and an
easy objection). Neither this file nor the platform is legal advice.

---

## The pre-send check

Run every generated message through this before enrolling. It is cheap and it catches the
expensive mistakes.

- [ ] **The competitor test.** Would line one also fit the recipient's competitor? Then it is
      not personalisation, it is a mail merge.
- [ ] **The salutation is complete and correctly gendered** — `Sehr geehrter Herr Meier` or
      `Sehr geehrte Frau Meier`, or `Hi Max` if the campaign is informal. Never a neutral
      fallback, never a guess below 0.8 confidence.
- [ ] **No dashes as sentence connectors.** Two short sentences instead. This is the loudest
      AI tell in the message.
- [ ] Is there a **real trigger** in line one?
- [ ] Concrete **result plus timeframe**, or no proof claim at all?
- [ ] **No empty slots** — check against a real row, including a sparse one.
- [ ] No filter vocabulary: "kostenlos", "garantiert", "Angebot", caps blocks, multiple
      exclamation marks.
- [ ] No empty superlatives, no meeting pressure.
- [ ] **No links, no tracking** in a cold body.
- [ ] Correct form of address — DACH B2B is formal "Sie" unless stated otherwise.
- [ ] Would *you* answer this?

When a model writes the copy, this checklist belongs **inside the prompt** as a negative
list. A rule you apply to the template you reviewed does not hold on the 3,999 variants you
did not.

## Generating fills, not messages

The reliable arrangement: a fixed template with a small number of generated values, each
produced by its own column with its own `output_schema`.

| Column | Prompt job | Output |
|---|---|---|
| `salutation` | the complete greeting, gendered, with title | `Sehr geehrte Frau Dr. Meier` |
| `signal` | strongest current trigger from news, postings, activity | 1–2 words |
| `pain_point` | likely challenge given size and industry | 3–4 words |
| `case_customer` | pick the matching case study by size and industry | one name from a **fixed list** |
| `quick_win` | what changes for them, in six words | short phrase |

Every one of those returns a short, typed, checkable value. The message is assembled from
them. That is what makes 4,000 rows read like 4,000 written messages instead of 4,000
variations on a hallucination — and what makes a bad campaign debuggable, because you can see
which column produced the weak fill.
