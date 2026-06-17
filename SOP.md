# Figuring Out Pharma — Master Publishing SOP

> Open this file every time you publish. Follow every step in order.
> Never skip a step. Never publish without completing the full checklist.
> This document is the single source of truth for the entire publishing workflow.

---

## SITE ARCHITECTURE — READ THIS FIRST

Understanding how the site is built is essential before touching any file.

**Tech stack:** Pure HTML, CSS, and vanilla JavaScript. No frameworks, no CMS. Hosted on Cloudflare Pages. Auto-deploys whenever you push via GitHub Desktop.

**The two JSON files are the source of truth for everything:**
- `articles.json` — every article. The homepage, blogs.html, categories.html, llms.txt, and sitemap.xml all read from this.
- `case-studies.json` — every case study. The homepage Case Studies grid, case-studies.html, llms.txt, and sitemap.xml all read from this.

**`build.py` is the automation script.** After you update either JSON file, you run `python3 build.py` and it regenerates: `sitemap.xml`, `llms.txt`, and five sections of `index.html` automatically. You never edit those files by hand.

**URL structure:** All article and case study pages live at `/articles/slug` (no `.html` at the end — Cloudflare strips it). Internal links throughout the site use clean paths: `articles/how-drugs-are-priced-in-india` not `articles/how-drugs-are-priced-in-india.html`.

**What is automatic vs manual:**

| File / Section | How it updates |
|---|---|
| sitemap.xml | Automatic — build.py |
| llms.txt | Automatic — build.py |
| index.html Latest (3 cards) | Automatic — build.py |
| index.html Also Reading (sidebar) | Automatic — build.py |
| index.html In Depth strip (6 cards) | Automatic — build.py |
| index.html Case Studies grid (6 cards) | Automatic — build.py |
| index.html Featured side cards | Automatic — build.py (see Featured rotation logic below) |
| index.html Editor's Pick card | Manual — you edit index.html by hand |
| blogs.html article grid | Automatic — driven by articles.json at runtime via JS |
| case-studies.html card grid | Automatic — driven by case-studies.json at runtime via JS |
| categories.html article counts | Automatic — driven by articles.json at runtime via JS |
| New article HTML file | Manual — you build it from the template |
| Related Articles inside each article | Manual — you pick 3 (build.py suggests them) |

---

## FEATURED SIDE CARD ROTATION LOGIC

The Featured section has 3 cards: one large Editor's Pick (always manual) and 2 smaller side cards (auto-managed by build.py).

The script counts how many case studies exist in `case-studies.json` and decides what the side cards show:

| Case study count | Side card 1 | Side card 2 |
|---|---|---|
| 1–6 | Fallback article (drug pricing) | Fallback article (FMCG) |
| 7 | Entry #7 from case-studies.json | Fallback article (FMCG) |
| 8 | Entry #7 from case-studies.json | Entry #8 from case-studies.json |
| 9+ | 2nd most recent beyond grid (index 7) | Most recent beyond grid (index 6) |

The Case Studies homepage grid always shows the first 6 entries in `case-studies.json`. New case studies go at the top of `case-studies.json`, so the newest ones appear in the side cards first once you pass 6.

---

## THE VARIABLES YOU NEED BEFORE STARTING

### For a new article — 9 variables

```
TITLE:         e.g. How drug advertising works in India — and why it is so restricted
               Sentence case. Use an em dash (—) if adding a subtitle.
SLUG:          e.g. how-drug-advertising-works-in-india
               Lowercase, hyphens only, no spaces, no special characters, 4–6 words max.
CATEGORY:      Marketing / Careers / Industry / Brand Strategy / Digital / Regulatory
EXCERPT:       One sentence. Max 160 characters. Used on the homepage, blogs.html, and in JSON.
DATE:          Today's date in YYYY-MM-DD format e.g. 2026-07-01
READ TIME:     e.g. 8 min
IMAGE FILE:    e.g. drug-advertising-india-cover.jpg  (saved to: images/filename.jpg)
LLMS TOPIC:    Comma-separated keywords for llms.txt e.g. "drug advertising, UCPMP, Rx promotion, India"
LLMS SUMMARY:  2–3 sentences for llms.txt. Same detail level as existing entries. Explains
               what the article covers and the specific insights it provides.
```

### For a new case study — 11 variables

```
TITLE:         e.g. The Opioid Crisis — how OxyContin destroyed trust in pharma
               Full title including subtitle after the em dash.
SLUG:          e.g. opioid-crisis-oxycontin
TAG:           Tragedy / Regulatory / Withdrawal / Breakthrough / Patent / M&A
TAG COLOUR:    t-red (Tragedy) / t-amber (Regulatory) / t-red (Withdrawal) /
               t-green (Breakthrough) / t-blue (Patent) / t-purple (M&A)
CARD COLOUR:   cc-red / cc-amber / cc-red / cc-green / cc-blue / cc-purple
               (matches the tag — see table in reference section below)
YEAR:          e.g. 1996 – 2007  or a single year e.g. 2004
               Use a hyphen with spaces in the JSON: "1996 - 2007"
               The script converts this to an en dash on the page automatically.
EXCERPT:       One sentence for cards. Max 160 characters.
DATE:          Today's date in YYYY-MM-DD format
READ TIME:     e.g. 10 min
IMAGE FILE:    e.g. opioid-crisis-cover.jpg  (saved to: images/filename.jpg)
LLMS TOPIC:    Comma-separated keywords
LLMS SUMMARY:  2–3 sentences for llms.txt
```

---

## STEP 1 — GENERATE THE COVER IMAGE

### Preferred tools (in order)

1. **Ideogram.ai** — best results for the flat editorial illustration style. Free tier, no watermark.
2. **Microsoft Designer** (designer.microsoft.com) — completely free with any Microsoft account. Outputs PNG — convert to JPG after downloading.
3. **Adobe Firefly** (firefly.adobe.com) — free tier with Adobe account.

### Master cover image prompt

```
Flat line illustration. [ONE LINE DESCRIBING THE VISUAL CONCEPT — make it a metaphor,
not a literal depiction. e.g. "a medicine bottle connected to a dollar sign by a tangled
wire" or "a magnifying glass over a document with a warning triangle"].
Forest green (#1a3a2a) lines and shapes on a cream or white (#faf8f2) background.
Minimal, editorial magazine style. No text. No gradients. No drop shadows.
No photorealistic elements. Clean geometric shapes only.
```

**Prompt tips:**
- Think objects, scales, charts, arrows, buildings, people as simple shapes
- If the first result is too complex, add: "Even more minimal. Fewer elements."
- If it looks too digital or tech, add: "Inspired by 1970s editorial print illustration."

### Rules for every cover image

- Canvas size: **1200 × 675px** (16:9). If the tool outputs a different size, crop to this.
- If the output is PNG, convert to JPG before saving.
- No text in the image. No photorealistic elements.
- Save as JPG. File name matches the IMAGE FILE variable.
- Save to the `images/` folder in your project root.

### Example prompts that have worked

> Flat line illustration. A pill strip sitting on one side of a weighing scale, rupee coins on the other. Forest green lines on cream background. Minimal, editorial. No text. No gradients.

> Flat line illustration. Two shelves side by side — one with consumer packaged goods, one with medicine boxes. Forest green lines on white background. Editorial magazine style. No text. No shadows.

> Flat line illustration. A smartphone showing a medicine delivery app on one side, a traditional pharmacy storefront on the other, connected by a simple dotted delivery route. Forest green lines on a cream background. Minimal, editorial magazine style. No text. No gradients. No shadows.

---

## STEP 2 — WRITE THE CONTENT

### 2A — Write the article or case study first

If you are working from research, a PDF, or notes — write the full content as plain text first and get it approved before touching any HTML. Never build the HTML before the content is finalised.

**Article voice — non-negotiable:**
- Written like a smart fresher explaining things to another fresher, not an academic or consultant
- Short paragraphs. Plain language. No jargon unless it is explained immediately after.
- Opens by calling out the gap between what textbooks say and what actually happens
- Each section builds on the last — not a list of disconnected facts
- Closes by connecting the topic to what it means for a pharma career
- Tone reference: read the opening three paragraphs of `how-drugs-are-priced-in-india` before writing anything
- Target length: ~1800 words of body copy (~9 min read)

**Case study voice — slightly different:**
- Opens with the stakes: what happened and why it mattered
- Tells it as a story with a clear timeline — not a list of facts
- Explains the industry consequences, not just the event itself
- Closes with what this means for pharma today or for a fresher's career
- Target length: ~2000 words (~10 min read)

### 2B — Create the HTML file

1. Open VS Code
2. Navigate to the `articles/` folder
3. Right-click `article-template.html` → Duplicate (or copy and paste in Finder/Explorer)
4. Rename the duplicate to `articles/[SLUG].html`

**Do not edit the template itself. Always duplicate first.**

### 2C — Verify the GA4 tag is present

Every new HTML file must have this block in the `<head>`, right after `</title>`:

```html
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-K3ENKKGSH5"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-K3ENKKGSH5');
</script>
```

The template already has this. Search for `G-K3ENKKGSH5` to confirm it is there before doing anything else. If it is missing, paste it in now.

### 2D — Fill in every EDIT marker in the HTML file

Work through the file top to bottom. Replace every placeholder marked EDIT.

**In the `<head>` block:**

```html
<title>[TITLE] — Figuring Out Pharma</title>
<meta name="description" content="[EXCERPT]">
<meta property="og:title" content="[TITLE]">
<meta property="og:description" content="[EXCERPT]">
<meta property="og:url" content="https://figuringoutpharma.com/articles/[SLUG]">
<link rel="canonical" href="https://figuringoutpharma.com/articles/[SLUG]">
```

Note: no `.html` at the end of the slug in URLs. Cloudflare handles the clean URL.

**For a regular article — header section:**

```html
<div class="art-cat">
  <a href="../blogs">[CATEGORY]</a>
</div>

<h1 class="art-title">[TITLE — use <em>tags</em> for the italic part]</h1>

<p class="art-deck">[DECK — 1 to 2 sentences expanding on the title]</p>

<span class="meta-author">Piyush Singh</span>
<span class="meta-date">[MONTH YEAR e.g. June 2026]</span>
<span class="meta-time">[READ TIME] read</span>
```

**For a case study — header section (different breadcrumb):**

```html
<div class="cs-breadcrumb">
  <a href="../case-studies">Case Studies</a>
  <span class="cs-breadcrumb-sep">/</span>
  <a href="../case-studies">[TAG e.g. Tragedy]</a>
</div>

<div class="cs-header-tag [TAG COLOUR e.g. t-red]">[TAG]</div>

<h1 class="cs-title">[TITLE — use <em>tags</em> for the italic subtitle part]</h1>

<p class="cs-deck">[DECK — 1 to 2 sentences]</p>

<span class="cs-meta-author">Piyush Singh</span>
<span class="cs-meta-date">[MONTH YEAR]</span>
<span class="cs-meta-time">[READ TIME] read</span>
```

**Cover image (same for both article types):**

```html
<img src="../images/[IMAGE FILE]"
     alt="[SHORT ALT TEXT describing the illustration]"
     style="width:100%;height:100%;object-fit:contain;background:#fff;">
```

**Article body structure:**

```html
<h2 id="section-slug">Section heading</h2>
<p>Body paragraph.</p>
<blockquote><p>A standout quote or key statement.</p></blockquote>
<div class="callout">
  <div class="callout-label">Key insight</div>
  <p>A key fact worth highlighting.</p>
</div>
<h3>Sub-heading inside a section</h3>
```

Every `<h2>` must have a unique `id=""`. The id must match the corresponding `href="#..."` in the Table of Contents sidebar.

**Table of Contents sidebar:**

```html
<li><a href="#section-slug">Short label for this section</a></li>
```

**Tags at the bottom of the article (4–6 tags):**

```html
<span class="tag-pill">Tag Name</span>
```

**Related Articles (3 cards) — fill in after running build.py in Step 4:**

```html
<div class="rel-card" onclick="window.location='[RELATIVE-SLUG-FROM-SAME-FOLDER]'">
  <div class="rel-cat">[CATEGORY]</div>
  <div class="rel-title">[TITLE]</div>
  <div class="rel-time">[READ TIME] read</div>
</div>
```

Use relative slugs without leading `../articles/` — e.g. `how-drugs-are-priced-in-india` not `../articles/how-drugs-are-priced-in-india`. The article pages are already inside the `articles/` folder so they link to siblings directly.

---

## STEP 3 — UPDATE THE JSON FILE

### For a regular article — add to `articles.json`

Open `articles.json`. Add a new entry **at the very top of the array**, above all existing entries. New articles always go at the top.

```json
{
  "title": "[TITLE in sentence case]",
  "category": "[CATEGORY]",
  "slug": "articles/[SLUG]",
  "excerpt": "[EXCERPT]",
  "date": "[DATE]",
  "readTime": "[READ TIME]",
  "featured": false,
  "llmsTopic": "[LLMS TOPIC]",
  "llmsSummary": "[LLMS SUMMARY]"
},
```

**JSON rules — these will break the site if you get them wrong:**
- Every entry except the last must end with a comma after the closing `}`
- The last entry must NOT have a trailing comma
- All field names and string values must be in double quotes
- The `&` character in titles must be written as `&` not `&amp;` in JSON
- `"featured": false` for almost every article. Set to `true` only for the Editor's Pick.

**Field reference:**

| Field | Description | Example |
|---|---|---|
| title | Full title in sentence case | "How drugs are priced in India — the real explanation" |
| category | One of the six fixed categories | "Industry" |
| slug | Path without domain, no .html | "articles/how-drugs-are-priced-in-india" |
| excerpt | Short description, max 160 chars | "DPCO, trade margins, and what your textbook skipped." |
| date | Publication date | "2026-07-01" |
| readTime | Estimated read time | "8 min" |
| featured | Is this the Editor's Pick? | false |
| llmsTopic | Keywords for llms.txt | "DPCO, drug pricing, NLEM, trade margins, India" |
| llmsSummary | 2–3 sentence description for llms.txt | "Explains how the NPPA calculates..." |

### For a case study — add to `case-studies.json`

Open `case-studies.json`. Add a new entry **at the very top of the array**.

```json
{
  "title": "[FULL TITLE — including subtitle after the em dash]",
  "tag": "[TAG]",
  "slug": "articles/[SLUG]",
  "excerpt": "[EXCERPT]",
  "year": "[YEAR e.g. 1996 - 2007 or just 2004]",
  "date": "[DATE]",
  "readTime": "[READ TIME]",
  "featured": false,
  "llmsTopic": "[LLMS TOPIC]",
  "llmsSummary": "[LLMS SUMMARY]"
},
```

Use a plain hyphen with spaces in the `year` field: `"1996 - 2007"`. The build script converts this to a proper en dash on the page automatically.

---

## STEP 4 — RUN BUILD.PY

This is the step that replaces all of the old manual Steps 4 and 5 from previous versions of this SOP. You do not edit sitemap.xml, llms.txt, or the auto sections of index.html by hand anymore.

### How to run it

Open Terminal (Mac) or Command Prompt (Windows). Navigate to your project root:

```
cd path/to/your/project-folder
```

Then run:

```
python3 build.py
```

On Windows, if `python3` gives an error, try `python build.py` instead.

### What it does

It reads your updated JSON files and rewrites:
- `sitemap.xml` — fully regenerated with every article and case study
- `llms.txt` — fully regenerated with all entries
- `index.html` — these five sections are regenerated between their AUTO markers:
  - Latest (3 newest articles by date)
  - Also Reading (articles ranked 4th–6th by date)
  - In Depth strip (top 6 articles by date)
  - Case Studies grid (first 6 entries from case-studies.json)
  - Featured side cards (see Featured rotation logic at the top of this SOP)

### What the output tells you

After running, the script prints:

**1. Confirmation lines** — `[OK] sitemap.xml`, `[OK] llms.txt`, `[OK] index.html`. If any of these say ERROR, stop and read the error message before continuing.

**2. Editor's Pick reminder** — tells you which article currently has `"featured": true`. If you want to change the Editor's Pick to the new article, edit the `feat-main` block in `index.html` by hand (see Step 5 below) and update `"featured"` in `articles.json`.

**3. Featured side card status** — tells you whether the side cards are showing fallback articles or case studies, and how many case studies you have vs the 6-card grid threshold.

**4. Related article suggestions** — for Step 6, a shortlist of same-category and different-category articles to use in the new article's Related section.

**5. Step 6B reminder** — lists 2–3 existing articles that might benefit from a cross-link to the new piece.

**6. llmsSummary note** — if any entries are missing `llmsSummary` in the JSON, the script lists them. This is not an error — the file still generates, just without Summary lines for those entries. Add the fields when you have time.

### If the script gives an error

**"Marker not found in index.html"** — the AUTO comment markers are missing or misspelled in index.html. Check that the file has all 10 marker comments (see Architecture section above). Do not edit the markers themselves.

**"json.JSONDecodeError"** — there is a formatting error in a JSON file. Common causes: missing comma after a `}`, extra comma after the last entry, missing quote marks. The error message will include a line number. Open the JSON file and fix the entry you just added.

**"No such file or directory"** — you are running the script from the wrong folder. Use `cd` to navigate to your project root first.

---

## STEP 5 — UPDATE THE EDITOR'S PICK (ONLY IF IT CHANGED)

The `feat-main` card is the only section of `index.html` the script never touches. If you want the new article to become the Editor's Pick:

**In `articles.json`:** Set `"featured": true` on the new article. Set `"featured": false` on whichever article previously had it.

**In `index.html`:** Find the `feat-main` block (it starts with `<div class="feat-main"`) and replace it with:

```html
<div class="feat-main" onclick="window.location='articles/[SLUG]'">
  <div class="feat-badge">Editor's Pick</div>
  <div class="art-cat">[CATEGORY]</div>
  <div class="art-title">[TITLE]</div>
  <p class="art-excerpt">[EXCERPT — can be slightly expanded to 2 sentences here]</p>
  <div class="art-meta"><span class="art-min">[READ TIME] read</span><span>[CATEGORY]</span></div>
</div>
```

After editing, run `python3 build.py` again so the `[OK]` reminder reflects the updated featured flag.

---

## STEP 6 — INTERNAL LINKING

### 6A — Related Articles in the new article's HTML

At the bottom of every article are 3 Related Article cards. Use the suggestions printed by build.py. Rules:

- At least 1 from the **same category** as the new article
- At least 1 from a **different category**
- Only link to published articles — if there is no suitable match, use `onclick="window.location='../blogs'"` as a temporary fallback

```html
<div class="rel-card" onclick="window.location='[SIBLING-SLUG]'">
  <div class="rel-cat">[CATEGORY]</div>
  <div class="rel-title">[TITLE]</div>
  <div class="rel-time">[READ TIME] read</div>
</div>
```

**Currently published articles and case studies** (slugs are relative to the articles/ folder — omit the `articles/` prefix when linking from one article page to another):

| Slug (from articles/ folder) | Category / Tag | Read time |
|---|---|---|
| how-drugs-are-priced-in-india | Industry | 5 min |
| fmcg-vs-pharma-marketing | Marketing | 11 min |
| how-crocin-became-a-household-brand | Brand Strategy | 9 min |
| how-online-pharmacies-changed-indian-pharma | Digital | 12 min |
| how-medical-reps-are-trained | Careers | 8 min |
| schedule-m-regulatory-shift-explained | Regulatory | 7 min |
| thalidomide-tragedy | Tragedy | 10 min |
| ranbaxy-and-the-fda | Regulatory | 7 min |
| vioxx-withdrawal | Withdrawal | 10 min |
| covid-vaccine-development | Breakthrough | 10 min |
| lipitor-patent-cliff | Patent | 10 min |
| bayer-monsanto-merger | M&A | 11 min |

Update this table every time you publish.

### 6B — Cross-links from existing articles

Every time you publish, check whether 1–2 existing articles should now link to the new one. Look at the Step 6B list the script printed. Open those files, find a placeholder `onclick="window.location='#'"` or an outdated Related card, and replace it.

This step matters for SEO. Orphan pages (pages with no incoming internal links) are not counted by search engines. Every article should be linked to by at least one other article.

---

## STEP 7 — PUSH TO GITHUB

1. Save all open files in VS Code: `Ctrl+S` (Windows) or `Cmd+S` (Mac)
2. Open **GitHub Desktop**
3. In the left panel, review the list of changed files. For a new article, you should see:
   - `articles/[SLUG].html` ✓ (the new article page)
   - `articles.json` ✓ (your new entry)
   - `case-studies.json` ✓ (only if publishing a case study)
   - `sitemap.xml` ✓ (regenerated by build.py)
   - `llms.txt` ✓ (regenerated by build.py)
   - `index.html` ✓ (regenerated sections by build.py)
   - `images/[IMAGE FILE].jpg` ✓ (the cover image)
   - Any existing articles you updated for cross-linking ✓

   If you see `sitemap.xml` or `llms.txt` NOT in the list — build.py did not run successfully. Run it again before committing.

4. Write a commit message:
   - For articles: `Publish: [SHORT TITLE]` — e.g. `Publish: Drug advertising regulations`
   - For case studies: `Publish: [TITLE] case study` — e.g. `Publish: Opioid crisis case study`
5. Click **Commit to main**
6. Click **Push origin**
7. Wait 2–3 minutes for Cloudflare Pages to deploy

---

## STEP 8 — POST-PUBLISH VERIFICATION

Open your browser. Go to `https://figuringoutpharma.com`. Hard refresh first: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac).

### For a new article

- [ ] Article URL loads without .html: `figuringoutpharma.com/articles/[SLUG]`
- [ ] Cover image displays correctly — not stretched, no broken image icon
- [ ] Table of contents links all scroll to their correct sections
- [ ] Homepage Latest section shows the new article as card 1
- [ ] Homepage In Depth strip shows the new article as card 01
- [ ] Homepage Also Reading shows correct rotation
- [ ] blogs.html shows the new article in the grid
- [ ] Category filter on blogs.html shows it under the correct category
- [ ] All 3 Related Article links at the bottom open the correct pages
- [ ] Dark mode looks correct — toggle the theme button to check
- [ ] On mobile: article is readable, cover image shows, TOC sidebar is hidden

### For a new case study (same checks plus)

- [ ] case-studies.html shows the new card in the grid
- [ ] Homepage Case Studies grid shows the updated cards
- [ ] If case study count is now 7 or 8, Featured side card rotation has triggered
- [ ] blogs.html does NOT show case studies — they stay separate

---

## STEP 9 — BEEHIIV NEWSLETTER

1. Log into Beehiiv
2. Go to **Campaigns** → find your most recent campaign
3. Click **Duplicate** — never edit the original template
4. Fill in every placeholder below
5. Preview on mobile before sending
6. Send

**Subject line format:**
```
New on Figuring Out Pharma: [SHORT TITLE]
```

**Email body template:**

---

Hey,

A new piece just went up on Figuring Out Pharma.

**[FULL ARTICLE TITLE]**

[2 to 3 sentences expanding on what the article covers. Plain language, no jargon. Tells the reader exactly what they will understand after reading it that they did not before. Do not copy the excerpt word for word — rewrite it slightly so it reads like you are talking to someone.]

This one is worth reading if you are [one line describing who this is most useful for — e.g. "trying to understand why drug prices in India work the way they do" or "figuring out what a medical rep actually does day to day"].

[BUTTON: Read the article →] — link: `https://figuringoutpharma.com/articles/[SLUG]`

---

That is it for this one.

If you found it useful, forward it to someone else who is figuring out pharma.

— Figuring Out Pharma

---

**Before hitting Send — check every item:**

- [ ] Subject line filled in
- [ ] Preview text filled in (under 100 characters — shown in email clients before the email is opened)
- [ ] Article title filled in
- [ ] 2 to 3 sentence paragraph written fresh (not copied from excerpt)
- [ ] "Worth reading if you are..." line filled in
- [ ] Button URL updated to the correct article slug — no .html at the end
- [ ] Previewed on mobile
- [ ] Duplicated from last campaign — original template not edited

---

## STEP 10 — AFTER PUBLISHING

Two things to do once the article is live.

### Update this SOP

Add the new article to the Published Articles table in Step 6A. Add the slug, category, and read time. This keeps the reference accurate for the next publish.

### Note future cross-links

If the new article mentions a topic you plan to cover in a future article, note it here so you can add the link when that article is published.

**Pending cross-links to add when future articles are published:**
- Crocin article → link to OTC vs Rx article (when published)
- Drug pricing article → link to DPCO deep-dive (when published)
- Online pharmacies article → link to regulatory/DCGI article (when published)

---

## REFERENCE — CATEGORY DEFINITIONS

| Category | What belongs here |
|---|---|
| Marketing | Brand strategy, OTC, advertising, campaigns, FMCG comparisons |
| Careers | Industrial training, job roles, day-in-the-life, how to enter the industry |
| Industry | Drug pricing, market structure, launches, IQVIA data, supply chain |
| Brand Strategy | Specific brand analyses, product lifecycle, positioning |
| Digital | Digital marketing in pharma, content strategy, social media, e-pharmacies |
| Regulatory | DPCO, DCGI, advertising laws, drug approval process, Schedule M |

---

## REFERENCE — CASE STUDY TAG AND COLOUR PAIRINGS

| Tag | Tag CSS class | Card CSS class | Colour shown |
|---|---|---|---|
| Tragedy | t-red | cc-red | Red |
| Regulatory | t-amber | cc-amber | Amber / gold |
| Withdrawal | t-red | cc-red | Red |
| Breakthrough | t-green | cc-green | Sage green |
| Patent | t-blue | cc-blue | Blue |
| M&A | t-purple | cc-purple | Purple |

---

## REFERENCE — SLUG NAMING RULES

- All lowercase
- Hyphens between words — no underscores, no spaces
- No special characters, no apostrophes, no brackets
- 4 to 6 words maximum
- Describes the article topic, not just the title

| Title | Good slug | Bad slug |
|---|---|---|
| How Crocin Turned a Generic Molecule Into a Household Brand | how-crocin-became-a-household-brand | how-crocin-turned-a-generic-molecule-into-a-household-brand |
| Why Pharma Cannot Advertise Drugs on TV in India | why-pharma-cant-advertise-on-tv | why_pharma_cant_advertise |
| What Does a Pharma Product Manager Actually Do | what-pharma-pm-actually-does | pharmapmrole2026 |

---

## REFERENCE — CURRENT SITE STATE

**Update this section every time you publish.**

### Published articles (6)

| Slug | Category | Date | Read time |
|---|---|---|---|
| schedule-m-regulatory-shift-explained | Regulatory | 2026-06-09 | 7 min |
| how-medical-reps-are-trained | Careers | 2026-06-09 | 8 min |
| how-online-pharmacies-changed-indian-pharma | Digital | 2026-06-08 | 12 min |
| how-crocin-became-a-household-brand | Brand Strategy | 2026-06-08 | 9 min |
| how-drugs-are-priced-in-india | Industry | 2026-06-08 | 5 min |
| fmcg-vs-pharma-marketing | Marketing | 2026-06-08 | 11 min |

### Published case studies (6)

| Slug | Tag | Date added to JSON |
|---|---|---|
| covid-vaccine-development | Breakthrough | — |
| lipitor-patent-cliff | Patent | — |
| bayer-monsanto-merger | M&A | — |
| thalidomide-tragedy | Tragedy | — |
| ranbaxy-and-the-fda | Regulatory | — |
| vioxx-withdrawal | Withdrawal | — |

### Current homepage state

| Section | What it shows |
|---|---|
| Editor's Pick | How online pharmacies changed the Indian pharma industry |
| Featured side card 1 | How drugs are priced in India (fallback article — fewer than 7 case studies) |
| Featured side card 2 | FMCG vs pharma marketing (fallback article — fewer than 7 case studies) |
| Latest card 1 | Schedule M explained |
| Latest card 2 | How medical reps are actually trained |
| Latest card 3 | How online pharmacies changed the Indian pharma industry |
| Also Reading 01 | How Crocin turned a generic molecule into a household brand |
| Also Reading 02 | How drugs are priced in India |
| Also Reading 03 | FMCG vs pharma marketing |
| In Depth 01 | Schedule M explained |
| In Depth 02 | How medical reps are actually trained |
| In Depth 03 | How online pharmacies changed the Indian pharma industry |
| In Depth 04 | How Crocin turned a generic molecule into a household brand |
| In Depth 05 | How drugs are priced in India |
| In Depth 06 | FMCG vs pharma marketing |

**This table is for reference only. From now on, the script keeps these sections accurate automatically. You do not need to update this table manually for the auto-sections — only for the Editor's Pick.**

---

## REFERENCE — HOW build.py WORKS (FOR HANDOFF TO ANOTHER LLM)

If you are handing this to a different AI assistant and they need to understand the automation:

**The script lives at:** project root, same folder as `articles.json`

**Run command:** `python3 build.py` (no arguments, no flags)

**Requires:** Python 3, no external packages

**It reads:** `articles.json` and `case-studies.json`

**It writes:** `sitemap.xml`, `llms.txt`, and 5 sections of `index.html`

**It finds sections in index.html using comment markers.** Each section is bounded by a START and END comment. The script finds the START marker, finds the END marker, and replaces everything in between. The markers are:

```
<!-- AUTO:ALSO-READING:START -->  ...  <!-- AUTO:ALSO-READING:END -->
<!-- AUTO:LATEST:START -->         ...  <!-- AUTO:LATEST:END -->
<!-- AUTO:IN-DEPTH:START -->       ...  <!-- AUTO:IN-DEPTH:END -->
<!-- AUTO:CASE-STUDIES:START -->   ...  <!-- AUTO:CASE-STUDIES:END -->
<!-- AUTO:FEAT-SIDE:START -->      ...  <!-- AUTO:FEAT-SIDE:END -->
```

**articles.json sort order:** Newest first by `date` field. The script sorts by date descending. Latest = index 0, 1, 2. Also Reading = index 3, 4, 5. In Depth = index 0–5.

**case-studies.json order:** The order in the file is the display order. Index 0–5 go into the Case Studies grid. Index 6 and 7 go into the Featured side cards when they exist.

**Featured side card logic:**
- `len(case_studies) <= 6` → both side cards are hardcoded fallback articles (drug pricing + FMCG)
- `len(case_studies) == 7` → side card 1 = `case_studies[6]`, side card 2 = fallback
- `len(case_studies) >= 8` → side card 1 = `case_studies[6]`, side card 2 = `case_studies[7]`

**llms.txt fields used from JSON:** `title`, `slug`, `llmsTopic` (→ Topic line), `llmsSummary` (→ Summary line). Entries without these fields generate a heading and URL only.

**sitemap.xml:** Regenerated completely. Static pages (/, /blogs, /case-studies, /categories) use the date of the newest article as `<lastmod>`. Article and case study entries use their own `date` field. Case studies without a `date` field fall back to the newest article date.

---

*Last updated: June 2026 — complete rewrite integrating build.py automation. Steps 4 and 5 are now a single automated step. Manual Ctrl+H homepage rotation is retired.*
*Maintained by: Figuring Out Pharma*
