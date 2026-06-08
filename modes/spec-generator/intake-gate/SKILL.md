# Generator Stage: Intake Gate

## 1. Purpose

Confirm the request is a full-generation job and source materials are usable.

## 2. Checks

1. user expects a full spec artifact, not a patch;
2. minimum source identity (GDD/brief/feature) is present;
3. scope boundaries are stated or explicitly marked unknown.

## 3. Output

* `intake-ok` | `intake-blocked`;
* if blocked: findings per `../../../shared/pass-loading-policy.md` §6;
* one clarifying question only if critical.

Report language: required `USER_LANGUAGE`.
