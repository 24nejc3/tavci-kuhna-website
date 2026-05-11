# SOP 02 — Design System

> **Layer 1 · Architecture.** Tokens, typography, components. Both pages share these tokens — change them in one place (`:root` block) and both pages update.

---

## Visual direction

**Warm editorial × design.** Reference benchmarks: Kinfolk magazine, Cereal magazine, The Gentlewoman, Dieter-Rams-restraint via Apple. Generous whitespace. Refined typography. Cream backgrounds. Forest-green and warm-wood accents. Natural-light photography.

**What we are NOT:** luxury restaurant, generic vegan startup, sterile health-food clichés, neon/cyberpunk, AI-art tropes (no glowing particles, no orbs, no sci-fi).

---

## Colour tokens

Defined in `:root` of both pages. Edit there to recolour the site.

| Variable | Hex | Role |
|---|---|---|
| `--paper` | `#fbf7ee` | Default page background |
| `--cream` | `#f6f1e7` | Card surfaces, sections that need lift |
| `--cream-dark` | `#ece4d3` | Subtle gradient end |
| `--ink` | `#2b2a26` | Primary text |
| `--ink-soft` | `#4a4842` | Body copy on cream |
| `--muted` | `#7d786e` | Captions, eyebrows, "price to confirm" |
| `--forest-deep` | `#2c421d` | Headers, dark bands, primary CTAs |
| `--forest` | `#3f5d2a` | Logo accent, link hover |
| `--moss` | `#6b8a4c` | Eyebrow keyword tags, decorative borders |
| `--terracotta` | `#b85c3a` | Kickers (Caveat script), "Popular" badges, cakes section |
| `--bled-blue` | `#527a93` | "Near Bled" kicker only |
| `--gold` | `#b88a3d` | Accent — sparingly |
| `--line` | `#d8cfb8` | Borders, dividers |
| `--wolt` | `#00c2e8` | Wolt CTA button (matches Wolt brand) |

---

## Typography

| Use | Font | Weight | Notes |
|---|---|---|---|
| Display (h1, h2, h3) | **Cormorant Garamond** | 500–600 | Italic variants used for emphasis (`<em>`) |
| Body, nav, buttons, captions | **Inter** | 300–700 | System fallback: `system-ui, sans-serif` |
| Kickers, decorative labels | **Caveat** | 500 | Used only for the small handwritten labels (e.g. "the menu", "step inside") |

Loaded via `<link>` from Google Fonts with `display=swap`. `preconnect` is set on both pages to reduce font-fetch latency.

**Headline scale uses `clamp()`** for fluid responsive sizing — e.g. `clamp(40px, 6vw, 80px)` on the homepage hero. Headlines will scale smoothly between mobile and ultrawide.

---

## Component library

All components are scoped via class selectors in the inline `<style>` block. Shared between `index.html` and `menu.html`.

| Component | Class | Used on |
|---|---|---|
| Utility bar | `.utility-bar` | Both |
| Sticky main nav | `.site-header` + `.site-nav` | Both |
| Logo | `.logo` (with `<em>` for italic accent) | Both |
| Buttons (primary) | `.btn .btn-primary` | Both |
| Buttons (ghost) | `.btn .btn-ghost` | Both |
| Buttons (Wolt cyan) | `.btn .btn-wolt` | Both |
| Buttons (dark on cream) | `.btn .btn-dark` | Both |
| Buttons (line) | `.btn .btn-line` | Both |
| Hero badge | `.badge` | Both |
| Eyebrow text | `.eyebrow` | Both |
| Script kicker | `.kicker` | Both |
| Trust strip | `.trust-strip` | Homepage |
| Category card | `.cat` | Homepage |
| Featured menu card | `.menu-card` | Menu |
| Menu list item | `.menu-item` | Menu |
| Section block | `.menu-section-block` (+ `.alt` for cream variant) | Menu |
| Footer | `.site-footer` + `.footer-grid` | Both |

---

## Spacing system

| Token | Value | Use |
|---|---|---|
| Section padding | `100px 0` (desktop) / `70px 0` (mobile <980px) | Major sections |
| Section padding tight | `50px 0` | Compact strips (delivery hours note) |
| Wrap max width | `min(1180px, 92vw)` | Default container |
| Narrow wrap max width | `min(820px, 92vw)` | About / closing copy |

---

## Image guidelines

- All `<img>` tags carry `alt` attributes (real, descriptive — not "image of X").
- Below-the-fold images use `loading="lazy"`.
- Atmosphere/Cakes collages use CSS `background-image` with `background-size: cover` to crop responsively.
- For production deploy: replace third-party hostnames (HappyCow / Tripadvisor / lh3.googleusercontent.com) with self-hosted CDN URLs once the team uploads the photos to tavci-kuhna.si — see `05-deployment.md`.

---

## Icon system

Inline SVG icons in the footer social row. Three icons, each as a self-contained `<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">` — no icon font needed:
- Facebook · `M22.675 0H1.325...`
- Instagram · `M12 2.163...`
- Map pin · `M12 2C8.13...`

Hover state inverts colours via the `.socials a:hover` rule.

---

## Mobile-first approach

- Hamburger nav appears at `max-width: 900px` (menu page) / `980px` (homepage)
- 7-column category grid collapses to 3 columns at 980px and 2 columns at 600px
- Trust strip's 3-column layout collapses to a vertical stack at 980px
- Atmosphere collage's 2-row asymmetric grid becomes a 2-column flat grid at 980px
- Visit-Us 2-column grid stacks at 980px

Test at: 360px, 768px, 1024px, 1280px, 1920px.
