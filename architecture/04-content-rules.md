# SOP 04 — Content Rules

> **Layer 1 · Architecture.** Tone, language, fabrication safeguards. The single most important SOP. **If in doubt, defer to this file.**

---

## Tone

Speak to first-time visitors, not to industry insiders or vegan purists. Warm, generous, locally rooted. Confident but unshouty. The voice of a small alpine deli that takes its food seriously and its mood lightly.

**Reference voices:** Kinfolk magazine columns, neighbourhood café chalkboard, a friend telling you where to eat.

**Examples that pass:**
- "Plant-based comfort food, worth the short trip from Bled."
- "Burgers, falafel, gyros, wraps, salads — and a cake counter that locals and travellers cross the valley for."
- "The address says 'industrial zone' — and it's true, technically. But the moment you step inside, it's a warm wooden alpine café and deli with free parking right at the door."

**Examples that don't pass:**
- "Discover our amazing 100% authentic vegan culinary experience" ❌ (industry jargon)
- "We are a leading vegan restaurant" ❌ (corporate)
- "Healthy, mindful, sustainable cuisine" ❌ (health-food cliché)

---

## Language register

- British/European English throughout (`favourites`, `flavour`, `colour`).
- `tavci-kuhna.si` is `.si` — keep `og:locale` as `en_GB`.
- Decimal prices use `€13.50` (not `13,50` despite Slovenian convention) because Wolt displays them this way.
- Currency symbol always before the number (`€15.00`).

---

## "Do Not" rules — hard

| Never | Because |
|---|---|
| Invent reviews, ratings, awards, dish names, prices, history | Falsifies the trust engine the whole site rests on |
| Quote a review you can't link to | Cites must be attributable to a real source (Wanderlog, Atly, Tripadvisor, Gault&Millau, etc.) |
| Use "luxury", "exclusive", "premium" framing | Not the brand — alpine deli, not Michelin |
| Use "100% authentic" / "true Slovenian" / nation-myth phrasing | Not how the kitchen describes itself |
| Add a "Subscribe — 25% off" newsletter form | Never confirmed live on existing site, dropped from this build |
| Claim Michelin, Gault&Millau stars, or awards beyond the verified Gault&Millau write-up | Verified facts only |
| Translate review quotes — keep them verbatim in the language they were written | Translations risk silent paraphrase |
| Use generic AI-art images (glowing particles, neon, sci-fi tropes) | Aesthetic violation per design system |
| Bake the embedded artifact iframe URL into final production deploy | It's a placeholder map; replace with Google Maps embed before launch |

---

## "Do Not" rules — soft (defaults that may be overridden by owner)

| Default | Override path |
|---|---|
| Items without confirmed price → `price to confirm` placeholder | Owner provides price → update both visible string AND JSON-LD `Offer` |
| `og:image` uses real GBP photo URL | Owner uploads a 1200×630 hero to tavci-kuhna.si CDN → swap |
| Reservation = `tel:` link to phone | Owner adds a real reservation system → swap with form/embed |

---

## Quote attribution rules

When quoting a review on the page:
1. **Always wrap in `<blockquote>`** with `<cite>` for attribution.
2. **Keep the quote verbatim.** Do not paraphrase. Trim with `[...]` only if needed.
3. **Attribute to the platform**, not the user (e.g. "Atly · returning customer", not the username).
4. **Star icons (★★★★★)** are decorative — they reflect the rating but are not part of the quote.

Real quotes used in the build (with attribution):
- Wanderlog — "One of the best vegan restaurants where I have ever eaten…"
- Tripadvisor — "We took two slices of Snickers cake away…"
- Atly — "A fantastic location — 10 minutes from Lake Bled…"
- Atly (returning customer) — "Great food. Everything vegan, lots of gluten-free options…"
- Find Me Gluten Free — "Delightful vegan restaurant. The food is delicious and the staff is extremely kind…"
- Gault&Millau — "In Gorenjska, there are very few places that exclusively serve plant-based dishes…"

---

## Photo rules

- Real photos beat AI mockups for trust signals. Use HappyCow / GBP / Tripadvisor / existing tavci-kuhna.si library.
- AI-generated visuals are acceptable ONLY for things that don't yet exist in real photos: packaging concepts, future cake-box designs, brand mockups. Mark them clearly.
- Never compose a photo that misrepresents the restaurant (e.g. a luxurious tablescape that doesn't match the actual interior).
- All photos must have descriptive `alt` attributes — see SOP 03.

---

## "Near Bled" framing

Position language consistently:
- ✅ "10 minutes from Lake Bled"
- ✅ "Worth the short trip from Bled"
- ✅ "Just outside Bled"
- ✅ "Quiet next-door neighbour to Bled"
- ❌ "5 minutes from Bled" (false — it's ~10)
- ❌ "In Bled" (false — Lesce is a separate town)
- ❌ "Closer than you think" (vague, weakens the message)

The 10-minute drive is the differentiator — it's quieter than central Bled, has free parking, and has a 9.8 Wolt rating because tourists who make the trip are happy. Lean into that, don't apologise for it.

---

## When in doubt

Read this file first, then `00-blueprint.md`. If both are silent, ask the owner. **Do not invent.**
