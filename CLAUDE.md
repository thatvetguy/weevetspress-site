# weevetspress-site: Claude Code Guide

The public website for **Wee Vets Press**, the imprint that publishes the *Wee Vets Coloring Adventures* books on Amazon KDP. Wee Vets Press is owned by **Small Animal Surgeries Inc.** (SASI). Book credit line: "Created by the Wee Vets Press team."

The owner talks in plain language. Follow the response style in the owner's global `~/.claude/CLAUDE.md`.

## Where the book content lives

Everything about the books is in the ColoringBooks project: `~/Developer/Codex/ColoringBooks/`. **Open sessions here with that folder added as a second working directory** so Claude can read it.

- **Book list, titles, status, ASINs, Amazon links, ISBNs:** read `PROJECT_STATE.md` there (its "Books" table) every time. Statuses change often. Never copy a status into this repo's docs; put it on the site only after checking it that day.
- **Cover images for the site:** `output/print/*-front-cover-for-listings-vNN.jpg`. Use the newest approved version named in `PROJECT_STATE.md`, not just the highest number.
- **Sources page:** each book's facts file in `planning/` keeps a source for every fact (owner decision, October 23, 2026: sources are never printed in the books; the website lists them). Use the facts version `PROJECT_STATE.md` names for each book; older versions are superseded.
- **Never edit anything in the ColoringBooks project from a website session.** Read only. Claude Code leads that project in its own sessions.

## What's in this repo

- `index.html`: home page (hero shelf of all seven covers, what's inside, one entry per book, about). Books 1–6 link to Amazon (links from the owner, November 3, 2026). Book 7 shows "Coming soon" until it is live.
- `sources.html`: built by `python3 tools/build_sources.py` from the facts files. Never hand-edit the part between the `SOURCES:START` and `SOURCES:END` markers. `--check` reports whether it is up to date. When a facts file gets a new version, update `BOOKS` in the script and rebuild.
- `images/covers/`: 720 px wide copies of each book's listing JPG. `images/wee-vets-press-logo.png`: the logo cut from Book 7's cover (concept 02 of the ColoringBooks logo set).
- Fonts: Young Serif (headings) and Noto Sans (body, the same family as the book interiors), from Google Fonts.
- Preview locally: `python3 -m http.server 8731 --bind 127.0.0.1` in this folder, then open http://127.0.0.1:8731/.

## Private files: never copy them

The ColoringBooks root holds the owner's private business records (every PDF and the JPG in that folder's top level; its own `CLAUDE.md` names them). **Never copy, read, or link any of them into this repo.** This repo will be public. Copy only the specific listing JPGs and text the site needs, file by file.

## Domains

Owned: `weevetspress.com`, `weevets.com`, `weevetpress.com`, `weevet.com`. Credentials are kept outside every project.

- `weevetspress.com` is the main address (owner, November 4, 2026). All four domains are registered at Cloudflare and use Cloudflare DNS, in the account the owner signs in to.
- weevetspress.com: GitHub Pages records, proxy **on** (orange cloud). Four A records (185.199.108–111.153), four AAAA (2606:50c0:8000–8003::153), `www` CNAME to `thatvetguy.github.io`. SSL/TLS mode pinned to **Full** (not Automatic, not Full Strict, not Flexible), and "Always Use HTTPS" is on. The lock icon is Cloudflare's certificate.
- Why proxied: on November 4, 2026, GitHub's certificate request sat at "new" for over two hours, even after removing and re-adding the domain, while its health check said the domain was eligible. So Cloudflare serves HTTPS instead. GitHub's "Enforce HTTPS" stays off; turning it on is unnecessary here and won't work while the proxy is on. Never switch the mode to Flexible.
- weevets.com, weevetpress.com, weevet.com: two placeholder AAAA records (`@` and `www` to `100::`), proxy **on**, plus one Redirect Rule each ("Forward to weevetspress.com": all requests, 301 to `concat("https://weevetspress.com", http.request.uri.path)`, query string kept).

## Hosting

GitHub Pages under the `thatvetguy` account (repo `thatvetguy/weevetspress-site`, public), built from `main`, root folder, like the other SASI sites. The `CNAME` file holds the custom domain; GitHub created it, so never delete it. Static HTML and CSS unless the site grows enough to need a build step.

Relevant gotchas in `~/Developer/SASI_Projects/Gotchas_CrossApp.md`:
- **GC-SITE-001:** GitHub Pages is case-sensitive. Match file-name casing exactly in HTML and CSS.
- **GC-SITE-004:** test desktop, tablet, and phone widths.
- **GC-SITE-006:** if a domain is moved to Cloudflare, its "Domain is locked" message can lag for hours.

## Content rules

- Audience: parents, caregivers, teachers, and vet professionals buying for kids ages 3–6. Warm, simple, trustworthy.
- Book facts and sources are educational content. Use the multi-AI review cadence before they go live (`~/Developer/SASI_Projects/MultiAI_Workflow_Convention.md`). The owner is the final reviewer for every fact.
- No medical advice: the site describes the books; it does not tell anyone how to treat an animal.
- Public publisher name is "Small Animal Surgeries Inc" (GC-BRND-007). Never "The True Blue Group."
- No personal contact details. Public contact: `support@smallanimalsurgeries.com` unless the owner sets up a Wee Vets Press address.
- Design taste: "editorial minimalist", a serif and sans pairing, one subtle depth element, gentle hover motion. Not flat or sparse.

## Hard stops (need the owner's explicit yes, every time)

Creating the GitHub repo, pushing, turning on GitHub Pages, changing DNS or domain settings, adding analytics or any third-party script, and anything that sends email.

## Verification

Before saying a page works: open it in a browser at desktop and phone widths and look at it. Check every Amazon link opens the right book. Counts and "all books" claims come from a command, not memory.
