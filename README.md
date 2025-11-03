# ThinkieSkills

Making Kent Beck's Thinkies available as Claude Skills.

## Goal

Validate whether Kent Beck’s Thinkies provide real user value when delivered as Claude Skills, and define a path to scale if validated.

## Objectives and success criteria

- **Primary objective**: Users reliably apply Thinkies to real problems inside Claude with minimal friction.
- **Success signals**:
  - **Engagement**: ≥30% of invited users use a Thinkie Skill 3+ times in 2 weeks.
  - **Outcome**: ≥60% of sessions rated “helpful” (thumbs up or Likert ≥4/5).
  - **Speed**: Median time-to-first-use <2 minutes for new users.
  - **Retention**: ≥25% week-4 retained users who used ≥2 distinct Thinkies.

## Scope and constraints

- **Audience**: Builders/ICs (engineers, PMs, designers) and coaches/leads.
- **Boundaries**: Start with 8–12 Thinkies that are general-purpose and low risk.
- **Constraints**: Preserve voice and intent; keep sessions short and actionable.

## Discovery and alignment

- **Catalog**: Collect and normalize Thinkies (title, purpose, steps, examples, anti-patterns).
- **Structure**: Convert into canonical schema: id, name, intent, inputs, instructions, probes, examples, failure modes, citations.
- **Voice**: Capture tone guidelines (succinct, invitational, non-judgmental).
- **Permissions**: Not required (author is Kent Beck). Ensure consistent attribution and voice stewardship.

## Product design for Claude Skills

- **Interaction model**:
  - Invocation: “Use Thinkie: X” and auto-suggest triggers from context (e.g., “stuck”, “trade-off”, “naming”).
  - Modes: guided dialog vs one-shot; allow branching prompts.
  - Inputs: minimal, ask just-in-time questions.
- **Packaging**:
  - One Skill per Thinkie for clarity; add a “Thinkie Router” Skill to suggest the best Thinkie from context.
  - Common UX: short intro, 1–3 probing questions, concise output, next suggested step.
- **Safety/guardrails**: Avoid authoritative prescriptions; emphasize options; highlight trade-offs.

## Technical design

- **Schema (storage)**: `thinkie_id`, `name`, `intent`, `triggers`, `preconditions`, `steps`, `questions`, `examples`, `pitfalls`, `voice`, `citations`.
- **Skill specification**: Prompt templates derived from schema; deterministic scaffolding + few-shot examples.
- **Parameters**: `user_goal`, `constraints`, `artifacts` (code, doc), `team_context`.
- **Router**: Heuristic + embedding-based matcher over `intent` and `triggers`; fall back to top-3 suggestion.
- **State**: Ephemeral per-session state; optional summary to memory with user consent (“What we decided”).
- **Telemetry**: Invocation source, completion success, user rating, drop-off step, time spent, follow-on actions.
- **Privacy**: Don’t store artifacts by default; explicit opt-in for memory.

## MVP plan (weeks 1–4)

- **MVP set (8–12 Thinkies)**: e.g., “Trade-off Triangle”, “Name the Purpose”, “One-Way Door vs Two-Way Door”, “Small Bets”, “Clarify the Constraint”, “Define ‘Done’”, “Reverse the Plan”, “Pick the Next Most Reversible Step”.
- **Authoring tooling**: Simple YAML/JSON author format + validation; preview Skill runner.
- **Baseline prompts**: Shared scaffolding + Thinkie-specific inserts.
- **Router v1**: Heuristic triggers (keywords, user intent).
- **Safety review**: Tone check, bias pass, failure-mode prompts.
- **Private pilot**: 15–30 users; capture qualitative feedback.

## Evaluation framework

- **Quantitative**: invocation → first answer rate, completion rate, multi-step continuation, thumbs up/down, time-to-outcome, repeated use, diversity of Thinkies used.
- **Qualitative**: post-session micro-survey (“Did this unstick you?”), 20-min interviews with 8 users, free-text pain points.
- **Comparatives**: A/B with “plain Claude prompt” vs “Thinkie Skill” on matched tasks.
- **Task batteries**: Naming, planning, trade-off selection, scope cut, retros framing.

## Iteration/scale plan (weeks 5–8)

- **Expand catalog**: 20–40 Thinkies; retire low-performers; merge near-duplicates.
- **Router v2**: Embedding-based similarity; context signals (recent words like “deadline”, “scope”, “risk”).
- **Personalization**: Lightweight preferences (tone, verbosity, role).
- **Skill chaining**: Offer next-step Thinkie based on outcome.
- **Artifacts-aware**: Optional code/doc ingestion to tailor probes.
- **Distribution**: Skill bundles per role (Engineer, PM, Design, EM/Coach).

## Operational readiness

- **Versioning**: Semantic version per Thinkie; change logs and rollback.
- **Analytics**: Dashboards for usage, satisfaction, fallout steps, router accuracy.
- **Feedback loop**: In-product “This missed because \_\_\_”; weekly review and edits.
- **Quality bar**: Definition-of-done rubric (clarity, brevity, actionability, alignment to voice).
- **Docs**: Short “How to pick a Thinkie” and “When not to use Thinkies”.

## Brand and authorship

- **Authorship**: Kent Beck as the author; ensure voice fidelity across Skills.
- **Attribution**: Prominent credit preserved in descriptions; link to source material where appropriate.

## Risks and mitigations

- **Overly generic output**: Embed concrete probes; require example/context; add anti-pattern reminders.
- **User fatigue**: Keep sessions short; show progress; allow skip/fast path.
- **Router misses**: Provide top-3 choices; allow user to override.
- **Measurement bias**: Use matched-task A/B; pre-register success metrics.

## Resourcing

- **People**: 1 PM, 1 UX writer/editor, 1 prompt/skills engineer, 0.5 MLE, 0.5 backend, 1 researcher for pilot.
- **Time**: 6–8 weeks to validate; 2–3 months to scale if greenlit.

## Milestones and timeline (example)

- **Week 1**: Finalize schema; select MVP Thinkies; author 2 end-to-end in the format.
- **Week 2**: Authoring tooling; baseline prompts; 4 Skills ready.
- **Week 3**: Router v1; safety review; 8–12 Skills complete.
- **Week 4**: Pilot launch; telemetry dashboard; interviews begin.
- **Week 5–6**: A/B experiments; expand catalog; router v2; iteration passes.
- **Week 7–8**: Go/No-Go; scaling plan; brand polish.

## Concrete next steps (1–2 weeks)

- **Draft schema** and author two Thinkies end-to-end to test the format.
- **Build preview runner** to dry-run Skills and capture probes/output.
- **Define metrics** and dashboard; instrument telemetry.
- **Recruit pilot users** and prepare 5-minute onboarding guide.

---

If useful, we can add a YAML schema stub and a sample Thinkie file next.

## Local usage

1. Create a virtual environment (optional) and install dependencies:

   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Run the Fun Bit Thinkie interactively:

   ```bash
   python runner.py --thinkie fun_bit
   ```

   Or specify a file directly:

   ```bash
   python runner.py --file thinkies/fun_bit.yaml
   ```

3. Answer the prompts. The runner will render the suggested next step using the Thinkie’s `output_template`.

## Add to Claude via MCP (Skills-like)

Expose Thinkies to vanilla Claude as tools using the Model Context Protocol (MCP).

1. Install deps (same venv is fine):

   ```bash
   pip install -r requirements.txt
   ```

2. In Claude Desktop: Tools → Developer → Add Server
   - Command: `python /Users/kentb/Dropbox/Mac/Documents/GitHub/ThinkieSkills/mcp_server.py`
   - Name: `Thinkies`

3. In a chat, enable the `Thinkies` tool. Available tools:
   - `thinkies.list` → shows available Thinkies
   - `thinkies.run` with params `{ "id": "fun_bit", "answers": { "task_summary": "...", "fun_candidates": "...", "energy_blockers": "..." } }`

If `answers` are omitted or incomplete, the tool returns the required question ids so you can supply them in a follow-up tool call.
