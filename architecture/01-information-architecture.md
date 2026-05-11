# SOP 01 — Information Architecture

> **Layer 1 · Architecture.** Page structure, section order, sticky nav logic. Update this file *before* re-ordering anything in HTML.

---

## Site map

```
/                              ← index.html  · Homepage
/menu                          ← menu.html   · Menu page
```

Future Phase 2 pages (described in showcase, not yet built):
```
/vegan-restaurant-near-bled    ← landing for tourists
/cakes                         ← dessert program
/about                         ← Ayatana partnership + team
/wolt-delivery                 ← delivery-focused landing
/visit                         ← contact + map
```

---

## Shared chrome (both pages)

1. **Utility bar** (forest-deep) — address · hours · phone · email — small, scrollable away
2. **Sticky main nav** (cream/blur backdrop) — logo · Home · Menu · About (anchor) · Visit (anchor) · Order on Wolt (CTA pill)
3. **Footer** (forest-deep) — brand block · visit info · order/connect · social row + copyright

Mobile: nav collapses behind a hamburger toggle (vanilla JS — no framework).

---

## Homepage section order (`index.html`)

1. **Hero** — full-bleed photo, badge ("Vegan · Lesce · 10 min from Bled"), big italic headline, lede paragraph, three CTAs (View Menu · Get Directions · Order on Wolt). `min-height: 88vh`.
2. **Trust strip** — forest-deep band, three columns: Wolt 9.8 · real Wanderlog quote · review count + Gault&Millau + Bled Tourism signals.
3. **Categories** — kicker + headline, 7 category cards (Burgers · Wraps · Gyros · Falafel · Salads · Cakes · Drinks), each linking to the corresponding `menu.html#anchor`.
4. **Near Bled** — text + embedded interactive map iframe. Includes audience pills (Tourists / Locals / Hikers / Cyclists / Families / Vegans & non-vegans) and a real Atly review pull-quote.
5. **Cakes moment** — stacked image collage + Snickers cake review quote.
6. **Atmosphere collage** — 5-photo grid of real GBP/HappyCow shots.
7. **About** (`#about`) — narrow narrative paragraph, then the Ayatana × note in a card.
8. **Visit Us** (`#visit`) — forest-deep band, two columns: narrative + Atly quote / info card with address, hours, phone, email, "from Bled" + 3 stacked CTAs.
9. **Final CTA** — kicker + headline + 3 CTAs.
10. **Footer** (shared)

**Anchor IDs that the nav links to:** `#about`, `#visit`. Smooth scroll via CSS `scroll-behavior: smooth` + `scroll-padding-top: 120px` to clear the sticky nav.

---

## Menu page section order (`menu.html`)

1. **Menu hero** — full-bleed photo, kicker + headline + paragraph, two CTAs (Order on Wolt · Get Directions from Bled).
2. **Sticky category sub-nav** — anchor links: Burgers · Wraps · Gyros · Falafel · Salads · Cakes · Drinks. Sticky beneath the main nav.
3. **Featured items** — 3 popular cards (Fungalist · Yo Soy Chicken · Falafel) with photos, descriptions, prices.
4. **Burgers** (`#burgers`) — all 6 with real Wolt prices.
5. **Wraps · Gyros · Falafel** (`#wraps-gyros`) — items mentioned in reviews; prices `to confirm`.
6. **Salads & Bowls** (`#salads`) — placeholder items; full lineup to confirm.
7. **Cakes & Desserts** (`#cakes`) — Snickers, Tropicana, Oreo, vegan cream cake; prices `to confirm`.
8. **Drinks & Deli** (`#drinks`) — Kombucha on tap, lemonades, coffee, Ayatana ferments.
9. **Order strip** — forest-deep band, 3 CTAs (Wolt · Call · Directions).
10. **Delivery hours note** — small, narrow, clarifies Wolt vs dine-in hours.
11. **Footer** (shared)

**Sticky-nav offset:** menu page has TWO sticky bars stacked (main nav + category sub-nav), so `scroll-padding-top: 130px` on the menu page (vs 120px on homepage).

---

## Conversion paths

Every page has at least these four exit ramps within reach (above-fold and in footer):

| Intent | CTA target |
|---|---|
| "Show me the food" | `menu.html` |
| "How do I get there" | Long Google Maps directions URL |
| "Let me order now" | `https://wolt.com/sl/svn/bled-lesce/restaurant/tavci-kuhna` |
| "Let me call" | `tel:+38669926772` |

The nav, hero, "Visit Us" card, and final CTA strip all repeat at least three of these four. No conversion path requires more than one tap.

---

## Anchor link behaviour

- Homepage category card click → `menu.html#burgers` (etc.) — opens menu page and scrolls to that section.
- Menu category-nav link click → smooth-scrolls within the same page.
- Footer "Back to homepage" / "View the menu" → cross-page navigation.

When updating an anchor ID, search both `public/index.html` and `public/menu.html` for the old ID and update consistently — anchor links break silently.
