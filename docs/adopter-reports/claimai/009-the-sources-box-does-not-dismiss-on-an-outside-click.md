# The sources box does not dismiss on an outside click, though the More menu beside it does

| Field | Value |
| :--- | :--- |
| **Target** | `htmldeck` — Gábor's own repository, cloned under `C:\Work\AgentPlugins` |
| **Kind** | Defect |
| **Status** | `closed` — closed 2026-08-29 by [T-268](../../../tasks/T-268-three-chrome-and-timing-defects-in-deck-js.md). **Taken as proposed**, and by the three-line document listener this report points at — the More menu's, applied to the component beside it. **Keyed to `.sources` rather than to `.sources-btn`**, which is the detail that makes it work: the button's own handler runs first and opens the box, so a listener sparing only the button would read the same click as outside and shut what it had just opened. Measured in a browser on a deck built from the edited shell, both directions: the box survives the click that opens it, and a click on the stage dismisses it. |
| **Found while** | Round 2 of the deck review on `D4 — Executive Board Presentation`, on 2026-08-25 |
| **Version seen** | `0.6.0` |

## What happens

Two pop-over surfaces sit in the same chrome and behave differently.

The **More menu** dismisses on a click anywhere else, bound on the document:

```js
/* A click anywhere else dismisses. Bound on the document rather than on a scrim, because a
   two-item chrome menu that laid a scrim over the deck would block the stage to close itself. */
document.addEventListener('click', function(e){
  if (!e.target.closest || !e.target.closest('.more')) closeMore();
});
```

`shell/deck.js:621–623`.

The **sources box** has no equivalent. It opens from its own button and closes only when something
else deliberately closes it:

| Route | Where |
| :--- | :--- |
| Its own button, pressed again | `deck.js:331` |
| Escape | `deck.js:540` |
| Another source box opening | `deck.js:347`, via `closeAllSources(s)` |
| The quick view opening | `deck.js:399` |
| Navigating to another slide | `deck.js:462` |

A click on the slide behind it does nothing. The box stays open over the content while the presenter
talks past it, and the only ways out are the key the audience cannot see them press, or the button
they have to find again.

The user's words: *the sources toggle should close on an outside click, the way More does.*

## Evidence

Open any deck with a `sources:` field, press the sources button, then click on the slide body. The
box remains. Do the same with the More menu and it closes. The two blocks quoted above are the whole
difference.

## What is missing

Two pop-overs in one chrome should dismiss the same way. The More menu's comment already argues the
case — a scrim would block the stage, so the dismissal is bound on the document — and that argument
applies unchanged to the sources box.

## Proposed fix

The same three lines, keyed to the sources root, added where the source buttons are wired
(`deck.js:329–333`):

```js
document.addEventListener('click', function(e){
  if (!e.target.closest || !e.target.closest('.sources')) closeAllSources(null);
});
```

`closeAllSources(null)` already exists and already closes every box. The one thing to watch is
ordering against the button's own handler: the toggle must not close the box the same click just
opened, which is why the guard tests for the whole `.sources` root rather than for the button.

The disclosure surfaces (`closeAllDiscs`) are worth the same look while this is open — the report
does not claim they have the defect, only that they are the third surface with the same shape.
