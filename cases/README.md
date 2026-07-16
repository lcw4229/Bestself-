# Case documents

Put client documents for a matter in a subfolder here, e.g.:

```
cases/
  smith-v-jones/
    medical-records-stjoseph.pdf
    police-report.pdf
    lost-wages-letter.pdf
    drafts/            <- demand-letter drafts are written here
    extractions/       <- document-analyzer output can be saved here
```

Then ask in plain language, e.g.:

> Draft a demand letter for the smith-v-jones matter from the documents in its folder. Demand $85,000, 30-day deadline.

The orchestrator will analyze each document in parallel and produce a draft in
`drafts/` with every fact cited back to its source, plus a review checklist.

**Confidentiality:** everything in this folder except this README is
git-ignored and stays local to the session — client documents are never
committed or pushed. Files exist only for the life of the session's container,
so upload them (or sync from a connected source) each session, and download
any drafts you want to keep.

**All output is a first draft** and requires attorney review before sending.
