# Answer-Format Spec — what "graded-correct" looks like per item type

This is the engine's grading contract: for every question format the TAMU Spanish
placement / credit-by-exam uses, the **exact output that earns full credit**. The
`spanish-answer-engine` agent follows this. No teaching — just the right answer, right
format.

The reference material the engine resolves answers from:
`01-grammar-reference.md` (rules) and `03-verb-reference.md` (conjugations).

---

## 1. Multiple choice (grammar / vocabulary)

**Input:** stem + options a–d.
**Full-credit output:** the letter **and** the exact option text. Nothing else needed.

```
Input : Espero que tú ____ bien. a) estás b) estés c) estabas d) estarás
Output: b) estés
```

Optional verify tag: `b) estés  [esperar que → present subjunctive]`

## 2. Fill-in-the-blank conjugation

**Input:** sentence with a blank and an infinitive cue.
**Full-credit output:** only the word(s) for the blank(s), correctly accented; multiple
blanks separated by ` / ` in order.

```
Input : Ayer yo ____ (ver) una película.        →  vi
Input : La casa ____ (ser) grande y ____ (tener) jardín.  →  era / tenía
Input : Cuando ____ (llegar, yo) mañana, te llamo.  →  llegue
```

## 3. Sentence transformation

Return the **full rewritten sentence**, correctly accented. Covers:

- **Pronoun replacement:** `Escribí una carta a María.` → `Se la escribí.`
- **Double-object + command:** `Dame el libro.` → `Dámelo.` · `No des el dinero a él.`
  → `No se lo des.`
- **Affirmative→negative command:** `Habla.` → `No hables.`
- **Tense shift:** "Put in preterite: *Como paella.*" → `Comí paella.`
- **Active→passive / passive-se:** `Venden libros aquí.` → `Se venden libros aquí.`

## 4. Translation (either direction)

**Full-credit output:** the single best sentence in the target language, accented and
punctuated (¿ ¡). If a second rendering is genuinely valid, add one `alt:` line.

```
Input : "I have known her for two years."
Output: Hace dos años que la conozco.
alt:    La conozco desde hace dos años.
```

Graders reward: correct tense/mood, ser/estar, por/para, gustar-structure, personal *a*,
agreement, accents. A literal word-for-word calque that breaks any of those is **not**
full credit even if "understandable."

## 5. Reading comprehension

- **Multiple choice:** letter + option text (as §1).
- **Open-ended (answer in Spanish):** one complete, correct sentence that answers exactly
  what's asked, drawn from the passage.
  ```
  Input : ¿Por qué aceptó Marta el proyecto?
  Output: Lo aceptó porque sabía que la experiencia la ayudaría en su carrera.
  ```
- **Vocabulary-in-context:** the option/synonym that survives substitution into the
  sentence.

## 6. Essay / written prompt

**Full-credit output:** a finished, submission-ready essay at the requested length —
nothing before or after it. It must visibly sustain range, because that is the rubric:

| Rubric dimension | What the output must contain |
|---|---|
| Task completion | Addresses every part of the prompt; clear thesis → support → conclusion |
| Grammatical range | ≥1 correctly-triggered subjunctive; a preterite/imperfect contrast; a compound or future/conditional tense |
| Accuracy | Flawless agreement, ser/estar, por/para, accents |
| Cohesion | Connectors: *sin embargo, por lo tanto, aunque, ya que, además, por otro lado* |
| Lexical range | Varied, precise vocabulary; no repeated basic words |

A worked, annotated model at the target register is in `04-reading-and-writing.md`.

## 7. Listening (if the version includes it)

Transcribe/parse the prompt, then answer in the item's format (§1 or §5). Same accuracy
discipline; the answer format does not change.

---

## Format quick-reference

| Item type | Output shape |
|---|---|
| Multiple choice | `letter) exact option text` |
| Fill-in-blank | just the accented word(s), `/`-separated for multiple blanks |
| Transformation | the full rewritten, accented sentence |
| Translation | one best sentence (+ optional `alt:`) |
| Reading MC | `letter) option text` |
| Reading open | one correct Spanish sentence |
| Essay | the finished essay only, at requested length |

**Verify tags** (bracketed, ≤10 words, naming the operative rule) are optional and exist
only so a human can confirm the engine read the item correctly — they are not part of the
graded answer and can be stripped.
