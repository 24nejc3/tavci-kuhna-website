# SOP 00 — Blueprint

> **Layer 1 · Architecture.** Defines the project's North Star, discovery answers, payload shape, and behavioural rules. If logic changes, **update this file before updating any code.**

---

## North Star (singular outcome)

A first-time visitor near Bled lands on the homepage and within five seconds knows:

1. What this place is (vegan restaurant, café, deli)
2. What it serves (burgers, falafel, cakes, kombucha, deli goods)
3. Where it is (Lesce, 10 minutes from Lake Bled)
4. Why it's worth visiting (real customer love — Wolt 9.8, 1,454 reviews)
5. How to act (View Menu · Get Directions · Order on Wolt · Call)

Every section above the fold serves one of these five answers. Anything else gets demoted or cut.

---

## Discovery — confirmed answers

| Field | Answer |
|---|---|
| Singular outcome | Convert "vegan restaurant near Bled" search traffic + GBP visitors into menu views, calls, directions, and Wolt orders. |
| Integrations | Wolt, Google Maps, Facebook, Instagram, Google Business Profile (read-only — photos and reviews) |
| Source of Truth | Owner-confirmed menu lives on Wolt. Reviews live on Wolt + Sesezogica + HappyCow + Atly + Tripadvisor + Wanderlog + Gault&Millau. Photos live on GBP + the existing tavci-kuhna.si WordPress library. |
| Delivery payload | A static `public/` folder of two HTML files + inlined CSS + external font links — drop-in deployable. |
| Behavioural rules | See `04-content-rules.md`. The short version: no fabrication, warm tone, alpine aesthetic, position "10 min from Bled" loud, treat GBP/Wolt as trust engine. |

---

## Payload shape — input

### Menu items (raw, source: Wolt)
```json
{
  "category": "Burgers | Wraps · Gyros · Falafel | Salads & Bowls | Cakes & Desserts | Drinks & Deli",
  "name": "Fungalist burger",
  "price_eur": 15.00,
  "popular": true,
  "description_source": "review_quote | kitchen_confirmed | placeholder",
  "image_url": "https://..."
}
```

### Trust signals (raw, source: review aggregators)
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

---

## Payload shape — output

### Rendered menu section
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

### Rendered trust strip (homepage)
```json
{
  "rating": { "value": "9.8", "label": "Wolt rating" },
  "quote": { "text": "...", "attribution": "..." },
  "signals": ["★★★★★ 1,454 local reviews", "Featured in Gault&Millau", "Listed by Bled Tourism"]
}
```

---

## Confirmed real menu data (Wolt, snapshot)

| Item | Price | Tags |
|---|---|---|
| Amaze burger | €13.50 | — |
| Mr. Bean Protein burger | €14.00 | description placeholder |
| Fungalist burger | €15.00 | Popular |
| Yo Soy Chicken burger | €12.50 | Popular |
| BBQ Cheezy burger | €14.00 | — |
| Shroomzee burger | €14.50 | — |

Items appearing in reviews but unconfirmed for price (e.g. wraps, gyros, falafel, all cakes, kombucha, lemonades, coffee, Ayatana ferments) are marked `price to confirm` until owner verifies.

---

## "Coding only begins once the payload is confirmed"

This was confirmed before any HTML was written. The two pages in `public/` strictly render content that conforms to the schemas above. No inferred prices. No invented dishes. No paraphrased reviews.
