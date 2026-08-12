# Exam sources & the corpus ("memory")

The app's `CORPUS` (in `app/index.html`) is the durable "memory": every question added
there autocompletes and returns its graded-correct answer. As of this note it holds
**190 items**:

| Source | Items | Notes |
|---|---|---|
| `UW-2009` | 56 | University of Wisconsin System Spanish placement **practice** exam (public), answered 56/56 against its printed key. |
| `Test 2` | 45 | Vocabulary/dialogue/reading test the user supplied (choices were blank; answers are the correct word/phrase, verified). |
| `Bank L2–L4` + `Bank Adv` | 63 | Authored, answer-checked items at **intermediate→advanced** level. Trivial L1 items were removed on purpose. |
| `Canterbury` | 26 | Canterbury School placement exam (public PDF; blank/no key). Preterite-vs-imperfect, ind/subj/inf, question formation, and error-correction (calques/false friends). Answers authored & verified. |

**MTEL Spanish (28)** was downloaded and reviewed but NOT bulk-ingested: it's a
teacher-licensure exam (C1/C2 — listening + reading + pedagogy), not the discrete-grammar
placement format, and its answer key is a multi-column worksheet that doesn't extract
cleanly. Kept as advanced reading-comprehension stretch material; ingest selectively only
if desired.

## Quality bar (do not lower it)

This is a placement/credit-by-exam graded by proficiency: distractors are built so that a
*merely acceptable* answer places the student LOW. Rules for every item added:

- **Stay at placement level.** No trivial "yo soy estudiante" items — they don't
  discriminate at the top, where high placement is decided. Removed the L1 set for this reason.
- **Distractors must include a lower-level-but-not-best trap**, and the key must be the
  **highest correct register/structure**: the right subjunctive *tense in sequence* (imperfect/
  pluperfect after a past main verb, not present subjunctive), the exact *si*-clause pairing,
  subjunctive after superlative+*que* / *no es que* / *el hecho de que* / concessive *por
  más/mucho que*, the standard DO pronoun (not *leísmo*), irregular participles (not regularized).
- The `spanish-answer-engine` spec encodes this as "Choose the HIGHEST-level correct answer."
  Keep that principle intact; it's the whole point.

## Why the web wasn't scraped in this session

This environment's **network egress policy blocks outbound fetching** of exam sites.
Confirmed `EGRESS_BLOCKED` (403-class org policy denials, not TLS issues) on: `artsci.tamu.edu`,
`www.depts.ttu.edu` (Texas Tech CBE review sheets), `www.123teachme.com`, `studyspanish.com`.
`WebSearch` returns snippets but `WebFetch` is denied, so full exams can't be pulled here.
Policy denials must not be bypassed — they're reported, not retried.

## Public sources to pull from a session WITH open egress

A future session (or a local run) with web access should extract items from these public
practice exams and append them to `CORPUS` (verify each answer independently — don't trust
scraped keys blindly):

- **Texas Tech K-12 CBE review sheets** (Spanish 1A/1B/2A/2B/3A, with answer keys) —
  `depts.ttu.edu/k12/cbe/review/` and the `.../pdfs/spanNx.pdf` files.
- **University of Wisconsin System** placement practice exam (the one already ingested) —
  `testing.wisc.edu`.
- **AP Spanish Language & Culture** past free-response + MC samples — `apcentral.collegeboard.org`
  (useful for the writing prompts and advanced grammar).
- Department placement/credit-by-exam practice pages (UC Riverside Hispanic Studies, Yale
  Spanish & Portuguese FAQ, and similar) surfaced via WebSearch.
- General graded item sources: `studyspanish.com` grammar tests, `123teachme` placement test.

## How to add items (keep this format)

Append to the `CORPUS` array in `app/index.html`:

```js
// multiple choice
{src:"<Test name>", s:"<stem with ___>", o:["opt a","opt b","opt c","opt d"], a:<correctIndex 0-3>, t:"<rule/kind tag>"},
// open answer (no options)
{src:"<Test name>", s:"<stem>", ans:"<correct word/phrase>", t:"<tag>"},
```

Verify every answer against the grammar in `../01-grammar-reference.md` and the conjugator;
tag reading items `reading: <passage>` and open-content dialogue items `open — sample`.
