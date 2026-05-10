<!-- Source: https://skills.sh/apollographql/skills/rust-best-practices -->
<!-- Install: npx skills add https://github.com/apollographql/skills --skill rust-best-practices -->

# Rust Best Practices

Apply these guidelines when writing or reviewing Rust code. Based on Apollo GraphQL's Rust Best Practices Handbook.

## Best Practices Reference

Before reviewing, familiarize yourself with Apollo's Rust best practices. Read ALL relevant chapters in the same turn in parallel. Reference these files when providing feedback:

* Chapter 1 - Coding Styles and Idioms: Borrowing vs cloning, Copy trait, Option/Result handling, iterators, comments
* Chapter 2 - Clippy and Linting: Clippy configuration, important lints, workspace lint setup
* Chapter 3 - Performance Mindset: Profiling, avoiding redundant clones, stack vs heap, zero-cost abstractions
* Chapter 4 - Error Handling: Result vs panic, thiserror vs anyhow, error hierarchies
* Chapter 5 - Automated Testing: Test naming, one assertion per test, snapshot testing
* Chapter 6 - Generics and Dispatch: Static vs dynamic dispatch, trait objects
* Chapter 7 - Type State Pattern: Compile-time state safety, when to use it
* Chapter 8 - Comments vs Documentation: When to comment, doc comments, rustdoc
* Chapter 9 - Understanding Pointers: Thread safety, Send/Sync, pointer types

## Quick Reference

### Borrowing & Ownership

* Prefer `&T` over `.clone()` unless ownership transfer is required
* Use `&str` over `String`, `&[T]` over `Vec<T>` in function parameters
* Small `Copy` types (≤24 bytes) can be passed by value
* Use `Cow<'_, T>` when ownership is ambiguous

### Error Handling

* Return `Result<T, E>` for fallible operations; avoid `panic!` in production
* Never use `unwrap()`/`expect()` outside tests
* Use `thiserror` for library errors, `anyhow` for binaries only
* Prefer `?` operator over match chains for error propagation

### Performance

* Always benchmark with `--release` flag
* Run `cargo clippy -- -D clippy::perf` for performance hints
* Avoid cloning in loops; use `.iter()` instead of `.into_iter()` for Copy types
* Prefer iterators over manual loops; avoid intermediate `.collect()` calls

### Linting

Run regularly: `cargo clippy --all-targets --all-features --locked -- -D warnings`

Key lints to watch:

* `redundant_clone` - unnecessary cloning
* `large_enum_variant` - oversized variants (consider boxing)
* `needless_collect` - premature collection

Use `#[expect(clippy::lint)]` over `#[allow(...)]` with justification comment.

### Testing

* Name tests descriptively: `process_should_return_error_when_input_empty()`
* One assertion per test when possible
* Use doc tests (`///`) for public API examples
* Consider `cargo insta` for snapshot testing generated output

### Generics & Dispatch

* Prefer generics (static dispatch) for performance-critical code
* Use `dyn Trait` only when heterogeneous collections are needed
* Box at API boundaries, not internally

### Type State Pattern

Encode valid states in the type system to catch invalid operations at compile time:

```rust
struct Connection<State> { /* ... */ _state: PhantomData<State> }
struct Disconnected;
struct Connected;

impl Connection<Connected> {
    fn send(&self, data: &[u8]) { /* only connected can send */ }
}
```

### Documentation

* `//` comments explain _why_ (safety, workarounds, design rationale)
* `///` doc comments explain _what_ and _how_ for public APIs
* Every `TODO` needs a linked issue: `// TODO(#42): ...`
* Enable `#![deny(missing_docs)]` for libraries
