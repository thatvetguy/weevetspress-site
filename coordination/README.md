# Coordination mailbox — Claude Code ↔ Codex (weevetspress-site)

Git-backed review channel between Claude Code's tree (`~/Developer/weevetspress-site`) and Codex's clone (`~/Developer/Codex/weevetspress-site`). This repo has no GitHub remote yet, so Codex's clone pulls from Claude's folder directly (`origin` = the local path).

**The protocol lives in ONE place:** `~/Developer/SASI_Projects/MultiAI_Workflow_Convention.md` → "Reviewer context economy" and "Review-round economy". This README does not restate it.

## Files (per task)
- `coordination/<Task>-request.md`: written by Claude Code.
- `coordination/<Task>-review.md`: written by Codex.
- Evidence files a request names (for example a link-check report) sit beside them.

Header fields and the status lifecycle are the hub's: see `~/Developer/SASI_Projects/coordination/README.md`.
