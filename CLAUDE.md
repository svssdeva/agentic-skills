# agentic-skills

A curated library of 75+ drop-in skills for Claude Code. Each skill is a `SKILL.md` file that encodes expert knowledge, workflows, and guardrails for a specific domain.

## Structure

```
<skill-name>/
└── SKILL.md
```

Skills are flat at the repo root — one kebab-case folder per skill, each containing exactly one `SKILL.md`. No nesting.

## Conventions

- Folder names: lowercase kebab-case (`golang-pro`, `extract-design-system`)
- Each `SKILL.md` starts with an HTML source comment (`<!-- Source: ... -->`) and optionally YAML frontmatter
- README.md groups skills by category (Angular, Go, Rust, etc.) — grouping is documentation-only, not reflected in directory structure
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

1. Create `my-skill/SKILL.md` with source comment header
2. Add the skill to the appropriate category table in `README.md`
3. Bump the skill count in the README headline
4. Run `/graphify . --update` to refresh the knowledge graph
