# Copy: the template doctrine

**Never write 1:1 personalised messages.** Not per lead, not "the model writes something
tailored". Always a **proven, deterministic template** with a small number of meaningful
variables, and a systematic A/B test on the CTA.

The reason is not style, it is control. A template you tested is a thing you can improve; four
thousand individually generated messages are four thousand unverified drafts. Predictability
is the product: the same shape at 40 rows and at 4,000, and when the reply rate moves you know
which part moved it.

---

## The five relevance proofs

Every cold message is trying to earn these, in this order. Three of five gets a reply; one gets
silence.

1. **Show me you know me** — the person, not the company field.
2. **Show me you know my business** — what they actually do.
3. **Show me you know my challenges** — in *their* words, not marketing language.
4. **Show me you solved this for someone like me** — a comparable company, a number.
5. **Show me value first** — something useful with no commitment attached.

Message one carries 1, 3 and 4. The lead magnet carries 5. That is the whole design.

The five building blocks it is assembled from, and the channel decides the dosage:

| Block | Job | Where it lives |
|---|---|---|
| **Signal** | show it is *now* | `{{hook}}`, generated |
| **Problem** | name the pain in their words | value prop, fixed |
| **Proof** | make it credible | value prop, fixed: a name and a number |
| **Value** | what changes for them | lead magnet, fixed |
| **Courtesy** | acknowledge, give an exit | fixed |

Email carries a longer argument, LinkedIn a shorter impulse. Same blocks, different dosage.

## The skeleton

Five parts. **Maximum three paragraphs.** Everything that is not a variable is fixed template
text that you wrote once, read once, and approved.

```
{{anrede}},

{{hook}}                     ← the only per-lead sentence, tied to the signal

<value prop: template, benefit-oriented, with a concrete reference>

<lead magnet: one attractive, zero-commitment offer>

{{signatur}}
```

| Part | Generated? | Rule |
|---|---|---|
| `{{anrede}}` | yes | `Sehr geehrter Herr Meier` / `Sehr geehrte Frau Meier`, or `Hi Max`. Its own prompt column |
| `{{hook}}` | yes | **one** sentence, references the signal, max 140 characters, no question |
| Value prop | **no** | fixed text. Benefit-oriented, with a named reference and a number |
| Lead magnet | **no** | fixed. One concrete, no-commitment offer |
| `{{signatur}}` | per sender | fixed per sender, plain text |

Two generated fields per message. Everything else is text a human wrote and approved.

**Why so few:** every generated field is a place the message can break at scale, and each one
you add makes the break harder to locate. Two are enough to make a message specific. Five make
it read like a form letter with more slots.

## No pitch, and nothing that trips the sales reflex

A reader decides in about two seconds whether this is a sales email. Once that switch flips,
nothing in the rest of the message is read. The whole craft is staying under that threshold.

What trips it, in rough order of severity:

| Trips it | Instead |
|---|---|
| "Ich möchte Ihnen unser Produkt vorstellen" | say what changed for a comparable company |
| "Wir sind der führende Anbieter für …" | no self-description at all in message one |
| Urgency: "nur diese Woche", "letzte Chance" | no urgency. There is none, and they know it |
| Fake familiarity: "Wie versprochen", `Re:` on a thread that never existed | write as a stranger, politely |
| Flattery: "Ich bin beeindruckt von Ihrem Wachstum" | state the observed fact, without the verdict |
| A calendar link in a cold body | offer the lead magnet, deliver it in the reply |
| Three questions stacked at the end | one question |
| "Kurze Frage" as an opener | just ask it |
| Feature lists, bullet points, bold text | three plain paragraphs |
| Superlatives with nothing behind them | a number and a name, or nothing |

**The value prop is not a pitch when it is about them.** "Musterverwaltung Nord spart 12
Stunden pro Woche in der Poststelle" is an observation about a comparable company. "Unsere
Software spart Ihnen Zeit" is a claim about you. Same fact, and only one of them gets read.

**No pressure anywhere, including the break-up.** "Falls ich nichts höre, gehe ich davon aus,
dass kein Interesse besteht" is pressure wearing a polite jacket. "Ich lasse das ruhen. Bei
Bedarf genügt eine Nachricht" is not, and it produces more later replies.

The test before sending: **would a colleague you respect write this to someone they might meet
at a conference?** If it would embarrass you in person, it does not improve at scale.

## The value prop names a reference and a number

Not what the product is. What changes for them, with a name and a number attached:

| Weak | Strong |
|---|---|
| "Wir bieten KI-gestützte Vertriebsautomatisierung." | "Musterverwaltung Nord hat die Recherchezeit pro Lead von 20 auf 4 Minuten gesenkt." |
| "Unsere Lösung verbessert Ihre Prozesse deutlich." | "Musterbau bearbeitet heute dreimal so viele Anfragen mit demselben Team." |

Rules for the reference: real, named, with a real number and a real timeframe, and comparable
in size and industry to the recipient. One reference, not three. If you have none for this
vertical, that is a finding about which vertical to run, not a licence to write "viele Kunden".

## The lead magnet carries the CTA

A meeting is a commitment. A lead magnet is not, which is why it converts a colder audience. It
has to be **concrete, immediately useful, and free of obligation**:

| Works | Does not |
|---|---|
| "Ich habe eine Liste mit 40 passenden Accounts zusammengestellt. Soll ich sie schicken?" | "Gerne sende ich Ihnen weitere Informationen." |
| "Eine zweiseitige Auswertung Ihrer Zustellbarkeit, in 24 Stunden, kostenlos." | "Lassen Sie uns unverbindlich sprechen." |
| "Der Benchmark-Report für Ihre Branche 2026." | "Auf unserer Website finden Sie mehr." |

The strong ones name a deliverable, a size and a timeframe. The weak ones ask for time and
offer nothing.

**No links in a cold body.** The lead magnet is offered as a question and delivered in the
reply. That is the deliverability rule, and it doubles as qualification: someone who asks for
it has raised their hand.

## A/B test the CTA, systematically

The CTA is the highest-leverage line and the cheapest to test, because everything else stays
identical.

1. **Two variants at a time.** Not four, and never "let the model vary it".
2. **One difference.** Same hook, same value prop, same lead magnet, same send window. Only the
   closing question changes.
3. **Split by row, not by day.** A formula column assigning `A`/`B` on an even/odd row index.
   Splitting by time confounds the test with the week.
4. **Wait for the number.** Below roughly 100 leads per variant a difference is noise. Of the
   messaging angles recorded across all workspaces, only about a quarter ever received traffic
   and fewer produced a result. An angle without volume is an opinion, not a test.
5. **Keep the winner as the new baseline**, retire the loser, and record *why* in the messaging
   angle asset so nobody re-runs it next quarter.

Families worth testing against each other:

| Family | Example |
|---|---|
| **Validating question** | "Spielt das bei Ihnen gerade eine Rolle?" |
| **Lead magnet offer** | "Soll ich Ihnen die Auswertung schicken?" |
| **Permission** | "Darf ich Ihnen dazu zwei Sätze schicken?" |
| **Direct** | "Passen 15 Minuten nächste Woche?" |

In the platform data, cold email carrying a question reaches a materially higher positive share
than cold email without one. So the baseline is a question. What you are testing is *which*.

## Follow-ups: a different angle every time

A follow-up is **not** the same message with more urgency. Every step runs a **different
messaging angle**, meaning a different reason to care:

| Step | Angle | Carries |
|---|---|---|
| 1 | the signal | why now, why them |
| 2 | proof | a different reference, a different outcome |
| 3 | cost of inaction | what the problem costs while it stays unsolved |
| 4 | break-up | understanding, exit, open door |

Each step gets its own lead magnet, or the same one framed differently. "Ich wollte nur nochmal
nachfassen" is not an angle. It is the absence of one, and it performs accordingly.

Angles live in the messaging angle asset, versioned, so a loser is retired with its evidence
rather than by opinion.

## One vertical per playbook

**Maximum one vertical per playbook.** Not "Fertigung und Logistik". Not "Mittelstand DACH".
One.

The template only works if the value prop, the reference and the lead magnet are fixed text,
and fixed text is only credible when everyone receiving it has the same problem. Two verticals
means either two sets of fixed text (two playbooks wearing one name) or one set that fits
neither.

This is also the strongest measured pattern in the platform data: narrow ICPs reply at roughly
twice the rate of broad ones. The template doctrine and the narrow-ICP finding are one rule
seen from two sides.

## Length: shorter wins, measurably

Within one channel, positive reply share falls as messages get longer. On email the gradient is
monotonic across four length buckets, and messages under 50 words reach roughly 2.5 times the
positive share of messages over 150. WhatsApp points the same way.

| Channel | Target |
|---|---|
| Email step 1 | **max 80 words**, three paragraphs |
| Email follow-up | max 50 words |
| Email break-up | max 30 words |
| LinkedIn connect | empty note, or max 50 characters |
| LinkedIn message | max 250 characters |
| WhatsApp | max 300 characters, 2 to 3 sentences |

Write shorter than feels right. Delete every adjective that proves nothing.

---

## The salutation is its own column

Two forms, nothing in between:

| Form | Looks like | When |
|---|---|---|
| **Formal** (default in DACH B2B) | `Sehr geehrter Herr Meier` · `Sehr geehrte Frau Meier` | anyone you have not met, any decision maker, unless told otherwise |
| **Informal** | `Hi Max` | startups, peers, and only when the customer says so |

Never mix them in one sequence, and never fall back to something neutral when the gender is
unclear. "Guten Tag Max Meier" and "Hallo zusammen" both announce that a machine wrote the line.

Build it as an **`ai` column**, not a formula. A formula cannot infer gender from a first name,
cannot handle an academic title, and cannot tell you when it does not know:

```bash
gtm call workspace_table_add_column --input '{
  "table": "Contacts", "key": "anrede", "kind": "ai",
  "config": {
    "prompt": "Erzeuge die Anrede-Zeile für einen deutschen B2B-Geschäftsbrief.\n\nVorname: {{lead.first_name}}\nNachname: {{lead.last_name}}\nTitel: {{lead.title}}\n\nREGELN\n1. Form: SIE. Ergebnis ist immer \"Sehr geehrter Herr <Nachname>\" oder \"Sehr geehrte Frau <Nachname>\".\n2. Akademischen Grad aufnehmen, wenn erkennbar: \"Sehr geehrter Herr Dr. Meier\".\n3. Geschlecht aus dem Vornamen ableiten. Wenn nicht eindeutig (Kim, Alex, Andrea, nur Initiale, nur Nachname): confidence unter 0.8 und salutation leer lassen. NICHT raten.\n4. Keine Grußfloskel, kein Komma am Ende.\n5. Umlaute korrekt ausschreiben.",
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

Then **gate the send on it**: `run_condition` on the enroll column, `anrede.confidence >= 0.8`.
A row whose gender could not be determined is held back rather than greeted with a guess. A
handful of rows written by hand, against a whole campaign opening with the wrong gender.

For the informal variant, the same column with rule 1 replaced by *Ergebnis ist immer
`Hi <Vorname>`*, plus a rule that strips titles.

## The hook is the other generated field

One sentence, tied to the signal, no question, max 140 characters. Its own column, its own
schema:

```
Prompt: Schreibe EINEN Satz, der auf das beobachtete Signal Bezug nimmt.

INPUT   Signal: {{cell.signal}} · Beleg: {{cell.signal_grund}} · Firma: {{company.name}}
REGELN  1. Genau ein Satz, höchstens 140 Zeichen.
        2. Nur das Signal. Keine Wertung, kein Pitch, keine Frage.
        3. Keine Gedankenstriche. Keine Floskeln ("spannend", "beeindruckend").
        4. Sie-Form.
        5. Wenn das Signal fehlt oder älter als 28 Tage ist: hook leer lassen.
OUTPUT  { "hook": "…", "usable": true|false }
```

Gate the enroll column on `hook.usable == true`. A message whose first line has nothing
specific in it is exactly the generic email you were trying not to send.

## Remove every AI trace

The dash is the loudest one, but it is not the only one. Every item below makes a reader think
"a machine wrote this", and that thought costs more than a weak sentence would.

**Punctuation and typography**

| Trace | Fix |
|---|---|
| An em dash or hyphen joining two clauses | two short sentences |
| Semicolons in a short message | a full stop |
| "…" as a trailing pause | end the sentence |
| Curly quotes mixed with straight ones | one style, consistently |
| Bold inside the body | none |
| Bullet lists in a cold email | three plain paragraphs |
| Emoji | none in a first message |

| Not this | This |
|---|---|
| `Ich sah X — spielt Y eine Rolle?` | `Ich sah X. Spielt Y eine Rolle?` |
| `Kurz nachgefasst — will es nicht liegen lassen.` | `Kurz nachgefasst. Ich wollte es nicht liegen lassen.` |
| `Verstehe — hat gerade keine Priorität.` | `Verstehe. Das hat gerade keine Priorität.` |

**Vocabulary that only models use in German business mail**

"spannend", "beeindruckend", "ganzheitlich", "innovativ", "nachhaltig" as filler,
"maßgeschneidert", "Synergien", "disruptiv", "in der heutigen schnelllebigen Zeit",
"Es freut mich, Sie zu kontaktieren", "Ich hoffe, diese Nachricht erreicht Sie gut".

**Structure that gives it away**

- Three sentences of exactly the same length in a row.
- A perfectly balanced "einerseits / andererseits" in a four-line message.
- A closing sentence that summarises what was just said.
- Every paragraph starting with the same word.
- The same adjective appearing in every variant across the batch, which is what happens when
  the model has one favourite and nobody read twenty rows.

**Put all of it in the generation prompt as a negative list**, not in your review habit. A rule
you apply to the template you read does not hold on the variants you did not. And read twenty
generated rows side by side before enrolling: single messages look fine, batches expose the
tics.

---

## Worked example: email step 1

Fixed template, two generated fields, three paragraphs, 61 words.

```
{{anrede}},

{{hook}}

Wir helfen Hausverwaltungen dabei, den Posteingang zu digitalisieren.
Musterverwaltung Nord spart damit seit Januar rund 12 Stunden pro Woche
in der Poststelle.

Ich habe eine kurze Auswertung vorbereitet, was das bei Ihrer Objektzahl
bedeutet. Soll ich sie Ihnen schicken?

{{signatur}}
```

- `{{anrede}}` → `Sehr geehrte Frau Krüger`
- `{{hook}}` → `Sie haben im August zwei neue Objekte in Kassel übernommen.`
- Value prop, reference, lead magnet and CTA: **fixed text**, written once, reviewed once.
- The A/B variant changes exactly one line: `Soll ich sie Ihnen schicken?` against
  `Spielt das bei Ihnen gerade eine Rolle?`

## Worked example: LinkedIn

| # | Step | Content |
|---|---|---|
| 1 | `linkedin_invite` | **empty note** |
| 2 | `linkedin_message` | `{{anrede}}, danke fürs Annehmen. {{hook}} Spielt das bei {{company.name}} eine Rolle?` |
| 3 | `linkedin_message` | different angle: proof. Fixed text, one reference, one number |
| 4 | `linkedin_message` | break-up, max 100 characters |

Same doctrine, shorter format: two generated fields, everything else fixed.

### LinkedIn targets

| Metric | Target | If below |
|---|---|---|
| Connection acceptance | > 30 % | the profile or the note, not the sequence |
| Reply rate on the opener | > 10 % | signal quality or persona |
| Meeting rate off the follow-up | > 2 % | the offer, or the proof is not comparable |
| Opt-out rate | < 2 % | the break-up is too pushy |

All four below target at once means the signal quality or the persona is wrong. Do not rewrite
the template; the template is rarely the problem.

## Worked example: WhatsApp

```
{{anrede}}, {{hook}} Wir helfen Betrieben in {{company.city}} dabei,
{{fixed: benefit}}. Ich schicke Ihnen gern die Kurzauswertung dazu.
Ein kurzes Nein genügt.
```

Under 300 characters, no link, explicit opt-out, the offer in message two after a reaction.

---

## The pre-send check

- [ ] **Is this a template with at most two generated fields?** If the whole body was
      generated, stop.
- [ ] **Three paragraphs maximum**, and under the channel word limit.
- [ ] **The competitor test** on the hook: would it also fit the recipient's competitor?
- [ ] **The value prop names a reference and a number**, and the reference is comparable.
- [ ] **The lead magnet is concrete**: a deliverable, a size, a timeframe. Not "more
      information".
- [ ] **The salutation is complete and correctly gendered.** No neutral fallback, no guess
      below 0.8 confidence.
- [ ] **No dashes as sentence connectors**, and no other AI trace from the list above.
- [ ] **Does not read as a pitch.** No self-description, no urgency, no flattery, no
      superlatives, one question.
- [ ] **Would a colleague you respect send this** to someone they might meet at a conference?
- [ ] **No links, no tracking** in a cold body.
- [ ] **No empty slots**, checked against a real row including a sparse one.
- [ ] **This follow-up carries a different angle** than the step before it.
- [ ] Would *you* answer this?

When a model writes any part of this, the checklist belongs **inside the prompt** as a negative
list. A rule you apply to the template you reviewed does not hold on the variants you did not.
