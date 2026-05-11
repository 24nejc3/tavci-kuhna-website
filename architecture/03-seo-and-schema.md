# SOP 03 — SEO & Schema.org

> **Layer 1 · Architecture.** Meta tags, structured data, keyword strategy. Both pages have distinct titles and descriptions tuned for the local Bled/Lesce market. Don't over-optimise — the rule is "natural language with intent words present."

---

## Target search intents

| Intent | Lands on | Priority |
|---|---|---|
| "vegan restaurant near Bled" | `/` | ★★★★★ |
| "vegan food Lesce" | `/` | ★★★★ |
| "plant-based food Bled" | `/` | ★★★★ |
| "vegan burgers near Bled" | `/menu#burgers` | ★★★★ |
| "vegan cakes near Bled" | `/menu#cakes` | ★★★★ |
| "vegan lunch near Bled" | `/` | ★★★ |
| "vegan takeaway Lesce" | `/menu` | ★★★ |
| "Tavči Kuhna" (brand) | `/` | ★★★★★ |

These keywords appear naturally in headings, body copy, and `alt` text — never stuffed.

---

## Page meta

### Homepage (`index.html`)

```html
<title>Tavči Kuhna × Ayatana — Vegan Restaurant Near Bled | Lesce, Slovenia</title>
<meta name="description" content="Plant-based comfort food, cakes, and deli favourites in Lesce — 10 minutes from Lake Bled. Burgers, falafel, gyros, wraps, salads, and the famous Snickers cake. Wolt 9.8. Open Mon–Sun, Tuesday closed." />
```

### Menu page (`menu.html`)

```html
<title>Menu — Vegan Burgers, Falafel & Cakes Near Bled | Tavči Kuhna × Ayatana</title>
<meta name="description" content="Real Wolt-priced menu: vegan burgers from €12.50, homemade falafel, gyros, wraps, salads, and the famous Snickers cake. In Lesce, 10 minutes from Lake Bled. Open Mon–Sun (Tuesday closed)." />
```

---

## Open Graph + Twitter Card

Both pages set:
- `og:type` (`restaurant.restaurant` for home, `restaurant.menu` for menu)
- `og:title`, `og:description`, `og:image`, `og:url`, `og:site_name`, `og:locale: en_GB`
- `twitter:card: summary_large_image`
- `twitter:title`, `twitter:description`, `twitter:image`

`og:image` currently uses real GBP / Tavči-site photo URLs. **For production**, swap to a self-hosted hero photo at `https://tavci-kuhna.si/og-image.jpg` (1200×630).

---

## Schema.org JSON-LD

### Homepage — `Restaurant`

Located at the top of `<head>` in `index.html`:
```json
{
  "@context": "https://schema.org",
  "@type": "Restaurant",
  "name": "Tavči Kuhna × Ayatana deli",
  "alternateName": "Tavci Kuhna",
  "image": [...],
  "url": "https://tavci-kuhna.si",
  "telephone": "+38669926772",
  "email": "tavcikuhna@gmail.com",
  "priceRange": "€€",
  "servesCuisine": ["Vegan", "Plant-based", "Deli", "Café"],
  "address": { "@type": "PostalAddress", ... },
  "geo": { "@type": "GeoCoordinates", "latitude": 46.3608115, "longitude": 14.1559427 },
  "openingHoursSpecification": [...],
  "menu": "/menu",
  "acceptsReservations": "True",
  "hasMap": "...",
  "sameAs": [...],
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "9.8",
    "ratingCount": 1454,
    "reviewCount": 1454
  }
}
```

### Menu page — `Menu` + `MenuSection` + `MenuItem`

Located at the top of `<head>` in `menu.html`. Includes all six burgers as structured `Offer` data with EUR prices. Google can lift these directly into rich results (carousel of menu items with prices).

---

## Validation

Before deploy, validate the JSON-LD using:
- **Google's Rich Results Test:** https://search.google.com/test/rich-results
- **Schema.org Validator:** https://validator.schema.org/

Or run `python3 tools/seo_audit.py` which extracts the JSON-LD blocks and checks them for parseability + required fields.

---

## Image alt text rules

- Be specific: `"Fungalist burger — vegan mushroom burger"` not `"image of food"`.
- Decorative-only background images use `role="img"` with descriptive `aria-label` attributes.
- Keep alt under ~120 characters.
- Include keywords naturally (e.g. `"Tavči Kuhna interior"` instead of just `"interior"`) — but only when accurate.

---

## Sitemap & robots

A static sitemap is not yet shipped. **For production**, add `public/sitemap.xml` and `public/robots.txt`:

```xml
<!-- sitemap.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://tavci-kuhna.si/</loc><priority>1.0</priority></url>
  <url><loc>https://tavci-kuhna.si/menu</loc><priority>0.9</priority></url>
</urlset>
```

```
# robots.txt
User-agent: *
Allow: /
Sitemap: https://tavci-kuhna.si/sitemap.xml
```

---

## What NOT to do

- Don't keyword-stuff. "Vegan restaurant near Bled" should appear naturally 1–2 times per page, not 10.
- Don't add hidden text or off-screen keyword blocks.
- Don't fabricate review counts. The `aggregateRating` value (9.8) and count (1454) come from Sesezogica.si and are real. If the count changes, update both the JSON-LD and the visible "1,454 local reviews" string.
- Don't use `og:image` URLs that may break — host the image yourself when ready.
