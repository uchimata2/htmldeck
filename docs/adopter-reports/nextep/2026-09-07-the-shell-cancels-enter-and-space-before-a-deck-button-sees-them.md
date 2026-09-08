---
tool: htmldeck
version: 0.7.0
date: 2026-09-07
severity: defect
---

# A real `<button>` on a slide is not operable by Enter or Space

## Expected

`DS-164` wants labelled controls and `DS-167` wants them keyboard operable. A slide that uses a real
`<button>` — the most conservative thing an author can do — should get Enter and Space for free from
the browser.

## Actual

The shell binds Enter and Space to paging on a **document-level capture listener** and calls
`preventDefault`. Capture runs before the event reaches the button, so the browser never synthesises
the button's `click`, and the control does nothing at all. Tab still reaches it and the focus ring
still shows, so the page looks operable and is not.

Stopping the event in the deck's own handler does not help: the default was already cancelled
upstream. The author has to *run the action by hand* on `keydown` and then stop the event so the
deck does not also page — which is not obvious, and nothing in the contract says it.

The failure is silent in both directions. No rule fails, and a build that only ever clicks with a
pointer never sees it.

## Command that proves it

In a browser, on a deck with a slide-authored `<button>`:

```js
const b = document.querySelector('#yourButton');
b.addEventListener('keydown', e => console.log(e.key, e.defaultPrevented));
b.addEventListener('click', () => console.log('click'));
b.focus();
```

Then press Enter. Measured 2026-09-07 on nextep.html: the log reads `Enter true` and **no `click`
follows**. Before the deck ran the action itself, five tour stages stayed in their resting state
under Tab-then-Enter.

## Suggested

The pager's capture handler could skip the key when `event.target` is a focusable control inside the
stage — `target.closest('button, [role="button"], a[href], input, select, textarea')` — which is the
same test a document-level shortcut usually owes a form. Failing that, say it in the contract, next
to `DS-164`: a slide control must run its own Enter and Space.
