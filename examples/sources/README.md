# Sources for the reference deck

**Riverbend is an illustrative city. It does not exist**, and neither do these documents outside
this repository. They are the model the reference deck's figures are outputs of — written so the
content half of the build check has a real case to reconcile against, rather than a fixture that
agrees with the deck by construction.

This is what DS-102 requires of an illustrative deck: the subject is stated to be illustrative, the
assumptions the numbers derive from are written down, and **nothing is attributed to a real study,
agency or place.** The alternative — quoting half-remembered real research — is where a
misremembered figure becomes a fabricated metric wearing a citation.

    python tools/deck/check.py examples/reference-deck.html --sources examples/sources

| File | What it carries |
| :--- | :--- |
| [`cost-model.md`](cost-model.md) | Capital and operating figures for both proposals |
| [`ridership-model.md`](ridership-model.md) | Catchment, corridor and elasticity figures |
| [`programme-timetable.md`](programme-timetable.md) | Dates, durations, thresholds and the review gate |

**A figure that reaches a slide and is not in one of these files is a finding**, not a rounding.
That is the whole point of keeping them: a deck can pass every presentation check and still put a
wrong number in front of a board.
