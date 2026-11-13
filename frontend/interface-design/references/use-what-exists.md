# Use What Exists

The most common way AI degrades a codebase: it hand-rolls what already exists. A bespoke `<div onClick>` "button" beside the project's real `Button`. A from-scratch dropdown with no keyboard support beside an installed primitive that has it. A 14-class Tailwind string copy-pasted onto every card instead of the component or token that's right there. Every one of these is the same failure — generating new instead of using what's present — and the result is inconsistent, inaccessible, and unmaintainable. **Before you build a control or style an element, look at what the project already gives you.**

## Controls: native → primitive → hand-roll

1. **Native HTML first** where it works. A `<button>` is a button; an `<a>` is a link; `<input type="text">`, `<dialog>`, `<details>` exist. Never `<div onClick>` something the platform already provides — you lose focus, keyboard, and semantics for free.
2. **A battle-tested headless primitive** for anything stateful and hard to get right — select, combobox, dialog, popover, tooltip, dropdown menu, tabs, date picker. These ship keyboard navigation, focus management, ARIA, and collision/positioning that take days to reproduce correctly. Reach for what the ecosystem already trusts (e.g. Radix UI, React Aria, Ark, Headless UI, Vaul, `cmdk` in React; the equivalent accessible primitive in other frameworks), then style it to your direction. "Build custom" means *compose and style a primitive*, not write the behavior from scratch.
3. **Hand-roll only as a genuine last resort** — no primitive fits, or there's no dependency budget. Then you owe the complete behavior contract: keyboard nav (arrow keys, Enter, Escape), focus trap/return, full ARIA roles and state, click-outside, and scroll-lock for overlays. A styled control missing these is broken, however good it looks.

## Styling: system → component → token → utility

1. **If the project has a design system, use it.** shadcn/`Button`, a CVA variant set, a theme, a component library — use `<Button variant="…">` and the existing variants before writing a one-off. Match the codebase's styling convention (Tailwind, CSS modules, CSS-in-JS), don't introduce your own.
2. **When a styled element repeats, extract a component.** The same utility string on nine buttons is duplication, not design. One component (or one CVA/variant) owns it; call sites stay clean. Extract on the second real reuse, not the first.
3. **Bind to semantic tokens, not hardcoded literals.** `bg-card border-border text-muted-foreground`, not `bg-white border-gray-200 text-gray-500`. Hardcoded `gray-200`/`#fff`/`px-4` raw values are the Tailwind form of random hex — they break theming and dark mode and signal no system. (See Token Architecture below.)
4. **Inline utilities are for genuine one-offs** — a layout nudge used once. The tell of slop is the *same* long className sprayed everywhere; that's a missing component or token, not styling.

---

