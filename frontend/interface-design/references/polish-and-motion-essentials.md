# Polish & Motion Essentials

A hundred small details compound into "feels great." These are the highest-leverage ones — enough to ship genuinely polished UI.

## Static polish

- **Concentric radius.** Nested rounded elements: `outerRadius = innerRadius + padding`. Same radius on parent and child is the most common thing that makes UI feel off.
- **Tabular numbers.** Any dynamic number (counters, prices, timers, table columns) gets `font-variant-numeric: tabular-nums` to prevent layout shift.
- **Optical alignment.** When geometric centering looks off, fix it optically — icon-side padding ≈ text-side − 2px; nudge play triangles ~2px right.
- **States are not optional.** Every interactive element needs default, hover, active, focus, disabled. Data needs loading, empty, error. Missing states feel broken — they're the fastest tell of an unfinished interface.
- **Hit areas — 44×44px (WCAG), 40 at minimum.** If the visible control is smaller (a 20px checkbox), extend with a pseudo-element. Never let two hit areas overlap.
- **Shadows over borders for elevation.** For cards/buttons/containers that lift, prefer a layered transparent `box-shadow` (it adapts to any background); keep real borders for dividers and input outlines. Light-mode lift stacks three layers — a 1px ring + two soft depths, e.g. `0 0 0 1px rgba(0,0,0,.06), 0 1px 2px -1px rgba(0,0,0,.06), 0 2px 4px rgba(0,0,0,.04)`; dark mode collapses to a single ring `0 0 0 1px rgba(255,255,255,.08)` (depth shadows don't read on dark).
- **Text wrapping.** `text-wrap: balance` on headings; `text-wrap: pretty` on body/captions to kill orphans.
- **Font smoothing.** `-webkit-font-smoothing: antialiased` on the root (macOS renders heavy otherwise).
- **Image outlines.** 1px inset outline, pure `rgba(0,0,0,0.1)` light / `rgba(255,255,255,0.1)` dark — never a tinted near-black/white (reads as dirt on the edge).

## Motion

Motion should be felt, not watched. Fast, purposeful, and *never* in the way.

- **Should it animate at all?** Actions repeated 100+×/day (keyboard shortcuts, command palette) get **no** animation — it makes them feel slow. Occasional surfaces (modals, drawers, toasts) get standard animation. Rare/first-run moments can add delight.
- **Duration < 300ms** for UI. Button press 100–160ms; tooltips/popovers 125–200ms; dropdowns 150–250ms; modals/drawers 200–500ms. A 180ms dropdown feels more responsive than a 400ms one.
- **Custom ease-out, never ease-in.** Built-in curves are too weak. Use `cubic-bezier(0.23, 1, 0.32, 1)` for entering/interactive; ease-in-out (`cubic-bezier(0.77, 0, 0.175, 1)`) for on-screen movement. `ease-in` delays the first frame — the moment the user is watching — and feels sluggish.
- **Press feedback.** `transform: scale(0.97)` on `:active` (never below 0.95). Tactile confirmation the UI heard the click.
- **Never animate from `scale(0)`.** Nothing appears from nothing — start at `scale(0.95)` + `opacity: 0`.
- **Origin-aware popovers.** Popovers scale from their trigger (`transform-origin` set to the trigger), not center. Modals are the exception — they stay centered.
- **Only animate `transform` and `opacity`** (GPU-composited). Animating width/height/margin/padding triggers layout + paint and drops frames. Never `transition: all` — name exact properties.
- **Stagger entrances** 30–80ms between items for a natural cascade; keep exits faster and subtler than enters.
- **Respect `prefers-reduced-motion`** — keep opacity/color transitions, drop movement.

---

