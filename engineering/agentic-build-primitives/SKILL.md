---
name: agentic-build-primitives
description: Primitives-first workflow for building a real product with a coding agent (Claude Code, Codex, Cursor) without AI slop. Use when scaffolding a project for agentic coding, writing AGENTS.md / CLAUDE.md rules, installing per-dependency skills, wiring deploys and env vars through the agent, when the agent needs to verify its own work against third-party APIs (local emulators, screenshot evidence), or when agent output drifts into unrequested migrations, backwards-compat code or over-engineering.
---

# Agentic Build Primitives

Give the agent reliable primitives (components, skills, schemas, rules), teach it how to use them,
then ask for the feature. Prompts get shorter as the codebase accumulates examples. Start strict,
loosen later.

## 1. Rules that go in AGENTS.md on day one

```markdown
## Git
Never create branches, worktrees or commits automatically. Only do so when the user explicitly
asks for that specific action in the current request. Leave changes uncommitted on the current
branch and let the user decide when and how to commit.

## Database (development phase)
Only `db push`. Never generate or run migrations; the migration script has been removed.
This is a development project: there is no backwards compatibility and the data is worthless.
Prefer data loss. Never backfill, migrate or preserve existing rows. Every schema change is a
clean slate. (Remove this section before production.)

## Deployment
The production worker/queue uses a different secret key than development. After adding any
environment variable, sync it to the deployment and to the worker's production environment.
```

Agents are notorious for unrequested backwards compatibility: they treat every project as
production and write backfills and shims. That is a large share of what reads as AI slop.

**CLAUDE.md must reference AGENTS.md.** If both files exist, Claude Code reads only CLAUDE.md;
tool installers often create a CLAUDE.md with a single "use X skills" line and your AGENTS.md
rules silently stop applying.

## 2. One skill per dependency, installed into the project

For every major dependency (component library, auth, database/ORM, AI SDK, job runner, sandbox,
deploy platform, error tracking) install its official skill before asking the agent to use it.

- Scope: **project** (so the skills are committed and every collaborator gets identical ones).
- Method: symbolic link if offered.
- Verify the same skill appears under both `.agents/` and `.claude/` (or your agent's folder).
  A missing folder means the agent will not load it.
- After installing: `/reload-skills` (or a new session), then open the skills dialogue and search
  for it. Commit the untracked skill files immediately so later diffs stay readable.
- Add `.claude` and `.agents` to `.dockerignore`. Skills ship template apps with their own
  `package.json`; Railpack/Nixpacks-style builders (Railway, Netlify, Vercel) will try to build them.

Prefer a dependency's CLI + skill over its dashboard: deploys, env-var sync, log fetching and
debugging then all happen from the agent.

## 3. Primitives-first prompt order for a feature

Ask for the layers in dependency order, naming the primitives to use, in one prompt:

1. Validation schema derived from the DB schema (e.g. drizzle-zod insert schema). This is the
   single source of truth for every form.
2. Server action / mutation using that schema and the auth helper for the user ID.
3. UI component built from the component-library primitive, wired to the action.
4. Close with: `use <component> skill, <db> skill, <auth> skill`.

Then: "Update AGENTS.md with rules on how to develop forms based on this conversation." Next time
the prompt is "implement a form for this entity".

Once the codebase has examples (queries folder, form pattern, dialogue pattern), the agent will
follow them even when your prompt is sloppy. Early strictness buys later leniency.

## 4. Prompt hygiene

- Crop screenshots to exactly the component you want; extra UI in the image becomes extra scope.
  Note when a reference shows a hover/focused state, or the agent will build that as the default.
- Say what NOT to build: "ignore group chats for now", "do not add any new features, tools or
  metadata except those needed for the migration", "this route doesn't exist yet, leave it".
- In a brand-new session, restate the primitives and skills; it has no memory of the last one.
- Mark third-party IDs as such ("`sandboxId` is a third-party ID") so the agent does not invent
  tables for them. Index foreign keys you will query by.
- Mention which tables share a transaction/batch so no orphan rows can exist.

## 5. Durability and memory

- Anything long-running (an agent loop, tool use, computer use) runs in a durable stateless
  worker (e.g. a job runner with its own persistence), never in a web route handler. A refresh or
  redeploy must not kill the run. The route handler only enqueues.
- Agent memory is a **tool** (`remember` / `recall` backed by a file or store), not a line in the
  system prompt telling it to "write to memory.md when appropriate". Instructions are flaky; tool
  calls are deterministic.
- Start every capability at its primitive level (one bot per turn, no handoff; a paid plan that
  gates everything, no ledger) and build the next level on top in a later prompt.

## 6. Verification the agent can run on its own

The agent finishes reliably only when it can prove its own work.

- **Emulate every third-party API the agent can't run itself.** Postgres and Redis run locally;
  real Gmail or Slack accounts block bots and rate-limit, and no live account resets to a known
  state. Point the integration at a stateful local clone: `emulate` as a pinned devDependency
  ([vercel-labs/emulate](https://github.com/vercel-labs/emulate): GitHub, Google, Slack, Stripe,
  Resend, Clerk, Twilio, AWS S3/SQS/IAM and more), LocalStack for fuller AWS. When no emulator
  exists, have the agent build one from the vendor's API docs: same routes and responses, an
  in-memory store, on localhost. Put each integration behind an interface so the emulator and the
  real service are interchangeable, and say so in AGENTS.md. A pass proves the code against the
  clone, not the real service.
- **Screenshots are the definition of done.** "Done" means a screenshot of every page and state
  the change touches (web, desktop, mobile), not the agent's report. Put it in the long-run goal
  ("not finished until every page has a screenshot") and later in CI, with screenshots attached to
  each PR, so a reviewer checks only what changed.
- **Never let an agent auto-merge outside contributions beyond trivial fixes.** PR text and diffs
  are a prompt-injection channel; a human approves the rest from the screenshots.

## 7. Checkpoints

Stage and commit after every working slice, and before installing a skill or running a large
generation, so the real diff stays visible. When the agent breaks its own rule (e.g. switches
branches), restate the rule in AGENTS.md more forcefully rather than arguing in chat.
