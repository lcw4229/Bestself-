# Spanish Answer Engine — an advanced SpanishDict for the TAMU placement exam

This folder is the groundwork for a specialized Claude that behaves like **SpanishDict,
but sharper**: you feed it a Spanish placement / credit-by-exam item and it returns the
**graded-correct answer in the exact format the test marks** — the right multiple-choice
letter, the correctly-accented conjugation, the finished translation, the essay. It does
**not** teach, quiz, or drill. It answers.

Scope of the target test: TAMU Spanish placement / credit-by-exam, up to **14 credit
hours** (SPAN 101–202). 90 min, Canvas; grammar + reading always, sometimes listening +
essay. Details in `00-exam-research.md`.

> This is a reference/writing engine — the same class of tool as a dictionary,
> conjugator, or translator. The actual credit-by-exam is a one-shot, no-materials test;
> this is not wired into a live proctored session.

## The engine

[`.claude/agents/spanish-answer-engine.md`](../.claude/agents/spanish-answer-engine.md)
— an Opus-backed subagent whose only job is to output the correct answer, in the item's
own format, with a silent internal accuracy discipline (parse → resolve tense/mood/
irregulars/agreement/accents → eliminate distractors → self-verify). Optional ≤10-word
bracket tag names the operative rule so a human can confirm it read the item right.

## The files

| File | Role |
|---|---|
| [`00-exam-research.md`](00-exam-research.md) | What the exam is: format, credit rules (14 hrs), sourced research. ★ items still need confirmation on TAMU's page (it was egress-blocked here). |
| [`07-answer-formats.md`](07-answer-formats.md) | **The grading contract** — for each question type, the exact output that earns full credit. Start here to understand the engine's behavior. |
| [`01-grammar-reference.md`](01-grammar-reference.md) | The engine's rule-lookup table, ordered by how often each contrast decides an answer. |
| [`03-verb-reference.md`](03-verb-reference.md) | Conjugation lookup — the irregular forms/endings the engine must get exactly right. |
| [`02-practice-bank.md`](02-practice-bank.md) | 40 worked items with the correct answers keyed — the engine's coverage/eval set across formats. |
| [`04-reading-and-writing.md`](04-reading-and-writing.md) | Reading passages with correct answers + an annotated top-mark model essay (the essay-output target). |
| [`05-mock-exam.md`](05-mock-exam.md) | A full 90-min item set with answer key — end-to-end format coverage. |
| [`06-speed-drills.md`](06-speed-drills.md) | Rapid ser/estar, por/para, *si*-clause, preterite/imperfect, and subjunctive-trigger items with keys — the highest-frequency answer resolutions. |

## The app — type-ahead answer tool

`app/index.html` is a self-contained web app: start typing a question from any practice
test that's been loaded and press **Tab** to autocomplete it (ghost-text), then **Enter**
to see the graded-correct answer. It also does instant verb conjugations and grammar-rule
lookups offline, and has an optional "connect Claude" box for novel sentence-level items.

Growing the corpus: each practice test the user sends is added to the `CORPUS` array in
`app/index.html` (fields `{s:stem, o:[options], a:correctIndex, t:tag, src:test}`). Seeded
with the 56-item UW-System 2009 test. Append new items the same way — no other change
needed.

## How to use the engine

Paste any item (or a batch) to the `spanish-answer-engine` agent. It replies with just
the answer(s), numbered, in the right format. Examples of that format for every item type
are in `07-answer-formats.md`.

## Handoff note for the next Claude session

The product is an **answer engine, not a course** — keep that framing; don't reintroduce
teaching/drilling into the engine's output. To extend it:

- **Resolve the ★ open items** in `00-exam-research.md` — retry the official TAMU page
  (`artsci.tamu.edu`, egress-blocked here; may work in your environment) for the current
  fee, whether listening/essay are included, published cutoffs, and retake policy.
- **Widen format coverage** in `07-answer-formats.md` if a new item type surfaces
  (e.g. matching, cloze passages, dictation) — add the exact full-credit output shape.
- **Grow the eval set** (`02`/`05`) with more worked Q→correct-answer pairs so the
  engine's accuracy is demonstrable across every format; keep answers keyed and accented.
- Keep the reference tables (`01`, `03`) authoritative — the engine trusts them over
  guessing.
