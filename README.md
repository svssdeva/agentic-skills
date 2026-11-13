# agentic-skills

> A curated library of **204 drop-in skills** for Claude Code — behavioral modules that make your AI agent smarter, faster, and domain-aware across 24 domains.

Skills are plain markdown (`SKILL.md`) files that Claude reads *before* it acts. Each one encodes the expert knowledge, workflow, and guardrails for a single domain — like hiring a specialist for the task at hand. There is nothing to compile and no runtime: point Claude at the folder and invoke a skill by name.

> [!TIP]
> New here? Browse every skill by category in the [Skill Library](#skill-library), or skip to [Getting Started](#getting-started) to wire them into your own project.

---

## Highlights

- **204 skills across 24 domains** — languages (Rust, Go, Python, TypeScript), frameworks (Angular, React, Astro, NestJS), and disciplines (testing, SEO, engineering practice, design, AI/RAG).
- **Zero install** — each skill is a single markdown file. No dependencies, no build step, no lock-in.
- **Stackable** — combine skills (for example, spec-driven + test-driven development) for compound expertise.
- **Provenance-tracked** — every imported skill records its upstream source and stays syncable. See [Sources](#sources).

---

## What's a Skill?

A skill is a `SKILL.md` file that tells Claude *how* to behave in a given context. When you invoke one, Claude loads it and follows its instructions exactly — covering everything from language idioms to development methodologies to content strategy.

```
/skill angular/angular-component            → expert Angular component authoring
/skill rust/rust-engineer                   → idiomatic Rust with ownership & error handling
/skill seo/reddit-automation                → Reddit automation for SEO and marketing
/skill engineering/tdd                      → red-green-refactor discipline
```

---

## Getting Started

**Install** — clone this repo anywhere and point Claude at it from your project's `CLAUDE.md`:

```bash
git clone https://github.com/svssdeva/agentic-skills ~/.claude/skills
```

**Invoke** — type a slash command in Claude Code:

```
/skill <category>/<skill-name>
```

Or reference a skill directly in your prompt:

```
Using the rust-engineer skill, refactor this module to use proper error propagation.
```

**Stack skills** — combine skills for compound expertise:

```
Using engineering/spec-driven-development + engineering/tdd, implement this feature.
```

---

## Skill Library

### Angular `10 skills`

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
| [`angular-new-app`](angular/angular-new-app/SKILL.md) | Scaffold a new Angular app with the Angular CLI (official angular/skills) |

### Astro `4 skills`

| Skill | What it does |
|---|---|
| [`astro`](astro/astro/SKILL.md) | Core Astro patterns and component model |
| [`astro-architecture`](astro/astro-architecture/SKILL.md) | Island architecture, routing, content collections |
| [`astro-expert`](astro/astro-expert/SKILL.md) | Advanced Astro — SSR, adapters, integrations |
| [`perf-astro`](astro/perf-astro/SKILL.md) | Core Web Vitals optimization for Astro sites |

### Bun `1 skill`

| Skill | What it does |
|---|---|
| [`bun`](bun/bun/SKILL.md) | Bun fundamentals — APIs, built-ins, gotchas |

### Rust `9 skills`

| Skill | What it does |
|---|---|
| [`rust-engineer`](rust/rust-engineer/SKILL.md) | Idiomatic Rust — ownership, lifetimes, traits |
| [`rust-best-practices`](rust/rust-best-practices/SKILL.md) | Clippy-clean code, error handling, API design |
| [`rust-async-patterns`](rust/rust-async-patterns/SKILL.md) | Tokio, async/await, channels, cancellation |
| [`rust-testing`](rust/rust-testing/SKILL.md) | Unit tests, integration tests, property testing |
| [`m15-anti-pattern`](rust/m15-anti-pattern/SKILL.md) | Detect and fix the M15 anti-pattern |
| [`tauri-v2`](rust/tauri-v2/SKILL.md) | Cross-platform desktop/mobile apps — tauri.conf.json, Rust commands, IPC, capabilities |
| [`tree-sitter-parsing`](rust/tree-sitter-parsing/SKILL.md) | Parse source to ASTs, grammar/ABI management, queries, generic walker |
| [`rusqlite-graph-store`](rust/rusqlite-graph-store/SKILL.md) | Embedded SQLite store, WAL, bounded graph BFS via recursive CTE |
| [`cargo-workspace-scaffold`](rust/cargo-workspace-scaffold/SKILL.md) | Library-first multi-crate workspace + cross-platform determinism CI |

### TypeScript `4 skills`

| Skill | What it does |
|---|---|
| [`typescript-expert`](typescript/typescript-expert/SKILL.md) | Full TypeScript expertise — types, config, tooling |
| [`typescript-advanced-types`](typescript/typescript-advanced-types/SKILL.md) | Conditional types, mapped types, template literals |
| [`typescript-pro`](typescript/typescript-pro/SKILL.md) | Advanced type systems — type guards, utility types, branded types, build optimization |
| [`modern-javascript-patterns`](typescript/modern-javascript-patterns/SKILL.md) | ES6+ and functional patterns — async/await, destructuring, memoization, throttling |

### Tailwind CSS `3 skills`

| Skill | What it does |
|---|---|
| [`tailwind-css-patterns`](tailwind/tailwind-css-patterns/SKILL.md) | Component patterns and design token usage |
| [`tailwind-design-system`](tailwind/tailwind-design-system/SKILL.md) | Design system authoring with Tailwind |
| [`tailwindcss-advanced-layouts`](tailwind/tailwindcss-advanced-layouts/SKILL.md) | Grid, flex, and responsive layout mastery |

### Mobile & Cross-Platform `2 skills`

| Skill | What it does |
|---|---|
| [`capacitor-best-practices`](mobile/capacitor-best-practices/SKILL.md) | Capacitor plugins, native bridging, deployment |
| [`sleek-design-mobile-apps`](mobile/sleek-design-mobile-apps/SKILL.md) | AI-powered mobile app design via Sleek API |

### Cloud & DevOps `4 skills`

| Skill | What it does |
|---|---|
| [`aws-solution-architect`](cloud/aws-solution-architect/SKILL.md) | AWS architecture — well-architected, cost-aware |
| [`aws-diagrams`](cloud/aws-diagrams/SKILL.md) | Infrastructure diagrams as code |
| [`ci-cd-and-automation`](cloud/ci-cd-and-automation/SKILL.md) | Pipelines, GitHub Actions, release automation |
| [`secure-linux-web-hosting`](cloud/secure-linux-web-hosting/SKILL.md) | Harden a cloud Linux server — SSH, firewall, Nginx, HTTPS |

### Docker & Containers `3 skills`

| Skill | What it does |
|---|---|
| [`docker-expert`](docker/docker-expert/SKILL.md) | Container optimization, security hardening, multi-stage builds, production deployment |
| [`docker-patterns`](docker/docker-patterns/SKILL.md) | Docker Compose, local-dev orchestration, networking, volumes, container security |
| [`multi-stage-dockerfile`](docker/multi-stage-dockerfile/SKILL.md) | Optimized, secure multi-stage Dockerfiles for any language or framework |

### AI & RAG `5 skills`

| Skill | What it does |
|---|---|
| [`rag-architect`](ai/rag-architect/SKILL.md) | Production RAG design — chunking, embeddings, hybrid search, reranking, evaluation |
| [`vector-index-tuning`](ai/vector-index-tuning/SKILL.md) | Tune vector indexes — HNSW params, quantization, recall/latency/memory |
| [`ai-research-explore`](ai/ai-research-explore/SKILL.md) | Structured deep-learning research exploration — candidate generation and novelty checks |
| [`ai-image-generation`](ai/ai-image-generation/SKILL.md) | Generate images with 50+ models (FLUX, GPT-Image, Gemini, Seedream) via the belt / inference.sh CLI |
| [`retrieval-strategy`](ai/retrieval-strategy/SKILL.md) | Pick a retrieval strategy before buying a vector index — one-shot RAG vs agent loop vs BM25 vs MCP connectors vs compiled wiki |

### Database `7 skills`

| Skill | What it does |
|---|---|
| [`neon-postgres`](database/neon-postgres/SKILL.md) | Neon Serverless Postgres — branching, autoscaling, pooling, SDKs, CLI/MCP |
| [`postgresql-optimization`](database/postgresql-optimization/SKILL.md) | PostgreSQL-specific features — JSONB, arrays, custom types, full-text, tuning |
| [`prisma-orm-setup`](database/prisma-orm-setup/SKILL.md) | Set up Prisma ORM 8 against Postgres, MySQL, SQLite, or MongoDB |
| [`prisma-postgres-setup`](database/prisma-postgres-setup/SKILL.md) | Prisma Postgres — Console, create-db CLI, Management API and SDK |
| [`prisma-upgrade-v7`](database/prisma-upgrade-v7/SKILL.md) | Migrate Prisma ORM v6 → v7, covering every breaking change |
| [`prisma-driver-adapter-implementation`](database/prisma-driver-adapter-implementation/SKILL.md) | Implement and modify Prisma 7 SQL driver adapters |
| [`supabase`](database/supabase/SKILL.md) | Supabase end to end — Database, Auth, Edge Functions, Realtime, Storage, RLS |

### SEO & Content `12 skills`

| Skill | What it does |
|---|---|
| [`content-strategy`](seo/content-strategy/SKILL.md) | Content planning, ICP alignment, funnel mapping |
| [`social-content`](seo/social-content/SKILL.md) | Social-first content with engagement hooks |
| [`product-marketing-context`](seo/product-marketing-context/SKILL.md) | Product marketing framing and messaging |
| [`copywriting`](seo/copywriting/SKILL.md) | Conversion copywriting — headlines, value props, CTAs, and messaging frameworks |
| [`marketing-psychology`](seo/marketing-psychology/SKILL.md) | Behavioral science and mental models for persuasion and decision-making |
| [`marketing-ideas`](seo/marketing-ideas/SKILL.md) | Generate marketing campaign and growth-channel ideas |
| [`analytics-tracking`](seo/analytics-tracking/SKILL.md) | Set up and audit analytics and measurement (GA4, GTM, events) |
| [`site-architecture`](seo/site-architecture/SKILL.md) | Plan SEO-friendly site structure, URLs, and internal linking |
| [`competitor-alternatives`](seo/competitor-alternatives/SKILL.md) | Build competitor comparison and alternative pages for SEO and sales |
| [`cro`](seo/cro/SKILL.md) | Conversion-rate optimization for marketing pages and lead-capture forms |
| [`aso`](seo/aso/SKILL.md) | App Store / Google Play listing optimization (ASO) — keywords, conversion, ranking |
| [`reddit-automation`](seo/reddit-automation/SKILL.md) | Find Reddit threads worth answering and draft disclosed, useful replies |

### NestJS `3 skills`

| Skill | What it does |
|---|---|
| [`nestjs-best-practices`](nestjs/nestjs-best-practices/SKILL.md) | 40 NestJS rules across architecture, DI, security, performance, testing, and DevOps |
| [`nestjs-expert`](nestjs/nestjs-expert/SKILL.md) | Full module/controller/service/DTO/test workflow with enforced MUST/MUST NOT constraints |
| [`nestjs-patterns`](nestjs/nestjs-patterns/SKILL.md) | Feature module structure, thin controllers, global ValidationPipe, guard and interceptor patterns |

### Python `7 skills`

| Skill | What it does |
|---|---|
| [`python-design-patterns`](python/python-design-patterns/SKILL.md) | KISS, SRP, composition over inheritance, rule of three, and dependency injection for Python |
| [`python-testing-patterns`](python/python-testing-patterns/SKILL.md) | pytest fixtures, parametrize, mocking, freezegun, markers, and coverage reporting |
| [`python-performance-optimization`](python/python-performance-optimization/SKILL.md) | cProfile, line_profiler, memory_profiler, py-spy, generators, and async profiling |
| [`dataverse-python-quickstart`](python/dataverse-python-quickstart/SKILL.md) | Microsoft Dataverse SDK setup — CRUD, bulk ops, paging, and file upload snippets |
| [`dataverse-python-advanced-patterns`](python/dataverse-python-advanced-patterns/SKILL.md) | Dataverse production patterns — retry logic, batch ops, OData queries, chunked file upload |
| [`dataverse-python-usecase-builder`](python/dataverse-python-usecase-builder/SKILL.md) | Architecture framework for Dataverse use cases — 6 categories from CRM to compliance |
| [`async-python-patterns`](python/async-python-patterns/SKILL.md) | Python asyncio, concurrency, and async/await patterns for I/O-bound apps |

### Engineering Practices `46 skills`

| Skill | What it does |
|---|---|
| [`tdd`](engineering/tdd/SKILL.md) | TDD with vertical tracer-bullet slicing — behavior-first, no horizontal slicing |
| [`spec-driven-development`](engineering/spec-driven-development/SKILL.md) | Spec-first — design the contract before the code |
| [`source-driven-development`](engineering/source-driven-development/SKILL.md) | Let the source of truth drive implementation |
| [`incremental-implementation`](engineering/incremental-implementation/SKILL.md) | Ship in small, safe, reviewable increments |
| [`improve-codebase-architecture`](engineering/improve-codebase-architecture/SKILL.md) | Surface shallow modules and propose deepening opportunities |
| [`idea-refine`](engineering/idea-refine/SKILL.md) | Sharpen vague ideas into actionable specs |
| [`code-simplification`](engineering/code-simplification/SKILL.md) | Remove accidental complexity ruthlessly |
| [`context-engineering`](engineering/context-engineering/SKILL.md) | Prompt and context design for AI-native systems |
| [`api-and-interface-design`](engineering/api-and-interface-design/SKILL.md) | Stable, hard-to-misuse API design (Hyrum's Law-aware) |
| [`documentation-and-adrs`](engineering/documentation-and-adrs/SKILL.md) | Docs and Architecture Decision Records |
| [`deprecation-and-migration`](engineering/deprecation-and-migration/SKILL.md) | Safe deprecation paths and migration strategies |
| [`security-and-hardening`](engineering/security-and-hardening/SKILL.md) | Security review, threat modeling, hardening |
| [`git-workflow-and-versioning`](engineering/git-workflow-and-versioning/SKILL.md) | Branching, commits, tagging, release flow |
| [`shipping-and-launch`](engineering/shipping-and-launch/SKILL.md) | Launch checklist, rollout strategy, monitoring |
| [`system-design`](engineering/system-design/SKILL.md) | Structured system design — requirements to trade-off analysis |
| [`architecture-patterns`](engineering/architecture-patterns/SKILL.md) | Clean, Hexagonal, and Domain-Driven Design backend architecture patterns |
| [`karpathy-guidelines`](engineering/karpathy-guidelines/SKILL.md) | Behavioral guidelines to reduce common LLM coding mistakes — surgical changes |
| [`documentation-writer`](engineering/documentation-writer/SKILL.md) | Diátaxis-framework technical documentation authoring |
| [`create-readme`](engineering/create-readme/SKILL.md) | Generate a project README.md |
| [`prd`](engineering/prd/SKILL.md) | Generate Product Requirements Documents — user stories, specs, risk analysis |
| [`email-and-password-best-practices`](engineering/email-and-password-best-practices/SKILL.md) | Better Auth email/password — verification, reset flows, policies, hashing |
| [`codebase-design`](engineering/codebase-design/SKILL.md) | Design deep modules — interface depth, boundaries, and shared vocabulary |
| [`diagnosing-bugs`](engineering/diagnosing-bugs/SKILL.md) | Diagnosis loop for hard bugs and performance regressions |
| [`to-spec`](engineering/to-spec/SKILL.md) | Turn the current conversation into a spec and publish it to the issue tracker |
| [`teach`](engineering/teach/SKILL.md) | Teach a new skill or concept in the context of this workspace |
| [`loop-me`](engineering/loop-me/SKILL.md) | Get grilled about the specs for workflows you want to build |
| [`writing-fragments`](engineering/writing-fragments/SKILL.md) | Writing, explore — mine raw fragments before any structure |
| [`writing-shape`](engineering/writing-shape/SKILL.md) | Writing, exploit — shape raw material into an article, paragraph by paragraph |
| [`writing-beats`](engineering/writing-beats/SKILL.md) | Writing, exploit — assemble material into a journey of grounded beats |
| [`domain-modeling`](engineering/domain-modeling/SKILL.md) | Build and sharpen the domain model — GLOSSARY.md ubiquitous language and ADRs |
| [`prototype`](engineering/prototype/SKILL.md) | Throwaway prototype to settle an ungrillable design question (UI or logic) |
| [`implement-spec`](engineering/implement-spec/SKILL.md) | Build a whole spec in one run — ticket task graph, parallel worktree implementers, one integration branch |
| [`retro`](engineering/retro/SKILL.md) | Retrospective on a coding session — suggests environment changes: pointers, deterministic checks, standards |
| [`to-questionnaire`](engineering/to-questionnaire/SKILL.md) | Turn a decision you cannot answer into a questionnaire for someone else to fill in |
| [`wizard`](engineering/wizard/SKILL.md) | Generate an interactive bash wizard for steps only a human can perform (credentials, dashboards, CI secrets) |
| [`writing-for-agents`](engineering/writing-for-agents/SKILL.md) | Writing documents for agents — skills, AGENTS.md, CLAUDE.md |
| [`reverse-engineer-anything`](engineering/reverse-engineer-anything/SKILL.md) | REA — reverse engineer native, Electron/JS, .NET, Android and web targets via MCP; evidence, graph, limitations, unknowns |
| [`agentic-build-primitives`](engineering/agentic-build-primitives/SKILL.md) | Primitives-first agentic app building — AGENTS.md rules, per-dependency skills, prompt order, durable workers, API emulators and screenshot verification |
| [`principle-attack-the-premise`](engineering/principle-attack-the-premise/SKILL.md) | After two fixes on one premise fail the same gate, write the premise down and test it before fix three (pstack) |
| [`principle-type-system-discipline`](engineering/principle-type-system-discipline/SKILL.md) | Make illegal states unrepresentable, brand primitives, parse at boundaries, exhaust variants (pstack) |
| [`deslop`](engineering/deslop/SKILL.md) | Remove AI slop from a branch diff — needless comments, defensive try/catch, `any` casts, deep nesting (Cursor team kit, via pstack) |
| [`grilling`](engineering/grilling/SKILL.md) | Grill the user relentlessly about a plan — maps the decision tree, asks the whole frontier each round |
| [`handoff`](engineering/handoff/SKILL.md) | Compact the current conversation into a handoff document for another agent |
| [`code-review`](engineering/code-review/SKILL.md) | Two-axis review of a diff since a fixed point — Standards (code smells) and Spec — by fresh reviewers |
| [`pr`](engineering/pr/SKILL.md) | PR body shape — smallest visual of the change, before/after evidence, merge-danger (one-way vs two-way door) |
| [`research`](engineering/research/SKILL.md) | Investigate a question against primary sources and capture findings as a Markdown file in the repo |

### Go `3 skills`

| Skill | What it does |
|---|---|
| [`golang-pro`](golang/golang-pro/SKILL.md) | Concurrent Go dev with goroutines, microservices, pprof optimization |
| [`golang-patterns`](golang/golang-patterns/SKILL.md) | Idiomatic Go patterns, error handling, concurrency, interfaces |
| [`golang-testing`](golang/golang-testing/SKILL.md) | Table-driven tests, benchmarks, fuzzing, TDD workflows |

### React `6 skills`

| Skill | What it does |
|---|---|
| [`vercel-react-best-practices`](react/vercel-react-best-practices/SKILL.md) | 70 React/Next.js performance rules from Vercel Engineering |
| [`vercel-react-view-transitions`](react/vercel-react-view-transitions/SKILL.md) | Native View Transition API animations — shared elements, route changes, Suspense reveals |
| [`react-components`](react/react-components/SKILL.md) | Convert Stitch designs into modular, type-safe React components |
| [`vercel-composition-patterns`](react/vercel-composition-patterns/SKILL.md) | React composition patterns that scale — compound components, context providers, React 19 APIs |
| [`react-doctor`](react/react-doctor/SKILL.md) | Scan and triage React diagnostics — lint, a11y, bundle size, architecture |
| [`react-modernization`](react/react-modernization/SKILL.md) | Upgrade React — class-to-hooks migration, concurrent features, latest versions |

### Frontend & Design `36 skills`

| Skill | What it does |
|---|---|
| [`frontend-ui-engineering`](frontend/frontend-ui-engineering/SKILL.md) | Production-grade UI engineering patterns |
| [`web-design-guidelines`](frontend/web-design-guidelines/SKILL.md) | Visual design, typography, spacing, accessibility |
| [`performance-optimization`](frontend/performance-optimization/SKILL.md) | Frontend and backend performance — measure first |
| [`remotion-best-practices`](frontend/remotion-best-practices/SKILL.md) | Programmatic video with Remotion |
| [`extract-design-system`](frontend/extract-design-system/SKILL.md) | Reverse-engineer a website's design tokens via Playwright |
| [`interface-design`](frontend/interface-design/SKILL.md) | Interface design for dashboards, admin panels, apps, and tools |
| [`redesign-existing-projects`](frontend/redesign-existing-projects/SKILL.md) | Upgrade existing sites/apps to premium quality without breaking functionality |
| [`impeccable`](frontend/impeccable/SKILL.md) | Design, critique, polish, and harden any frontend interface — live iteration |
| [`design-system-patterns`](frontend/design-system-patterns/SKILL.md) | Scalable design systems — tokens, theming, component architecture |
| [`responsive-design`](frontend/responsive-design/SKILL.md) | Responsive layouts — container queries, fluid type, CSS Grid, mobile-first |
| [`frontend-patterns`](frontend/frontend-patterns/SKILL.md) | React/Next.js frontend patterns — state, performance, UI best practices |
| [`web-quality-performance`](frontend/web-quality-performance/SKILL.md) | Web performance optimization — faster loading, reduced load time (Lighthouse) |
| [`web-quality-best-practices`](frontend/web-quality-best-practices/SKILL.md) | Modern web best practices — security, compatibility, code-quality audits |
| [`anti-ui-slop`](frontend/anti-ui-slop/SKILL.md) | Stop generic agent UI — build product-specific interfaces from real screen references |
| [`design-taste-frontend`](frontend/design-taste-frontend/SKILL.md) | Anti-slop landing pages, portfolios, and redesigns with inferred design direction |
| [`apple-design`](frontend/apple-design/SKILL.md) | Apple's interface and fluid-motion principles translated for the web |
| [`imagegen-frontend-mobile`](frontend/imagegen-frontend-mobile/SKILL.md) | Premium app-native mobile screen concepts and flows via image generation |
| [`image-to-code`](frontend/image-to-code/SKILL.md) | Image-first web design — generate section design images, then implement to match |
| [`hallmark`](frontend/hallmark/SKILL.md) | Anti-AI-slop design skill (v2.0) — a non-waivable floor, 50 themes, 21 macrostructures, redesign / audit verbs, Node lint scripts (`sloplint`) |
| [`subframe-motion`](frontend/subframe-motion/SKILL.md) | Subframe Motion catalogue — 309 copy-paste React animations, motion components and WebGL shaders, licence headers kept; optional no-account MCP |
| [`scroll-world`](frontend/scroll-world/SKILL.md) | Scroll-scrubbed cinematic "fly through the world" landing page from AI-generated clips (Higgsfield / Runway via MCP) |
| [`stitch`](frontend/stitch/SKILL.md) | Google Stitch from the terminal — generate screens and variants, capture a running route into Stitch, extract / upload DESIGN.md, review a live app against it (the official `stitch agent-skills add` skill) |
| [`scrollytelling`](frontend/scrollytelling/SKILL.md) | Scroll-driven storytelling — pinned sections, progressive reveals, CSS scroll-timeline / IntersectionObserver / GSAP ScrollTrigger, reduced-motion and mobile rules |
| [`commodity-ceiling`](frontend/commodity-ceiling/SKILL.md) | Make features and pages feel premium — state table before code, check agent claims on the running UI, cross-screen consistency walk, break-it-on-purpose failure states |
| [`emil-design-eng`](frontend/emil-design-eng/SKILL.md) | Emil Kowalski's design-engineering philosophy — UI polish, component design, when and how to animate |
| [`animate`](frontend/animate/SKILL.md) | Build an animation from scratch in the right order — should it animate, purpose, trigger, easing, duration |
| [`review-animations`](frontend/review-animations/SKILL.md) | Review motion code against Emil's craft bar — ease-out, never ease-in, frequency-based durations, before/after/why notes |
| [`improve-animations`](frontend/improve-animations/SKILL.md) | Audit a codebase's motion code and write prioritized, self-contained implementation plans |
| [`find-animation-opportunities`](frontend/find-animation-opportunities/SKILL.md) | Read-only search for places that should animate (and the many that shouldn't), with exact values |
| [`animation-vocabulary`](frontend/animation-vocabulary/SKILL.md) | Reverse glossary — turn "the bouncy thing when a popover opens" into the exact motion term |
| [`animation-performance`](frontend/animation-performance/SKILL.md) | Keep web animations inside the frame budget — composite-only properties, off-main-thread motion, jank diagnosis |
| [`break-ui`](frontend/break-ui/SKILL.md) | Feed UI its worst-case data (long names, zero items, huge counts) behind a dev toggle and report what broke |
| [`ui-prototype`](frontend/ui-prototype/SKILL.md) | Build several genuinely different versions of a UI piece behind a live picker and promote the winner (Emil's `prototype`; installing it upstream as `prototype` collides with `engineering/prototype`) |
| [`mobile-native`](frontend/mobile-native/SKILL.md) | Make a web app feel native on a phone — tap states, 16px inputs, safe areas, meta tags |
| [`pick-ui-library`](frontend/pick-ui-library/SKILL.md) | Curated, opinionated library picks per frontend task — numbers, OTP, charts, command menus, drag and drop |
| [`ask-sonner`](frontend/ask-sonner/SKILL.md) | Sonner toast library guide — Toaster setup, toast() variants, promise toasts, updating and dismissing |

### 3D & WebGL `5 skills`

| Skill | What it does |
|---|---|
| [`3d-web-experience`](3d/3d-web-experience/SKILL.md) | Three.js, React Three Fiber, Spline, and WebGL for product configurators and immersive sites |
| [`web3d-integration-patterns`](3d/web3d-integration-patterns/SKILL.md) | Combine Three.js, GSAP ScrollTrigger, R3F, Motion, and React Spring in one app |
| [`lightweight-3d-effects`](3d/lightweight-3d-effects/SKILL.md) | Decorative pseudo-3D with Zdog, Vanta.js, and Vanilla-Tilt.js |
| [`threejs-3d-generator`](3d/threejs-3d-generator/SKILL.md) | Generate, texture, rig, and export 3D game assets via the Tripo API |
| [`spline`](3d/spline/SKILL.md) | Build and edit live Spline 3D scenes and 2D designs through the Spline MCP server — routing, authoring guides, screenshot-and-refine loop (official, needs MCP) |

### Game Development `21 skills`

Godot 4.7 subset of [gamedev-skills/awesome-gamedev-agent-skills](https://github.com/gamedev-skills/awesome-gamedev-agent-skills) (Apache-2.0), picked for a GDScript, web/Android, single-player pipeline. Unity, Unreal, C#, multiplayer and the router are not imported; install the upstream plugin for those.

| Skill | What it does |
|---|---|
| [`godot-gdscript`](gamedev/godot-gdscript/SKILL.md) | Idiomatic typed GDScript: node lifecycle, `@export`/`@onready`/`@tool`, signals, `await` |
| [`godot-nodes-scenes`](gamedev/godot-nodes-scenes/SKILL.md) | Scene tree and node composition, instancing `PackedScene`, autoload singletons |
| [`godot-signals-groups`](gamedev/godot-signals-groups/SKILL.md) | Event-driven gameplay with custom signals, Callables and node groups |
| [`godot-2d-movement`](gamedev/godot-2d-movement/SKILL.md) | `CharacterBody2D` + `move_and_slide()`: platformer and top-down movement, slopes, collisions |
| [`godot-tilemap`](gamedev/godot-tilemap/SKILL.md) | `TileMapLayer`/`TileSet`: terrain autotiling, collision/nav layers, cell access from code |
| [`godot-physics`](gamedev/godot-physics/SKILL.md) | Rigid/Static/Area/Character bodies, layers vs masks, contact signals, raycasts |
| [`godot-ui-control`](gamedev/godot-ui-control/SKILL.md) | `Control` UI: anchors, containers, themes, keyboard/gamepad focus |
| [`godot-animation`](gamedev/godot-animation/SKILL.md) | `AnimationPlayer`, `AnimationTree` and `Tween` |
| [`godot-shaders`](gamedev/godot-shaders/SKILL.md) | Godot shading language: `canvas_item` 2D and `spatial` 3D shaders, uniforms, screen reads |
| [`godot-3d-essentials`](gamedev/godot-3d-essentials/SKILL.md) | `Node3D`, cameras, lights, `WorldEnvironment`, materials, `GridMap` |
| [`godot-resources`](gamedev/godot-resources/SKILL.md) | Data-driven design with custom `Resource` classes and `.tres` files |
| [`godot-audio`](gamedev/godot-audio/SKILL.md) | `AudioStreamPlayer` variants, buses and effects, music vs SFX, beat sync |
| [`godot-export`](gamedev/godot-export/SKILL.md) | Export templates and presets (desktop, Web, Android), headless CLI builds, web COOP/COEP |
| [`godot-gdscript-headless-testing`](gamedev/godot-gdscript-headless-testing/SKILL.md) | GDScript tests via `godot --headless` with non-zero exit on failure for CI |
| [`game-feel`](gamedev/game-feel/SKILL.md) | Juice: screen shake, hit-stop, easing, squash and stretch, layered feedback |
| [`create-game-assets`](gamedev/create-game-assets/SKILL.md) | Art direction for cohesive sprites, tiles, UI and 3D assets: lock a target, build families, normalise, check in-game |
| [`procedural-gen`](gamedev/procedural-gen/SKILL.md) | Seeded RNG, noise, dungeon/grid generation (BSP, random walk, WFC), loot tables |
| [`save-systems`](gamedev/save-systems/SKILL.md) | What to serialise, slots, atomic crash-safe writes, schema versioning, autosave |
| [`puzzle`](gamedev/puzzle/SKILL.md) | Grid/board state, rule resolution (match-3, sokoban, tile logic), scoring, undo |
| [`prototype-fast`](gamedev/prototype-fast/SKILL.md) | One-hour greybox prototype to answer "is it fun?", with keep/kill criteria |
| [`steam-publish`](gamedev/steam-publish/SKILL.md) | Steamworks depots and packages, `steamcmd` uploads, branches, release checklist |

### Video `3 skills`

HyperFrames skills are installed from upstream into `~/.claude/skills` — see [INSTALL-EXTERNAL.md](INSTALL-EXTERNAL.md).

| Skill | What it does |
|---|---|
| [`video-edit`](video/video-edit/SKILL.md) | Agent-driven video editing pipeline |
| [`3d-animation-short-generator`](video/3d-animation-short-generator/SKILL.md) | Story-driven 3D animated shorts — concept, shot table, storyboard, render |
| [`ai-video-generation`](video/ai-video-generation/SKILL.md) | Generate videos with 40+ models (Veo, Seedance, Wan, Grok) via the belt / inference.sh CLI |

### Testing `2 skills`

| Skill | What it does |
|---|---|
| [`playwright-best-practices`](testing/playwright-best-practices/SKILL.md) | E2E testing — selectors, fixtures, parallelism |
| [`browser-testing-with-devtools`](testing/browser-testing-with-devtools/SKILL.md) | DevTools-driven testing and debugging |

### Productivity `2 skills`

| Skill | What it does |
|---|---|
| [`jira-integration`](productivity/jira-integration/SKILL.md) | Retrieve, analyze, update, and transition Jira tickets from your workflow |
| [`confluence`](productivity/confluence/SKILL.md) | Confluence pages and spaces — documentation and knowledge management |

### Utilities `6 skills`

| Skill | What it does |
|---|---|
| [`agent-browser`](utils/agent-browser/SKILL.md) | Browser automation CLI for AI agents — CDP, accessibility tree, Electron, Slack |
| [`audit-website`](utils/audit-website/SKILL.md) | Full-site audit — performance, SEO, accessibility |
| [`caveman-compress`](utils/caveman-compress/SKILL.md) | Compress CLAUDE.md / memory files into caveman-speak to save tokens |
| [`caveman`](utils/caveman/SKILL.md) | Ultra-compressed communication mode (~75% fewer tokens) |
| [`cuawright-web`](utils/cuawright-web/SKILL.md) | Drive a local Playwright browser to solve web tasks code-as-action, with screenshots |
| [`apify-ultimate-scraper`](utils/apify-ultimate-scraper/SKILL.md) | AI-powered web scraper for 25+ platforms via Apify actors |

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

> [!NOTE]
> When adding a skill, keep the counts in sync — bump the headline total and the per-category count, add a row to the matching table, then run `python3 scripts/check_skills.py`.

Pull requests welcome.

---

## Sources

Skills in this library are sourced from upstream authors (tracked in each `SKILL.md` via `<!-- Source: -->` and `<!-- Install: -->` comments) and custom-authored skills. Key upstream collections include:

- [analogjs/angular-skills](https://github.com/analogjs/angular-skills) — Angular skills
- [apollographql/skills](https://github.com/apollographql/skills) — Rust best practices
- [affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code) — Bun runtime, Go, Rust testing
- [squirrelscan/skills](https://github.com/squirrelscan/skills) — Website audit
- [xixu-me/skills](https://github.com/xixu-me/skills) — Linux web hosting
- [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) — Vercel, web design, React performance, React Native, composition patterns
- [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) — Browser automation CLI
- [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills) — Stitch-to-React component generation
- [mattpocock/skills](https://github.com/mattpocock/skills) — TDD, architecture, grilling, caveman mode
- [emilkowalski/skills](https://github.com/emilkowalski/skills) — animation, motion review, UI polish, Sonner, Swift (MIT)
- [michael-denyer/pstack-claude](https://github.com/michael-denyer/pstack-claude) — Claude port of Lauren Tan's Cursor pstack; only standalone skills imported, install the full plugin for the rest (MIT)
- [splinetool/spline-skills](https://github.com/splinetool/spline-skills) — Spline 3D scenes via the Spline MCP server (MIT)
- [gamedev-skills/awesome-gamedev-agent-skills](https://github.com/gamedev-skills/awesome-gamedev-agent-skills) — Godot 4.7 subset only; install the upstream plugin for the rest (Apache-2.0)
- [sleekdotdesign/agent-skills](https://github.com/sleekdotdesign/agent-skills) — Mobile app design via Sleek
- [juliusbrussee/caveman](https://github.com/juliusbrussee/caveman) — Caveman commit, review, compress
- [currents-dev/playwright-best-practices-skill](https://github.com/currents-dev/playwright-best-practices-skill) — Playwright
- [remotion-dev/skills](https://github.com/remotion-dev/skills) — Remotion
- [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) — SEO & content
- [kadajett/agent-nestjs-skills](https://github.com/kadajett/agent-nestjs-skills) — NestJS best practices
- [jeffallan/claude-skills](https://github.com/jeffallan/claude-skills) — NestJS expert workflow
- [affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code) — NestJS patterns, Bun, Go, Rust
- [wshobson/agents](https://github.com/wshobson/agents) — Python design patterns, testing, performance
- [github/awesome-copilot](https://github.com/github/awesome-copilot) — Dataverse Python SDK skills
- [addyosmani/web-quality-skills](https://github.com/addyosmani/web-quality-skills) — Lighthouse-based SEO, web performance, best practices
- [wshobson/agents](https://github.com/wshobson/agents) — Backend architecture, async Python, design systems, responsive design, LangChain, React modernization
- [leonxlnx/taste-skill](https://github.com/leonxlnx/taste-skill) — High-end visual design, minimalist UI, redesign
- [pbakaus/impeccable](https://github.com/pbakaus/impeccable) — Frontend interface design and critique
- [dammyjay93/interface-design](https://github.com/dammyjay93/interface-design) — Interface/product design
- [millionco/react-doctor](https://github.com/millionco/react-doctor) — React diagnostics scanner
- [neondatabase/agent-skills](https://github.com/neondatabase/agent-skills) — Neon Serverless Postgres
- [github/awesome-copilot](https://github.com/github/awesome-copilot) — Documentation, PRD, README, PostgreSQL optimization
- [better-auth/skills](https://github.com/better-auth/skills) — Email/password authentication best practices
- [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) — CRO, ASO, lead magnets
- [apify/agent-skills](https://github.com/apify/agent-skills) — Universal web scraper
- [microsoft/webwright](https://github.com/microsoft/webwright) — Playwright-driven web task automation
- [forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills) — LLM coding behavioral guidelines
- [juliusbrussee/caveman](https://github.com/juliusbrussee/caveman) — Cavecrew subagent delegation, caveman stats
- [nodnarbnitram/claude-code-extensions](https://github.com/nodnarbnitram/claude-code-extensions) — Tauri v2 development
- [morluto/rea](https://github.com/morluto/rea) — Reverse Engineer Anything (REA) agent skill
- [nutlope/hallmark](https://github.com/nutlope/hallmark) — Hallmark anti-AI-slop design skill
- [oso95/scroll-world](https://github.com/oso95/scroll-world) — Scroll World cinematic scroll-scrubbed landing pages
- [@google/stitch (npm)](https://www.npmjs.com/package/@google/stitch) — the official Stitch CLI skill (`skills/design/stitch`), Apache-2.0
- [doodledood/claude-code-plugins](https://github.com/doodledood/claude-code-plugins) — scrollytelling skill (no licence file in the repo)
- Custom skills authored for this library — all `engineering/`, `utils/`, and others without a Source comment

Skills installed from plugins or upstream instead of copied here: see [INSTALL-EXTERNAL.md](INSTALL-EXTERNAL.md).
