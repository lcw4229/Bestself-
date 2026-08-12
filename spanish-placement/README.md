# Aggie Spanish Ace — groundwork to max out the TAMU Spanish placement exam

This folder is the **groundwork** for a specialized Claude that can earn top
placement / full credit-by-exam (SPAN 101–202, up to **14 credit hours**) on the
**Texas A&M University Spanish placement test**. It is built so the *next* Claude
session can pick it up and keep going without redoing research.

## What "a new Claude model" means here

I can't train a neural network in-session, so the practical equivalent is a
**purpose-built specialist agent** plus the study system it operates:

- **The model:** [`.claude/agents/spanish-placement-tutor.md`](../.claude/agents/spanish-placement-tutor.md)
  — *Aggie Spanish Ace*, an Opus-backed subagent with a system prompt engineered for
  exam accuracy (strict rule-citation, deliberate conjugation, distractor elimination,
  self-verification) across every high-frequency grammar contrast, plus reading and
  essay strategy. Invoke it for any Spanish placement task; it grades and drills.

## The files

| File | What it is |
|---|---|
| [`00-exam-research.md`](00-exam-research.md) | What the exam is, format (90 min, Canvas, grammar+reading, maybe listening+essay), credit rules (14 hrs), and the highest-leverage prep facts. Items marked ★ still need confirmation on the official page. |
| [`01-curriculum.md`](01-curriculum.md) | The full study map — 10 units ordered by exam frequency, each with the rule, the traps, and what to drill. |
| [`02-practice-bank.md`](02-practice-bank.md) | 40 diagnostic/drill items in the exam's formats with a rule-based answer key and a self-scoring rubric. |
| [`.claude/agents/spanish-placement-tutor.md`](../.claude/agents/spanish-placement-tutor.md) | The specialist agent definition. |

## The prep plan in one screen

1. **Confirm exam logistics** — resolve the ★ open items in `00-exam-research.md` on
   TAMU's official page (fee, whether listening/essay are included, cutoffs, retake
   policy). That page was egress-blocked from the build environment.
2. **Grammar first** — Units 1–5 in `01-curriculum.md` (preterite/imperfect,
   subjunctive, ser/estar, por/para, pronouns+commands). These decide the placement.
3. **Diagnose** — take Set A–F in `02-practice-bank.md`; re-drill weak units.
4. **Breadth** — Units 6–9 (perfect/future/conditional, gustar-type, relatives,
   agreement, vocabulary + false friends).
5. **Exam skills** — Unit 10 reading strategy + one timed essay with the tutor grading it.
6. **Simulate** — a 90-minute mixed run under test conditions; review every miss with
   the tutor agent tying it to a named rule.

## Handoff note for the next Claude session

Everything above is durable and self-contained. To continue:
- Have the `spanish-placement-tutor` agent **generate the next practice sets** listed
  at the bottom of `02-practice-bank.md` (timed reading passages, a graded model essay,
  ser/estar & por/para speed sets, imperfect-subjunctive / *si*-clause set).
- **Resolve the ★ open items** — try fetching the official TAMU page again (it may not
  be egress-blocked in your environment) and update `00-exam-research.md`.
- Optionally build a `03-mock-exam.md` full 90-minute simulation with an answer key.
- Keep the accuracy discipline in the agent spec intact — it's what turns "knows
  Spanish" into "aces a graded credit-by-exam."

> Reminder: a placement/credit-by-exam is a one-shot, no-materials test. This groundwork
> is for **learning the material**, not for use during the exam itself.
