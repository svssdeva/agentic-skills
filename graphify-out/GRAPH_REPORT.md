# Graph Report - .  (2026-04-28)

## Corpus Check
- 77 files · ~89,025 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 90 nodes · 153 edges · 9 communities detected
- Extraction: 18% EXTRACTED · 82% INFERRED · 0% AMBIGUOUS · INFERRED: 126 edges (avg confidence: 0.84)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Go & Design Patterns|Go & Design Patterns]]
- [[_COMMUNITY_Code Quality & Testing|Code Quality & Testing]]
- [[_COMMUNITY_Astro & Performance|Astro & Performance]]
- [[_COMMUNITY_Engineering Methodology|Engineering Methodology]]
- [[_COMMUNITY_DevOps & Tooling|DevOps & Tooling]]
- [[_COMMUNITY_Angular & TypeScript|Angular & TypeScript]]
- [[_COMMUNITY_Mobile & CSS Frameworks|Mobile & CSS Frameworks]]
- [[_COMMUNITY_SEO & Content Strategy|SEO & Content Strategy]]
- [[_COMMUNITY_Context Compression|Context Compression]]

## God Nodes (most connected - your core abstractions)
1. `Angular Developer` - 9 edges
2. `Go Development Patterns` - 9 edges
3. `README.md — Skill Library Index` - 8 edges
4. `Golang Pro` - 8 edges
5. `Test-Driven Development` - 7 edges
6. `SEO Audit` - 7 edges
7. `Spec-Driven Development` - 7 edges
8. `CI/CD and Automation` - 6 edges
9. `Performance Optimization` - 6 edges
10. `Go Testing Patterns` - 6 edges

## Surprising Connections (you probably didn't know these)
- `Remotion Video Engineering` --conceptually_related_to--> `Web Design Guidelines`  [INFERRED]
  remotion-best-practices/SKILL.md → web-design-guidelines/SKILL.md
- `AWS Architecture Diagrams` --conceptually_related_to--> `Documentation and ADRs`  [INFERRED]
  aws-diagrams/SKILL.md → documentation-and-adrs/SKILL.md
- `Angular Tooling` --conceptually_related_to--> `Angular Developer`  [INFERRED]
  angular-tooling/SKILL.md → angular-developer/SKILL.md
- `Extract Design System` --semantically_similar_to--> `System Design`  [INFERRED] [semantically similar]
  extract-design-system/SKILL.md → system-design/SKILL.md
- `Root Cause Investigation Methodology` --semantically_similar_to--> `Trade-off Analysis`  [INFERRED] [semantically similar]
  systematic-debugging/SKILL.md → system-design/SKILL.md

## Hyperedges (group relationships)
- **Go Language Skill Cluster** — skill_golang_patterns, skill_golang_pro, skill_golang_testing [EXTRACTED 1.00]
- **Systematic Analysis Methodologies** — skill_systematic_debugging, skill_system_design, concept_tradeoff_analysis, concept_root_cause_analysis [INFERRED 0.75]
- **Testing and Quality Assurance Practices** — skill_golang_testing, skill_systematic_debugging, concept_tdd_workflow, concept_table_driven_tests [INFERRED 0.75]

## Communities

### Community 0 - "Go & Design Patterns"
Cohesion: 0.17
Nodes (21): CLAUDE.md — Repo Conventions, Concurrency Patterns (goroutines, channels, context), Context Propagation and Cancellation, Design Tokens Extraction, Error Handling Patterns, Functional Options Pattern, Graphify Knowledge Graph, Interface Design (small, focused, consumer-side) (+13 more)

### Community 1 - "Code Quality & Testing"
Cohesion: 0.25
Nodes (11): Angular Testing, Code Review and Quality, Code Simplification, Debugging and Error Recovery, M15 Anti-Pattern Detection, Playwright E2E Testing, Rust Async Patterns, Rust Best Practices (+3 more)

### Community 2 - "Astro & Performance"
Cohesion: 0.27
Nodes (11): Astro Framework, Astro Architecture, Astro Expert, Astro SEO, Website Audit, Browser Testing with DevTools, Astro Performance, Performance Optimization (+3 more)

### Community 3 - "Engineering Methodology"
Cohesion: 0.38
Nodes (10): API and Interface Design, Context Engineering, Deprecation and Migration, Documentation and ADRs, Idea Refinement, Incremental Implementation, Planning and Task Breakdown, Source-Driven Development (+2 more)

### Community 4 - "DevOps & Tooling"
Cohesion: 0.27
Nodes (10): Angular Tooling, AWS Architecture Diagrams, AWS Solution Architecture, Bun Fundamentals, Bun Development Workflows, Bun Runtime Internals, CI/CD and Automation, Git Workflow and Versioning (+2 more)

### Community 5 - "Angular & TypeScript"
Cohesion: 0.39
Nodes (9): Angular Components, Angular Developer, Angular Dependency Injection, Angular Directives, Angular Forms, Angular HTTP Client, Angular Signals, TypeScript Advanced Types (+1 more)

### Community 6 - "Mobile & CSS Frameworks"
Cohesion: 0.42
Nodes (9): Capacitor Native Bridge, Expo with Tailwind (NativeWind), Frontend UI Engineering, Ionic Framework, Ionic Design System, Tailwind CSS Patterns, Tailwind Design System, Tailwind Advanced Layouts (+1 more)

### Community 7 - "SEO & Content Strategy"
Cohesion: 0.57
Nodes (7): AI-First SEO, Content Strategy, Product Marketing Context, Programmatic SEO, SEO Audit, Geo-Targeted SEO, Social Content Strategy

### Community 8 - "Context Compression"
Cohesion: 1.0
Nodes (2): Aggressive Context Compression, Context Compression

## Knowledge Gaps
- **5 isolated node(s):** `Context Compression`, `Aggressive Context Compression`, `TypeScript Advanced Types`, `Design Tokens Extraction`, `Functional Options Pattern`
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Context Compression`** (2 nodes): `Aggressive Context Compression`, `Context Compression`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Performance Optimization` connect `Astro & Performance` to `Mobile & CSS Frameworks`?**
  _High betweenness centrality (0.188) - this node is a cross-community bridge._
- **Why does `Test-Driven Development` connect `Code Quality & Testing` to `Engineering Methodology`, `Angular & TypeScript`?**
  _High betweenness centrality (0.173) - this node is a cross-community bridge._
- **Why does `Angular Testing` connect `Code Quality & Testing` to `Angular & TypeScript`?**
  _High betweenness centrality (0.163) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `Angular Developer` (e.g. with `Angular Testing` and `TypeScript Expert`) actually correct?**
  _`Angular Developer` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `Go Development Patterns` (e.g. with `Golang Pro` and `Go Testing Patterns`) actually correct?**
  _`Go Development Patterns` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `Golang Pro` (e.g. with `Go Development Patterns` and `Go Testing Patterns`) actually correct?**
  _`Golang Pro` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `Test-Driven Development` (e.g. with `Debugging and Error Recovery` and `Spec-Driven Development`) actually correct?**
  _`Test-Driven Development` has 7 INFERRED edges - model-reasoned connections that need verification._