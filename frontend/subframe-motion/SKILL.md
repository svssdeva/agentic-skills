<!-- Source: locally authored from https://www.subframe.com/motion (checked 2026-10-30) -->

---
name: subframe-motion
description: Find a ready-made React animation, motion component or WebGL shader in the Subframe Motion library (309 copy-paste examples, no account) instead of hand-writing one. Use when a React UI needs a micro-interaction, animated button or selector, text effect, background shader, or "make it feel alive" polish, or when the user names Subframe Motion. Not for HyperFrames videos or plain CSS pages.
---

# Subframe Motion

A free catalogue at <https://www.subframe.com/motion>: 309 examples under three filters: Components & interactions, Animation & motion, and WebGL & shaders. Each example has its own page, `https://www.subframe.com/motion/<slug>` (for example `shimmer-button`, `mark-focus`, `liquid-chrome`).

## Use it

1. Browse the catalogue, or fetch an example page (`https://r.jina.ai/https://www.subframe.com/motion/<slug>` gives clean text), and pick the closest match to the job.
2. Each page's "Add to your project" box says what the example needs. The one checked (`shimmer-button`) is a single React file with its styles inlined and no extra packages (React 19; in Next.js, a client component). Copy it into the project as its own component.
3. **Keep the licence header.** Examples can be adapted from other open-source libraries: `shimmer-button` is Magic UI's MIT component with its copyright kept. Read the header of each file before you use it, and keep it in the copied file.
4. Fit it to the project. Replace the literal colours and fonts with the project's tokens. Keep the example's `prefers-reduced-motion` and pause handling, or add them if they're missing. Never animate `width`, `height`, `top` or `left`, and never use `transition: all` (the same rules as `hallmark`'s floor).
5. Check it in the real page: keyboard focus, reduced motion, and a phone-width layout.

## MCP (optional)

Subframe serves the same library over MCP with no account. Adding it changes the user's Claude Code config, so show the command and get an OK first:

```
claude mcp add --transport http --scope user subframe-motion https://mcp.subframe.com/motion/mcp
```

This is the command the page's "Install Motion MCP" button generates (read from the page source on 2026-10-30, not run). The plain web pages above need nothing installed.

## Pairs with

- `hallmark`, `impeccable`, `design-taste-frontend`: decide where motion belongs; this skill supplies the component.
- `animate`, `improve-animations`, `review-animations`: timing, easing and review of whatever you drop in.
- `pick-ui-library`: when you need a general animation library (Motion) rather than one finished effect.
