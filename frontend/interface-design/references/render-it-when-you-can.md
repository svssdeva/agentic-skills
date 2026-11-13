# Render It When You Can

If an inline visual-rendering tool is available in the session (e.g. a `show_widget` / `visualize` tool that renders HTML or SVG inline in the conversation), prefer **showing** the design over describing it. A direction trapped in prose is a fraction as useful as one the person can look at. This is conditional: when no such tool is present (CI, headless agents, plain terminals), fall back to code, tokens, and a written proposal. Never assume the tool exists; check, then use it.

Render at three moments:

1. **Proposing a direction.** Alongside the Suggest + Ask block, render a small live specimen: the palette as actual swatches, the type scale in the real typeface, the surface-elevation steps as stacked cards, the signature element as a real component. The person should *see* "warm like a notebook," not read the words.
2. **Designing a component.** Render the actual component (or a tight before/after, both variants side by side) so the craft decisions — spacing, borders, hierarchy, states — are visible, not asserted. Render the real states (default, hover, empty, error) where they matter.
3. **Critiquing or auditing.** Render the current version and the improved version together so the gap is shown, not narrated.

Rules when rendering:

- The widget shows the **visual only**. All reasoning, the domain exploration, the rejected-defaults list, and the recommendation stay in your response text — never paste prose into the widget.
- Match the rendering tool's own design-system contract (load its `read_me`/guidance if it has one). Use its theme variables so the specimen inherits light/dark mode and sits native in the host. Don't fight the host chrome.
- The specimen must still pass the checks below. A rendered default is still a default — rendering is how craft gets *seen*, not a substitute for it.
- This renders to the *conversation*, not the project. The actual implementation still lands in the codebase through normal edits.

The point: collapse the loop between "here's my thinking" and "here's what it looks like" into a single message the person can react to.

---

