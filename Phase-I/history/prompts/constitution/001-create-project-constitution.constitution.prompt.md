---
id: 001
title: create-project-constitution
stage: constitution
date: 2026-01-02
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: user
command: /sp.constitution
labels: ["constitution","setup","governance"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - None
---

## Prompt

# sp.constitution — Phase I Todo In-Memory Console App

## 1. Project Setup
- Language: Python 3.13+
- Tooling: UV, Claude Code, Spec-Kit Plus
- App Type: CLI (In-Memory only)

Required structure:
/
├─ src/
├─ specs/history/
├─ sp.constitution.md
├─ CLAUDE.md
└─ pyproject.toml

---

## 2. Development Rules
- **No manual coding allowed**
- All code must be generated via **Claude Code**
- Follow **Agentic Dev Stack** strictly
- Every change must originate from a spec

---

## 3. Mandatory Workflow (Per Phase)
1. `/sp.specify`
2. `/sp.clarify`
3. `/sp.plan`
4. `/sp.tasks`
5. `/sp.implement`
6. Commit to Git

(Steps must not be skipped or reordered)

---

## 4. Quality Standards
- Clean, readable, modular Python
- Clear naming and single-responsibility functions
- No business logic in `main.py`
- Graceful error handling

---

## 5. Phase I Scope (Locked)
Allowed features only:
- Add Todo (title, description)
- View Todos (ID, status)
- Update Todo (by ID)
- Delete Todo (by ID)
- Mark Complete / Incomplete

Not allowed:
- Persistence
- Auth
- UI frameworks
- External APIs

---

## 6. Specs & Docs
- All specs stored in `/specs/history/`
- Specs are immutable once committed
- README: setup + run instructions
- CLAUDE.md: Claude Code rules

---

## 7. Success Criteria
- All 5 features working in console
- Specs → Plan → Tasks → Code traceable
- Repo follows constitution exactly

---

## 8. Enforcement
If any rule is violated, restart from `/sp.specify`.

**This constitution is final once committed.**

## Response snapshot

Successfully created the Phase I Todo In-Memory Console App Constitution at `.specify/memory/constitution.md` with:
- Version 1.0.0 (initial ratification)
- Six core principles: Spec-Driven Development, Agentic Dev Stack, Phase Scope Isolation, Code Quality Standards, Workflow Rigidity, and Documentation Traceability
- Additional constraints sections covering Phase I scope lock, in-memory constraint, and technology lock
- Development workflow with mandatory per-phase sequence and quality gates
- Governance section with constitutional authority, amendment procedure, compliance enforcement, and runtime guidance
- Full sync impact report documenting version change, added sections, and template compatibility validation

## Outcome

- ✅ Impact: Established formal governance structure with six core principles, explicit scope constraints, mandatory workflow sequence, and enforcement mechanisms
- 🧪 Tests: None applicable (governance document)
- 📁 Files: Created/updated .specify/memory/constitution.md
- 🔁 Next prompts: Proceed with /sp.specify to create initial feature specification for Phase I
- 🧠 Reflection: Constitution provides clear, testable guardrails with semantic versioning for amendments. Templates remain compatible. Phase I scope is well-defined and locked.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A (governance document)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
