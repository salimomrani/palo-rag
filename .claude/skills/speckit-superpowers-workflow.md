# Skill: speckit + superpowers — Integrated Workflow

## When to apply

- Any feature or non-trivial change → follow this workflow in full
- Small fix (typo, label, 1-2 lines) → direct edit, no spec, no skill

---

## Phase 1 — SPEC (speckit)

```
/speckit.specify    ← create spec from description (specs/<NNN>-<name>/spec.md)
/speckit.clarify    ← resolve ambiguities (optional, if spec has [NEEDS CLARIFICATION])
/speckit.plan       ← generate plan.md (tech decisions, architecture)
/speckit.tasks      ← generate tasks.md (ordered, parallelizable)
/speckit.analyze    ← cross-artifact consistency check (optional but recommended)
```

Specs always live in `specs/<NNN>-<short-name>/`. Created by `/speckit.specify`.

**Forbidden**: `superpowers:writing-plans`, `superpowers:executing-plans` — speckit replaces them.

---

## Phase 2 — IMPLEMENTATION (superpowers)

```
superpowers:subagent-driven-development   ← reads plan.md + tasks.md, orchestrates subagents
  └─ superpowers:test-driven-development  ← RED → GREEN → REFACTOR (mandatory per task)
  └─ superpowers:systematic-debugging     ← when blocked (never brute-force)
```

Update `specs/<feature>/tasks.md` after each task: `[ ]` → `[x]`.

---

## Phase 3 — COMPLETION

```
superpowers:requesting-code-review        ← review against plan before PR
superpowers:finishing-a-development-branch ← cleanup, final checks
commit-commands:commit-push-pr            ← commit + push + open PR
```

Never push directly to `master` — always open a PR.

---

## Parallel execution

Use `superpowers:dispatching-parallel-agents` when backend and frontend tasks are independent.

---

## Quick reference

| Situation | Action |
|---|---|
| New feature | `/speckit.specify` → full pipeline |
| Spec exists, ready to code | `superpowers:subagent-driven-development` |
| Blocked on a bug | `superpowers:systematic-debugging` |
| Before PR | `superpowers:requesting-code-review` |
| PR ready | `commit-commands:commit-push-pr` |
| Small fix | Direct edit, no skill |
