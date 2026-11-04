```
task: Wee Vets Press website, first version (home page + sources page)
branch: main
base: 947672754e2c5249f87b9ad587e9264c4d4aebbb   # round 2: the head you reviewed in round 1
commit: c0bde6fcc93f856946375f4d19b429a3e5155cb5
stage: implementation
status: locked   # Codex round 2, c6d1c4c
scope: public claims on index.html and sources.html, and whether tools/build_sources.py lists the right sources for each book
vault-doc: none (this repo has no vault handoff yet; CLAUDE.md is the project doc)
```

**Review tier: full cadence** (educational content for children; owner's rule). Round 0: self-review only, no subagent (the two-lane pilot is IronLog-only). Round 0: 4 findings, all fixed — URLs containing parentheses were cut short (`tools/build_sources.py:105`); the sources intro overclaimed (`sources.html:34`); "What's in every book" and the Paws and Learn bubble claimed Vet Tips, spot-the-difference, a certificate, and wild animals for all seven books, but Book 1 has none of those and Book 2 has no wild animals (`index.html:55-66`, fixed in `9476727`); About said the same (`index.html:195`).

## How to get the code

No GitHub remote yet. Your clone is `~/Developer/Codex/weevetspress-site`, with `origin` = `~/Developer/weevetspress-site`. Run `git pull`. The range is two commits: `8efcfcc` (19 files, all added) and `9476727` (claim fixes, `index.html` only). Diff from the empty tree: `git diff 4b825dc642cb6eb9a060e54bf8d69288fbee4904 9476727`.

Book content (read only, not a clone of this repo): `~/Developer/Codex/ColoringBooks/`. Book table: `PROJECT_STATE.md` "Books". Approved descriptions: `planning/*-kdp-setup-sheet-*.md` and `planning/*-bowker-description-*.txt`.

## Changed files

All `A` (`git diff --name-status 4b825dc 9476727 | wc -l` → 19): `.gitignore`, `AGENTS.md`, `CLAUDE.md`, `README.md`, `coordination/README.md`, `coordination/SourcesPage-linkcheck-2026-11-03.txt`, 7 cover JPGs + 1 logo PNG under `images/`, `index.html`, `sources.html`, `style.css`, `tools/build_sources.py`, `tools/check_links.py`.

## Logical changes, anchored

1. **Hero claim** `index.html:36`: "Coloring books about real animals, checked by a veterinarian." Basis: every KDP description says the Paws and Learn facts and Vet Tips are "checked by a veterinarian".
2. **"What's inside"** `index.html:55-61`: four claims written by Claude, not taken from a listing, now scoped by book ("Books 2 to 7 add…", "Books 3 to 7 also meet wild animals"). Checked against the seven approved descriptions by grep (maze, match, find, spot-the, certificate, vet tip, wild: Book 1 has 0 for spot-the, certificate, vet tip, wild; Book 2 has 0 for wild).
3. **Paws and Learn bubble** `index.html:64-67`: "Paws and Learn signs in every book, and Vet Tips in Books 2 to 7"; "A veterinarian checks every one."
4. **Per-book entries** `index.html:77-187`: titles and subtitles from the setup sheets. The `about` paragraphs are the approved description's opening, **trimmed for Books 4, 5, 6** (sentences dropped, no words changed). The `specs` lines (`:85, :101, :117, :133, :149, :165, :181`) are shortened from each description's bullets. Amazon links for Books 1-6 were given by the owner in chat on 2026-11-03; Book 7 shows "Coming soon" (`:183`) because KDP's weekly limit blocks publishing until Sunday.
5. **About + footer** `index.html:194-205`: Claude-written; `:195` now says "Books 3 to 7 also meet wild animals, from rattlesnakes to whale sharks." Publisher line "Wee Vets Press is an imprint of Small Animal Surgeries Inc." (GC-BRND-007: never "The True Blue Group").
6. **Sources intro** `sources.html:34`: "the pages we used to check the facts in each book. A veterinarian also reviewed every fact before the book went to print."
7. **Source extraction** `tools/build_sources.py`: facts file per book `:27-43` (Book 1's facts are a section of its text draft; Book 4 adds its basics draft); sections skipped as review notes, not sources `:45-48`; publishing links dropped `:50`; URL pattern `:105-106`; site names `:52-100`; label clean-up `:127, :201`. Output between `sources.html:38` and `:2140`, never hand-edited.

## Known risks (please weigh these)

- **R1. The list is every link in each facts file's fact sections, not only links behind printed facts.** Facts files keep sources for rows that were rewritten or cut. Is the label "the pages we used to check the facts" honest for that?
- **R2. Weaker sources are listed alongside primary ones:** Wikipedia, news stories, a pet-product blog (`beardeddragonsworld.com`, `reptiledirect.com`). Should any be dropped from a public page, or is listing what was consulted the honest choice?
- **R3. Skip rules may drop real sources or keep non-sources.** `SKIP_SECTION` is a heading regex. A source cited only inside a "ChatGPT review" or "Questions for the owner" section is dropped.
- **R4. Facts-file versions** in `BOOKS` were read from `PROJECT_STATE.md` on 2026-11-03 (it names several Book 6 versions; v06 is the newest, and each version is cumulative).
- **R5. Three dead links** in the link check (below). Not removed: the facts files are the source of truth, and the owner decides.

## Gates run (in Claude's tree; build, link, and file checks at 8efcfcc, unchanged by 9476727, which touches only `index.html` text)

| Check | Command | Result |
|---|---|---|
| Sources page matches the facts files | `python3 tools/build_sources.py --check` | `up to date` |
| Per-book counts | `python3 tools/build_sources.py` | Book 1: 16 · 2: 44 · 3: 95 · 4: 114 · 5: 88 · 6: 132 · 7: 154 links (643 citations, 632 distinct URLs) |
| No truncated URLs | brackets balanced in every href (inline Python in session) | 643 citations, 0 unbalanced |
| Links still open | `python3 tools/check_links.py` | 632 URLs: ok 559 · blocked 61 (403/429, bot protection) · dead 3 · other 6 (307/308 redirects not followed) · error 3 · sum 632. Full list: `coordination/SourcesPage-linkcheck-2026-11-03.txt` |
| Local file paths and casing (GC-SITE-001) | each `src`/`href` to `images/` and `style.css` tested with `[ -f ]` | 9 of 9 exist |
| No private files | `git ls-files \| grep -iE '\.pdf$\|\.zip$\|16X20\|fbn\|affidavit\|tax\|identity'` | no output (19 files tracked) |
| Whitespace | `git diff --cached --check` before commit | clean |
| Phone layout (GC-SITE-004) | browser at 375 × 812: `document.documentElement.scrollWidth` | 375 (no sideways scroll) |
| Visual check | screenshots at 1280 × 800 and 375 × 812, home + sources | looked at by Claude; owner has not reviewed |

Not run: an HTML validator; a contrast checker (colors chosen for AA: navy `#1e2a4a` on white, teal `#1f6b76` on white; amber is used only behind navy text).

## Specific asks

1. Is each claim in changes 1-6 true for **all seven** books? Flag any that only hold for some.
2. Do the trimmed `about` paragraphs and `specs` lines (change 4) still match the approved descriptions in meaning?
3. R1 and R2: your recommendation for what a public sources page should include.
4. Does `build_sources.py` (change 7) miss or wrongly include links? Spot-check at least one book end to end against its facts file.
5. Anything else a parent, teacher, or veterinarian reading this site would find wrong or misleading.

---

# Round 2 — fixes for review `382eefc`

Range: `git diff 9476727 c0bde6f`. The commits between them, `0e96df8` (this request) and `382eefc` (your review), touch only `coordination/`. Changed in `c0bde6f`: `A coordination/SourcesPage-linkcheck-2026-11-04.txt`, `M index.html`, `M sources.html`, `M style.css`, `M tools/build_sources.py` (`git diff --name-status 9476727 c0bde6f` minus coordination files).

## Dispositions

- **P2.1 fixed.** The heading filter is gone (`tools/build_sources.py:44-47` explains why); every section is read and non-fact links are removed by host only (`SKIP_HOST`). Effect measured by loading the script and running `collect()` with and without the filter: Book 2 44 → 45 (adds only `https://doi.org/10.1007/s00359-006-0093-x`); Books 1, 3, 4, 5, 6, 7 unchanged (16, 95, 114, 88, 132, 154). `grep -c 00359-006-0093 sources.html` → 1.
- **P2.2 fixed.** `index.html:58` now reads: "Each picture is printed on one side, with a blank back. Using markers? Slip a sheet of scrap paper behind the page."
- **P2.3 fixed.** `--check` exits 1 on a mismatch (`tools/build_sources.py:253`). Proof, without touching the real page: copied the script and `sources.html` to a scratch folder; fresh copy `--check` → exit 0; after changing "Book 2: Small Pet Friends" to "Book 2: STALE" in the copy → exit 1 with "sources.html is out of date…". Real `sources.html` SHA-256 prefix `3cb343cb59dce882` before and after. In the real tree, between the P2.1 edit and the rebuild, `--check` also returned exit 1; after the rebuild, exit 0.
- **P3.1 fixed (annotate, no substitution).** The three 404 URLs stay listed with "(page no longer online, checked November 3, 2026)" (`tools/build_sources.py:110-115`, styled `style.css:255`). The script exits if that list names a URL no facts file cites (`:239-241`), so the note can't go stale silently. Archive or replacement URLs are left to the owner. In the browser, the note shows on Book 2's Wayne State rat guide and on Book 4's Bearded Dragons World and BGSU care-sheet links.
- **R1 (recommended) applied.** New paragraph `sources.html:35`: the lists include background research, some pages cover facts not in the final book, and listing a site is not an endorsement. The intro line at `:34` now says "the pages we read while checking the facts".
- **R2:** kept every consulted source, per your answer.
- **Packet wording (answer 2):** accepted. Book 5's paragraph also trims clauses and changes punctuation, not only whole sentences. No wording change made.

## Gates (at `c0bde6f`)

| Check | Result |
|---|---|
| `python3 tools/build_sources.py --check` | `up to date`, exit 0 |
| Per-book counts | 16 · 45 · 95 · 114 · 88 · 132 · 154 (644 citations) |
| `python3 tools/check_links.py` → `coordination/SourcesPage-linkcheck-2026-11-04.txt` | 633 distinct URLs: ok 554 · blocked 66 · dead 3 · other 6 · error 4 · sum 633. The new DOI is in none of the failure buckets. ok/blocked moved from 559/61 on 2026-11-03: the same sites answer 403/429 differently from run to run (bot protection), and the dead set is the same 3 URLs. |
| `git diff --cached --check` before commit | clean |

## Asks

Fixes-first per the checklist: confirm each disposition, and flag any regression these fixes introduced.
