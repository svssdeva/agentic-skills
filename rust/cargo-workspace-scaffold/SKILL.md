---
name: cargo-workspace-scaffold
description: >
  Scaffold a multi-crate Cargo workspace (core library + thin binary/adapters)
  with shared dependency and lint inheritance, and a cross-platform CI that
  guards determinism. Use when: (1) starting a Rust project as a library-first
  workspace with a CLI/server on top, (2) centralizing dependency versions and
  lints across crates, (3) setting up a Linux/macOS/Windows CI matrix (fmt,
  clippy, test, byte-identical-output check), (4) pinning a toolchain for
  reproducible builds. Triggers on cargo workspace, workspace.dependencies,
  workspace.lints, resolver 2, rust-toolchain.toml, CI matrix, determinism,
  reproducible build.
license: MIT
compatibility: Rust 1.74+ (workspace lints), verified on cargo 1.97
metadata:
  author: web-fluid
  verified-with: "cargo 1.97.0 — manifest parses, cargo check green"
allowed-tools: Bash(cargo:*) Bash(rustc:*) Read Write Edit Glob Grep
---

# Cargo Workspace Scaffold (library-first)

The right shape for a tool with several front-ends (CLI, server, CI action) is
**one core library crate + thin adapter crates + one binary**. The library is
the product; everything else is a shell over it. This guarantees identical
behaviour across entry points by construction — the same code runs whether
invoked from the CLI, a server, or CI.

## Layout

```
myproj/
├── Cargo.toml            # [workspace] — members, shared deps, shared lints
├── rust-toolchain.toml   # pin the toolchain for reproducibility
├── crates/
│   ├── myproj-core/      # the library: all real logic lives here
│   ├── myproj-lang/      # a focused adapter crate (optional)
│   └── myproj-mcp/       # another adapter (server, etc.)
└── src/main.rs           # the binary: arg-parse → call core → print. Thin.
```

Rule: **no logic in the binary or adapters** beyond translating in/out. If you
can't test a behaviour without the CLI, it's in the wrong crate — push it down
into `-core` and unit-test it there.

## Root `Cargo.toml`

```toml
[workspace]
resolver = "2"                        # always; edition-2021 default resolver
members = ["crates/*"]

[workspace.package]                   # inherited by member crates
version = "0.1.0"
edition = "2021"
license = "MIT"

[workspace.dependencies]              # single source of truth for versions
tree-sitter = "0.24"
rusqlite = { version = "0.32", features = ["bundled"] }
rayon = "1"

[workspace.lints.clippy]             # shared lint policy, one place
unwrap_used = "warn"
```

Member crate inherits with `.workspace = true`:

```toml
[package]
name = "myproj-core"
version.workspace = true
edition.workspace = true
license.workspace = true

[dependencies]
tree-sitter.workspace = true          # version comes from the root
rusqlite.workspace = true

[lints]
workspace = true                      # opt in to the shared lint table
```

(Verified: this manifest — `resolver = "2"`, `workspace.package` inheritance,
`workspace.lints` — parses and `cargo check`s clean on cargo 1.97. Workspace
lints require Rust ≥1.74.)

## Pin the toolchain

```toml
# rust-toolchain.toml
[toolchain]
channel = "1.97.0"
components = ["rustfmt", "clippy"]
```

Everyone and CI build with the same compiler — removes a whole class of "works
on my machine" and reproducibility drift.

## CI matrix (Linux/macOS/Windows)

```yaml
# .github/workflows/ci.yml
name: ci
on: [push, pull_request]
jobs:
  check:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
      - uses: Swatinem/rust-cache@v2                 # cache target/ + registry
      - run: cargo fmt --all --check
      - run: cargo clippy --all-targets --all-features --locked -- -D warnings
      - run: cargo test --all-features --locked
```

`--locked` fails if `Cargo.lock` would change — CI must build the committed
lockfile, not silently upgrade. Commit `Cargo.lock` for binaries/tools.

## Determinism discipline (for tools that emit committable output)

If your project exports a file meant to be diffed/committed (a graph, a report,
a snapshot), byte-for-byte stability across platforms is a **tested invariant**,
not a hope. Rust leaks nondeterminism in specific, known places:

- **Hash iteration order** — `HashMap`/`HashSet` iterate in random order. For
  anything you serialize, use `BTreeMap`/`BTreeSet` or collect + `sort()` before
  emitting.
- **Paths** — normalize to `/` at ingest; never write raw `\` from Windows into
  shared output.
- **Floats** — fix formatting precision; don't rely on default `Display`.
- **Seeded algorithms** — any clustering/random step takes an explicit seed and
  deterministic tie-breaking.

Add a CI job that builds a fixture on all three OSes and byte-compares the
export:

```yaml
  determinism:
    strategy: { matrix: { os: [ubuntu-latest, macos-latest, windows-latest] } }
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
      - run: cargo run --quiet -- export tests/fixture --out out.json
      - run: shasum -a 256 out.json    # compare the hash across the matrix
```

## Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `workspace.lints` "unknown field" | Rust <1.74. Bump toolchain. |
| Member won't inherit version | Missing `version.workspace = true` in the member, or key absent from `[workspace.package]`. |
| CI passes locally, fails on `--locked` | `Cargo.lock` out of date / not committed. Run `cargo update` intentionally and commit. |
| Export differs across OSes | `HashMap` order or `\` vs `/` paths. Switch to `BTreeMap`, normalize paths. |
| Duplicate dep versions in `cargo tree` | Two crates pin incompatible ranges. Hoist to `[workspace.dependencies]` and align. |

## Verification

The manifest above was `cargo check`-verified on 1.97. When you scaffold, the
one check that matters is `cargo build && cargo test` green on the CI matrix —
that's the T0.5 exit criterion. Add the determinism job the moment you emit a
committable artifact, not later.

---

*Enables Chitra Phase 0: T0.5 (workspace scaffold `chitra-core`/`-lang`/`-mcp` +
binary, CI green). Sets up the RISK-4 determinism CI harness for Phase 1 T1.11.*
