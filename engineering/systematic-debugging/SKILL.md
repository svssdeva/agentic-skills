<!-- Source: https://www.skills.sh/obra/superpowers/systematic-debugging -->
<!-- Install: npx skills add https://github.com/obra/superpowers --skill systematic-debugging -->
---
name: systematic-debugging
description: Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes
---

# Systematic Debugging

## Overview

Random fixes waste time and create new bugs. Quick patches mask underlying issues.

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

**Violating the letter of this process is violating the spirit of debugging.**

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

## When to Use

Use for ANY technical issue:
- Test failures
- Bugs in production
- Unexpected behavior
- Performance problems
- Build failures
- Integration issues

**Use this ESPECIALLY when:**
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- You've already tried multiple fixes
- Previous fix didn't work
- You don't fully understand the issue

## The Four Phases

You MUST complete each phase before proceeding to the next.

### Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

1. **Read Error Messages Carefully** — don't skip past errors or warnings; read stack traces completely
2. **Reproduce Consistently** — can you trigger it reliably? What are the exact steps?
3. **Check Recent Changes** — what changed that could cause this? Git diff, recent commits, new dependencies
4. **Gather Evidence in Multi-Component Systems** — add diagnostic instrumentation at each component boundary, run once to gather evidence showing WHERE it breaks, THEN investigate that specific component
5. **Trace Data Flow** — where does bad value originate? Keep tracing up until you find the source; fix at source, not at symptom

### Phase 2: Pattern Analysis

1. **Find Working Examples** — locate similar working code in the same codebase
2. **Compare Against References** — read reference implementation COMPLETELY; understand the pattern fully before applying
3. **Identify Differences** — list every difference between working and broken, however small
4. **Understand Dependencies** — what other components, settings, config, environment?

### Phase 3: Hypothesis and Testing

1. **Form Single Hypothesis** — state clearly: "I think X is the root cause because Y"
2. **Test Minimally** — make the SMALLEST possible change to test hypothesis; one variable at a time
3. **Verify Before Continuing** — did it work? Yes → Phase 4. Didn't work? Form NEW hypothesis
4. **When You Don't Know** — say "I don't understand X"; ask for help; research more

### Phase 4: Implementation

1. **Create Failing Test Case** — simplest possible reproduction; automated test if possible; MUST have before fixing
2. **Implement Single Fix** — address the root cause; ONE change at a time; no "while I'm here" improvements
3. **Verify Fix** — test passes? No other tests broken? Issue actually resolved?
4. **If Fix Doesn't Work** — STOP. Count: How many fixes have you tried? If < 3: return to Phase 1. If ≥ 3: question the architecture.
5. **If 3+ Fixes Failed: Question Architecture** — each fix revealing new coupling is an architectural problem; discuss with your human partner before attempting more fixes

## Red Flags - STOP and Follow Process

If you catch yourself thinking:
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- **"One more fix attempt" (when already tried 2+)**

**ALL of these mean: STOP. Return to Phase 1.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple, don't need process" | Simple issues have root causes too. Process is fast for simple bugs. |
| "Emergency, no time for process" | Systematic debugging is FASTER than guess-and-check thrashing. |
| "Just try this first, then investigate" | First fix sets the pattern. Do it right from the start. |
| "Multiple fixes at once saves time" | Can't isolate what worked. Causes new bugs. |
| "One more fix attempt" (after 2+ failures) | 3+ failures = architectural problem. Question pattern. |

## Quick Reference

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| **1. Root Cause** | Read errors, reproduce, check changes, gather evidence | Understand WHAT and WHY |
| **2. Pattern** | Find working examples, compare | Identify differences |
| **3. Hypothesis** | Form theory, test minimally | Confirmed or new hypothesis |
| **4. Implementation** | Create test, fix, verify | Bug resolved, tests pass |
