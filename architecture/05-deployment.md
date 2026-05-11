# SOP 05 — Deployment

> **Layer 1 · Architecture.** Phase 5 of B.L.A.S.T. — moving the static `public/` bundle from local testing into production at `tavci-kuhna.si`.

---

## Pre-flight checklist

Before clicking deploy, run:

```bash
# 1. Verify all external links resolve
python3 tools/verify_links.py

# 2. Audit SEO meta + schema.org JSON-LD
python3 tools/seo_audit.py

# 3. Visual review at three breakpoints
cd public && python3 -m http.server 8000
# Then check: http://localhost:8000 at 360px, 768px, 1280px
```

All three should pass with zero errors before progressing.

---

## Production substitutions to make

These are the items still using preview values. Update before final cloud deploy:

### 1. The embedded Bled-area map iframe

**File:** `public/index.html` ~line 991
**Status:** ✅ FIXED & UPDATED (2026-05-10)
**Current (Production Ready - Directions from Bled):**
```html
<iframe src="https://www.google.com/maps/embed?pb=!1m28!1m12!1m3!1d44051.77850055319!..."
        loading="lazy" title="Directions from Bled to Tavči Kuhna"
        style="border:0;" allowfullscreen=""
        referrerpolicy="no-referrer-when-downgrade"></iframe>
```
The previous hyperagent.com preview link has been replaced with a stable Google Maps embed. No further action needed.

### 2. Self-hosted hero photo for OG/Twitter cards

**Files:** `public/index.html` and `public/menu.html` `<meta property="og:image">`
**Current:** External URLs (HappyCow / tavci-kuhna.si WordPress).
**Replace with:** A 1200×630 JPG uploaded to the production CDN — typically `https://tavci-kuhna.si/og-image.jpg`.

### 3. Self-hosted food and interior photos

**Files:** Both pages — multiple `<img>`, `background-image`, and CSS fallbacks.
**Current:** Lazy-loaded from `images.happycow.net`, `dynamic-media-cdn.tripadvisor.com`, `lh3.googleusercontent.com`, `tavci-kuhna.si/wp-content`.
**Replace with:** Upload originals to `tavci-kuhna.si/wp-content/uploads/website/` and update each URL.

A safe migration script: `tools/build_handoff.py` produces an `image_inventory.json` listing every external image URL with its source — feed that to your CDN-uploader.

### 4. `canonical` link tags

**Files:** Both pages.
**Current:** No `<link rel="canonical">`.
**Add:**
```html
<!-- index.html -->
<link rel="canonical" href="https://tavci-kuhna.si/" />
<!-- menu.html -->
<link rel="canonical" href="https://tavci-kuhna.si/menu" />
```

### 5. Add `sitemap.xml` and `robots.txt`

See `03-seo-and-schema.md` for the templates.

---

## Deploy paths

### A) Netlify / Vercel / Cloudflare Pages (recommended)

1. Create a new Git repo containing this whole project.
2. Set the publish directory to `public/`.
3. Deploy. Done.
4. Point `tavci-kuhna.si` DNS A record (or CNAME) at the host.

### B) Static drop (no Git)

1. Upload `public/index.html` and `public/menu.html` directly via SFTP/FTP to the web root of `tavci-kuhna.si`.
2. The site becomes live immediately.

### C) Replace WordPress (current site)

The current site is WordPress + Elementor at `tavci-kuhna.si`. Two options:

**B.1 Subdomain swap (cleanest, lowest risk):**
- Deploy the new static site to `new.tavci-kuhna.si` first
- Owner reviews
- Once approved, change the DNS A record so `tavci-kuhna.si` → static host, `tavci-kuhna.si/wp-admin` becomes inaccessible (or redirect /wp-admin to a backup subdomain for archives).

**B.2 In-place replace (more work, more risk):**
- Use the WordPress "Headers and Footer Scripts" plugin to inject the JSON-LD blocks
- Recreate the homepage and menu sections as Elementor templates manually — copy the HTML/CSS structure into Elementor's HTML widgets
- Keep the inlined CSS in `<style>` tags

Recommend Option A or B.1.

---

## DNS handover

Owner currently controls the `tavci-kuhna.si` domain. Hand the developer:
1. Domain registrar credentials (or Owner does the DNS swap)
2. Current WordPress hosting account access (to disable the old site or back up)
3. The static `public/` bundle from this project

---

## Post-deploy verification

After the cutover, verify:

- [ ] `https://tavci-kuhna.si/` loads in ≤ 2.5s on 4G mobile (Lighthouse → Performance ≥ 90)
- [ ] `https://tavci-kuhna.si/menu` loads
- [ ] All four primary CTAs work: Wolt, Maps directions, tel, mailto
- [ ] Mobile hamburger nav opens and closes
- [ ] Schema.org validates at https://search.google.com/test/rich-results — both pages should show eligibility
- [ ] Open Graph preview renders correctly at https://www.opengraph.xyz/
- [ ] All images load (no broken icons in DevTools Network tab)
- [ ] Anchor links from homepage category cards land in the right menu sections
- [ ] Google Search Console — submit `sitemap.xml`

---

## Roll-back plan

If anything breaks post-cutover:
1. Revert DNS to the previous WordPress IP (typical TTL = 5 min).
2. Inform owner.
3. Investigate locally before re-attempting.

Keep the WordPress backup for at least 30 days post-cutover.

---

## Maintenance Log entry template

After every meaningful deploy or change, append to `gemini.md` → Self-Annealing Log:

```
- 2026-XX-XX · [what changed] · [why] · [next step if any]
```

Example:
```
- 2026-05-15 · Updated Snickers cake price to €5.50 in menu.html and JSON-LD · Owner confirmed via Wolt update · No next step needed.
```
