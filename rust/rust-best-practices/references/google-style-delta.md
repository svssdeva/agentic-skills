<!-- Local addition (not from apollographql). Source: https://google.github.io/styleguide/rustguide.html, checked 2026-10-28. -->

# Google Rust Style Guide: where it differs from or adds to this skill

Google's guide targets large shared codebases (Android, Chromium, Fuchsia). Use these when the
code is a library other teams consume; for a small app, the Apollo defaults in SKILL.md stand.

## Conflicts with the Quick Reference

| Topic | This skill (Apollo) | Google |
|---|---|---|
| Panics | Quick Reference: never `unwrap()`/`expect()` outside tests | `panic!` for violated invariants is fine; when panicking, `expect("reason")` over `unwrap()` |
| Failure type | `Result<T, E>` for fallible operations | `Option` when the cause is obvious and the caller gains nothing from detail (e.g. `checked_add`); `Result` when it does; `panic!` for violated invariants |

## Additions

- **Avoid `Rc`/`Arc` by default:** prefer unique ownership and borrowing unless that makes the
  structure unreasonably complex.
- **`Option<&T>` over `&Option<T>`** and `&T` over `&Box<T>` in parameters.
- **Newtypes over aliases** when values have distinct meaning, need their own API, or are easy to
  swap (`Day(u32)` vs `Month(u32)`). A `type` alias gives no protection.
- **`enum` over `bool`** parameters whose meaning isn't obvious at the call site.
- **Named fields** over tuples and non-newtype tuple structs.
- **`#[non_exhaustive]`** on public enums and public-field structs that cross team or crate-version
  boundaries (adding a variant stays non-breaking). Skip it for closed sets (RGB, Visible/Hidden)
  and for your own crate's enums, where exhaustive matching is the point.
- **Matching a `non_exhaustive` enum:** prefer naming known variants and put don't-cares in the `_`
  arm (required only outside the defining crate); use `if let` when one variant matters.
- **`#[must_use]`** on functions whose ignored result is a bug, on error types and on lazy values.
- **Imports:** no glob imports; one module per `use`; types imported unqualified; top-level
  functions called module-qualified (`mem::swap`); trait imports scoped locally.
- **Explicit types** on `.into()`, `.parse()` and long iterator chains.
- **`format!`/`write!`** to join three or more strings.
- **Never** `panic::catch_unwind` in first-party code (narrow defense-in-depth exception), code
  before `main()` (`ctor`), or reaching into a poisoned mutex.
- **Unsafe:** encapsulate it and write a `// SAFETY:` comment.
