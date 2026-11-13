# Craft Foundations

## Subtle Layering (the backbone)

Regardless of direction, this applies to everything. You should *barely notice the system working* — when you look at Vercel's dashboard you don't think "nice borders," you just understand the structure. Invisible craft is working craft.

**Surface elevation.** Surfaces stack: a dropdown sits above a card sits above the page. Build a numbered system — base, then increasing levels. Each jump is only a few percentage points of lightness — e.g. dark mode base → +7% → +9% → +12%; light mode stays light and adds shadow instead. You can barely see one step in isolation, but stacked, the hierarchy emerges. Whisper-quiet shifts you feel rather than see.

- **Sidebars:** same background as canvas, not a different color. Different colors fragment the space into "sidebar world" and "content world." A subtle border is enough.
- **Dropdowns/popovers:** one level above their parent surface, or they blend in and layering is lost.
- **Inputs:** slightly *darker* than surroundings, not lighter. Inputs are inset — they receive content. A darker fill signals "type here" without heavy borders.

**Borders.** Should disappear when you're not looking for them, but be findable when you need structure. Low-opacity rgba blends with the background and defines an edge without demanding attention; solid hex borders look harsh by comparison. Dark mode lives around `rgba(255,255,255,0.06–0.12)`, light mode slightly higher. Build a progression — standard, softer separation, emphasis, focus-ring — and match intensity to the importance of the boundary.

**The squint test:** blur your eyes at the interface. You should still perceive hierarchy — what's above what, where sections divide — but nothing should jump out. No harsh lines, no jarring shifts. Just quiet structure. Get this wrong and nothing else matters.

## Infinite Expression

Every pattern has infinite expressions — **no two interfaces should look the same.** A metric display could be a hero number, inline stat, sparkline, gauge, progress bar, comparison delta, or trend badge. Same sidebar width, same card grid, same icon-left-number-big-label-small metric boxes every time *signals AI-generated immediately* and is forgettable. Linear's cards don't look like Notion's; Vercel's metrics don't look like Stripe's. Same concepts, infinite expressions. Before building, ask: what's the ONE thing users do here, and what product solves a similar problem brilliantly?

## Color Lives Somewhere

Every product exists in a world, and that world has colors. Before reaching for a palette, walk into the physical version of this space — what materials, what light, what objects? Your palette should feel like it came FROM somewhere, not applied TO something. Temperature is one axis; also ask quiet or loud, dense or spacious, serious or playful, geometric or organic. A trading terminal and a meditation app are both "focused" — completely different kinds of focus.

---

