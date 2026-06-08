# Source Priority and Conflict Policy

## 1. Priority Order

Use this source order for all three modes:

1. explicit user statements in the current request;
2. source specification or source design document under work;
3. later user-confirmed decisions in the same thread;
4. shared regulation and core principles from this package;
5. project rules as a verification layer only.

Project rules must not create new gameplay/product requirements.

---

## 2. Conflict Handling

When sources conflict:

1. never silently choose a side;
2. preserve both conflicting meanings in findings/issues;
3. ask one critical clarifying question only when required to proceed;
4. if unresolved, keep status as open question/issue (mode dependent);
5. do not rewrite source intent to match assumptions.

---

## 3. What May Be Derived

Allowed derivation:

* traceability links;
* consistency checks;
* risk classification;
* explicit uncertainty markers.

Not allowed derivation:

* inventing architecture/classes/APIs without grounding;
* inventing business/gameplay behavior;
* converting suggestions into confirmed requirements.

---

## 4. Decision Promotion Rule

A proposal becomes requirement/decision only after explicit user confirmation.

Before confirmation it must be tracked as one of:

* proposal;
* assumption;
* open question;
* issue/risk.
