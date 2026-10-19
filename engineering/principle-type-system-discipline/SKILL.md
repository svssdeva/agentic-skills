<!-- Source: https://github.com/michael-denyer/pstack-claude/tree/main/plugins/pstack/skills/principle-type-system-discipline -->
<!-- Install: /plugin marketplace add michael-denyer/pstack-claude && /plugin install pstack@pstack-claude (full pstack plugin) -->
<!-- License: MIT (c) 2026 Lauren Tan; port (c) 2026 Michael Denyer -->
---
name: principle-type-system-discipline
description: "Apply when designing types, reviewing a function signature, or writing code in any statically-typed language. Make illegal states unrepresentable, brand semantic primitives, parse external data at boundaries, exhaust variants, derive from authoritative schemas."
user-invocable: false
---

# Type System Discipline

Make the compiler reject impossible states, mismatched primitives, and unhandled variants. Prefer defining errors and special cases out of existence over proliferating handlers. For TypeScript syntax, see the [typescript-best-practices](https://github.com/michael-denyer/pstack-claude/blob/main/plugins/pstack/skills/typescript-best-practices/SKILL.md) skill.

- **Brand semantic primitives.** `UserId` and `OrderId` are strings underneath but should not be interchangeable. Give each its own type, such as a branded intersection in TypeScript or a newtype elsewhere. Validate once at creation, trust the type downstream. If two arguments share a primitive type but mean different things, brand them.
- **External data is untyped until parsed.** RPC payloads, JSON, IPC messages, CLI args, config files, environment variables, database rows. Have a parse function at every boundary that turns unstructured input into the typed model. The [boundary-discipline](https://github.com/michael-denyer/pstack-claude/blob/main/plugins/pstack/skills/principle-boundary-discipline/SKILL.md) principle skill says where to put validation.
- **Derive types from authoritative schemas.** When a protocol buffer, OpenAPI spec, GraphQL schema, database migration, design-token file, or another file owns a shape, derive from it instead of hand-rolling a parallel type. See the [encode-lessons-in-structure](https://github.com/michael-denyer/pstack-claude/blob/main/plugins/pstack/skills/principle-encode-lessons-in-structure/SKILL.md) principle skill.
