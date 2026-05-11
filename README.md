# Tavči Kuhna × Ayatana — Website (Homepage + Menu)

A production-ready static website for **Tavči Kuhna × Ayatana deli** — vegan restaurant, café and deli in Lesce, Slovenia, ten minutes from Lake Bled.

**Built under the B.L.A.S.T. protocol.** See `gemini.md` for the project map.

---

## 🚀 Quick Start (developer)

```bash
# 1. Preview locally
cd public
python3 -m http.server 8000
# → open http://localhost:8000

# 2. Verify all external links resolve (Wolt, Maps, social)
python3 tools/verify_links.py

# 3. Audit SEO meta + schema.org JSON-LD
python3 tools/seo_audit.py

# 4. Bundle for deployment
python3 tools/build_handoff.py
# → produces .tmp/tavci-kuhna-handoff.zip
```

---

## 📁 What's in the box

| Path | Purpose |
|---|---|
| `public/` | **The deliverable.** Deploy this folder. |
| `public/index.html` | Homepage — hero, trust strip, categories, near-Bled, cakes, atmosphere, about, visit, footer |
| `public/menu.html` | Menu page — featured items, all 6 burgers (real Wolt prices), wraps/gyros/falafel, salads, cakes, drinks |
| `gemini.md` | Project map — state, schemas, blueprint, endpoint registry |
| `architecture/` | SOPs for design, IA, SEO, content rules, and deployment |
| `tools/` | Python utilities for verification and handoff |

---

## 🛠️ Deploy Options

The site is a pure static HTML bundle — no build step required.

### Netlify / Vercel / Cloudflare Pages
Drop the `public/` folder into a deploy. Done.

### WordPress (replacement for current tavci-kuhna.si)
The current site runs WordPress + Elementor. Two options:
1. **Cleanest:** export the static `public/` files to a hosting subdomain, then point `tavci-kuhna.si` at it via DNS.
2. **In-place:** replicate the `index.html` and `menu.html` markup into custom Elementor templates. The CSS is fully inlined in `<style>` tags so it travels with the page.

Full deploy SOP: `architecture/05-deployment.md`

---

## ⚠️ Critical Rules (do not break)

- **Never invent menu items, prices, reviews, ratings, history, or awards.** All current content was sourced from real Wolt / GBP / review-platform data.
- Items currently marked `price to confirm` must be filled in by the owner before launch — do not guess.
- The map iframe in `index.html` (~line 986) is a placeholder live artifact — replace with a Google Maps embed for production. See `architecture/05-deployment.md`.
- Reviews quoted on the homepage and in trust signals are **real, attributed, verbatim** quotes from Wanderlog, Atly, Tripadvisor, and Gault&Millau. Do not edit the wording.

---

## ✅ What's already production-ready

- ✅ Real food/interior photos from GBP, HappyCow, Tripadvisor lazy-loaded
- ✅ Real menu prices for all 6 burgers (€12.50–€15) sourced from Wolt
- ✅ Wolt order CTA, phone CTA, Maps directions CTA, email CTA wired
- ✅ Real Facebook + Instagram links in footer
- ✅ Schema.org Restaurant markup with `aggregateRating`, `openingHoursSpecification`, `geo`, `sameAs`
- ✅ Schema.org Menu markup with all six burger prices as structured `Offer` data (Google can lift these straight to rich results)
- ✅ Open Graph + Twitter card meta on both pages
- ✅ Sticky responsive nav, mobile hamburger toggle, smooth-scroll category jumping
- ✅ Editorial typography (Cormorant Garamond × Inter), alpine palette, Kinfolk-magazine restraint

---

## 🔄 Maintenance Loop

After post-launch changes (e.g. menu price update on Wolt):

1. Update the relevant section in `public/menu.html` (and the JSON-LD `Offer` block at the top).
2. Run `python3 tools/verify_links.py` to catch any link rot.
3. Run `python3 tools/seo_audit.py` to re-validate the schema markup.
4. Add a 1–3 line entry to the **Self-Annealing Log** in `gemini.md` describing what changed.

---

## 📞 Owner Contact (verified)

- **Tavči Kuhna × Ayatana deli** — Alpska cesta 43C, 4248 Lesce, Slovenia
- **Phone:** +386 69 926 772
- **Email:** tavcikuhna@gmail.com
- **Hours:** Mon–Sun 11:00–20:00 (Tuesday closed)
- **Wolt:** https://wolt.com/sl/svn/bled-lesce/restaurant/tavci-kuhna
- **Facebook:** https://www.facebook.com/profile.php?id=100028103306507
- **Instagram:** https://www.instagram.com/tavci_kuhna
