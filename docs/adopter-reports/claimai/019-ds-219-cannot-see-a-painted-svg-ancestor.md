# DS-219 cannot see a painted SVG ancestor, so a light label on a filled panel can never pass

| Field | Value |
| :--- | :--- |
| **Target** | `htmldeck` — Gábor's own repository, cloned under `C:\Work\AgentPlugins` |
| **Kind** | Defect |
| **Status** | `open` |
| **Severity** | High — the rule is unsatisfiable for a whole class of correct diagrams, so a deck carries a permanent failure it cannot fix |
| **Found while** | Naming the launch conditions on a slide of their own, on 2026-08-24 — `E41`; hit again on 2026-08-26 — `E45` |
| **Version seen** | 0.6.0 |

## What happens

`DS-219` requires a label sitting on a data mark to clear **3:1 against the ground**. To find the
ground it walks to the text run's *nearest painted background* — and it stops at the mark. It does
not see that the mark itself sits on a painted panel.

So a pale label on a pale card, where the card rests on a filled panel, is measured against the card
alone. The pair can never reach 3:1, however the deck is coloured, because the two are meant to be
close: the panel supplies the contrast a reader actually uses.

`D4 — Executive Board Presentation` fails `DS-219` at **40 of 46** labels and has since the build.
Every attempt to fix it made the slide worse, because the rule is asking for a difference the design
deliberately does not have at that level.

## The repository already doubts this rule

`docs/DESIGN-RATIONALE.md` §5.7 is headed *two rules that said more than they meant*, and says of
this one:

> the prohibition outran its own argument

This report is independent evidence for that doubt, from a deck built without knowing the section
existed.

## A second face of the same blind spot

On 2026-08-26 seven hit rectangles were given a class and no fill rule. An SVG `rect` with no fill
declaration is black. `DS-215` reported fourteen text runs under 4.5:1 and `DS-219`'s count rose by
exactly fourteen — the same fourteen. One fill rule cleared both. The rule can see a painted
*sibling* it was never meant to measure, and cannot see a painted *ancestor* that is the real ground.

## What to change

1. **Walk the full ancestor chain for the ground**, compositing painted ancestors rather than
   stopping at the first one. That is what a reader's eye does.
2. **Where the walk cannot resolve a ground, say so** rather than failing the pair. An unmeasurable
   pair and a failing pair are different findings and should read differently.
3. **Settle the `never`.** `DESIGN-RATIONALE.md` §5.7 already names the question. A deck permanently
   failing 40 of 46 is the case for settling it.
