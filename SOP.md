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

Use this prompt in **Canva AI** (Text to Image). Copy it exactly and replace the bracketed parts.

### Standard Cover Image Prompt

```
Flat line illustration. [DESCRIBE THE CORE CONCEPT IN ONE LINE — e.g. "a medicine strip 
and a shopping cart on opposite sides of a balance scale"]. Forest green lines on a cream 
or white background. Minimal, editorial style. No text. No gradients. No shadows. 
Clean geometric shapes. Think editorial magazine illustration.
```

### Rules for every cover image:
- Canvas size: **1200 × 675px** (16:9)
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

---

## Step 2 — Create the Article HTML File

1. Open VS Code
2. Open `articles/article-template.html`
3. **Do not edit the template.** Right-click the file → **Duplicate** (or copy-paste in Finder/Explorer)
4. Rename the duplicate to: `articles/[SLUG].html`
   - Example: `articles/how-crocin-became-a-household-brand.html`

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
<a href="../blogs.html">[CATEGORY]</a>

<!-- Title — use <em> tags for the italic part -->
<h1 class="art-title">[TITLE WITH <em>ITALIC PART</em>]</h1>

<!-- Deck — one or two sentences expanding on the title -->
<p class="art-deck">[DECK]</p>

<!-- Meta row -->
<span class="meta-author">Figuring Out Pharma</span>
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

The Latest section shows 3 article cards. Shift cards down by one and add the new article as card 1:

```html
<!-- Card 1 — NEW ARTICLE -->
<div class="art-card" onclick="window.location='articles/[SLUG].html'">
  <div class="art-cat">[CATEGORY]</div>
  <div class="art-title">[TITLE]</div>
  <p class="art-excerpt" style="font-family:var(--body);font-size:0.83rem;font-weight:300;color:var(--text2);line-height:1.72;font-style:italic;margin-bottom:0.75rem;margin-top:0.5rem">[EXCERPT]</p>
  <div class="art-meta"><span class="art-min">[READ TIME]</span></div>
</div>
```

Remove the oldest card (card 3) to keep it at 3 total. That article is still accessible via blogs.html.

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
- *(add new articles here as you publish them)*

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
3. Click **Duplicate**
4. Update the subject line: `New: [TITLE]`
5. Replace the article title, excerpt, and link in the email body
6. Update the cover image in the email
7. Preview on mobile before sending
8. Send

**Standard subject line format:**
```
New on Figuring Out Pharma: [SHORT TITLE]
```

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
- FMCG vs Pharma article → link to Crocin article (when published — update Related section)

---

## Quick Reference — Article Categories

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

## Canva AI Prompt — Master Template

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

*Last updated: June 2026*  
*Maintained by: Figuring Out Pharma*
