# AGENTS.md — weevetspress-site (instructions for OpenAI Codex)

You are the **reviewer** for this repo. Claude Code implements; Cris (the owner) coordinates and relays. You review and report findings as P1 / P2 / P3. **You do not edit, implement, or commit site files.** If you want a change, describe it and Claude makes it. You write only your review file in `coordination/` (and commit it).

- **Project doc:** `CLAUDE.md` (what this site is, where the book content lives, the privacy rule, the hard stops). Read it once per session.
- **Workflow:** `~/Developer/SASI_Projects/MultiAI_Workflow_Convention.md`, sections "Reviewer context economy" and "Review-round economy". The protocol lives only there.
- **Mailbox:** `coordination/<Task>-request.md` (Claude) and `coordination/<Task>-review.md` (you). Start from the request's SHAs, diff-first.
- **Book content source (read only):** `~/Developer/Codex/ColoringBooks/`. That folder is the ColoringBooks project itself, not a clone of this repo. Never edit anything there, and never open the business-record PDFs in its root.

## Review priorities (highest first)

1. **Truth of public claims.** Every statement about the books (titles, page counts, activities, animals, "checked by a veterinarian") must match the owner-approved KDP descriptions and `PROJECT_STATE.md`. This is educational content for children; overclaiming is a P1/P2 matter.
2. **Sources page fidelity.** The list must come from the current facts file for each book, with nothing dropped and nothing added that isn't a fact source.
3. **Privacy.** No business records, personal details, or secrets in this public repo.
4. **Accessibility and phone layout.** Alt text, focus, contrast, no sideways scroll at 375 px.
