# Project instructions for Claude Code

## Delegation policy (always in effect — do not wait to be reminded)

This project has specialist subagents in `.claude/agents/`. Route work to them
automatically; the user will phrase tasks in plain language and will NOT split
them up, name an agent, or specify file paths. Interpreting and dividing the
work is Claude's job, not the user's.

Routing rules:

1. **Multi-step, vague, or compound requests** (anything that touches more than
   one specialty, or whose scope isn't spelled out — "make sure X works",
   "clean up Y", "why is Z broken?") → delegate to the **orchestrator** agent,
   passing the user's request verbatim. It interprets the task, finds the
   relevant code itself, fans out to the specialists, and returns one answer.
2. **Single-focus requests** go straight to the matching specialist:
   - locating code, symbols, usages → **code-explorer**
   - running or checking tests → **test-runner**
   - security or vulnerability review → **security-reviewer**
   - looking up external docs, libraries, URLs → **doc-fetcher**
   - digesting logs, build/CI output, crash dumps → **log-analyzer**
   - reading/summarizing a single case or legal document → **document-analyzer**
   - any single file over ~50 pages / ~5 MB (voluminous records, depositions,
     huge logs or data files) → **large-document-analyzer**
   - drafting or revising a demand letter (extractions already done) →
     **demand-letter-drafter**
   - anything involving a whole matter or multiple case documents ("draft a
     demand letter for X", "review the Smith file") → **orchestrator**
3. Keep heavy output out of the main conversation: prefer a subagent whenever a
   step would dump large files, full test output, whole web pages, or long logs
   into context.
4. Never ask the user which agent to use or where code lives — decide, act, and
   state any assumptions made in the final answer.

Do the work directly (no subagent) only when it's a quick edit or question
where delegation adds more overhead than it saves.

## Legal work — confidentiality (non-negotiable)

- Client/case documents live under `cases/<matter>/` and are git-ignored.
  NEVER commit, push, or transmit them (or drafts derived from them) to any
  external service, and never weaken `cases/.gitignore`.
- Every drafted letter is a DRAFT requiring attorney review; keep the draft
  header and review checklist intact.
- The firm letter template lives at `templates/demand-letter.md`.
