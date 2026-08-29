---
name: tree-sitter-parsing
description: >
  Parse source code into ASTs with tree-sitter in Rust and extract structural
  facts (functions, classes, calls, imports). Use when: (1) building a code
  parser, linter, or knowledge-graph over source, (2) choosing between grammar
  crates and managing tree-sitter ABI versions, (3) writing tree-sitter queries
  (.scm) or walking the tree with a cursor, (4) supporting many languages behind
  one generic, config-driven walker. Triggers on tree-sitter, tree_sitter,
  grammar, AST, parser, query, S-expression, LanguageFn, incremental parsing.
license: MIT
compatibility: Rust 1.75+, tree-sitter 0.24.x
metadata:
  author: web-fluid
  verified-with: "tree-sitter 0.24.7, tree-sitter-rust 0.23.3 (cargo test, green)"
allowed-tools: Bash(cargo:*) Bash(rustc:*) Read Write Edit Glob Grep
---

# Tree-sitter Parsing in Rust

Tree-sitter turns source text into a concrete syntax tree, incrementally and
error-tolerantly. In Rust you get first-class bindings (no FFI boilerplate) and
per-file parallelism (no GIL). This skill covers the API as of the **0.24 line**
— the API moved recently, so the version matters.

## The ABI-version trap (read this first)

Each language is a separate crate (`tree-sitter-rust`, `tree-sitter-python`, …).
Every one is compiled against a tree-sitter **ABI version**, and a grammar crate
built for a newer/older core than your `tree-sitter` dependency **fails to load
at runtime or won't link**. This is the single biggest source of pain when
supporting many languages.

Discipline:

- Pin `tree-sitter` once in `[workspace.dependencies]` and let every grammar
  crate resolve against it. Never let two grammar crates pull incompatible cores.
- Before adding a grammar, check its `Cargo.toml` for the `tree-sitter` version
  range it targets. `cargo tree -i tree-sitter` shows who pulls what.
- API shape changed at 0.20→0.22→0.24: old grammars expose `fn language() ->
  Language`; current ones expose a `LANGUAGE: LanguageFn` constant. Convert with
  `.into()`. If a crate only has `language()`, it's older — verify ABI match.
- For breadth beyond a curated set, prefer **runtime grammar loading** (load a
  compiled `.so`/`.dylib`/`.wasm` grammar via `Language::from_raw`/`wasm`) over
  compiling in dozens of crates. Compile-time crates for the few you support
  deeply; runtime loading for the long tail.

## Setup

```toml
[dependencies]
tree-sitter = "0.24"
tree-sitter-rust = "0.23"       # grammar crate; version tracks the grammar, not the core
streaming-iterator = "0.1"      # QueryCursor::matches() is a StreamingIterator in 0.24
```

## Parse and extract with a query (preferred)

Queries (S-expression `.scm` patterns) are the idiomatic, config-friendly way to
pull facts out — you declare *what* to match, not *how* to walk. This is the
foundation of a generic multi-language walker: one query set per language, one
extraction loop.

```rust
use streaming_iterator::StreamingIterator; // 0.24: matches() streams, not Iterator
use tree_sitter::{Parser, Query, QueryCursor};

/// Return (function name, 1-based line) for every top-level fn.
fn parse_fns(source: &str) -> Vec<(String, usize)> {
    let mut parser = Parser::new();
    let language = tree_sitter_rust::LANGUAGE.into(); // LanguageFn -> Language
    parser.set_language(&language).expect("load grammar");
    let tree = parser.parse(source, None).expect("parse");

    let query = Query::new(&language, "(function_item name: (identifier) @name)").unwrap();
    let name_idx = query.capture_index_for_name("name").unwrap();

    let mut cursor = QueryCursor::new();
    let mut out = Vec::new();
    let mut it = cursor.matches(&query, tree.root_node(), source.as_bytes());
    while let Some(m) = it.next() {
        for cap in m.captures.iter().filter(|c| c.index == name_idx) {
            let text = cap.node.utf8_text(source.as_bytes()).unwrap();
            out.push((text.to_string(), cap.node.start_position().row + 1));
        }
    }
    out
}
```

Key API facts (0.24, verified): `set_language` takes `&Language`; `parse`
returns `Option<Tree>`; `Query::new` takes `&Language`; `QueryCursor::matches`
yields a **`StreamingIterator`** — you must `use streaming_iterator::Streaming
Iterator` and drive it with `while let Some(m) = it.next()`, *not* a `for` loop.
`node.utf8_text(src_bytes)` slices the original source; positions are 0-based
rows/cols (`start_position().row`).

## Manual cursor walk (when a query won't express it)

For whole-tree traversal (counting, generic node-kind dispatch), a `TreeCursor`
pre-order walk is allocation-free and fast:

```rust
let mut cursor = tree.walk();
loop {
    // ... visit cursor.node(): cursor.node().kind() is the grammar node type ...
    if cursor.goto_first_child() { continue; }
    loop {
        if cursor.goto_next_sibling() { break; }
        if !cursor.goto_parent() { /* back at root, done */ return; }
    }
}
```

## Generic config-driven walker

To support N languages without N hand-written parsers: hold a per-language config
of node-kind sets — which `kind()`s are definitions, which are call sites, which
name field to read — and one extraction pass keyed off `node.kind()`. Grammars
differ (`function_item` in Rust, `function_definition` in Python), so the config
is a table, not code. Grammar-specific field names come from each grammar's
`node-types.json` / `grammar.js`; the [tree-sitter playground](https://tree-sitter.github.io/tree-sitter/playground)
shows the tree for a snippet.

## Parallelism

`Parser` is **not** `Sync` and holds internal state — do not share one across
threads. Create one `Parser` per rayon worker (or `thread_local!`), parse files
independently, merge results after. Parsing is embarrassingly parallel; this is
where Rust beats a GIL-bound runtime.

## Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `set_language` type error on `language()` | Old-API grammar. Use `LANGUAGE.into()`; if only `language()` exists, the crate targets an older core — check ABI match. |
| `matches()` "is not an iterator" | 0.24 returns a `StreamingIterator`. Add `streaming-iterator` and `while let Some(m) = it.next()`. |
| Runtime "incompatible language version" | Grammar built against a different tree-sitter ABI. Align versions; `cargo tree -i tree-sitter`. |
| Empty captures | Capture name mismatch. `capture_index_for_name` returns `None` if the `@name` isn't in the query string. |
| Garbled `utf8_text` | Passed the wrong byte slice. Always pass the *same* bytes you parsed. |

## Verification

The snippets above are lifted from a probe compiled and tested green against the
pinned versions. Any non-trivial parser you build should keep at least one test
that asserts extracted names/lines on a small fixture — grammar upgrades silently
change node kinds, and a fixture test is what catches it.

---

*Enables Chitra Phase 0: T0.1 (grammar-crate survey + ABI), T0.2 (compile-time vs
runtime loading ADR), T0.4 (`LanguageConfig` generic walker).*
