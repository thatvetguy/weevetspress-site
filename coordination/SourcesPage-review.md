# SourcesPage — Codex review, round 1

Verdict: **changes requested** — 0 P1, 3 P2, 1 P3.

Reviewed implementation `947672754e2c5249f87b9ad587e9264c4d4aebbb` against empty tree `4b825dc642cb6eb9a060e54bf8d69288fbee4904`. Local HEAD `0e96df8` adds only the request packet; implementation files match the requested head. Round 0 is recorded. Read AGENTS.md, CLAUDE.md, the workflow's reviewer/context and round rules, and GC-SITE entries. No site or book-content edits.

## Findings

### P2.1 — Heading filter drops a source for a printed caption

`tools/build_sources.py:45-48, 118-119`: `review` in any level-2 heading suppresses the entire section. Book 2's current `second-book-facts-v02.md:108-111` has “October 16, 2026 changes (owner review of preview v01)”, which explicitly sources page 81's caption, “Marbles takes short naps in the day and at night,” to Refinetti 2006 (`https://doi.org/10.1007/s00359-006-0093-x`). That DOI is absent from the generated Book 2 list. This is actual fact provenance, not just review administration, and violates the no-dropped-sources requirement. Include substantive source-bearing amendments even when their headings mention review; verify this DOI appears after rebuilding. An audit of unique URLs excluded by the heading rule across the configured seven books found this one additional animal-fact URL (Book 1's excluded publishing links are correctly excluded).

### P2.2 — Blank backs do not guarantee markers cannot damage another picture

`index.html:58`: “if markers soak through, they never ruin another picture” exceeds the approved descriptions' supported claim, “each printed on one side only.” Ink can penetrate the blank reverse and reach the next sheet. Retain the single-sided/blank-back statement; remove the absolute guarantee, or advise using a protective sheet behind the page. No change to the approved books is requested.

### P2.3 — Stale generated content still passes the check command

`tools/build_sources.py:234-236`: both the up-to-date and out-of-date branches return normally, so `python3 tools/build_sources.py --check` exits 0 even when regeneration would change the page. A future facts update can therefore pass an automated freshness gate with a stale public bibliography. Return a nonzero exit status for a mismatch. Verify the current page exits 0 and a deliberately stale temporary fixture exits nonzero, without altering the real page.

### P3.1 — Resolve or annotate the three known unavailable source URLs

`coordination/SourcesPage-linkcheck-2026-11-03.txt:12-15` records three 404s (beardeddragonsworld brumation, Wayne State rat PDF, BGSU crested-gecko PDF), and the public lists present them without an availability note. This impedes readers checking those citations. Ask the book-content owner to approve successor/archive URLs, or retain the original citation with a clear availability note. Do not silently drop consulted sources or substitute different evidence. These statuses are from the submitted link report, not a fresh live recheck.

## Answers to the packet's asks

1. The seven approved KDP descriptions support the ages, size, outlines, one-sided printing, Paws and Learn and veterinarian-review claims. Vet Tips, spot-the-difference pages and certificates are correctly scoped to Books 2–7; wild animals to Books 3–7. The marker guarantee is the exception above. The sources intro's veterinarian-review statement is supported by the approved descriptions and recorded owner reviews; it is not a claim that every linked website is veterinarian-authored.
2. Titles, hooks, animal names and kinds, summaries and activity counts match the current setup sheets: first v01, second v01, third v01, fourth v03, fifth v05, sixth v02, seventh v01. Books 4–6 omit details without changing meaning. Book 5 also changes sentence punctuation and removes clauses within sentences; that is harmless, but the packet's “sentences dropped, no words changed” description is imprecise. The 40/54/55 activity-page counts are distinct from the 80/108/110 physical-page counts and are correctly described. Six Amazon ASINs and Book 7's coming-soon status match PROJECT_STATE.md.
3. R1: a consulted-source bibliography is reasonable, including sources behind facts later rewritten or cut. Say explicitly that it includes background research and may cover material not printed in the final book; the current intro can be read as an exact printed-fact mapping. This clarification is recommended, not an additional blocker. R2: retain genuinely consulted sources even when they are secondary or commercial; do not improve appearances by deleting provenance. Prefer authoritative evidence when the book-content owner revises a fact, and describe the list as sources consulted rather than an endorsement of each site's entire contents.
4. Book 1 checked end to end independently: its 14 fact/source table rows contain 16 distinct URLs, exactly the 16 published links, with zero missing or extra. This includes the optional F61 tooth-count sources, consistent with the consulted-research approach. For all seven books, generated/published URL sets agree (16, 44, 95, 114, 88, 132, 154; 643 book-specific citations, 632 distinct URLs). That proves output fidelity to the extractor, not completeness of the extractor: P2.1 is the counterexample. Configured files match PROJECT_STATE.md, including Book 4's supplementary notes and Book 6 v06.
5. No additional misleading public book claims or private-record disclosures found in the reviewed text and tracked-file inventory. No business-record PDFs were opened. Static accessibility review found descriptive linked-cover alternatives, a skip link, keyboard focus styles and native details controls. The request reports desktop/375px visual checks; I did not independently repeat browser or Amazon destination checks and do not claim those passed independently.

## Verification

Read the requested diff, current approved descriptions, PROJECT_STATE.md and configured facts headings/source-bearing exclusions. Ran `python3 tools/build_sources.py --check`: all seven counts above, “up to date.” Used an independent HTML parser to compare each book's published href set to collected URLs (zero missing/extra for every book), plus independent extraction of Book 1's complete facts table. Inspected the check command's mismatch control flow statically. Did not rerun the full network matrix. Initial working tree was clean; `git pull --ff-only` could not write `.git/FETCH_HEAD` under the session permissions, but the requested implementation was already present and verified locally.

---

# SourcesPage — Codex review, round 2

Verdict: **approved / review locked** — 0 open P1, 0 open P2, 0 open P3. No new findings.

Reviewed fixes-first range `947672754e2c5249f87b9ad587e9264c4d4aebbb..c0bde6fcc93f856946375f4d19b429a3e5155cb5`, including the changed source-generation logic, public text, availability notes and CSS. Local HEAD `5516139` differs from the requested head only in the request packet. Initial working tree clean.

## Dispositions

- **P2.1 closed.** Removing the heading filter restores the Refinetti 2006 DOI. Independently loaded old and new collectors and compared every book's complete URL set: Book 2 adds exactly `https://doi.org/10.1007/s00359-006-0093-x`; all six other books have no additions; none of the seven books loses a URL. The generated HTML contains the added citation. No unrelated links were introduced by reading the formerly excluded sections of the current configured files.
- **P2.2 closed.** `index.html:58` states the supported blank-back claim and recommends scrap paper behind marker work; the absolute bleed-through guarantee is removed.
- **P2.3 closed.** The mismatch path now exits 1. Independently copied the script and page into a temporary directory: fresh page exits 0 with “up to date”; a deliberately stale Book 2 heading exits 1 with the out-of-date message. The real page's SHA-256 was identical before and after these controls.
- **P3.1 closed.** All three original unavailable URLs are retained, each with an adjacent dated availability note. The added text uses the existing secondary text color and inherits the list's wrapping behavior. The new guard fails if an annotated URL is no longer cited. The submitted November 4 link report still identifies the same three 404s; no live network recheck was performed in this review.
- **R1 recommendation addressed.** The introduction now explicitly includes background research and material omitted from the final book. **R2 disposition accepted:** consulted sources remain listed without endorsing each site's entire contents.
- The Book 5 packet-wording correction is acknowledged; no product change was needed.

## Verification and scope

`python3 -B tools/build_sources.py --check` reports up to date, exit 0: per-book counts 16 / 45 / 95 / 114 / 88 / 132 / 154 (644 citations). The submitted link report accounts for 633 distinct URLs: 554 ok + 66 blocked + 3 dead + 6 other + 4 error = 633. The source URL-set comparison and scratch freshness controls above passed; `git diff --check 9476727 c0bde6f` is clean. Static review found no regression introduced by these fixes. Browser/phone checks and the network matrix were not independently repeated. This locks the code/content review; owner visual validation and publication decisions remain with Cris. Only this review file was edited.
