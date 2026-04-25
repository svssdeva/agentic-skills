# agentic-skills

> A curated library of **69 skills** for Claude Code — drop-in behavioral modules that make your AI agent smarter, faster, and domain-aware.

Skills are plain markdown files (`SKILL.md`) that Claude reads before acting. Each one encodes expert knowledge, workflows, and guardrails for a specific domain. No code to install — just point Claude at the folder.

---

## What's a Skill?

A skill is a `SKILL.md` file that tells Claude *how* to behave in a given context. When you invoke a skill, Claude loads it and follows its instructions exactly — like hiring a specialist for the task at hand.

```
/skill angular-component    → expert Angular component authoring
/skill rust-engineer        → idiomatic Rust with ownership & error handling
/skill seo-audit            → structured technical SEO review
/skill test-driven-development → red-green-refactor discipline
```

Skills cover everything from language idioms to development methodologies to content strategy.

---

## Using Skills in Claude Code

**Install** — clone this repo anywhere and point Claude at it in your project's `CLAUDE.md`:

```bash
git clone https://github.com/your-username/agentic-skills ~/.claude/skills
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
Using spec-driven-development + test-driven-development, implement this feature.
```

---

## Skill Library

### Angular `9 skills`

| Skill | What it does |
|---|---|
| [`angular-component`](angular-component/SKILL.md) | Idiomatic component authoring with smart/dumb separation |
| [`angular-developer`](angular-developer/SKILL.md) | Full Angular developer persona — architecture to deployment |
| [`angular-di`](angular-di/SKILL.md) | Dependency injection patterns, tokens, providers |
| [`angular-directives`](angular-directives/SKILL.md) | Structural and attribute directive authoring |
| [`angular-forms`](angular-forms/SKILL.md) | Reactive forms, validation, form arrays |
| [`angular-http`](angular-http/SKILL.md) | HttpClient, interceptors, error handling |
| [`angular-signals`](angular-signals/SKILL.md) | Signals, computed, effects — Angular reactivity model |
| [`angular-testing`](angular-testing/SKILL.md) | Unit and integration testing with TestBed |
| [`angular-tooling`](angular-tooling/SKILL.md) | CLI, build config, workspace setup |

### Astro `5 skills`

| Skill | What it does |
|---|---|
| [`astro`](astro/SKILL.md) | Core Astro patterns and component model |
| [`astro-architecture`](astro-architecture/SKILL.md) | Island architecture, routing, content collections |
| [`astro-expert`](astro-expert/SKILL.md) | Advanced Astro — SSR, adapters, integrations |
| [`astro-seo`](astro-seo/SKILL.md) | SEO-first Astro builds with structured data |
| [`perf-astro`](perf-astro/SKILL.md) | Core Web Vitals optimization for Astro sites |

### Bun `3 skills`

| Skill | What it does |
|---|---|
| [`bun`](bun/SKILL.md) | Bun fundamentals — APIs, built-ins, gotchas |
| [`bun-development`](bun-development/SKILL.md) | Bun-first development workflows and patterns |
| [`bun-runtime`](bun-runtime/SKILL.md) | Runtime internals, FFI, native modules |

### Rust `4 skills`

| Skill | What it does |
|---|---|
| [`rust-engineer`](rust-engineer/SKILL.md) | Idiomatic Rust — ownership, lifetimes, traits |
| [`rust-best-practices`](rust-best-practices/SKILL.md) | Clippy-clean code, error handling, API design |
| [`rust-async-patterns`](rust-async-patterns/SKILL.md) | Tokio, async/await, channels, cancellation |
| [`rust-testing`](rust-testing/SKILL.md) | Unit tests, integration tests, property testing |

### TypeScript `2 skills`

| Skill | What it does |
|---|---|
| [`typescript-expert`](typescript-expert/SKILL.md) | Full TypeScript expertise — types, config, tooling |
| [`typescript-advanced-types`](typescript-advanced-types/SKILL.md) | Conditional types, mapped types, template literals |

### Tailwind CSS `3 skills`

| Skill | What it does |
|---|---|
| [`tailwind-css-patterns`](tailwind-css-patterns/SKILL.md) | Component patterns and design token usage |
| [`tailwind-design-system`](tailwind-design-system/SKILL.md) | Design system authoring with Tailwind |
| [`tailwindcss-advanced-layouts`](tailwindcss-advanced-layouts/SKILL.md) | Grid, flex, and responsive layout mastery |

### Mobile & Cross-Platform `4 skills`

| Skill | What it does |
|---|---|
| [`ionic`](ionic/SKILL.md) | Ionic components, navigation, native APIs |
| [`ionic-design`](ionic-design/SKILL.md) | Ionic design system and theming |
| [`capacitor-best-practices`](capacitor-best-practices/SKILL.md) | Capacitor plugins, native bridging, deployment |
| [`expo-tailwind-setup`](expo-tailwind-setup/SKILL.md) | Expo + NativeWind (Tailwind) setup and patterns |

### Cloud & DevOps `5 skills`

| Skill | What it does |
|---|---|
| [`aws-solution-architect`](aws-solution-architect/SKILL.md) | AWS architecture — well-architected, cost-aware |
| [`aws-diagrams`](aws-diagrams/SKILL.md) | Infrastructure diagrams as code |
| [`ci-cd-and-automation`](ci-cd-and-automation/SKILL.md) | Pipelines, GitHub Actions, release automation |
| [`vercel-react-best-practices`](vercel-react-best-practices/SKILL.md) | React on Vercel — SSR, caching, edge functions |
| [`vercel-composition-patterns`](vercel-composition-patterns/SKILL.md) | Vercel composability — monorepos, turborepo |

### SEO & Content `7 skills`

| Skill | What it does |
|---|---|
| [`ai-seo`](ai-seo/SKILL.md) | SEO for LLM-driven discovery — AIO, GEO, AEO |
| [`seo-audit`](seo-audit/SKILL.md) | Technical SEO audit with actionable findings |
| [`seo-geo`](seo-geo/SKILL.md) | Geo-targeted SEO, hreflang, local search |
| [`programmatic-seo`](programmatic-seo/SKILL.md) | Programmatic page generation for SEO at scale |
| [`content-strategy`](content-strategy/SKILL.md) | Content planning, ICP alignment, funnel mapping |
| [`social-content`](social-content/SKILL.md) | Social-first content with engagement hooks |
| [`product-marketing-context`](product-marketing-context/SKILL.md) | Product marketing framing and messaging |

### Development Methodology `16 skills`

| Skill | What it does |
|---|---|
| [`test-driven-development`](test-driven-development/SKILL.md) | Red-green-refactor discipline, enforced |
| [`spec-driven-development`](spec-driven-development/SKILL.md) | Spec-first — design the contract before the code |
| [`source-driven-development`](source-driven-development/SKILL.md) | Let the source of truth drive implementation |
| [`incremental-implementation`](incremental-implementation/SKILL.md) | Ship in small, safe, reviewable increments |
| [`planning-and-task-breakdown`](planning-and-task-breakdown/SKILL.md) | Task decomposition and sequencing |
| [`idea-refine`](idea-refine/SKILL.md) | Sharpen vague ideas into actionable specs |
| [`code-review-and-quality`](code-review-and-quality/SKILL.md) | Thorough code review with prioritized feedback |
| [`code-simplification`](code-simplification/SKILL.md) | Remove accidental complexity ruthlessly |
| [`context-engineering`](context-engineering/SKILL.md) | Prompt and context design for AI-native systems |
| [`debugging-and-error-recovery`](debugging-and-error-recovery/SKILL.md) | Systematic debugging — hypothesize, isolate, verify |
| [`api-and-interface-design`](api-and-interface-design/SKILL.md) | Stable, hard-to-misuse API design (Hyrum's Law-aware) |
| [`documentation-and-adrs`](documentation-and-adrs/SKILL.md) | Docs and Architecture Decision Records |
| [`deprecation-and-migration`](deprecation-and-migration/SKILL.md) | Safe deprecation paths and migration strategies |
| [`security-and-hardening`](security-and-hardening/SKILL.md) | Security review, threat modeling, hardening |
| [`git-workflow-and-versioning`](git-workflow-and-versioning/SKILL.md) | Branching, commits, tagging, release flow |
| [`shipping-and-launch`](shipping-and-launch/SKILL.md) | Launch checklist, rollout strategy, monitoring |

### Frontend & Design `4 skills`

| Skill | What it does |
|---|---|
| [`frontend-ui-engineering`](frontend-ui-engineering/SKILL.md) | Production-grade UI engineering patterns |
| [`web-design-guidelines`](web-design-guidelines/SKILL.md) | Visual design, typography, spacing, accessibility |
| [`performance-optimization`](performance-optimization/SKILL.md) | Frontend and backend performance — measure first |
| [`remotion-best-practices`](remotion-best-practices/SKILL.md) | Programmatic video with Remotion |

### Testing `2 skills`

| Skill | What it does |
|---|---|
| [`playwright-best-practices`](playwright-best-practices/SKILL.md) | E2E testing — selectors, fixtures, parallelism |
| [`browser-testing-with-devtools`](browser-testing-with-devtools/SKILL.md) | DevTools-driven testing and debugging |

### Utilities `5 skills`

| Skill | What it does |
|---|---|
| [`using-agent-skills`](using-agent-skills/SKILL.md) | How to discover and invoke skills effectively |
| [`audit-website`](audit-website/SKILL.md) | Full-site audit — performance, SEO, accessibility |
| [`m15-anti-pattern`](m15-anti-pattern/SKILL.md) | Detect and fix the M15 anti-pattern |
| [`compress`](compress/SKILL.md) | Lossless context compression for long conversations |
| [`caveman-compress`](caveman-compress/SKILL.md) | Aggressive compression when token budget is critical |

---

## Knowledge Graph

This repo includes a graphify knowledge graph (`graphify-out/`) that maps relationships between all 69 skills — which ones share concepts, which cluster together, and which bridge multiple domains.

Open `graphify-out/graph.html` in any browser to explore the interactive graph.

To rebuild the graph after adding new skills:

```
/graphify .
```

---

## Adding Skills

Each skill lives in its own folder with a single `SKILL.md` file:

```
my-skill/
└── SKILL.md
```

A minimal `SKILL.md`:

```markdown
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

Skills in this library are sourced from:

- [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) — development methodology and engineering skills
- Custom skills built for specific frameworks and domains
