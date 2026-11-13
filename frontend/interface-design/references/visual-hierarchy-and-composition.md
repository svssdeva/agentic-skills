# Visual Hierarchy & Composition

The single biggest driver of "this looks designed" versus "this looks generated." Defaults produce *flatness* — everything the same size, weight, and spacing, so nothing leads and the eye has nowhere to go. Craft produces *hierarchy* — the eye knows instantly what matters. These are concrete moves, not vibes.

## One focal point per view

Every screen has one thing the user came to do. That thing dominates — through size, contrast, position, or the space around it. When everything competes equally, nothing wins and the interface reads like a parking lot. Before building, name the focal element out loud. Then make it win: bigger, higher-contrast, or ringed in whitespace. Demote everything else deliberately.

## Type scale is a ratio, and weight beats size

Don't pick sizes by feel. Pick a ratio and step it: ~1.2 (minor third) for dense/calm UI, ~1.25 for most product UI, ~1.333 for expressive. From a 14–16px body that yields a *visibly* distinct scale, not 15/16/17 mush. A 14px base at 1.25: `caption 11 · body 14 · h4 16 · h3 18 · h2 22 · h1 28 · display 44+`. Round to whole pixels and to your spacing grid.

The Apple/Linear move: **weight and color do more hierarchy work than size.** A single 14px size holds three tiers through weight + opacity alone — `value: 600 / primary`, `label: 500 / secondary`, `meta: 400 / muted` — separating more cleanly than two regular weights two points apart. Build from three levers together (size, weight, color/opacity), never size alone. If you squint and can't tell headline from body from label, the hierarchy is too weak.

Worked example — a metric, flat vs decided. *Flat:* `Revenue` / `$48,200` both 14px regular gray, three identical boxes, no focal point. *Decided:* `REVENUE` 11px/500/muted/tracked · `$48,200` 28px/600/primary/tabular-nums (the hero) · `↑12%` 12px/500/success. Same data, opposite legibility — the figure leads through size+weight+one accent, the label is demoted, secondary metrics drop to a lower tier.

## Density is a decision, expressed in px

Linear is tight; Stripe is airy. Neither is default — both are *chosen*, and the choice is the same number repeated everywhere. Decide the density up front and name the values: a tool panel at 12–16px padding feels workbench-tight; the same card at 24px feels like a brochure. The same number can be right in one context and lazy in another. Pick deliberately, then hold it.

## Spatial rhythm — breathe unevenly

Great interfaces don't space everything equally. Dense control zones give way to open content; heavy elements balance against light ones; the eye travels with purpose. Monotone layouts — same card size, same gap, same density everywhere — are the sound of no one deciding. Vary the rhythm on purpose: group tightly-related things, then put real air between groups.

## Proportions speak

A 280px sidebar next to full-width content says "navigation serves content." A 360px sidebar says "these are peers." The specific number declares what matters. If you can't articulate what a proportion is saying, it isn't saying anything. Choose widths and ratios that state a relationship.

## Distribution and restraint (the "expensive" look)

- **~60/30/10**: a dominant neutral surface, a secondary tone, and ~10% accent. Color is a scarce resource — most of the screen is structure.
- **One accent, used with intention**, beats five colors used without thought. Gray builds structure; color *communicates* (status, action, identity). Unmotivated color is noise.
- **Hierarchy through space and weight, not lines.** Reach for whitespace and tonal shift before borders and dividers. The most premium interfaces are mostly invisible structure.
- **Optical sizing on large type**: tighten letter-spacing as type gets bigger (headings slightly negative tracking); loosen line-height on body for readability (~1.5). Tight type reads as crafted; default tracking on a 32px heading reads as a document.

---

