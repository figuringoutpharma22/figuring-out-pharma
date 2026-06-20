#!/usr/bin/env python3
"""
build.py - Figuring Out Pharma
================================
Run this AFTER you add a new entry to articles.json or case-studies.json,
and BEFORE you git add / commit / push.

It regenerates four files automatically:
  1. sitemap.xml
  2. llms.txt
  3. index.html   - Latest (3), Also Reading (3), In Depth (6),
                    Case Studies grid (6), Featured side cards (see below)
  4. Prints related-article suggestions for Step 6 of the SOP

What stays manual:
  - The Editor's Pick card (feat-main) - you edit index.html by hand
  - The new article's own HTML file
  - The 3 Related Articles cards inside each article's HTML

Featured side cards logic:
  - You have 6 case studies right now -> side cards show 2 fallback articles
  - When you add case study #7 -> side card 1 becomes that case study
  - When you add case study #8 -> side card 2 becomes that case study
  - From #9 onward -> always the 2 most recent case studies beyond the first 6

USAGE
-----
Run from your project root (same folder as articles.json):

    python3 build.py

Needs Python 3. No installs. No internet connection needed.
"""

import json
import re
from datetime import date
from pathlib import Path

# ---------------------------------------------------------------------------
# File paths - all relative to where this script lives
# ---------------------------------------------------------------------------
ROOT              = Path(__file__).resolve().parent
ARTICLES_JSON     = ROOT / "articles.json"
CASE_STUDIES_JSON = ROOT / "case-studies.json"
INDEX_HTML        = ROOT / "index.html"
SITEMAP_XML       = ROOT / "sitemap.xml"
LLMS_TXT          = ROOT / "llms.txt"
SITE              = "https://figuringoutpharma.com"

# ---------------------------------------------------------------------------
# Colour map for case study tags
# ---------------------------------------------------------------------------
TAG_COLOURS = {
    "Tragedy":      ("t-red",    "cc-red"),
    "Regulatory":   ("t-amber",  "cc-amber"),
    "Withdrawal":   ("t-red",    "cc-red"),
    "Breakthrough": ("t-green",  "cc-green"),
    "Patent":       ("t-blue",   "cc-blue"),
    "M&A":          ("t-purple", "cc-purple"),
}
DEFAULT_TAG_COLOUR = ("t-teal", "cc-teal")

# ---------------------------------------------------------------------------
# Fallback articles shown in Featured side cards until you have 7+ case studies
# These are the article slugs currently hardcoded in your index.html side cards
# ---------------------------------------------------------------------------
FEATURED_FALLBACK = [
    {
        "slug":     "articles/how-drugs-are-priced-in-india",
        "category": "Industry",
        "title":    "How drugs are priced in India - the real explanation",
        "excerpt":  "DPCO, trade margins, and what your pharmacoeconomics textbook quietly skipped.",
        "readTime": "5 min",
        "type":     "article",
    },
    {
        "slug":     "articles/fmcg-vs-pharma-marketing",
        "category": "Marketing",
        "title":    "FMCG vs pharma marketing - explained from scratch, no assumptions",
        "excerpt":  "People keep saying pharma is just like FMCG. It is not. Here is the full breakdown.",
        "readTime": "11 min",
        "type":     "article",
    },
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def esc(text):
    """Minimal HTML-escape so titles with & < > don't break the page."""
    return (str(text)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;"))


def short_title(full_title):
    """
    Returns the part of a title before the first em-dash or en-dash.
    Used for the homepage case study cards which have less horizontal space.
    'The Thalidomide Tragedy - and the untold Indian chapter'
    -> 'The Thalidomide Tragedy'
    """
    for sep in [" - ", " - ", " - "]:
        if sep in full_title:
            return full_title.split(sep)[0].strip()
    return full_title


def year_html(year_str):
    """Converts '1957 - 1962' to '1957 &#x2013; 1962' for proper en-dash rendering."""
    return year_str.replace(" - ", " &#x2013; ").replace(" - ", " &#x2013; ")


def replace_block(html, start_marker, end_marker, new_content):
    """
    Replaces everything between start_marker and end_marker (inclusive)
    with start_marker + new_content + end_marker.
    Raises a clear error if the markers are not found.
    """
    pattern = re.compile(
        re.escape(start_marker) + r".*?" + re.escape(end_marker),
        re.DOTALL
    )
    if not pattern.search(html):
        msg = "Marker not found in index.html: " + start_marker + " -- Has the HTML structure changed? Check that both START and END markers are present."
        raise RuntimeError(msg)
    
    replacement = start_marker + "\n" + new_content + "\n" + end_marker
    return pattern.sub(replacement, html, count=1)

# ---------------------------------------------------------------------------
# 1. sitemap.xml
# ---------------------------------------------------------------------------

STATIC_PAGES = [
    ("/",             "weekly",  "1.0"),
    ("/blogs",        "weekly",  "0.9"),
    ("/case-studies", "weekly",  "0.9"),
    ("/categories",   "monthly", "0.7"),
    ("/about",          "monthly", "0.6"),
    ("/privacy-policy", "yearly",  "0.3"),
    ("/terms",          "yearly",  "0.3"),
]


def build_sitemap(articles, case_studies):
    today = date.today().isoformat()
    latest_article_date = articles[0]["date"] if articles else today

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        "<!--",
        "  SITEMAP - Figuring Out Pharma",
        "  AUTO-GENERATED by build.py - do not edit by hand.",
        "  Edit articles.json / case-studies.json and re-run build.py.",
        "-->",
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        "",
        "  <!-- SITE PAGES -->",
    ]

    for path, freq, pri in STATIC_PAGES:
        lines += [
            "  <url>",
          f"    <loc>{SITE}{path}</loc>",
            f"    <lastmod>{latest_article_date}</lastmod>",
            f"    <changefreq>{freq}</changefreq>",
            f"    <priority>{pri}</priority>",
            "  </url>",
            "",
        ]

    lines.append("  <!-- ARTICLES -->")
    for a in articles:
        lines += [
            "  <url>",
            f"    <loc>{SITE}/{a['slug']}</loc>",
            f"    <lastmod>{a['date']}</lastmod>",
            "    <changefreq>monthly</changefreq>",
            "    <priority>0.8</priority>",
            "  </url>",
            "",
        ]

    lines.append("  <!-- CASE STUDIES -->")
    for cs in case_studies:
        lastmod = cs.get("date", latest_article_date)
        lines += [
            "  <url>",
            f"    <loc>{SITE}/{cs['slug']}</loc>",
            f"    <lastmod>{lastmod}</lastmod>",
            "    <changefreq>monthly</changefreq>",
            "    <priority>0.8</priority>",
            "  </url>",
            "",
        ]

    lines.append("</urlset>")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 2. llms.txt
# ---------------------------------------------------------------------------

def build_llms(articles, case_studies):
    lines = [
        "# Figuring Out Pharma",
        "> A pharma editorial blog written for B.Pharma students and freshers in India "
        "who want to understand how the pharmaceutical industry actually works - "
        "not how textbooks say it does.",
        "",
        "The site covers pharma marketing, drug pricing, brand strategy, regulatory affairs, "
        "careers, and industry history. All content is written in plain language with no "
        "assumed prior knowledge. Published by a final-year B.Pharma student based in Mumbai.",
        "",
        f"URL: {SITE}",
        "",
        "---",
        "",
        "## Articles",
        "",
    ]

    for a in reversed(articles):   # oldest first, consistent with current llms.txt
        lines.append(f"### {a['title']}")
        lines.append(f"URL: {SITE}/{a['slug']}")
        if a.get("llmsTopic"):
            lines.append(f"Topic: {a['llmsTopic']}")
        if a.get("llmsSummary"):
            lines.append(f"Summary: {a['llmsSummary']}")
        lines.append("")

    lines += [
        "---",
        "",
        "## Case Studies",
        "",
    ]

    for cs in reversed(case_studies):   # oldest first
        lines.append(f"### {cs['title']}")
        lines.append(f"URL: {SITE}/{cs['slug']}")
        if cs.get("llmsTopic"):
            lines.append(f"Topic: {cs['llmsTopic']}")
        if cs.get("llmsSummary"):
            lines.append(f"Summary: {cs['llmsSummary']}")
        lines.append("")

    lines += [
        "---",
        "",
        "## Site Information",
        "",
        "Published: June 2026",
        "Author: Figuring Out Pharma (B.Pharma student, Mumbai, India)",
        "Primary audience: B.Pharma students and freshers entering the Indian pharmaceutical industry",
        "Content types: Long-form articles (5-12 min read), pharma case studies (10-11 min read)",
        "Topics covered: Pharma marketing, drug pricing, brand strategy, regulatory affairs, "
        "pharma careers, industry history, global case studies",
        "Contact: contact@figuringoutpharma.com",
    ]

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 3. index.html section renderers
# ---------------------------------------------------------------------------

# Each section is wrapped in a pair of HTML comment markers.
# The script finds the START marker, finds the END marker, and replaces
# everything in between with freshly generated HTML.

MARKERS = {
    "ALSO_READING":  ("<!-- AUTO:ALSO-READING:START -->",  "<!-- AUTO:ALSO-READING:END -->"),
    "LATEST":        ("<!-- AUTO:LATEST:START -->",         "<!-- AUTO:LATEST:END -->"),
    "IN_DEPTH":      ("<!-- AUTO:IN-DEPTH:START -->",       "<!-- AUTO:IN-DEPTH:END -->"),
    "CASE_STUDIES":  ("<!-- AUTO:CASE-STUDIES:START -->",   "<!-- AUTO:CASE-STUDIES:END -->"),
    "FEAT_SIDE":     ("<!-- AUTO:FEAT-SIDE:START -->",      "<!-- AUTO:FEAT-SIDE:END -->"),
}

EXCERPT_STYLE = (
    "font-family:var(--body);font-size:0.83rem;font-weight:300;"
    "color:var(--text2);line-height:1.72;font-style:italic;"
    "margin-bottom:0.75rem;margin-top:0.5rem"
)


def render_latest_card(a):
    return (
        f'      <a class="art-card" href="{a["slug"]}">\n'
        f'        <div class="art-cat">{esc(a["category"])}</div>\n'
        f'        <div class="art-title">{esc(a["title"])}</div>\n'
        f'        <p class="art-excerpt" style="{EXCERPT_STYLE}">{esc(a["excerpt"])}</p>\n'
        f'        <div class="art-meta"><span class="art-min">{esc(a["readTime"])}</span></div>\n'
        f'      </a>'
    )


def render_in_depth_card(a, num):
    return (
        f'    <a class="scroll-card" href="{a["slug"]}">\n'
        f'      <div class="scroll-num">{num:02d}</div>\n'
        f'      <div class="art-cat">{esc(a["category"])}</div>\n'
        f'      <div class="art-title" style="font-size:0.9rem">{esc(a["title"])}</div>\n'
        f'      <div class="art-meta" style="margin-top:0.75rem">'
        f'<span class="art-min">{esc(a["readTime"])}</span></div>\n'
        f'    </a>'
    )


def render_also_reading_item(a, num):
    return (
        f'      <a class="hs-item" href="{a["slug"]}">\n'
        f'        <div class="hs-num">{num:02d}</div>\n'
        f'        <div class="hs-cat">{esc(a["category"])}</div>\n'
        f'        <div class="hs-title">{esc(a["title"])}</div>\n'
        f'        <div class="hs-time">{esc(a["readTime"])} read</div>\n'
        f'      </a>'
    )


def render_case_grid_card(cs):
    tag_class, card_class = TAG_COLOURS.get(cs["tag"], DEFAULT_TAG_COLOUR)
    return (
        f'      <a class="case-card {card_class}" href="{cs["slug"]}">\n'
        f'        <div class="cs-tag {tag_class}">{esc(cs["tag"])}</div>\n'
        f'        <div class="cs-year">{year_html(cs["year"])}</div>\n'
        f'        <div class="cs-title">{esc(short_title(cs["title"]))}</div>\n'
        f'        <p class="cs-sum">{esc(cs["excerpt"])}</p>\n'
        f'        <span class="cs-read">Read case study &#x2192;</span>\n'
        f'      </a>'
    )


def render_feat_side_article(item):
    return (
        f'        <a class="side-art" href="{item["slug"]}">\n'
        f'          <div class="art-cat">{esc(item["category"])}</div>\n'
        f'          <div class="art-title">{esc(item["title"])}</div>\n'
        f'          <p class="art-excerpt">{esc(item["excerpt"])}</p>\n'
        f'          <div class="art-meta" style="margin-top:auto;padding-top:0.75rem">'
        f'<span class="art-min">{esc(item["readTime"])}</span></div>\n'
        f'        </a>'
    )


def render_feat_side_case_study(cs):
    tag_class, _ = TAG_COLOURS.get(cs["tag"], DEFAULT_TAG_COLOUR)
    return (
        f'        <a class="side-art" href="{cs["slug"]}">\n'
        f'          <div class="art-cat" style="display:flex;gap:6px;align-items:center">'
        f'<span class="cs-tag {tag_class}" style="margin:0">{esc(cs["tag"])}</span>'
        f'<span>{year_html(cs["year"])}</span></div>\n'
        f'          <div class="art-title">{esc(short_title(cs["title"]))}</div>\n'
        f'          <p class="art-excerpt">{esc(cs["excerpt"])}</p>\n'
        f'          <div class="art-meta" style="margin-top:auto;padding-top:0.75rem">'
        f'<span class="art-min">{esc(cs["readTime"])}</span></div>\n'
        f'        </a>'
    )


def compute_feat_side_cards(case_studies):
    """
    Returns a list of exactly 2 items to render as Featured side cards.

    Rule:
      - case studies 1-6  -> grid only, side cards use fallback articles
      - case study 7      -> side card 1; side card 2 still fallback article
      - case study 8      -> side card 1; side card 2 is the 8th case study
      - case study 9+     -> always the 2 most recent beyond the first 6
        (i.e. index 6 and index 7 in the list, 0-based)

    case_studies is the full list in JSON order (newest first = index 0).
    The "grid 6" are index 0-5. Beyond the grid starts at index 6.
    """
    beyond_grid = case_studies[6:]   # empty if <= 6 case studies

    side_items = []

    if len(beyond_grid) == 0:
        # Fewer than 7 case studies - both side cards are fallback articles
        side_items = [
            {"render": "article", "data": FEATURED_FALLBACK[0]},
            {"render": "article", "data": FEATURED_FALLBACK[1]},
        ]
    elif len(beyond_grid) == 1:
        # Exactly 7 case studies - side card 1 = newest beyond grid, side 2 = fallback
        side_items = [
            {"render": "case_study", "data": beyond_grid[0]},
            {"render": "article",    "data": FEATURED_FALLBACK[1]},
        ]
    else:
        # 8+ case studies - both side cards are the 2 most recent beyond grid
        side_items = [
            {"render": "case_study", "data": beyond_grid[0]},
            {"render": "case_study", "data": beyond_grid[1]},
        ]

    return side_items


def render_feat_side_block(case_studies):
    side_items = compute_feat_side_cards(case_studies)
    cards = []
    for item in side_items:
        if item["render"] == "article":
            cards.append(render_feat_side_article(item["data"]))
        else:
            cards.append(render_feat_side_case_study(item["data"]))
    return "\n".join(cards)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    # Load JSON
    articles      = load_json(ARTICLES_JSON)
    case_studies  = load_json(CASE_STUDIES_JSON)

    # Sort articles newest-first by date
    articles_by_date = sorted(articles, key=lambda a: a["date"], reverse=True)

    # ------------------------------------------------------------------
    # 1. sitemap.xml
    # ------------------------------------------------------------------
    sitemap = build_sitemap(articles_by_date, case_studies)
    SITEMAP_XML.write_text(sitemap, encoding="utf-8")
    print(f"[OK] sitemap.xml  - {len(articles)} articles + {len(case_studies)} case studies")

    # ------------------------------------------------------------------
    # 2. llms.txt
    # ------------------------------------------------------------------
    # Check for entries that have no llmsSummary yet - warn but don't fail
    missing_summary = [
        a["title"] for a in articles if not a.get("llmsSummary")
    ] + [
        cs["title"] for cs in case_studies if not cs.get("llmsSummary")
    ]

    llms = build_llms(articles_by_date, case_studies)
    LLMS_TXT.write_text(llms, encoding="utf-8")
    print(f"[OK] llms.txt     - {len(articles)} articles + {len(case_studies)} case studies")

    if missing_summary:
        print()
        print("  NOTE: These entries are missing 'llmsSummary' in their JSON.")
        print("  They appear in llms.txt without a Summary line.")
        print("  Add 'llmsSummary' and 'llmsTopic' to each JSON entry when you have time:")
        for t in missing_summary:
            print(f"    - {t}")

    # ------------------------------------------------------------------
    # 3. index.html
    # ------------------------------------------------------------------
    html = INDEX_HTML.read_text(encoding="utf-8")

    # Latest - top 3 articles by date
    latest = articles_by_date[:3]
    latest_html = "\n".join(render_latest_card(a) for a in latest)
    html = replace_block(html, *MARKERS["LATEST"], latest_html)

    # Also Reading - articles ranked 4th-6th by date
    also = articles_by_date[3:6]
    also_html = "\n".join(render_also_reading_item(a, i + 1) for i, a in enumerate(also))
    html = replace_block(html, *MARKERS["ALSO_READING"], also_html)

    # In Depth - top 6 articles by date
    in_depth = articles_by_date[:6]
    indepth_html = "\n".join(render_in_depth_card(a, i + 1) for i, a in enumerate(in_depth))
    html = replace_block(html, *MARKERS["IN_DEPTH"], indepth_html)

    # Case Studies grid - first 6 from case-studies.json
    cs_grid = case_studies[:6]
    cs_html = "\n".join(render_case_grid_card(cs) for cs in cs_grid)
    html = replace_block(html, *MARKERS["CASE_STUDIES"], cs_html)

    # Featured side cards - auto based on case study count
    feat_side_html = render_feat_side_block(case_studies)
    html = replace_block(html, *MARKERS["FEAT_SIDE"], feat_side_html)

    INDEX_HTML.write_text(html, encoding="utf-8")
    print(f"[OK] index.html   - Latest, Also Reading, In Depth, Case Studies, Featured side cards")

    # ------------------------------------------------------------------
    # 4. Editor's Pick reminder
    # ------------------------------------------------------------------
    featured = [a for a in articles if a.get("featured")]
    print()
    if not featured:
        print("REMINDER: No article has \"featured\": true in articles.json.")
        print("  The Editor's Pick card in index.html was NOT changed - edit it by hand.")
    elif len(featured) > 1:
        print(f"WARNING: {len(featured)} articles have \"featured\": true - only one should.")
        for a in featured:
            print(f"  - {a['title']}")
    else:
        print(f"REMINDER: Editor's Pick is currently: \"{featured[0]['title']}\"")
        print("  If this has changed, edit the feat-main card in index.html by hand.")

    # ------------------------------------------------------------------
    # 5. Featured side card status
    # ------------------------------------------------------------------
    beyond = case_studies[6:]
    print()
    if len(beyond) == 0:
        print("Featured side cards: showing 2 fallback ARTICLES (you have " + str(len(case_studies)) + "/6 case studies in the grid)")
        print(f"  - Add case study #7 to trigger auto-rotation")
    elif len(beyond) == 1:
        print("Featured side cards: side 1 = case study #" + str(len(case_studies)) + " | side 2 = fallback article")
    else:
        print("Featured side cards: both auto-rotated from case studies #7 and #8 (beyond grid)")

    # ------------------------------------------------------------------
    # 6. Related-article suggestions for the newest piece
    # ------------------------------------------------------------------
    newest = articles_by_date[0]
    same_cat  = [a for a in articles_by_date[1:] if a["category"] == newest["category"]]
    other_cat = [a for a in articles_by_date[1:] if a["category"] != newest["category"]]

    print()
    print(f'Related-article suggestions for: "{newest["title"]}"')
    print("  Pick 3 for the Related Articles section of the new article page.")
    print("  At least 1 same-category, at least 1 different-category:")
    print("  Same category:")
    for a in same_cat[:3]:
        print(f"    {a['slug']}")
        print(f"    \"{a['title']}\"")
    if not same_cat:
        print("    (none - this is the only article in this category so far)")
    print("  Different category:")
    for a in other_cat[:3]:
        print(f"    {a['slug']}")
        print(f"    \"{a['title']}\"")

    print()
    print("Step 6B - existing articles that may now link back to the new one:")
    for a in (same_cat[:2] + other_cat[:1]):
        print(f"  Open: {a['slug']}")
        print(f"  Check its Related Articles section for a '#' placeholder to replace")

    print()
    print("Done. Review the changes in GitHub Desktop, then commit and push.")


if __name__ == "__main__":
    main()
