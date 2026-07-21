# agentic-skills

A curated library of 160 drop-in skills for Claude Code. Each skill is a `SKILL.md` file that encodes expert knowledge, workflows, and guardrails for a specific domain.

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
| `database/` | Postgres, Neon, query optimization |
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
| `video/` | HTML video composition (HyperFrames) |

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

## Updating Skills from Upstream

Each headered `SKILL.md` tracks its origin via the `<!-- Source: -->` / `<!-- Install: -->` comments. To resync against upstream, folder by folder:

1. Parse `<owner>/<repo>` and the `--skill <name>` from each Install line; `git clone --depth 1` each unique repo (use `GIT_TERMINAL_PROMPT=0` + `--no-checkout` then a tolerant checkout — large repos have Windows-invalid filenames; set `core.longpaths=true`).
2. Match the upstream `SKILL.md` by parent folder == `<name>`, excluding hidden mirror dirs (`.claude/`, `.gemini/`, `.cursor/`, `.kiro/`, `.agents/`) and `docs/`/locale translation copies; pick the largest candidate. Many skills were renamed on import — fall back to matching by frontmatter `name:` or topic.
3. Normalize before diffing (strip CRLF, drop the 2 header comment lines, drop leading blanks) to avoid false diffs.
4. To update: replace the body with upstream content but KEEP the local 2 header comment lines, and copy sibling files/dirs the SKILL.md references (`references/`, `scripts/`, `rules/`, `schemas/`, `AGENTS.md`). Skip cruft (LICENSE/README/metadata.json/eval*).
5. Leave HEADERLESS custom composites (no Source/Install) untouched. If an upstream skill is gone or replaced by a "has moved"/signpost stub, keep the local content — never overwrite a real skill with a redirect.
