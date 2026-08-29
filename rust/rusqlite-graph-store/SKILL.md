---
name: rusqlite-graph-store
description: >
  Use SQLite (via rusqlite, bundled) as an embedded, queryable store — including
  graph data with bounded traversal in SQL. Use when: (1) persisting nodes/edges
  or any relational data in a single-file embedded DB, (2) doing blast-radius /
  reachability / BFS in SQL with a recursive CTE instead of loading a graph into
  memory, (3) setting WAL mode, busy_timeout, transactions, and prepared
  statements correctly, (4) writing forward-only schema migrations. Triggers on
  rusqlite, SQLite, WAL, recursive CTE, prepared statement, params!, query_map,
  embedded database, graph traversal in SQL.
license: MIT
compatibility: Rust 1.75+, rusqlite 0.32.x (bundled SQLite)
metadata:
  author: web-fluid
  verified-with: "rusqlite 0.32.1, libsqlite3-sys 0.30.1 (cargo test, green)"
allowed-tools: Bash(cargo:*) Bash(rustc:*) Read Write Edit Glob Grep
---

# rusqlite as a Graph / Embedded Store

SQLite is a real database in a single file: transactional, queryable, no server.
With the `bundled` feature, rusqlite compiles SQLite in — the binary ships with
zero system dependency. For a code graph (or any node/edge data) it beats an
in-memory graph lib: you get indexed lookups, bounded traversal in SQL, and
persistence for free.

## Setup

```toml
[dependencies]
rusqlite = { version = "0.32", features = ["bundled"] }
```

`bundled` = no `libsqlite3` on the host, reproducible across Linux/macOS/Windows.
Drop it only if you deliberately want the system SQLite.

## Open with the right pragmas

```rust
use rusqlite::Connection;

fn open(path: &str) -> rusqlite::Result<Connection> {
    let conn = Connection::open(path)?;
    conn.pragma_update(None, "journal_mode", "WAL")?;  // concurrent readers during a write
    conn.pragma_update(None, "busy_timeout", 5000)?;   // ms to wait on a locked db, not fail
    conn.pragma_update(None, "foreign_keys", "ON")?;   // off by default in SQLite
    Ok(conn)
}
```

- **WAL** gives you concurrent readers while one writer commits — essential if a
  watcher writes while a server reads. WAL persists on the file; set it once.
- **busy_timeout** turns "database is locked" errors into a bounded wait. Set it
  or you *will* hit spurious lock failures under concurrency.
- SQLite has exactly **one writer** at a time. Design for it: one owning write
  connection/thread; readers use their own connections. Don't fight this — it's
  the model, not a limitation to work around.

## Schema and statements

```rust
conn.execute_batch(
    "CREATE TABLE IF NOT EXISTS nodes(
         qualified_name TEXT PRIMARY KEY, kind TEXT, file TEXT, line INTEGER);
     CREATE TABLE IF NOT EXISTS edges(
         source TEXT, target TEXT, kind TEXT, line INTEGER,
         PRIMARY KEY(source, target, kind, line));
     CREATE INDEX IF NOT EXISTS idx_edges_target ON edges(target);", // BFS reads this
)?;
```

Index the column your traversal joins on. A reverse-edge BFS joins `edges.target`
→ index `target`; a forward BFS joins `edges.source` → index `source`.

Always parameterize — never format values into SQL (injection + no plan caching):

```rust
use rusqlite::params;
conn.execute(
    "INSERT OR REPLACE INTO edges VALUES (?1, ?2, ?3, ?4)",
    params![src, tgt, "CALLS", line],
)?;
```

## Bounded BFS in one query (recursive CTE)

Reachability without materializing the graph in Rust. Depth-bounded, set-based,
runs in SQLite:

```rust
use rusqlite::params;

/// Reverse blast-radius: everything that reaches `start` within `max_depth` hops.
fn bounded_bfs(conn: &Connection, start: &str, max_depth: i64) -> rusqlite::Result<Vec<String>> {
    let mut stmt = conn.prepare(
        "WITH RECURSIVE reach(node, depth) AS (
             SELECT ?1, 0
           UNION                                   -- UNION (not ALL) dedups → terminates on cycles
             SELECT e.source, r.depth + 1
             FROM edges e JOIN reach r ON e.target = r.node
             WHERE r.depth < ?2
         )
         SELECT DISTINCT node FROM reach WHERE node <> ?1 ORDER BY node",
    )?;
    stmt.query_map(params![start, max_depth], |row| row.get::<_, String>(0))?
        .collect()
}
```

Verified behaviour on `a→b→c→d`: reverse BFS from `c` at depth 1 → `[b]`; at
depth 2 → `[a, b]`. Notes that matter:

- **`UNION`, not `UNION ALL`** — dedup is what makes it terminate on cyclic
  graphs (call graphs have cycles). `UNION ALL` loops forever.
- Flip the join (`e.source = r.node` selecting `e.target`) for forward reachability.
- `ORDER BY` for deterministic output — required if you diff/snapshot results.
- The `WHERE r.depth < ?2` bound caps work; add a total-node cap in Rust
  (`.take(n)`) if you need a hard ceiling with a `truncated` flag.

## Transactions and atomic per-file replace

For "replace everything belonging to file X" (incremental re-parse), do it in one
transaction so a reader never sees a half-updated file:

```rust
let tx = conn.transaction()?;                 // BEGIN
tx.execute("DELETE FROM nodes WHERE file = ?1", params![file])?;
tx.execute("DELETE FROM edges WHERE source LIKE ?1", params![format!("{file}::%")])?;
// ... re-insert this file's rows ...
tx.commit()?;                                 // atomic; on drop-without-commit it rolls back
```

For write contention, `conn.transaction_with_behavior(TransactionBehavior::Immediate)`
takes the write lock up front instead of on first write — fewer mid-transaction
"locked" surprises.

## Migrations

Keep a `schema_version` in a `metadata` table; apply forward-only steps in order
on open. Don't hand-edit a live schema. `user_version` pragma works too:
`conn.pragma_update(None, "user_version", n)`.

## Troubleshooting

| Symptom | Cause / fix |
|---|---|
| "database is locked" | No `busy_timeout`, or two writers. Set the timeout; funnel writes through one connection. |
| Recursive CTE hangs / OOM | `UNION ALL` on a cyclic graph. Use `UNION`. |
| WAL files (`-wal`, `-shm`) linger | Normal; they checkpoint. `PRAGMA wal_checkpoint(TRUNCATE)` to flush. |
| Slow BFS on big graphs | Missing index on the joined edge column. Add `idx_edges_target`/`_source`. |
| Values not escaping | You formatted SQL by hand. Use `params![]` / `?1` always. |

## Verification

Snippets are from a probe compiled and `cargo test`-green against the pinned
versions. Any traversal you write deserves one fixture test asserting the
bounded result on a tiny known graph — off-by-one on `depth <` vs `depth <=` is
the classic bug, and a 3-edge fixture catches it.

---

*Enables Chitra Phase 0: T0.3 (SQL bounded best-score relaxation BFS prototype in
rusqlite).*
