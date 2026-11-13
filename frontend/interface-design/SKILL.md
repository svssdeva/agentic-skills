<!-- Source: https://skills.sh/dammyjay93/interface-design/interface-design -->
<!-- Install: npx skills add https://github.com/dammyjay93/interface-design --skill interface-design -->

---
name: interface-design
description: Craft-first interface design for dashboards, admin panels, SaaS apps, tools, settings pages, data interfaces, and interactive products. Use when designing, building, reviewing, auditing, or refining product UI where visual craft, layout hierarchy, tokens, states, visual direction, or design-system consistency matter. Not for marketing pages, landing pages, campaigns, or brand-only work.
---

# Interface Design

Build product interfaces with the craft of a top design team — Linear, Vercel, Stripe, Apple. The difference between those and generic output is not talent. It is that every decision was *decided*, the hierarchy is unmistakable, and a hundred small details are correct at once. This skill is how you get there.

## Scope

**Use for:** Dashboards, admin panels, SaaS apps, tools, settings pages, data interfaces.

**Not for:** Landing pages, marketing sites, campaigns, brand-only work. Use a marketing/frontend design skill for those.

This skill is self-contained: direction, visual hierarchy, design-system architecture, and the polish and motion essentials needed to ship production-grade UI all live here.

---

# The Problem

You will generate generic output. Your training has seen thousands of dashboards, and the patterns are strong. You can follow this entire process — explore the domain, name a signature, state your intent — and still produce a template: warm colors on cold structures, friendly fonts on generic layouts.

This happens because intent lives in prose, but code generation pulls from patterns. The gap between them is where defaults win. Process helps, but it doesn't guarantee craft. You have to catch yourself, and you have to know the concrete moves that defaults don't.

**The bar:** If another AI, given a similar prompt, would produce substantially the same output, you have failed. Not different for its own sake — different because the interface emerged from *this* user, *this* task, *this* world. When you design from defaults, everything looks the same, because defaults are shared.

---

# Where Defaults Hide

Defaults disguise themselves as infrastructure — the parts that feel like they just need to work, not be designed.

- **Typography feels like a container.** But type isn't holding your design, it *is* your design. The weight of a headline, the personality of a label, the texture of a paragraph shape how the product feels before anyone reads a word. Reaching for your usual font means you're not designing.
- **Navigation feels like scaffolding.** But navigation *is* the product — where you are, where you can go, what matters. A page floating in space is a component demo, not software.
- **Data feels like presentation.** But a number on screen is not design. What does it *mean* to the person looking? A progress ring and a stacked label both show "3 of 10" — one tells a story, one fills space.
- **Token names feel like implementation detail.** But `--ink` and `--parchment` evoke a world; `--gray-700` and `--surface-2` evoke a template. Someone reading only your tokens should guess what product this is.

There are no structural decisions. Everything is design. The moment you stop asking "why this?" is the moment defaults take over.

---

# Intent First

Before touching code, answer these. Keep it a compact working brief unless the direction needs user confirmation.

- **Who is this human?** Not "users." The actual person. Where are they when they open this? What did they do 5 minutes ago, what will they do 5 minutes after? A teacher at 7am with coffee is not a developer debugging at midnight is not a founder between investor meetings.
- **What must they accomplish?** The verb. Grade these submissions. Find the broken deployment. Approve the payment. The answer determines what leads, what follows, what hides.
- **What should this feel like?** In words that mean something. "Clean and modern" means nothing — every AI says that. Warm like a notebook? Cold like a terminal? Dense like a trading floor? Calm like a reading app? This shapes color, type, spacing, density — everything.

If the prompt is too vague to identify the human, task, and feel, ask one concise question. If context allows a responsible assumption, state it briefly and proceed.

**Intent must be systemic.** Saying "warm" then using cold colors is not following through. If the intent is warm: surfaces, text, borders, accents, semantic colors, type — all warm. If dense: spacing, type size, information architecture — all dense. Check every token against the stated intent. For every choice — layout, color temperature, typeface, spacing scale, hierarchy — you must be able to say *why*. "It's common" or "it works" means you defaulted.

---

# Product Domain Exploration

This is where defaults get caught — or don't. Generic path: Task type → visual template → theme. Crafted path: Task type → product domain → signature → structure + expression. The difference is time spent in the product's world before any visual thinking.

**Produce all four before proposing any direction:**

- **Domain** — concepts, metaphors, vocabulary from this product's world. Not features — territory. Minimum 5.
- **Color world** — what colors exist *naturally* here? Not "warm" or "cool" — go to the actual world. If this product were a physical space, what would you see? List 5+.
- **Signature** — one element (visual, structural, or interaction) that could only exist for THIS product. If you can't name one, keep exploring.
- **Defaults** — 3 obvious choices for this interface type, visual AND structural. You can't avoid patterns you haven't named.

**The test:** Read your proposal with the product name removed. Could someone identify what it's for? If not, explore deeper.

---

# Before Writing Each Component

**Every time** you write UI code — even small additions — state:

```
Intent:     [who is this human, what must they do, how should it feel]
Hierarchy:  [the focal element, and how it wins — size / weight / contrast / space]
Palette:    [colors from your exploration — and WHY they fit this world]
Depth:      [borders / subtle shadows / layered — and WHY it fits the intent]
Surfaces:   [your elevation scale — and WHY this temperature]
Typography: [typeface + the size/weight/color levers — and WHY]
Spacing:    [base unit + chosen density]
```

This checkpoint is mandatory. If you can't explain WHY for each, you're defaulting — stop and think.

---

# Design System Essentials

The token, spacing, and depth architecture beneath every craft decision.

- **Token architecture.** Every color traces to a small set of primitives: foreground (text), background (surface), border, brand, semantic (destructive/warning/success). No random hex — everything maps to primitives.
- **Text hierarchy — four levels.** Primary, secondary, tertiary, muted (default / supporting / metadata / disabled). Using only two means the hierarchy is too flat.
- **Spacing.** Pick a base unit (4 or 8px), use multiples only. Scale by context: micro (icon gaps), component (within buttons/cards), section (between groups), major (between areas). Random values signal no system.
- **Padding.** Symmetrical — if one side has a value, the others match unless content genuinely demands asymmetry.
- **Depth — choose ONE and commit.** Borders-only (clean, technical, dense tools) · subtle shadows (approachable) · layered shadows (premium, dimensional) · surface-color shifts (tints, no shadows). Don't mix strategies.
- **Border radius — a scale.** Small for inputs/buttons, medium for cards, large for modals. Don't mix sharp and soft randomly.
- **Control tokens.** Inputs/selects/checkboxes get dedicated background, border, and focus tokens — don't reuse surface tokens, so you can tune controls independently. Native `<select>`/`<input type="date">` can't be styled — compose a headless primitive instead of hand-rolling one (see "Use What Exists").
- **Dark mode.** Shadows are weak on dark — lean on borders. Desaturate semantic colors slightly. Same hierarchy system, inverted values. Keep one hue; shift only lightness across surfaces.

---

# Avoid

- **Harsh borders** — if borders are the first thing you see, they're too strong
- **Dramatic surface jumps** — elevation should be whisper-quiet
- **Flat hierarchy** — everything one size/weight; no clear focal point
- **Monotone layout** — same card size, gap, and density everywhere
- **Inconsistent spacing** — the clearest sign of no system
- **Mixed depth strategies** — pick one and commit
- **Missing states** — hover, focus, disabled, loading, empty, error
- **Dramatic drop shadows** — subtle, not attention-grabbing
- **Large radius on small elements**; **thick decorative borders**
- **Gradients and color for decoration** — color should mean something
- **Multiple accent colors** — dilutes focus
- **Different hues for different surfaces** — keep one hue, shift only lightness
- **Default typography** — system/Inter fonts and size-only hierarchy where a direction was set
- **Structural hacks** — negative margins undoing parent padding, escape-hatch `calc()`, absolute positioning to dodge layout flow

---

# Workflow

## Communication
Be invisible. Don't announce modes or narrate process. Never say "I'm in ESTABLISH MODE" or "Let me check system.md." Jump into the work; state suggestions with reasoning.

## Execution discipline
Use this skill as a working discipline, not just advice. When editing UI:

1. Inspect the existing app, design tokens, component patterns, and `.interface-design/system.md` if present.
2. Make the domain exploration concrete before choosing layout, color, type, density, and navigation.
3. For greenfield screens, major redesigns, or vague direction, consider a visual reference pass *if an image-generation tool is available* (skip otherwise — it's a companion, never the deliverable). Four modes: **direction board** (2–3 abstract mood/material/color explorations before code — no real UI), **UI reference** (medium-fidelity composition for a chosen direction), **paintover** (a stronger version of an existing screenshot), **raster asset** (empty-state art, textures — never icons/logos/charts). Always reject generic SaaS, illegible text, off-domain palettes; extract palette/density/proportions/signature, then build it in real code and verify in the browser.
4. Patch the implementation, then run the relevant build/typecheck/tests when available.
5. Verify visually for non-trivial UI. Use the inline render tool, a local browser, or screenshots at desktop and mobile widths; fix overlap, broken spacing, blank states, unreadable text, missing assets, and generic composition before presenting.
6. Keep user-facing updates short. Don't expose long private design monologues — surface the useful recommendation or decision.

## Suggest + Ask
Lead with exploration and recommendation, then confirm:

```
Domain:     [5+ concepts from the product's world]
Color world:[5+ colors that exist in this domain]
Signature:  [one element unique to this product]
Rejecting:  [default 1] → [alternative], [default 2] → [alternative], [default 3] → [alternative]
Direction:  [approach connecting to the above]
```

Then ask: "Does that direction feel right?" If an inline render tool is available, render a live specimen of the direction in the same message — show the palette, type, and signature, don't just name them.

## Build flow
- **If `.interface-design/system.md` exists:** read it and apply — decisions are made.
- **If not:** explore domain (all four outputs) → propose (reference all four) → confirm when the direction is ambiguous or costly to change → build → run the checks below → offer to save.

## The checks (before showing)
Run these against your output; if any fails, iterate before presenting.

- **Swap test** — swap your typeface for the usual one, your layout for a standard template: would anything feel different? Where swapping wouldn't matter is where you defaulted.
- **Squint test** — blur your eyes: hierarchy still readable? Nothing jumping out harshly?
- **Signature test** — point to five specific elements where your signature appears. "The overall feel" doesn't count.
- **Token test** — read your CSS variables aloud: do they belong to this product's world, or any project?

---

# After Completing a Task

Always offer to save: "Want me to save these patterns for future sessions?" If yes, write to `.interface-design/system.md`:

- Direction and feel
- Depth strategy (borders/shadows/layered) and spacing base unit
- Hierarchy decisions (type scale ratio, density values, focal pattern)
- Key component patterns — add when a component is used 2+ times, is reusable, or has measurements worth remembering (not one-offs or prop variations). Record the values, e.g. `Button primary — 36px h · 12px 16px pad · 6px radius · 14px/500`.
- Visual direction notes and selected references when an image pass shaped the design

**Consistency checks.** If system.md defines values, hold to them: spacing on the grid, the declared depth strategy throughout, colors from the palette, documented patterns reused not reinvented. This compounds — each save makes future work faster and more consistent.

---

# Commands

- `/interface-design:design-review` — strict craft + hierarchy review of a build, with an approval bar; renders before/after when possible
- `/interface-design:design-deslop` — fast, diff-scoped pass that strips visual slop from a branch

If a user asks for design status, audit, or pattern extraction in natural language: read `.interface-design/system.md` and summarize it, check UI files against it for drift, or scan for repeated spacing/radius/color/component values and propose a system.md — perform the equivalent inline.

## References

Read the file that matches the task; all text moved here verbatim from this SKILL.md.

- [Render It When You Can](references/render-it-when-you-can.md) — read when a browser or screenshot tool is available, to check the UI visually.
- [Visual Hierarchy & Composition](references/visual-hierarchy-and-composition.md) — read when laying out a view: focal point, type scale, density, spacing rhythm, proportions.
- [Craft Foundations](references/craft-foundations.md) — read when styling surfaces, depth, borders and colour.
- [Use What Exists](references/use-what-exists.md) — read before hand-rolling any control or styling: native, primitive, component, token order.
- [Polish & Motion Essentials](references/polish-and-motion-essentials.md) — read before finishing a component: static polish, states and motion.
