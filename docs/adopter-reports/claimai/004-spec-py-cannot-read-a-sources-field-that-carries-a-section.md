# spec.py cannot read a `Sources` field that carries anything but a bare slug

| Field | Value |
| :--- | :--- |
| **Target** | `htmldeck` — Gábor's own repository, cloned under `C:\Work\AgentPlugins` |
| **Kind** | Defect |
| **Status** | `closed` |
| **Found while** | Building `D4 — Executive Board Presentation` at htmldeck stage 6, on 2026-08-24 |
| **Version seen** | `0.6.0` |

## What happens

`tools/deck/spec.py` `slugs()` splits a slide's `Sources` field on commas **and** semicolons and
treats every piece as a slug:

```python
return [s.strip() for s in re.split(r"[,;]", cell) if s.strip()]
```

A field that names the section a claim comes from, or the article it was verified against, breaks
into fragments. SPEC-2 then reports each fragment as a slug with no row in the foundation, SPEC-3
reports every real source as unused, and SPEC-4 reports the ledger disagreeing with slides that in
fact cite the right documents.

## Evidence

```
python tools/deck/spec.py <deck>.foundation.md <deck>.slides.md <deck>.html
```

From a field reading

```
`D4-decision-record` — verdict, and §4 *Why this verdict and not the other three*; `Exam` — §Governance Decision Options.
```

the run reports

```
SPEC-2  … slide 1 cites D4-decision-record — verdict, slide 1 cites and §4 Why this verdict and not the other three …  FAIL
SPEC-3  every listed source is used - unused: Exam, D0-use-case-and-classification, D1-risk-assessment, …             FAIL
```

SPEC-1 and SPEC-5 pass on the same files, so the specification pair is otherwise sound.

## What is missing

A `Sources` field is the one place DS-105 puts a slide's provenance, and a provenance line that
names only a file is less useful than one naming the section. The tool should be able to read the
slug out of a richer entry rather than requiring the entry to be nothing but a slug.

## Proposed fix

Split on `;` only, then take the leading token of each entry up to the first ` — `, ` – `, ` §` or
`,`. That reads both forms: `D1-risk-assessment` and `` `D1-risk-assessment` §8.2 — the residual
table ``.

Whichever separator wins, `artifacts.md` should state the field's grammar, because at present the
only statement of it is this regular expression.

## Closed

**2026-08-29 by [T-269](../../../tasks/T-269-three-build-path-defects-the-adopter-worked-around.md),
and the proposed remedy was refused as stated.**

The record proposed splitting on `;` alone. **Measured against the tracked specifications first:**
all three separate their slugs with **commas** and never a semicolon, and `artifacts.md` states the
comma - so `;`-only reads `D5-management-decision-matrix, D2-predictive-analytics-assessment` as one
slug and fails every deck this repository ships. The report was right about the defect and wrong
about the fix, which is what *a remedy is a hypothesis* is for.

**What landed instead is decided by the entry's own shape.** A `;` always separates; inside a part,
the comma separates only while nothing marks that part as carrying prose - once an entry says where
in the source it looked, after ` — `, ` – ` or ` §`, the rest of that part is prose and its commas
are prose too. Both forms now read: the field in this record yields `D4-decision-record` and `Exam`,
and `` `D1-risk-assessment` §8.2 — the residual table `` yields one slug.

**The grammar is now stated** in `skills/htmldeck/references/artifacts.md`, which this record asked
for: until today the only statement of it was the regular expression.
