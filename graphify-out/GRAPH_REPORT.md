# Graph Report - .  (2026-04-25)

## Corpus Check
- 69 files · ~82,975 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 69 nodes · 118 edges · 9 communities detected
- Extraction: 0% EXTRACTED · 100% INFERRED · 0% AMBIGUOUS · INFERRED: 118 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Astro, Vercel & Performance|Astro, Vercel & Performance]]
- [[_COMMUNITY_Cloud, DevOps & Tooling|Cloud, DevOps & Tooling]]
- [[_COMMUNITY_Development Methodology|Development Methodology]]
- [[_COMMUNITY_Mobile & UI Design|Mobile & UI Design]]
- [[_COMMUNITY_Angular & TypeScript|Angular & TypeScript]]
- [[_COMMUNITY_Testing & Code Quality|Testing & Code Quality]]
- [[_COMMUNITY_SEO & Content|SEO & Content]]
- [[_COMMUNITY_Rust|Rust]]
- [[_COMMUNITY_Context Compression|Context Compression]]

## God Nodes (most connected - your core abstractions)
1. `Angular Developer` - 9 edges
2. `Test-Driven Development` - 7 edges
3. `SEO Audit` - 7 edges
4. `Spec-Driven Development` - 7 edges
5. `CI/CD and Automation` - 6 edges
6. `Performance Optimization` - 6 edges
7. `Web Design Guidelines` - 5 edges
8. `Code Review and Quality` - 5 edges
9. `Security and Hardening` - 5 edges
10. `AI-First SEO` - 5 edges

## Surprising Connections (you probably didn't know these)
- `Remotion Video Engineering` --conceptually_related_to--> `Web Design Guidelines`  [INFERRED]
  remotion-best-practices/SKILL.md → web-design-guidelines/SKILL.md
- `AWS Architecture Diagrams` --conceptually_related_to--> `Documentation and ADRs`  [INFERRED]
  aws-diagrams/SKILL.md → documentation-and-adrs/SKILL.md
- `Angular Tooling` --conceptually_related_to--> `Angular Developer`  [INFERRED]
  angular-tooling/SKILL.md → angular-developer/SKILL.md
- `Programmatic SEO` --conceptually_related_to--> `Source-Driven Development`  [INFERRED]
  programmatic-seo/SKILL.md → source-driven-development/SKILL.md
- `M15 Anti-Pattern Detection` --conceptually_related_to--> `Code Review and Quality`  [INFERRED]
  m15-anti-pattern/SKILL.md → code-review-and-quality/SKILL.md

## Communities

### Community 0 - "Astro, Vercel & Performance"
Cohesion: 0.27
Nodes (11): Astro Framework, Astro Architecture, Astro Expert, Astro SEO, Website Audit, Browser Testing with DevTools, Astro Performance, Performance Optimization (+3 more)

### Community 1 - "Cloud, DevOps & Tooling"
Cohesion: 0.27
Nodes (10): Angular Tooling, AWS Architecture Diagrams, AWS Solution Architecture, Bun Fundamentals, Bun Development Workflows, Bun Runtime Internals, CI/CD and Automation, Git Workflow and Versioning (+2 more)

### Community 2 - "Development Methodology"
Cohesion: 0.38
Nodes (10): API and Interface Design, Context Engineering, Deprecation and Migration, Documentation and ADRs, Idea Refinement, Incremental Implementation, Planning and Task Breakdown, Source-Driven Development (+2 more)

### Community 3 - "Mobile & UI Design"
Cohesion: 0.42
Nodes (9): Capacitor Native Bridge, Expo with Tailwind (NativeWind), Frontend UI Engineering, Ionic Framework, Ionic Design System, Tailwind CSS Patterns, Tailwind Design System, Tailwind Advanced Layouts (+1 more)

### Community 4 - "Angular & TypeScript"
Cohesion: 0.39
Nodes (9): Angular Components, Angular Developer, Angular Dependency Injection, Angular Directives, Angular Forms, Angular HTTP Client, Angular Signals, TypeScript Advanced Types (+1 more)

### Community 5 - "Testing & Code Quality"
Cohesion: 0.38
Nodes (7): Angular Testing, Code Review and Quality, Code Simplification, Debugging and Error Recovery, M15 Anti-Pattern Detection, Playwright E2E Testing, Test-Driven Development

### Community 6 - "SEO & Content"
Cohesion: 0.57
Nodes (7): AI-First SEO, Content Strategy, Product Marketing Context, Programmatic SEO, SEO Audit, Geo-Targeted SEO, Social Content Strategy

### Community 7 - "Rust"
Cohesion: 0.83
Nodes (4): Rust Async Patterns, Rust Best Practices, Rust Engineer, Rust Testing

### Community 8 - "Context Compression"
Cohesion: 1.0
Nodes (2): Aggressive Context Compression, Context Compression

## Knowledge Gaps
- **3 isolated node(s):** `Context Compression`, `Aggressive Context Compression`, `TypeScript Advanced Types`
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Context Compression`** (2 nodes): `Aggressive Context Compression`, `Context Compression`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Performance Optimization` connect `Astro, Vercel & Performance` to `Mobile & UI Design`?**
  _High betweenness centrality (0.322) - this node is a cross-community bridge._
- **Why does `Test-Driven Development` connect `Testing & Code Quality` to `Development Methodology`, `Angular & TypeScript`, `Rust`?**
  _High betweenness centrality (0.297) - this node is a cross-community bridge._
- **Why does `Angular Testing` connect `Testing & Code Quality` to `Angular & TypeScript`?**
  _High betweenness centrality (0.281) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `Angular Developer` (e.g. with `TypeScript Expert` and `Angular Dependency Injection`) actually correct?**
  _`Angular Developer` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `Test-Driven Development` (e.g. with `Debugging and Error Recovery` and `Spec-Driven Development`) actually correct?**
  _`Test-Driven Development` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `SEO Audit` (e.g. with `Programmatic SEO` and `AI-First SEO`) actually correct?**
  _`SEO Audit` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `Spec-Driven Development` (e.g. with `Idea Refinement` and `Test-Driven Development`) actually correct?**
  _`Spec-Driven Development` has 7 INFERRED edges - model-reasoned connections that need verification._