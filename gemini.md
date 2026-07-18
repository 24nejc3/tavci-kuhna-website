# Project Map — Tavči Kuhna × Ayatana Website

**Source of Truth · State Tracker · Resume File**

---

## Identity

System Pilot build for **Tavči Kuhna × Ayatana deli** — vegan restaurant, café and deli in Lesce, Slovenia. The deliverable is a static, two-page production website (homepage + menu) ready to deploy in place of the current WordPress site at `tavci-kuhna.si`.

Built under the **B.L.A.S.T.** protocol (Blueprint → Link → Architect → Stylize → Trigger) and the **A.N.T.** 3-layer architecture (Architecture · Navigation · Tools).

---

## 🟢 State

| Phase | Status | Notes |
|---|---|---|
| 0. Initialization | ✅ Done | gemini.md initialized as project map |
| 1. Blueprint | ✅ Done | Discovery answered, schemas defined, SOPs written |
| 2. Link | ✅ Done | All external endpoints verified (Wolt, Maps, social) |
| 3. Architect | ✅ Done | Two HTML pages built; tools/ has verifier + SEO auditor |
| 4. Stylize | ✅ Done | Editorial design — Cormorant Garamond × Inter, alpine palette |
| 5. Trigger | ⏳ Pending owner approval | Cloud deploy to `tavci-kuhna.si` (WordPress replacement) |

**Last meaningful change:** Restructured project from showcase-style artifact into B.L.A.S.T. architecture; HTML moved to `public/` with relative-path navigation; SOPs written; tooling added.
**Next step:** Owner reviews ZIP, confirms `price to confirm` items, hands to a developer for cloud deploy.

---

## 🏗️ Blueprint — Discovery Answers

| Question | Answer |
|---|---|
| **North Star** | A first-time visitor near Bled lands on the homepage and within 5 seconds knows: what this place is, what it serves, where it is, why it's worth visiting, and how to order or get there. |
| **Integrations** | Wolt (delivery), Google Maps (directions + map), Google Business Profile (reviews/photos source), Facebook, Instagram. No write-back integrations — this is a static site that *links to* services, not a backend. |
| **Source of Truth** | Owner-confirmed menu items + prices live on Wolt. Reviews live on Wolt, Google, HappyCow, Tripadvisor. Photos live on Google Business Profile + the existing tavci-kuhna.si WordPress library. The website is the storefront layer that aggregates and presents these. |
| **Delivery Payload** | A static `public/` folder containing `index.html`, `menu.html` and any local assets — drop-in deployable to any static host (Netlify, Vercel, Cloudflare Pages) or extractable into WordPress as static blocks. |
| **Behavioral Rules** | Warm, owner-friendly tone. Vegan-positioned but welcoming to non-vegans. Position "10 min from Bled" loud. Treat GBP reviews as the trust engine. **Never fabricate reviews, prices, dish names, ratings, or history**. Items without confirmed prices stay marked `price to confirm`. Aesthetic: alpine, wooden, generous, food-focused. NOT luxury, NOT generic vegan startup, NOT health-food cliché. |

---

## 📦 Data Schemas

### Input — Menu Item (raw, source: Wolt)

```json
{
  "category": "Burgers",
  "name": "Fungalist burger",
  "price_eur": 15.00,
  "popular": true,
  "description_source": "review_quote | kitchen_confirmed | placeholder",
  "image_url": "https://..."
}
```

### Output — Menu Section Render

```json
{
  "section_id": "burgers",
  "title": "Burgers",
  "note": "prices via Wolt · vegan · gluten-free options",
  "items": [
    {
      "name": "Fungalist burger",
      "tags": ["popular"],
      "description": "Mushroom-forward, deeply savoury — reviewers name this one.",
      "price_display": "€15.00",
      "schema_offer": { "price": "15.00", "priceCurrency": "EUR" }
    }
  ]
}
```

### Input — Trust Signal (raw, source: review aggregators)

```json
{
  "source": "Wolt | Sesezogica | HappyCow | Atly | Wanderlog | Tripadvisor | GaultMillau",
  "rating_value": 9.8,
  "rating_max": 10,
  "review_count": 1454,
  "verbatim_quote": "...",
  "attribution": "Atly · returning customer"
}
```

### Output — Restaurant JSON-LD (rendered into homepage `<script type="application/ld+json">`)

See `public/index.html` lines 30–80 for the full schema.org Restaurant payload, including `aggregateRating` (9.8 / 1454), `openingHoursSpecification`, `geo` (46.3608115, 14.1559427), `sameAs` (Wolt, Facebook, Instagram, HappyCow, Bled tourism), and `menu` (relative URL).

---

## 🔌 External Endpoints (verified in Link phase)

| Service | Endpoint | Purpose |
|---|---|---|
| Wolt (delivery) | `https://wolt.com/sl/svn/bled-lesce/restaurant/tavci-kuhna` | Order CTA, menu source |
| Google Maps | Flexible Directions URL (empty origin) | "Get Directions" CTA |
| Phone | `tel:+38669926772` | Direct dial |
| Email | `mailto:tavcikuhna@gmail.com` | Contact |
| Facebook | `https://www.facebook.com/profile.php?id=100028103306507` | Footer social |
| Instagram | `https://www.instagram.com/tavci_kuhna` | Footer social |
| Bled tourism listing | `https://www.bled.si/en/what-to-see-do/cuisine/catering-facilities/1` | `sameAs` schema entry |

---

## 🧱 A.N.T. Layer Map

| Layer | Lives in | Contents |
|---|---|---|
| **Architecture (L1)** | `architecture/*.md` | SOPs — blueprint, IA, design system, SEO/schema, content rules, deployment |
| **Navigation (L2)** | This file (`gemini.md`) | The reasoning + state log routing data between SOPs and tools |
| **Tools (L3)** | `tools/*.py` | Deterministic Python utilities — link verifier, SEO auditor, handoff bundler |

---

## 📂 Repository Layout

```
tavci-kuhna-site/
├── gemini.md                       # ← you are here · Project Map & State
├── README.md                       # Quick-start for the receiving developer
├── .env.example                    # API-key template (no real secrets)
├── .gitignore
├── public/                         # ← THE DELIVERABLE — deploy this folder
│   ├── index.html                  # Homepage (warm editorial, 88vh hero)
│   └── menu.html                   # Menu page (real Wolt prices)
├── architecture/                   # Layer 1 · SOPs
│   ├── 00-blueprint.md             # Discovery, schemas, behavioral rules
│   ├── 01-information-architecture.md   # Page sections + sticky nav logic
│   ├── 02-design-system.md         # Tokens, typography, components
│   ├── 03-seo-and-schema.md        # Meta tags, schema.org, keyword strategy
│   ├── 04-content-rules.md         # Tone, "do not" list, photo rules
│   └── 05-deployment.md            # Deploy SOP — Netlify / Vercel / WordPress paths
├── tools/                          # Layer 3 · Python scripts
│   ├── verify_links.py             # Crawl public/*.html and HEAD-check every external link
│   ├── seo_audit.py                # Verify SEO meta tags + schema.org JSON-LD validity
│   └── build_handoff.py            # Bundle public/ into a developer-ready ZIP
└── .tmp/                           # Intermediate artefacts (gitignored)
```

---

## 🛡️ Self-Annealing Log

When a tool fails, errors are patched in `tools/`, then the cause is documented here so it doesn't repeat:

- 2026-05-09 · `seo_audit.py` flagged that `<meta name="description">` on both pages exceeded the 170-char recommended cap (200 and 187), and `menu.html` `<title>` was 71 chars (over 70-char cap). · Why it matters: long descriptions get truncated in search snippets and titles get truncated in browser tabs / SERP. · Fix: tightened both descriptions to ~143–144 chars, shortened menu title to 65 chars by dropping "× Ayatana" suffix. · Lesson: run `tools/seo_audit.py` before every publish; SEO meta is easy to bloat when copywriting feels generous.
- 2026-05-10 · Synchronized `menu.html` with the full PDF pricelist. Added new sections for Brunch, Daily Offer, Kids' Menu, Sides, and an exhaustive Drinks & Alcohol list.
- 2026-05-10 · Implemented `Image-SEO-optimization` skill: Converted 35 assets to WebP (quality 80), standardized naming to `tavci-g-[service]-[location]-[descriptor]`, and enforced file-size budgets (Hero < 200KB, Standard < 100KB). Updated `index.html` and `menu.html` with descriptive local SEO alt text and optimized references. Deleted ~15MB of legacy high-res JPGs.
- 2026-05-10 · Replaced broken hyperagent.com map iframe with official Google Maps embed in `index.html`. Per user request, updated it further to specifically show the directions route from Bled to the restaurant and adjusted the zoom level to 11z to show Lake Bled. Updated `architecture/05-deployment.md` SOP.
- 2026-05-10 · Updated all "Get Directions" buttons to use a Google Maps Directions URL with an empty origin (`?api=1&destination=...`). This allows users to input their own starting point or use GPS, improving UX for visitors coming from locations other than Bled. Updated "Get Directions from Bled" text on menu page to "Get Directions".
- 2026-05-10 · Replaced 5 food-focused images in the "Atmosphere" section of `index.html` with interior and seating photos (`interior-hero`, `seating-area`, `cozy-sofa`, `cake-counter`, `product-shelf`) to align with the "Warm wood. Alpine light." messaging. Updated ARIA labels accordingly.
- 2026-05-10 · Performed Advanced Image SEO optimization on 13 new interior assets. Processed images using the Windows long-path prefix (`\\?\`) to handle complex filenames; converted all to WebP (quality 80) and applied `tavci-g-` local SEO naming convention. Replaced 4 images in the `index.html` atmosphere grid with high-fidelity interior, bar, and bakery display shots.
- 2026-05-10 · Enhanced `menu.html` with thematic imagery for every section. Implemented a premium "editorial" layout using a mix of alternating side-images and wide-header visuals. Updated CSS for responsive grid handling and sticky visuals.
- 2026-05-11 · Re-generated and replaced the Google Maps iframe embed code in `index.html` to correctly show the fastest driving route from Bled to Tavči Kuhna. The previous iframe `pb` parameter became invalid/corrupted, resulting in a map load error.
- 2026-05-11 · Translated lingering Slovenian words across `menu.html` to English (e.g., drinks, desserts, and sides) for a cohesive user experience. Also extracted the "Smoothies" from just the Brunch section and gave them their own dedicated sub-category under Drinks so they aren't missed.
- 2026-05-12 · Integrated native scroll-stop decomposing hero video animation using high-precision HTML5 video scrubbing mapped to a top-level canvas frame renderer in `index.html`. Maintained the original background image as an instant-loading base state before video overlay triggers. Configured graceful opacity transitions on the hero text block to ensure an unhindered visual view of the floating food array upon scrolling. Added `tavci-feast-deconstruction.mp4` to `public/assets/video/`.
- 2026-05-13 · Implemented the Scroll-Stop Builder Skill for the signature plant-based burger directly inside the unified landing Hero section. Merged the primary landing visuals and content block as an absolute overlay above the exploding burger layers `<canvas>`. Optimized the HTML5 video scrubbing engine by quantizing seek timestamp targets to discrete 25fps intervals, completely eliminating decoder stuttering/lag during fast scrolling. Included snap-stop progress zones with staccato read pauses for 3 distinct custom-styled glassmorphic annotation cards detailing the bun, patty/cheeze, and fresh crisp layers.

---

## ✅ Maintenance Checklist (post-launch)

- [x] Replace `price to confirm` items in `menu.html` with real prices once owner confirms (Updated 2026-05-10 from PDF)
- [x] Replace embedded Bled-area iframe (line ~991 of `index.html`) with a Google Maps embed for production (Fixed 2026-05-10)
- [ ] Re-host the food/interior images on tavci-kuhna.si CDN (currently lazy-loaded from HappyCow / Tripadvisor / existing site)
- [ ] Add Open Graph image `og:image` once a hero photo is uploaded to the production CDN
- [ ] Verify `aggregateRating` count once per quarter; current: 9.8 / 1454 (Sesezogica baseline)
- [ ] When prices change on Wolt, run `python tools/verify_links.py` and update `menu.html` accordingly
