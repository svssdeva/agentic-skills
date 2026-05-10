# agentic-skills

> A curated library of **76 skills** for Claude Code — drop-in behavioral modules that make your AI agent smarter, faster, and domain-aware.

Skills are plain markdown files (`SKILL.md`) that Claude reads before acting. Each one encodes expert knowledge, workflows, and guardrails for a specific domain. No code to install — just point Claude at the folder.

---

## What's a Skill?

A skill is a `SKILL.md` file that tells Claude *how* to behave in a given context. When you invoke a skill, Claude loads it and follows its instructions exactly — like hiring a specialist for the task at hand.

```
/skill angular/angular-component    → expert Angular component authoring
/skill rust/rust-engineer           → idiomatic Rust with ownership & error handling
/skill seo/seo-audit                → structured technical SEO review
/skill engineering/test-driven-development → red-green-refactor discipline
```

Skills cover everything from language idioms to development methodologies to content strategy.

---

## Using Skills in Claude Code

**Install** — clone this repo anywhere and point Claude at it in your project's `CLAUDE.md`:

```bash
git clone https://github.com/svssdeva/agentic-skills ~/.claude/skills
```

**Invoke** — type a slash command in Claude Code:

```
/skill <skill-name>
```

Or reference skills directly in your prompt:

```
Using the rust-engineer skill, refactor this module to use proper error propagation.
```

**Stack skills** — combine skills for compound expertise:

```
Using engineering/spec-driven-development + engineering/test-driven-development, implement this feature.
```

---

## Skill Library

### Angular `9 skills`

| Skill | What it does |
|---|---|
| [`angular-component`](angular/angular-component/SKILL.md) | Idiomatic component authoring with smart/dumb separation |
| [`angular-developer`](angular/angular-developer/SKILL.md) | Full Angular developer persona — architecture to deployment |
| [`angular-di`](angular/angular-di/SKILL.md) | Dependency injection patterns, tokens, providers |
| [`angular-directives`](angular/angular-directives/SKILL.md) | Structural and attribute directive authoring |
| [`angular-forms`](angular/angular-forms/SKILL.md) | Reactive forms, validation, form arrays |
| [`angular-http`](angular/angular-http/SKILL.md) | HttpClient, interceptors, error handling |
| [`angular-signals`](angular/angular-signals/SKILL.md) | Signals, computed, effects — Angular reactivity model |
| [`angular-testing`](angular/angular-testing/SKILL.md) | Unit and integration testing with TestBed |
| [`angular-tooling`](angular/angular-tooling/SKILL.md) | CLI, build config, workspace setup |

### Astro `5 skills`

| Skill | What it does |
|---|---|
| [`astro`](astro/astro/SKILL.md) | Core Astro patterns and component model |
| [`astro-architecture`](astro/astro-architecture/SKILL.md) | Island architecture, routing, content collections |
| [`astro-expert`](astro/astro-expert/SKILL.md) | Advanced Astro — SSR, adapters, integrations |
| [`astro-seo`](astro/astro-seo/SKILL.md) | SEO-first Astro builds with structured data |
| [`perf-astro`](astro/perf-astro/SKILL.md) | Core Web Vitals optimization for Astro sites |

### Bun `3 skills`

| Skill | What it does |
|---|---|
| [`bun`](bun/bun/SKILL.md) | Bun fundamentals — APIs, built-ins, gotchas |
| [`bun-development`](bun/bun-development/SKILL.md) | Bun-first development workflows and patterns |
| [`bun-runtime`](bun/bun-runtime/SKILL.md) | Runtime internals, FFI, native modules |

### Rust `5 skills`

| Skill | What it does |
|---|---|
| [`rust-engineer`](rust/rust-engineer/SKILL.md) | Idiomatic Rust — ownership, lifetimes, traits |
| [`rust-best-practices`](rust/rust-best-practices/SKILL.md) | Clippy-clean code, error handling, API design |
| [`rust-async-patterns`](rust/rust-async-patterns/SKILL.md) | Tokio, async/await, channels, cancellation |
| [`rust-testing`](rust/rust-testing/SKILL.md) | Unit tests, integration tests, property testing |
| [`m15-anti-pattern`](rust/m15-anti-pattern/SKILL.md) | Detect and fix the M15 anti-pattern |

### TypeScript `2 skills`

| Skill | What it does |
|---|---|
| [`typescript-expert`](typescript/typescript-expert/SKILL.md) | Full TypeScript expertise — types, config, tooling |
| [`typescript-advanced-types`](typescript/typescript-advanced-types/SKILL.md) | Conditional types, mapped types, template literals |

### Tailwind CSS `3 skills`

| Skill | What it does |
|---|---|
| [`tailwind-css-patterns`](tailwind/tailwind-css-patterns/SKILL.md) | Component patterns and design token usage |
| [`tailwind-design-system`](tailwind/tailwind-design-system/SKILL.md) | Design system authoring with Tailwind |
| [`tailwindcss-advanced-layouts`](tailwind/tailwindcss-advanced-layouts/SKILL.md) | Grid, flex, and responsive layout mastery |

### Mobile & Cross-Platform `4 skills`

| Skill | What it does |
|---|---|
| [`ionic`](mobile/ionic/SKILL.md) | Ionic components, navigation, native APIs |
| [`ionic-design`](mobile/ionic-design/SKILL.md) | Ionic design system and theming |
| [`capacitor-best-practices`](mobile/capacitor-best-practices/SKILL.md) | Capacitor plugins, native bridging, deployment |
| [`expo-tailwind-setup`](mobile/expo-tailwind-setup/SKILL.md) | Expo + NativeWind (Tailwind) setup and patterns |

### Cloud & DevOps `6 skills`

| Skill | What it does |
|---|---|
| [`aws-solution-architect`](cloud/aws-solution-architect/SKILL.md) | AWS architecture — well-architected, cost-aware |
| [`aws-diagrams`](cloud/aws-diagrams/SKILL.md) | Infrastructure diagrams as code |
| [`ci-cd-and-automation`](cloud/ci-cd-and-automation/SKILL.md) | Pipelines, GitHub Actions, release automation |
| [`vercel-react-best-practices`](cloud/vercel-react-best-practices/SKILL.md) | React on Vercel — SSR, caching, edge functions |
| [`vercel-composition-patterns`](cloud/vercel-composition-patterns/SKILL.md) | Vercel composability — monorepos, turborepo |
| [`secure-linux-web-hosting`](cloud/secure-linux-web-hosting/SKILL.md) | Harden a cloud Linux server — SSH, firewall, Nginx, HTTPS |

### SEO & Content `7 skills`

| Skill | What it does |
|---|---|
| [`ai-seo`](seo/ai-seo/SKILL.md) | SEO for LLM-driven discovery — AIO, GEO, AEO |
| [`seo-audit`](seo/seo-audit/SKILL.md) | Technical SEO audit with actionable findings |
| [`seo-geo`](seo/seo-geo/SKILL.md) | Geo-targeted SEO, hreflang, local search |
| [`programmatic-seo`](seo/programmatic-seo/SKILL.md) | Programmatic page generation for SEO at scale |
| [`content-strategy`](seo/content-strategy/SKILL.md) | Content planning, ICP alignment, funnel mapping |
| [`social-content`](seo/social-content/SKILL.md) | Social-first content with engagement hooks |
| [`product-marketing-context`](seo/product-marketing-context/SKILL.md) | Product marketing framing and messaging |

### Engineering Practices `18 skills`

| Skill | What it does |
|---|---|
| [`test-driven-development`](engineering/test-driven-development/SKILL.md) | Red-green-refactor discipline, enforced |
| [`spec-driven-development`](engineering/spec-driven-development/SKILL.md) | Spec-first — design the contract before the code |
| [`source-driven-development`](engineering/source-driven-development/SKILL.md) | Let the source of truth drive implementation |
| [`incremental-implementation`](engineering/incremental-implementation/SKILL.md) | Ship in small, safe, reviewable increments |
| [`planning-and-task-breakdown`](engineering/planning-and-task-breakdown/SKILL.md) | Task decomposition and sequencing |
| [`idea-refine`](engineering/idea-refine/SKILL.md) | Sharpen vague ideas into actionable specs |
| [`code-review-and-quality`](engineering/code-review-and-quality/SKILL.md) | Thorough code review with prioritized feedback |
| [`code-simplification`](engineering/code-simplification/SKILL.md) | Remove accidental complexity ruthlessly |
| [`context-engineering`](engineering/context-engineering/SKILL.md) | Prompt and context design for AI-native systems |
| [`debugging-and-error-recovery`](engineering/debugging-and-error-recovery/SKILL.md) | Systematic debugging — hypothesize, isolate, verify |
| [`api-and-interface-design`](engineering/api-and-interface-design/SKILL.md) | Stable, hard-to-misuse API design (Hyrum's Law-aware) |
| [`documentation-and-adrs`](engineering/documentation-and-adrs/SKILL.md) | Docs and Architecture Decision Records |
| [`deprecation-and-migration`](engineering/deprecation-and-migration/SKILL.md) | Safe deprecation paths and migration strategies |
| [`security-and-hardening`](engineering/security-and-hardening/SKILL.md) | Security review, threat modeling, hardening |
| [`git-workflow-and-versioning`](engineering/git-workflow-and-versioning/SKILL.md) | Branching, commits, tagging, release flow |
| [`shipping-and-launch`](engineering/shipping-and-launch/SKILL.md) | Launch checklist, rollout strategy, monitoring |
| [`system-design`](engineering/system-design/SKILL.md) | Structured system design — requirements to trade-off analysis |
| [`systematic-debugging`](engineering/systematic-debugging/SKILL.md) | Four-phase debugging with enforced root cause investigation |

### Go `3 skills`

| Skill | What it does |
|---|---|
| [`golang-pro`](golang/golang-pro/SKILL.md) | Concurrent Go dev with goroutines, microservices, pprof optimization |
| [`golang-patterns`](golang/golang-patterns/SKILL.md) | Idiomatic Go patterns, error handling, concurrency, interfaces |
| [`golang-testing`](golang/golang-testing/SKILL.md) | Table-driven tests, benchmarks, fuzzing, TDD workflows |

### Frontend & Design `5 skills`

| Skill | What it does |
|---|---|
| [`frontend-ui-engineering`](frontend/frontend-ui-engineering/SKILL.md) | Production-grade UI engineering patterns |
| [`web-design-guidelines`](frontend/web-design-guidelines/SKILL.md) | Visual design, typography, spacing, accessibility |
| [`performance-optimization`](frontend/performance-optimization/SKILL.md) | Frontend and backend performance — measure first |
| [`remotion-best-practices`](frontend/remotion-best-practices/SKILL.md) | Programmatic video with Remotion |
| [`extract-design-system`](frontend/extract-design-system/SKILL.md) | Reverse-engineer a website's design tokens via Playwright |

### Testing `2 skills`

| Skill | What it does |
|---|---|
| [`playwright-best-practices`](testing/playwright-best-practices/SKILL.md) | E2E testing — selectors, fixtures, parallelism |
| [`browser-testing-with-devtools`](testing/browser-testing-with-devtools/SKILL.md) | DevTools-driven testing and debugging |

### Utilities `4 skills`

| Skill | What it does |
|---|---|
| [`using-agent-skills`](utils/using-agent-skills/SKILL.md) | How to discover and invoke skills effectively |
| [`audit-website`](utils/audit-website/SKILL.md) | Full-site audit — performance, SEO, accessibility |
| [`compress`](utils/compress/SKILL.md) | Lossless context compression for long conversations |
| [`caveman-compress`](utils/caveman-compress/SKILL.md) | Aggressive compression when token budget is critical |

---

## Knowledge Graph

This repo includes a graphify knowledge graph (`graphify-out/`) that maps relationships between all 76 skills — which ones share concepts, which cluster together, and which bridge multiple domains.

Open `graphify-out/graph.html` in any browser to explore the interactive graph.

To rebuild the graph after adding new skills:

```
/graphify .
```

---

## Adding Skills

Each skill lives inside its category folder with a single `SKILL.md` file:

```
<category>/
└── my-skill/
    └── SKILL.md
```

A minimal `SKILL.md`:

```markdown
<!-- Source: https://skills.sh/<user>/<repo>/<skill> -->
<!-- Install: npx skills add https://github.com/<user>/<repo> --skill my-skill -->
---
name: my-skill
description: One-line description of what this skill does and when to use it.
---

# My Skill

## When to Use
...

## Core Principles
...
```

Pull requests welcome.

---

## Sources

Skills in this library are sourced from upstream authors (tracked in each `SKILL.md` via `<!-- Source: -->` and `<!-- Install: -->` comments) and custom-authored skills. Key upstream collections include:

- [analogjs/angular-skills](https://github.com/analogjs/angular-skills) — Angular skills
- [apollographql/skills](https://github.com/apollographql/skills) — Rust best practices
- [affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code) — Bun runtime, Go, Rust testing
- [squirrelscan/skills](https://github.com/squirrelscan/skills) — Website audit
- [xixu-me/skills](https://github.com/xixu-me/skills) — Linux web hosting
- [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) — Vercel, web design
- [currents-dev/playwright-best-practices-skill](https://github.com/currents-dev/playwright-best-practices-skill) — Playwright
- [remotion-dev/skills](https://github.com/remotion-dev/skills) — Remotion
- [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) — SEO & content
- Custom skills authored for this library — all `engineering/`, `utils/`, and others without a Source comment
