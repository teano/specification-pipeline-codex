# Generator Stage: Grounded Extraction

## 1. Purpose

Extract **normative, owner-attributed requirements** from source design materials — not a GDD paraphrase or topical outline (`Input`, `Score`, `UI` chapters detached from grounded project/domain owners).

Mandatory pass: `PASS-003` — `../../../shared/passes/PASS-003-source-grounding-and-conflicts.md`.

---

## 2. Anti-GDD-retelling rules

Forbidden outcomes:

- Copying GDD section structure as the spec structure.
- Narrative summary without `REQ`-level (or regulation-equivalent) extractable statements.
- Mechanics floating without a named, grounded owning system/entity.
- Invented requirements without `Assumption` label.
- Silent merge of contradictory sources.
- “The system does X” with no state/rule/input/config owner.

Required outcome:

- Each significant mechanic tied to: grounded project entity kind, rule owner, state owner, input path, visual owner (if any), config owner (if any), data models, branches, edge cases, forbidden shortcuts.
- If owner is unclear → **Open Question**, not an arbitrary controller name.

---

## 3. Mandatory internal analysis

Complete **before** writing spec prose. Results inform extraction; emit only if the user asked for the analysis artifact.

| # | Question |
|---|---|
| 1 | What is being built (mini-game, mechanic, screen, module, feature, integration)? |
| 2 | Player/user goal? |
| 3 | Core loop to implement? |
| 4 | Which systems naturally follow from GDD? |
| 5 | Which entities exist inside those systems? |
| 5a | How are those systems/entities grounded in the current project context or `grounding.md` fallback? |
| 6 | Entity and feature-level states? |
| 7 | Player actions available? |
| 8 | Rules making actions valid/invalid? |
| 9 | Events that change feature state? |
| 10 | Win/lose/complete/exit conditions? |
| 11 | Tunable parameters and **which system owns** them? |
| 12 | Data to model in data models section? |
| 13 | Visual reactions and which UI/visual system displays them? |
| 14 | UI elements, popups, tutorial, pause, endgame flows (if in GDD)? |
| 15 | External systems touched (only if confirmed in GDD/project context)? |
| 16 | Internal GDD contradictions? |
| 17 | Where are Open Questions required? |
| 18 | Where could a coding agent satisfy wording but implement wrongly? |
| 19 | Subsystems to split (change, variability, ownership, lifecycle, boundary, God Object risk)? |
| 20 | Mandatory subsystems vs implementation details? |
| 21 | Where is shallow decomposition insufficient? |
| 22 | GDD domain terms, hidden synonyms, duplicates per regulation terminology rules; which detected names are code/API or decomposition signatures and therefore excluded from glossary? |

---

## 4. Extraction through systems (not topical lists)

Apply while reading GDD. Full document formatting → `../../../shared/specification-document-regulation.md`.

### 4.1 System signals in GDD

Look for responsibility groups, not class names. Signals include:

- Separate state to store/update.
- Decision rules and multi-step processes.
- Data/parameter sources; object lifecycles.
- Distinct user interactions or visual feedback flows.
- External integration; variant behavior; localized edge cases.
- Phrases such as: “player can…”, “system checks…”, “object enters state…”, “every N seconds…”, “when condition…”, “if action impossible…”, “chance depends on…”, “value is configurable…”, “after animation…”, “result is sent…”, “hint is shown…”, “data is saved…”.

These phrases **do not** auto-create classes; they trigger an ownership check.

### 4.2 Mechanics, input, visual, data, progression, integration, assets

| Slice | Generator must determine |
|---|---|
| Mechanic | Rule owner, state owner, input/command receiver, result displayer, config owner, models, branches, edges, forbidden UI/view decisions, no hardcoded tunables |
| Input | Gesture recognition vs logical command vs validity vs apply vs preview/invalid feedback; view may recognize gestures; gameplay decision stays in logic unless project says otherwise |
| Visual/UI/VFX | Static style vs gameplay/UI feedback vs VFX vs timing vs highlights; visual lifecycle owner (trigger, blocker, completion before next step, pause/endgame/restart/destroy, cleanup); view must not own gameplay truth |
| Data/config | Models per regulation; configs as decomposition entities (parameters, defaults if confirmed, validity, consumers, not runtime state); no invented numbers |
| Progression/score/endgame | Who stores/calculates/decides/completes/notifies UI/external flow |
| Integration | Boundary inside decomposition: who talks externally, payloads, forbidden deps; no invented API names |
| External assets/manual setup | Implementation constraints or open questions; no hidden framework/editor fallbacks |

---

### 4.3 Terminology extraction boundary

When extracting terminology, keep separate lists internally:

- domain glossary candidates: feature/domain nouns, states, resources, UI concepts, config concepts, and non-signature project roles that need semantic disambiguation;
- signature candidates: confirmed or proposed type, method, property, field, event, config key, namespace, folder, file, Unity/C# API, or framework name.

Only the first list can become `## 3. Terminology and Glossary`. Signature candidates belong in decomposition, data/config, integration, or implementation contract sections. If a signature is confirmed, reuse it exactly throughout the spec; if it is not confirmed, keep it as an assumption/open question instead of adding it to terminology.

---

## 5. Requirement strength classes

When classifying extracted items (document placement per regulation):

| Class | Meaning |
|---|---|
| Requirement | From GDD, user, confirmed decision, or mandatory project constraint |
| Implementation constraint | Technical condition required to implement a requirement safely |
| Proposal | Useful, not confirmed mandatory — mark optional / separate |

Never hide **Assumption** inside requirement wording.

---

## 6. Stage execution steps

1. Read all source materials; apply `../../../shared/source-priority-policy.md`.
2. Run the mandatory internal analysis.
3. Extract grounded requirements with owners and project-domain entity kinds; run `PASS-003`.
4. Record conflicts as findings, not silent merges.
5. Emit extraction artifact (internal or user-visible per request): requirement list + grounding refs + pass status.

---

## 7. Quality criteria

1. Every requirement links to source location or explicit assumption.
2. Conflicts between sources → findings, not merged wording.
3. Missing sections → open questions or assumptions, not invented fill.
4. No undifferentiated GDD retelling.

---

## 8. Blocking anti-patterns

- GDD summary without extractable requirements.
- Invented mechanics/APIs without assumption label.
- Ignored contradictions.
- Topical chapters (`Analytics`, `Config`) that orphan mechanics from owners.

---

## 9. Output

| Field | Content |
|---|---|
| Stage status | `extraction-ok` \| `extraction-warning` \| `extraction-blocked` |
| Artifact | Grounded requirement set (with owners where known) |
| Pass table | `PASS-003` + profile passes if run in parallel per policy |
| Findings | Per `../../../shared/pass-loading-policy.md` §6 |
| Language | Required `USER_LANGUAGE` |

Do not proceed to system-mapping on `extraction-blocked` without a remediation plan in findings.
