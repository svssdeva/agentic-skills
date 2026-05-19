# agentic-skills

A curated library of 116 drop-in skills for Claude Code. Each skill is a `SKILL.md` file that encodes expert knowledge, workflows, and guardrails for a specific domain.

## Structure

```
<category>/
└── <skill-name>/
    └── SKILL.md
```

Skills live inside category folders at the repo root. Each category is a lowercase kebab-case folder; each skill inside it is also a lowercase kebab-case folder containing exactly one `SKILL.md`.

## Categories

| Folder | Domain |
|---|---|
| `ai/` | RAG, LLM applications, vector search and indexing |
| `angular/` | Angular framework skills |
| `astro/` | Astro framework skills |
| `bun/` | Bun runtime and tooling |
| `cloud/` | AWS, Vercel, CI/CD, Linux hosting |
| `docker/` | Docker, containerization, Compose, multi-stage builds |
| `engineering/` | Development methodology and practices |
| `frontend/` | UI engineering, design systems, performance |
| `golang/` | Go language skills |
| `nestjs/` | NestJS framework skills |
| `python/` | Python language skills |
| `react/` | React and Next.js skills |
| `mobile/` | Ionic, Capacitor, Expo |
| `rust/` | Rust language skills |
| `seo/` | SEO, content strategy, marketing |
| `tailwind/` | Tailwind CSS skills |
| `testing/` | Testing tools and practices |
| `typescript/` | TypeScript skills |
| `utils/` | Utilities and meta-skills (compression, skill discovery, site audit) |

## Conventions

- Category folder names: lowercase kebab-case (`golang`, `engineering`, `mobile`)
- Skill folder names: lowercase kebab-case (`golang-pro`, `extract-design-system`)
- Each `SKILL.md` starts with an HTML source comment (`<!-- Source: ... -->`) and optionally YAML frontmatter
- Source/Install comments track upstream provenance — do not modify them
- Skill count in README headline must stay accurate when adding/removing skills

## Knowledge Graph

This repo has a graphify knowledge graph at `graphify-out/` that maps relationships between all skills.

- `graphify-out/graph.json` — structured graph data
- `graphify-out/graph.html` — interactive visualization (open in browser)
- `graphify-out/GRAPH_REPORT.md` — audit report with god nodes, surprising connections, suggested questions

**Before answering questions about skill relationships, clusters, or cross-cutting concerns, consult the graph first** — it's faster and more accurate than re-reading individual files.

Rebuild after adding skills:

```
/graphify . --update
```

## Adding a Skill

1. Place the skill in the appropriate category: `<category>/my-skill/SKILL.md`
2. Add `<!-- Source: ... -->` and `<!-- Install: ... -->` header comments
3. Add the skill to the appropriate category table in `README.md` with the nested path link
4. Bump the skill count in the README headline
5. Run `/graphify . --update` to refresh the knowledge graph
