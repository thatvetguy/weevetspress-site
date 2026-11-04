#!/usr/bin/env python3
"""Build sources.html from the ColoringBooks facts files.

Reads each book's current facts file (read only), pulls out every source link,
drops duplicates and non-fact links (KDP help, copyright office), groups the
links by website, and writes the list into sources.html between the
SOURCES:START and SOURCES:END markers.

Run from the repo root:   python3 tools/build_sources.py
Check only (no write):    python3 tools/build_sources.py --check

When a book's facts file gets a new version, update BOOKS below.
"""
import html
import re
import sys
from pathlib import Path
from urllib.parse import urlparse, unquote

PLANNING = Path.home() / "Developer/Codex/ColoringBooks/planning"
SITE = Path(__file__).resolve().parent.parent
PAGE = SITE / "sources.html"

# Current facts files, as PROJECT_STATE.md names them (checked 2026-11-03).
# Book 1 has no separate facts file: its facts table lives in the text draft,
# in the section "Paws and Learn facts and sources".
BOOKS = [
    (1, "My Pet's Trip to the Vet", "book1-my-pets-trip-to-the-vet.jpg",
     [("first-book-text-draft-v03.md", "Paws and Learn facts and sources")]),
    (2, "Small Pet Friends", "book2-small-pet-friends.jpg",
     [("second-book-facts-v02.md", None)]),
    (3, "Snakes from Head to Tail", "book3-snakes-from-head-to-tail.jpg",
     [("third-book-facts-v05.md", None)]),
    (4, "Lizard Scales and Tales", "book4-lizard-scales-and-tales.jpg",
     [("fourth-book-facts-v09.md", None), ("fourth-book-facts-basics-draft-v02.md", None)]),
    (5, "Tiny Turtles to Giant Tortoises", "book5-tiny-turtles-to-giant-tortoises.jpg",
     [("fifth-book-facts-v02.md", None)]),
    (6, "Feathers, Beaks, and Tweets", "book6-feathers-beaks-and-tweets.jpg",
     [("sixth-book-facts-v06.md", None)]),
    (7, "From Ponds to Ocean Blue", "book7-from-ponds-to-ocean-blue.jpg",
     [("seventh-book-facts-v02.md", None)]),
]

# Every section of a facts file is read. An earlier heading filter ("review",
# "question", ...) dropped a real fact source: Book 2's "October 16, 2026 changes
# (owner review of preview v01)" sources the page 81 caption (Codex review P2.1).
# Non-fact links are removed by host instead (SKIP_HOST).

# Links that are about publishing, not about animals.
SKIP_HOST = ("kdp.amazon.com", "amazon.com", "copyright.gov", "bowker.com", "myidentifiers.com")

SITE_NAMES = {
    "merckvetmanual.com": "Merck Veterinary Manual",
    "animaldiversity.org": "Animal Diversity Web (University of Michigan)",
    "vcahospitals.com": "VCA Animal Hospitals",
    "rspca.org.uk": "RSPCA",
    "lafeber.com": "LafeberVet",
    "floridamuseum.ufl.edu": "Florida Museum of Natural History",
    "nps.gov": "U.S. National Park Service",
    "home.nps.gov": "U.S. National Park Service",
    "cdc.gov": "U.S. Centers for Disease Control and Prevention",
    "archive.cdc.gov": "U.S. Centers for Disease Control and Prevention",
    "fws.gov": "U.S. Fish and Wildlife Service",
    "pmc.ncbi.nlm.nih.gov": "PubMed Central (U.S. National Library of Medicine)",
    "pubmed.ncbi.nlm.nih.gov": "PubMed (U.S. National Library of Medicine)",
    "fisheries.noaa.gov": "NOAA Fisheries",
    "oceanservice.noaa.gov": "NOAA Ocean Service",
    "oceanexplorer.noaa.gov": "NOAA Ocean Exploration",
    "nationalzoo.si.edu": "Smithsonian's National Zoo",
    "doi.org": "Research papers",
    "fishbase.se": "FishBase",
    "animals.sandiegozoo.org": "San Diego Zoo Wildlife Alliance",
    "allaboutbirds.org": "Cornell Lab of Ornithology: All About Birds",
    "academy.allaboutbirds.org": "Cornell Lab of Ornithology: All About Birds",
    "mdc.mo.gov": "Missouri Department of Conservation",
    "myfwc.com": "Florida Fish and Wildlife Conservation Commission",
    "australian.museum": "Australian Museum",
    "petmd.com": "PetMD",
    "audubon.org": "National Audubon Society",
    "ask.ifas.ufl.edu": "University of Florida IFAS Extension",
    "blogs.ifas.ufl.edu": "University of Florida IFAS Extension",
    "nationalgeographic.com": "National Geographic",
    "seaworld.org": "SeaWorld Parks and Entertainment",
    "rabbit.org": "House Rabbit Society",
    "pdsa.org.uk": "PDSA",
    "aspca.org": "ASPCA",
    "akc.org": "American Kennel Club",
    "en.wikivet.net": "WikiVet",
    "en.wikipedia.org": "Wikipedia",
    "britannica.com": "Britannica",
    "kids.britannica.com": "Britannica Kids",
    "nas.er.usgs.gov": "U.S. Geological Survey",
    "usgs.gov": "U.S. Geological Survey",
    "umesc.usgs.gov": "U.S. Geological Survey",
    "fda.gov": "U.S. Food and Drug Administration",
    "my.clevelandclinic.org": "Cleveland Clinic",
    "healthychildren.org": "American Academy of Pediatrics: HealthyChildren.org",
    "georgiaaquarium.org": "Georgia Aquarium",
    "iucn.org": "IUCN",
    "amnh.org": "American Museum of Natural History",
}

# A URL may hold balanced parentheses, as DOIs and some PDF names do:
# "...(2001-2005)/Mitrus_2001.pdf". Stop at an unbalanced ")" (the markdown close).
_URL = r"https?://(?:[^\s()<>|`\"*]|\([^\s()<>|`\"*]*\))+"
# Links that returned 404 in tools/check_links.py (report:
# coordination/SourcesPage-linkcheck-2026-11-03.txt). They stay listed, because
# they were consulted, with a note. Remove a URL here once the owner approves a
# replacement in the facts file, or once it works again.
UNAVAILABLE = {
    "https://beardeddragonsworld.com/brumation-winter-sleep/",
    "https://research.wayne.edu/dlar/pdf/rat.pdf",
    "https://www.bgsu.edu/content/dam/BGSU/college-of-arts-and-sciences/biological-sciences/Herpetarium-documents/Lizards/new-caledonian-crested-gecko-bgsu-herpetarium.pdf",
}
UNAVAILABLE_NOTE = " (page no longer online, checked November 3, 2026)"

LINK = re.compile(r"\[([^\]]+)\]\((" + _URL + r")\)|(" + _URL + r")")


def sections(text, only=None):
    """Yield (heading, body) for each level-2 section; with `only`, just that one."""
    parts = re.split(r"^## +(.+)$", text, flags=re.M)
    yield ("(top)", parts[0])
    for i in range(1, len(parts), 2):
        head, body = parts[i].strip(), parts[i + 1]
        if only and head != only:
            continue
        yield (head, body)


def host_of(url):
    h = urlparse(url).netloc.lower()
    return h[4:] if h.startswith("www.") else h


def title_from_url(url):
    path = unquote(urlparse(url).path).rstrip("/")
    segs = [x for x in path.split("/") if x and x.lower() not in ("index.html", "index.htm", "index", "default.aspx")]
    slug = segs[-1] if segs else ""
    slug = re.sub(r"\.(html?|aspx|php|pdf)$", "", slug, flags=re.I)
    words = re.sub(r"[-_+]+", " ", slug).strip()
    if len(re.findall(r"[A-Za-z]", words)) < 4 or re.fullmatch(r"[\w ]*\d{4,}[\w ]*", words) and " " not in words:
        return None
    return words[:1].upper() + words[1:]


def clean_url(url):
    return url.rstrip(".,;:")


def collect(book_files):
    found = {}  # url -> label
    for name, only in book_files:
        text = (PLANNING / name).read_text(encoding="utf-8")
        if only and f"## {only}" not in text:
            sys.exit(f"Section '{only}' not found in {name}")
        for head, body in sections(text, only):
            if head == "(top)" and only:
                continue
            for m in LINK.finditer(body):
                label, url = (m.group(1), m.group(2)) if m.group(2) else (None, m.group(3))
                url = clean_url(url)
                if any(host_of(url) == h or host_of(url).endswith("." + h) for h in SKIP_HOST):
                    continue
                if label and (label.startswith("http") or len(label) < 3):
                    label = None
                if url not in found or (label and not found[url]):
                    found[url] = label
    return found


PREFIX = re.compile(r"^([^:]{2,60}):\s+(.+)$")


def split_label(label):
    """'Merck: Diet for Rabbits' -> ('Merck', 'Diet for Rabbits')."""
    m = PREFIX.match(label) if label else None
    return (m.group(1).strip(), m.group(2).strip()) if m else (None, label)


def md_inline(text):
    """Escape, then turn markdown *italic* and **bold** into HTML."""
    t = html.escape(text)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"\*(.+?)\*", r"<em>\1</em>", t)
    return t.replace("*", "")


def render(books):
    out = []
    for num, title, cover, files in books:
        found = collect(files)
        groups = {}
        # For sites not in SITE_NAMES, the most common label prefix names the group.
        prefixes = {}
        for url, label in found.items():
            p = split_label(label)[0]
            if p:
                prefixes.setdefault(host_of(url), []).append(p)
        for url, label in found.items():
            h = host_of(url)
            prefix, rest = split_label(label)
            if h in SITE_NAMES:
                group = SITE_NAMES[h]
            elif h in prefixes:
                group = max(sorted(set(prefixes[h])), key=prefixes[h].count)
            else:
                group = h
            # A bare year or abbreviation says nothing on its own: use the page name instead.
            if not rest or len(rest) < 6 or rest.isdigit() or rest == group:
                rest = title_from_url(url) or label or h
            groups.setdefault(group, []).append((rest, url))
        order = sorted(groups, key=lambda g: (-len(groups[g]), g.lower()))
        out.append(f'<details class="source-book" id="sources-book-{num}">')
        out.append("  <summary>")
        out.append(f'    <img src="images/covers/{cover}" alt="" width="56" height="72" loading="lazy">')
        out.append(f'    <span><span class="t">Book {num}: {html.escape(title)}</span>'
                   f'<span class="n">{len(found)} sources from {len(groups)} websites</span></span>')
        out.append('    <span class="chev" aria-hidden="true">+</span>')
        out.append("  </summary>")
        out.append('  <div class="source-body">')
        for g in order:
            out.append('    <div class="source-group">')
            out.append(f"      <h3>{md_inline(g)}</h3>")
            out.append("      <ul>")
            for label, url in sorted(groups[g], key=lambda x: x[0].lower().lstrip("*")):
                note = f'<span class="gone">{UNAVAILABLE_NOTE}</span>' if url in UNAVAILABLE else ""
                out.append(f'        <li><a href="{html.escape(url, quote=True)}" rel="noopener">{md_inline(label)}</a>{note}</li>')
            out.append("      </ul>")
            out.append("    </div>")
        out.append("  </div>")
        out.append("</details>")
        print(f"Book {num}: {len(found)} links, {len(groups)} sites")
    return "\n".join(out)


def main():
    listed = {u for _, _, _, f in BOOKS for u in collect(f)}
    missing = UNAVAILABLE - listed
    if missing:
        sys.exit(f"UNAVAILABLE names URLs no facts file cites: {sorted(missing)}")
    block = render(BOOKS)
    page = PAGE.read_text(encoding="utf-8")
    start, end = "<!-- SOURCES:START -->", "<!-- SOURCES:END -->"
    if start not in page or end not in page:
        sys.exit("Markers missing from sources.html")
    new = page.split(start)[0] + start + "\n" + block + "\n" + end + page.split(end)[1]
    if "--check" in sys.argv:
        if new == page:
            print("up to date")
            return
        print("sources.html is out of date: run python3 tools/build_sources.py")
        sys.exit(1)
    PAGE.write_text(new, encoding="utf-8")
    print("wrote", PAGE)


if __name__ == "__main__":
    main()
