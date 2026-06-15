# Figuring Out Pharma — Article Publishing SOP

> Open this file every time you publish. Follow every step in order.  
> Never skip a step. Never publish without completing the full checklist.

---

## Before You Start — Is the Article Ready?

Check all of these before touching any file:

- [ ] Article draft is fully written and approved
- [ ] All facts have been checked — no unverified numbers or claims
- [ ] Brand claims are attributed (e.g. "the brand claims..." not stated as fact)
- [ ] Cover image has been generated (see Step 1 below)
- [ ] You know the article's: **title, category, slug, excerpt, read time, date**

---

## The 8 Variables You Need Before Opening VS Code

Fill these in before you start. You will paste them into multiple files.

```
TITLE:        e.g. How Crocin Turned a Generic Molecule Into a Household Brand
SLUG:         e.g. how-crocin-became-a-household-brand
              (lowercase, hyphens only, no spaces, no special characters)
CATEGORY:     Marketing / Careers / Industry / Brand Strategy / Digital / Regulatory
EXCERPT:      One sentence. Max 160 characters. Used in articles.json and meta description.
DATE:         Today's date in YYYY-MM-DD format e.g. 2026-06-08
READ TIME:    e.g. 9 min
IMAGE FILE:   e.g. crocin-household-brand-cover.jpg
              (save as: images/crocin-household-brand-cover.jpg)
```

---

## Step 1 — Generate the Cover Image

### Preferred tools (in order):

1. **Ideogram.ai** — best results for flat editorial illustration style. Free tier, no watermark.
2. **Microsoft Designer** (designer.microsoft.com) — completely free, sign in with any Microsoft account. Outputs PNG — convert to JPG after downloading.
3. **Adobe Firefly** (firefly.adobe.com) — free tier with Adobe account.

Canva AI is no longer the primary tool as free limits run out quickly.

### Standard Cover Image Prompt

```
Flat line illustration. [DESCRIBE THE CORE CONCEPT IN ONE LINE — e.g. "a medicine strip 
and a shopping cart on opposite sides of a balance scale"]. Forest green lines on a cream 
or white background. Minimal, editorial style. No text. No gradients. No shadows. 
Clean geometric shapes. Think editorial magazine illustration.
```

### Rules for every cover image:
- Canvas size: **1200 × 675px** (16:9) — if the tool outputs a different size, crop or resize before saving
- If the output is PNG, convert to JPG before saving
- If the output is not exactly 16:9, use Paint (Windows) or Preview (Mac) to crop — centring on the illustration. The `object-fit:contain` tag on the site means a slightly different ratio will still display correctly with cream letterboxing, so this is not critical.
- Style: flat line illustration, forest green on cream/white
- No text in the image
- No photorealistic elements
- Save as JPG
- File name: matches your IMAGE FILE variable above
- Save location: `images/` folder in your project root

### Example prompts that have worked:

**Drug pricing article:**
> Flat line illustration. A pill strip sitting on one side of a weighing scale, rupee coins on the other. Forest green lines on cream background. Minimal, editorial. No text. No gradients.

**FMCG vs Pharma article:**
> Flat line illustration. Two shelves side by side — one with consumer packaged goods, one with medicine boxes. Forest green lines on white background. Editorial magazine style. No text. No shadows.

**Online pharmacies article:**
> Flat line illustration. A smartphone showing a medicine delivery app on one side, a traditional pharmacy storefront on the other, connected by a simple dotted delivery route. Forest green lines on a cream background. Minimal, editorial magazine style. No text. No gradients. No shadows.

---

## Step 2 — Write and Create the Article HTML File

### 2A — Write the article first (if working from research/PDF)

If the article is being written from a research document or PDF rather than a pre-written draft:

1. **Show the written article to Piyush before building any HTML.** Claude reads the source material, writes the full article body in the site's voice, and shares it as plain text first.
2. Wait for approval or edits before proceeding to HTML.

**The site's voice — non-negotiable:**
- Written like a smart fresher explaining things to another fresher, not an academic or consultant
- Short paragraphs. Plain language. No jargon unless it is explained immediately after.
- Opens by calling out the gap between what textbooks say and what actually happens
- Each section builds on the last — not a list of disconnected facts
- Closes by connecting the topic to what it means for a pharma career
- Tone reference: read the opening three paragraphs of `how-drugs-are-priced-in-india.html` before writing anything

**Length:** Target 9 minutes read time (~1800 words of body copy). Use the research to choose the most interesting parts — do not try to include everything.

### 2B — Create the HTML file

1. Open VS Code
2. Open `articles/article-template.html`
3. **Do not edit the template.** Right-click the file → **Duplicate** (or copy-paste in Finder/Explorer)
4. Rename the duplicate to: `articles/[SLUG].html`
   - Example: `articles/how-crocin-became-a-household-brand.html`

### 2C — Add the GA4 tracking tag

Immediately after the closing `</title>` tag in the `<head>` of every new HTML file — whether a regular article, case study, or any new page — paste this block:

<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-K3ENKKGSH5"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-K3ENKKGSH5');
</script>

Rules:
- Every new file without exception — articles, case studies, new pages
- Place it right after </title> and before the first <meta> description tag
- Never skip — without it the page will not appear in Google Analytics
- Do not add it twice — search for G-K3ENKKGSH5 before pasting to confirm it is not already there
- Both templates (article-template.html and case-study-template.html) already have this tag baked in — so any file duplicated from them will have it automatically

### Fill in every EDIT marker — in order:

**In the `<head>`:**
```html
<title>[TITLE] — Figuring Out Pharma</title>
<meta name="description" content="[EXCERPT]">
<meta property="og:title" content="[TITLE]">
<meta property="og:description" content="[EXCERPT]">
<meta property="og:url" content="https://figuringoutpharma.com/articles/[SLUG].html">
```

**Article header section:**
```html
<!-- Category breadcrumb -->
<a href="../blogs">[CATEGORY]</a>

<!-- Title — use <em> tags for the italic part -->
<h1 class="art-title">[TITLE WITH <em>ITALIC PART</em>]</h1>

<!-- Deck — one or two sentences expanding on the title -->
<p class="art-deck">[DECK]</p>

<!-- Meta row -->
<span class="meta-author">Piyush Singh</span>
<span class="meta-date">[MONTH YEAR e.g. June 2026]</span>
<span class="meta-time">[READ TIME] read</span>
```

**Cover image:**
```html
<img src="../images/[IMAGE FILE]" 
     alt="[SHORT ALT TEXT]" 
     style="width:100%;height:100%;object-fit:contain;background:#fff;">
```

**Article body:** Paste your approved article content using the prose structure:
- `<h2 id="section-slug">` for every main section
- `<h3>` for sub-headings
- `<p>` for paragraphs
- `<blockquote>` for standout quotes
- `<div class="callout">` for key insight boxes

**Table of Contents (right sidebar):**
```html
<li><a href="#section-slug">Short label</a></li>
```
Every `href="#..."` must exactly match the `id="..."` on your `<h2>` tags.

**Tags (bottom of article):**
```html
<span class="tag-pill">[TAG]</span>
```
Add 4–6 relevant tags.

**Related Articles (3 cards at the bottom):**
See Step 6 for how to choose these.

---

## Step 3 — Update articles.json

Open `articles.json`. Add a new entry **at the very top** of the array (newest first).

```json
{
  "title": "[TITLE]",
  "category": "[CATEGORY]",
  "slug": "articles/[SLUG].html",
  "excerpt": "[EXCERPT]",
  "date": "[DATE]",
  "readTime": "[READ TIME]",
  "featured": false
},
```

**Rules:**
- The new entry goes at the top — above all existing entries
- Comma after the closing `}` — it must be valid JSON
- `featured: true` only for the one article you want as Editor's Pick on the homepage
- Double-check: no trailing comma on the last entry in the array

---

## Step 4 — Update sitemap.xml

Open `sitemap.xml`. Add a new `<url>` block **inside the `<urlset>` tag**, after the existing article blocks:

```xml
<url>
  <loc>https://figuringoutpharma.com/articles/[SLUG].html</loc>
  <lastmod>[DATE]</lastmod>
  <changefreq>monthly</changefreq>
  <priority>0.8</priority>
</url>
```

Also update the homepage `<lastmod>` to today's date:
```xml
<url>
  <loc>https://figuringoutpharma.com/</loc>
  <lastmod>[DATE]</lastmod>
  ...
</url>
```

---

## Step 5 — Update index.html (All Three Sections)

Open `index.html`. You need to update **three separate sections** in one go. Do not close the file until all three are done.

### Before making any changes — read the current code first

Before touching index.html, read the actual code to confirm what is currently a placeholder 
and what is a real article. A placeholder uses onclick="sendPrompt(...)" or 
onclick="window.location='#'". A real article uses onclick="window.location='articles/slug.html'".

For every change in Step 5, write out:
- FIND: the exact text string currently in the file
- REPLACE WITH: the exact text string to put in its place
so the editor can use Ctrl+H (Find and Replace) in VS Code without needing to locate 
lines manually.

Rule: Only replace placeholders. Never displace a real article card unless the article 
count justifies it (i.e. you have more published articles than available card slots).

### 5A — Featured Section

The Featured section has one **main card (Editor's Pick)** and **two side cards**.

**If this article is the new Editor's Pick**, replace the main card's `onclick` and content:
```html
<div class="feat-main" onclick="window.location='articles/[SLUG].html'">
  <div class="feat-badge">Editor's Pick</div>
  <div class="art-cat">[CATEGORY]</div>
  <div class="art-title">[TITLE]</div>
  <p class="art-excerpt">[EXCERPT — slightly expanded, 1–2 sentences]</p>
  <div class="art-meta"><span class="art-min">[READ TIME]</span><span>[CATEGORY]</span></div>
</div>
```

**If it goes in a side card**, update one of the two `.side-art` divs:
```html
<div class="side-art" onclick="window.location='articles/[SLUG].html'">
  <div class="art-cat">[CATEGORY]</div>
  <div class="art-title">[TITLE]</div>
  <p class="art-excerpt">[SHORT EXCERPT]</p>
  <div class="art-meta" style="margin-top:auto;padding-top:0.75rem">
    <span class="art-min">[READ TIME]</span>
  </div>
</div>
```

### 5B — Latest Section

The Latest section shows exactly 3 article cards, newest first. Every time a new article is published, the rotation is done with **two separate Ctrl+H operations** — one to insert the new article at card 1, one to delete card 3.

**Rotation logic:**
- New article → card 1
- Previous card 1 → card 2
- Previous card 2 → card 3
- Previous card 3 → deleted from Latest, moves to Also Reading (see 5D)

**Operation 1 — Insert new article at card 1.**
Find the opening line of the current card 1 and replace it with the new article card + the current card 1 opening line below it:

Find:
```html
<div class="art-card" onclick="window.location='articles/[CURRENT CARD 1 SLUG].html'">
```

Replace with:
```html
<div class="art-card" onclick="window.location='articles/[NEW SLUG].html'">
        <div class="art-cat">[CATEGORY]</div>
        <div class="art-title">[TITLE]</div>
        <p class="art-excerpt" style="font-family:var(--body);font-size:0.83rem;font-weight:300;color:var(--text2);line-height:1.72;font-style:italic;margin-bottom:0.75rem;margin-top:0.5rem">[EXCERPT]</p>
        <div class="art-meta"><span class="art-min">[READ TIME]</span></div>
      </div>
      <div class="art-card" onclick="window.location='articles/[CURRENT CARD 1 SLUG].html'">
```

**Operation 2 — Delete card 3.**
Find the entire card 3 block and replace with nothing (leave the Replace field empty):

Find:
```html
<div class="art-card" onclick="window.location='articles/[CURRENT CARD 3 SLUG].html'">
        <div class="art-cat">[CARD 3 CATEGORY]</div>
        <div class="art-title">[CARD 3 TITLE]</div>
        <p class="art-excerpt" style="font-family:var(--body);font-size:0.83rem;font-weight:300;color:var(--text2);line-height:1.72;font-style:italic;margin-bottom:0.75rem;margin-top:0.5rem">[CARD 3 EXCERPT]</p>
        <div class="art-meta"><span class="art-min">[CARD 3 READ TIME]</span></div>
      </div>
```

Replace with: *(nothing — empty field)*

### 5D — Also Reading Section (Hero sidebar)

The Also Reading section always has exactly 3 items. Every time a new article is published, the rotation is done with **two separate Ctrl+H operations** — one to insert the dropped article at position 01, one to delete position 03.

**Rotation logic:**
- Article removed from Latest card 3 → position 01
- Previous position 01 → position 02
- Previous position 02 → position 03
- Previous position 03 → deleted from Also Reading entirely

**Operation 1 — Insert dropped article at position 01.**
Find the opening line of the current position 01 and replace with the new item + current 01 below it:

Find:
```html
<div class="hs-item" onclick="window.location='articles/[CURRENT 01 SLUG].html'">
        <div class="hs-num">01</div>
```

Replace with:
```html
<div class="hs-item" onclick="window.location='articles/[DROPPED FROM LATEST SLUG].html'">
        <div class="hs-num">01</div>
        <div class="hs-cat">[CATEGORY]</div>
        <div class="hs-title">[TITLE]</div>
        <div class="hs-time">[READ TIME] read</div>
      </div>
      <div class="hs-item" onclick="window.location='articles/[CURRENT 01 SLUG].html'">
        <div class="hs-num">02</div>
```

Note: this also renumbers the old 01 to 02 in the same operation.

**Operation 2 — Delete position 03 and renumber 02 → 03.**
Find the current position 02 (which is now becoming 03) and update its number, then find position 03 and delete it:

Find:
```html
<div class="hs-num">02</div>
```
Replace with:
```html
<div class="hs-num">03</div>
```

Then find the current position 03 block and replace with nothing:

Find:
```html
<div class="hs-item" onclick="window.location='articles/[CURRENT 03 SLUG].html'">
        <div class="hs-num">03</div>
        <div class="hs-cat">[CURRENT 03 CATEGORY]</div>
        <div class="hs-title">[CURRENT 03 TITLE]</div>
        <div class="hs-time">[CURRENT 03 READ TIME] read</div>
      </div>
```

Replace with: *(nothing — empty field)*

**Always provide the exact Ctrl+H FIND and REPLACE strings for all operations in 5B and 5D.**

### 5C — In Depth Strip

The In Depth strip is a horizontal scroll of cards numbered 01, 02, 03... Add the new article as card 01 and renumber everything:

```html
<div class="scroll-card" onclick="window.location='articles/[SLUG].html'">
  <div class="scroll-num">01</div>
  <div class="art-cat">[CATEGORY]</div>
  <div class="art-title" style="font-size:0.9rem">[TITLE — shortened if needed]</div>
  <div class="art-meta" style="margin-top:0.75rem"><span class="art-min">[READ TIME]</span></div>
</div>
```

Renumber existing cards: what was 01 becomes 02, 02 becomes 03, and so on. Remove the last placeholder card if the strip gets too long (keep it at 6 cards max).

---

## Step 6 — Internal Linking

### 6A — Related Articles in the NEW article

At the bottom of every article are 3 Related Article cards. Choose them like this:

**Rule:** Pick articles that a reader of this article would logically want to read next.
- At least 1 should be from the **same category**
- At least 1 should be from a **different category** (to encourage exploration)
- Avoid linking to placeholder articles that are not published yet — use `onclick="window.location='../blogs.html'"` as a fallback

```html
<div class="rel-card" onclick="window.location='[SLUG-OF-RELATED].html'">
  <div class="rel-cat">[CATEGORY]</div>
  <div class="rel-title">[TITLE]</div>
  <div class="rel-time">[READ TIME] read</div>
</div>
```

**Current published articles to choose from:**
- `fmcg-vs-pharma-marketing.html` — Marketing, 11 min
- `how-drugs-are-priced-in-india.html` — Industry, 5 min
- `how-crocin-became-a-household-brand.html` — Brand Strategy, 9 min
- `how-online-pharmacies-changed-indian-pharma.html` — Digital, 9 min

### 6B — Update Related Articles in EXISTING articles

Every time you publish a new article, go back into each existing article and check if the new article should replace a `#` placeholder in their Related Articles section.

**Quick rule:** If the new article is topically related to an existing one, update that existing article's Related section to link to the new one.

Example: Publishing the Crocin article → open `how-drugs-are-priced-in-india.html` → the Related card that says "OTC vs prescription" with `onclick="window.location='#'"` could be replaced with the Crocin article since both cover brand/pricing strategy.

**This step takes 10 minutes and is important. Do not skip it.**

---

## Step 7 — Push to GitHub

1. Save all files: `Ctrl+S` (or `Cmd+S`) on every open file
2. Open **GitHub Desktop**
3. In the left panel, verify you can see all the files you changed:
   - `articles/[SLUG].html` ✓
   - `articles.json` ✓
   - `sitemap.xml` ✓
   - `index.html` ✓
   - `images/[IMAGE FILE].jpg` ✓
   - Any existing articles you updated for cross-linking ✓
4. Write a commit message: `Publish: [SHORT ARTICLE TITLE]`
   - Example: `Publish: Crocin brand strategy`
5. Click **Commit to main**
6. Click **Push origin**
7. Wait 2–3 minutes for Cloudflare Pages to deploy

---

## Step 8 — Post-Publish Verification

Open your browser. Go to `https://figuringoutpharma.com`

Do a **hard refresh** first: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac). This clears the cache.

Check every item:

- [ ] New article URL loads: `figuringoutpharma.com/articles/[SLUG].html`
- [ ] Cover image displays correctly (not stretched, no broken image)
- [ ] Table of contents links scroll to the right sections
- [ ] Homepage Featured section shows the article correctly
- [ ] Homepage Latest section shows the article as card 1
- [ ] Homepage In Depth strip shows the article as card 01
- [ ] blogs.html shows the article in the grid
- [ ] Category filter on blogs.html shows it under the correct category
- [ ] All Related Article links in the new article work (no broken links)
- [ ] Dark mode looks correct (toggle the theme button)
- [ ] On mobile: article is readable, cover image displays, TOC is hidden

---

## Step 9 — Beehiiv Newsletter

1. Log into Beehiiv
2. Go to **Campaigns** → find your last newsletter
3. Click **Duplicate** — never edit the original template directly
4. Fill in every EDIT placeholder using the template below
5. Preview on mobile before sending
6. Send

**Standard subject line format:**
```
New on Figuring Out Pharma: [SHORT TITLE]
```
**Email body:**

---

Hey,

A new piece just went up on Figuring Out Pharma.

**[EDIT: FULL ARTICLE TITLE]**

[EDIT: 2 to 3 sentences expanding on what the article covers. Plain language, no jargon, tells the reader exactly what they will understand after reading it that they did not before. Do not copy the excerpt word for word — rewrite it slightly so it feels personal.]

This one is worth reading if you are [EDIT: one line describing who this is most useful for — e.g. "figuring out what pharma marketing actually looks like on the ground" or "trying to understand why drug prices in India work the way they do"].

[BUTTON: Read the article →] — links to [EDIT: full article URL e.g. https://figuringoutpharma.com/articles/SLUG.html]

---

That is it for this one.

If you found it useful, forward it to someone else who is figuring out pharma.

— Figuring Out Pharma

---

### Email EDIT checklist — complete before hitting Send

- [ ] Subject line updated
- [ ] Preview text updated — under 100 characters
- [ ] Article title updated
- [ ] 2 to 3 sentence body paragraph written fresh
- [ ] "Worth reading if you are..." line filled in
- [ ] Button URL updated to correct article slug
- [ ] Previewed on mobile
- [ ] Duplicated from last campaign — original template untouched

---

## Step 10 — After Publishing (Content Connections)

Once the article is live, do these two things:

### Update this SOP
In Step 6A above, add the new article to the "Current published articles" list:
```
- `[SLUG].html` — [Category], [read time]
```

### Note any future cross-links needed
If the new article mentions a topic you plan to cover in a future article, note it here. When that future article is published, come back and add the link.

**Pending cross-links to add when articles are published:**
- Crocin article → link to OTC vs Rx article (when published)
- Drug pricing article → link to DPCO deep-dive (when published)
- Online pharmacies article → link to regulatory/DCGI article (when published)

---

## Quick Reference — Current Homepage State

Use this to know what is currently live on the homepage before making any changes.

| Section | Position 1 | Position 2 | Position 3 |
|---|---|---|---|
| Featured Editor's Pick | Online Pharmacies | — | — |
| Featured side cards | Drug Pricing | FMCG vs Pharma | — |
| Latest | Schedule M | Medical Reps | Online Pharmacies |
| Also Reading | FMCG (01) | Drug Pricing (02) | Crocin (03) |

In Depth strip (left to right): FMCG (01) → Drug Pricing (02) → Crocin (03) → Online Pharmacies (04) → Medical Reps (05) → Schedule M (06)

**Update this table every time you publish.** This is the source of truth before any Ctrl+H.

---

## CASE STUDY PUBLISHING WORKFLOW

Case studies live on `case-studies.html`, not `blogs.html`. They are a separate content type with a different page, different card design, and different HTML template. Follow this workflow every time you publish a case study.

---

### CS Variables You Need Before Starting

```
TITLE:        e.g. The Thalidomide Tragedy
SLUG:         e.g. thalidomide-tragedy
              (save as: articles/thalidomide-tragedy.html)
TAG:          Tragedy / Regulatory / Withdrawal / Breakthrough / Patent / M&A
TAG COLOUR:   t-red / t-amber / t-green / t-blue / t-purple / t-teal
CARD COLOUR:  cc-red / cc-amber / cc-green / cc-blue / cc-purple / cc-teal
YEAR:         e.g. 1957 – 1962
EXCERPT:      One sentence summary for the card. Max 160 characters.
DATE:         Today's date in YYYY-MM-DD format
READ TIME:    e.g. 10 min
IMAGE FILE:   e.g. thalidomide-tragedy-cover.jpg
```

Tag and card colour pairings:
| Tag | Tag class | Card class |
|---|---|---|
| Tragedy | t-red | cc-red |
| Regulatory | t-amber | cc-amber |
| Breakthrough | t-green | cc-green |
| Patent / Industry | t-blue | cc-blue |
| M&A | t-purple | cc-purple |
| Withdrawal / Teal | t-teal | cc-teal |

---

### CS Step 1 — Write the Case Study First

Same rules as articles (Step 2A). Show the written case study to Piyush before building HTML.

**Case study voice — slightly different from articles:**
- Opens with the stakes: what happened and why it matters
- Tells it as a story with a clear timeline — not a list of facts
- Explains the industry consequences, not just the event itself
- Closes with what this means for pharma today or for your career
- Same plain language, same short paragraphs, same "no assumptions" tone
- Target length: 10 minutes read time (~2000 words)

---

### CS Step 2 — Create the HTML File

Case studies use the same article template as regular articles (`articles/article-template.html`). Duplicate it and save as `articles/[SLUG].html`.

Fill in all EDIT markers exactly as you would for a regular article. The structure is identical — header, cover image, prose body, TOC, related articles, footer.

The only difference is the category breadcrumb — use the case study tag instead of a category:
```html
<div class="art-cat">
  <a href="../case-studies">Case Studies</a>
  <span class="art-cat-sep">/</span>
  <a href="../case-studies">[TAG — e.g. Tragedy]</a>
</div>
```

---

### CS Step 3 — Update articles.json

Add the case study entry at the top of `articles.json` exactly like a regular article. Use the tag as the category field:

```json
{
  "title": "[TITLE]",
  "category": "[TAG — e.g. Tragedy]",
  "slug": "articles/[SLUG].html",
  "excerpt": "[EXCERPT]",
  "date": "[DATE]",
  "readTime": "[READ TIME]",
  "featured": false
},
```

---

### CS Step 4 — Update sitemap.xml

Add a new `<url>` block exactly as you would for a regular article.

---

### CS Step 5 — Update case-studies.html

This is the main step that is different from regular articles.

Open `case-studies.html`. Find the coming-soon placeholder block OR find the existing card for this case study (which currently has `onclick="sendPrompt(...)"`) and replace it with a real card.

**The card block to use:**

```html
<div class="cs-card [CARD COLOUR e.g. cc-red]" onclick="window.location='articles/[SLUG].html'">
  <div class="tag [TAG COLOUR e.g. t-red]">[TAG e.g. Tragedy]</div>
  <div class="csc-year">[YEAR e.g. 1957 – 1962]</div>
  <div class="csc-title">[TITLE]</div>
  <p class="csc-sum">[EXCERPT]</p>
  <span class="csc-read">Read case study →</span>
</div>
```

**Before making any changes — read the current code first.** Identify which card is still a placeholder (`onclick="sendPrompt(...)"`) and which are real articles (`onclick="window.location='...'"`) before touching anything. Write out the exact FIND and REPLACE strings for Ctrl+H.

**If the coming-soon block is still showing** (no cards published yet), replace the entire coming-soon div with the first card:

Find:
```html
<div class="cs-coming">
```
*(replace the whole cs-coming block)*

Replace with the card block above.

---

### CS Step 6 — Update index.html Case Studies Section

The homepage has a Case Studies section with 6 cards. All 6 currently show `onclick="sendPrompt(...)"`. Replace the matching placeholder card with the real one using Ctrl+H.

Find the card with the matching title and replace its `onclick`:

**Find:**
```
onclick="sendPrompt('Write a detailed case study article on: [MATCHING TITLE]')"
```

**Replace with:**
```
onclick="window.location='articles/[SLUG].html'"
```

This is a targeted single-line replacement — you only need to change the onclick, not the whole card. The title, tag, year, and summary are already correct in the placeholder.

---

### CS Step 7 — Push to GitHub

Same as regular articles. Commit message format: `Publish: [CASE STUDY TITLE] case study`

Files to verify in GitHub Desktop:
- `articles/[SLUG].html` ✓
- `articles.json` ✓
- `sitemap.xml` ✓
- `case-studies.html` ✓
- `index.html` ✓
- `images/[IMAGE FILE].jpg` ✓

---

### CS Step 8 — Post-Publish Verification

- [ ] Case study URL loads: `figuringoutpharma.com/articles/[SLUG].html`
- [ ] Cover image displays correctly
- [ ] `case-studies.html` shows the new card (not the coming-soon block)
- [ ] Clicking the card on case-studies.html opens the article correctly
- [ ] Homepage Case Studies section card now links to the article (not sendPrompt)
- [ ] blogs.html does NOT show case studies — they are separate content
- [ ] Dark mode looks correct

---

### Current Case Studies State

| Case Study | Status | Slug when published |
|---|---|---|
| The Thalidomide Tragedy | Published | thalidomide-tragedy |
| Ranbaxy and the FDA | Published | ranbaxy-and-the-fda |
| The Vioxx Withdrawal | Published | vioxx-withdrawal |
| COVID-19 Vaccine Development | Published | covid-vaccine-development |
| Lipitor's Patent Cliff | Published | lipitor-patent-cliff |
| Bayer–Monsanto Merger | Published | bayer-monsanto-merger |

Update Status to "Published" and add the actual slug each time one goes live.

---

| Category | What belongs here |
|---|---|
| Marketing | Brand strategy, OTC, advertising, campaigns, FMCG comparisons |
| Careers | Industrial training, job roles, day-in-the-life, how to enter the industry |
| Industry | Drug pricing, market structure, launches, IQVIA data, supply chain |
| Brand Strategy | Specific brand analyses, product lifecycle, positioning |
| Digital | Digital marketing in pharma, content strategy, social media |
| Regulatory | DPCO, DCGI, advertising laws, drug approval process |

---

## Quick Reference — Slug Naming Rules

- All lowercase
- Hyphens between words, no underscores
- No special characters, no apostrophes, no brackets
- Keep it short — 4 to 6 words maximum
- Should describe the article, not just the title

| Title | Good slug | Bad slug |
|---|---|---|
| How Crocin Turned a Generic Molecule Into a Household Brand | `how-crocin-became-a-household-brand` | `how-crocin-turned-a-generic-molecule-into-a-household-brand` |
| Why Pharma Can't Advertise Drugs on TV in India | `why-pharma-cant-advertise-on-tv` | `why_pharma_cant_advertise` |
| What Does a Pharma PM Actually Do | `what-pharma-pm-actually-does` | `pharmapmrole2026` |

---

## Image Generation Prompt — Master Template

Keep this nearby every time you make a cover image.

```
Flat line illustration. [ONE LINE DESCRIBING THE VISUAL CONCEPT]. 
Forest green (#1a3a2a) lines and shapes on a cream or white (#faf8f2) background. 
Minimal, editorial magazine style. No text. No gradients. No drop shadows. 
No photorealistic elements. Clean geometric shapes only.
```

**Tips:**
- The visual concept should be a *metaphor* for the article, not a literal depiction
- Think objects, scales, charts, arrows, buildings, people as simple shapes
- If the first result is too complex, add: "Even more minimal. Fewer elements."
- If it looks too digital/tech, add: "Inspired by 1970s editorial print illustration."

---

*Last updated: June 2026 — updated with precise Latest push-down and Also Reading rotation rules, corrected homepage state table, added full Case Study publishing workflow.*  
*Maintained by: Figuring Out Pharma*
