<!-- Source: locally authored from Tim Gabe, "The Psychology of Premium Apps" (youtube.com/watch?v=8EAYZe6y3I8), 2026-10-18 -->

---
name: commodity-ceiling
description: Audit and build protocol that takes an app or site from "looks decent" to premium. Use before shipping a feature or page, when a product built with AI tools looks fine but generic, or when asked to make something feel premium, polished or trustworthy. Covers the three places users find evidence of quality (core-flow hand-holding, cross-screen consistency, failure recovery), a state table to write before code, a Design Theater check of agent output, and a break-it-on-purpose pass.
---

# Commodity Ceiling

AI tools make the look a commodity; premium comes from product-specific states and recovery.
Visual craft is covered by `frontend/anti-ui-slop`, `frontend/interface-design` and
`frontend/high-end-visual-design`; this skill covers behaviour and states.

## 1. Core flow hand-holding (the part AI leaves out)

- Rule: after every action the user knows what just happened, can take it back, and knows what to
  do next.
- Agents skip this. Design Theater (Imteyaz et al., AIES 2026, arXiv 2607.22928; 120 interfaces,
  5 tools, 24 tasks): about 25% of stated design rationale was not implemented, 34% for
  functional requirements. Per the video, the parts skipped were system status, undo and error recovery.
- Never accept the agent's explanation of what it built. Check the rendered UI.
- Example from the video (Undertone): a user who hit stop on a mic test was told "too short to count" with
  nothing shown. Founder quote: "I was expecting anything instead of nothing ... that right there
  is where we lose them."
- Per-screen state list (minimum): loading, empty, partial (some data loaded or some items failed),
  success feedback, error, offline, permission denied, undo, next step.

## 2. Consistency across screens (screen 80 next to screen 1)

- Teams review one screen at a time. Users live in all of them for months.
- Petrie, Papadofragkakis, Power & Swallow 2009 (University of York): moving the nav bar mid-task
  more than doubled time on the page and slowed later pages too. Participants said it did not slow them down
  much. Users under-report the cost, so interviews and analytics miss it (the abstract confirms the doubling and its persistence).
- Agents spin up a screen in a minute, so drift compounds.
- Example from the video (Undertone): two separate out-of-sessions screens showed the same generic
  message, no count, no date. Replaced by one shared pattern: a "2 of 2 sessions used" badge, one
  sentence ("You've used both sessions this month"), the exact refresh date.
- Procedure: click every route in the core flow and screenshot each. Compare nav, buttons, empty
  states, copy tone, date and number formats. Log each mismatch as screen A vs screen B. If a human
  is available, use the product for an hour as a real user and log every spot where it stops
  feeling like one product. Fix each by naming one pattern both places share.

## 3. Failure recovery (where premium stops being an opinion)

- Service recovery paradox (de Matos, Henrique & Rossi 2007, Journal of Service Research
  meta-analysis): a well-handled failure raises satisfaction above the no-failure baseline. No
  significant effect on repurchase intent or word of mouth, so do not sell it as retention.
- Example from the video (crypto card client): a declined payment now shows an alert saying to
  check the balance, with a contact-support button in place.
- Procedure, break it on purpose: wifi off mid-flow, fail a payment, empty every list, expire the
  session, submit twice, kill the tab mid-save. Design each state as carefully as the success
  screen: what happened, what to do, how to reach a human.
- Full edge-case list: `frontend/impeccable/reference/harden.md`.

## Build protocol for a feature or page

1. State table before code, saved as `<feature>/STATES.md` (one markdown table). Rows = screens,
   columns = the nine states from section 1. Each cell is designed copy or behaviour, or "n/a"
   with a reason.
   - For a static page, columns that cannot occur are "n/a: static"; still run steps 4, 6 and 7.
2. Name the existing pattern every new screen inherits (component, copy, empty state).
   - No new pattern without a written reason.
3. Build. Primitives first, per `engineering/agentic-build-primitives`.
4. Design Theater check: list every claim in the agent's summary, open the running UI, mark each
   implemented or missing.
   - A missing claim is a blocker, not a note.
   - Open the UI with `testing/browser-testing-with-devtools` or Playwright and attach a
     screenshot to each claim.
5. Break-it pass from section 3.
6. Fresh-context adversarial review. The reviewer gets the state table and the running app, not the
   agent's explanation.
   - Skip only when a fresh-context reviewer already marked every claim and every state-table
     cell verified on screen. The builder's own verification never counts.
7. Consistency walk (section 2) across old and new screens, then ship. Pass = no empty cells, zero
   missing claims, every logged seam fixed or ticketed, reviewer returns no BLOCKER. Keep
   STATES.md next to the feature.

## Agent routing (token budget)

- Orchestrator (strong model): owns and approves the state table, runs the audits, decides what
  ships.
- Cheaper model: drafts state-table cells, copy, empty-state text and documentation.
- Reviewer: fresh context, read-only tools. Never let the builder review its own screens.
- Pass file:line references and screenshots between agents, not prose summaries.

## Evidence

| Claim | Source | Note |
|---|---|---|
| About 25% of stated rationale not implemented, 34% for functional requirements | Imteyaz et al., AIES 2026, arXiv 2607.22928 | 120 interfaces, 5 tools, 24 tasks |
| Moving the nav bar more than doubled page time | Petrie et al. 2009, University of York | Abstract confirmed at source (INTERACT 2009, doi 10.1007/978-3-642-03655-2_46) |
| Well-handled failure lifts satisfaction, not repurchase or word of mouth | de Matos, Henrique & Rossi 2007, J. Service Research | Meta-analysis |
