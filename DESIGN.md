---
name: Manan Bhullar Real Estate
description: A dual residential/commercial REALTOR® site built on restraint — one accent, sharp corners, real facts only.
colors:
  ink: "#121212"
  ink-soft: "#4A4A4A"
  paper: "#FAFAF8"
  paper-raised: "#FFFFFF"
  accent: "#1E5FD9"
  accent-deep: "#164FB8"
  accent-on-dark: "#5B8AF0"
  line: "#E4E2DD"
  line-soft: "#EDEBE6"
typography:
  display:
    fontFamily: "'General Sans', sans-serif"
    fontSize: "2.5rem"
    fontWeight: 700
    lineHeight: 1.15
  headline:
    fontFamily: "'General Sans', sans-serif"
    fontSize: "1.9rem"
    fontWeight: 700
  body:
    fontFamily: "'General Sans', sans-serif"
    fontSize: "16px"
    lineHeight: 1.55
rounded:
  none: "0px"
spacing:
  section: "80px"
  section-tight: "56px"
components:
  button-primary:
    backgroundColor: "{colors.accent}"
    textColor: "#ffffff"
    padding: "14px 24px"
  button-primary-hover:
    backgroundColor: "{colors.accent-deep}"
  button-outline:
    backgroundColor: "transparent"
    textColor: "#ffffff"
    padding: "14px 24px"
---

# Design System: Manan Bhullar Real Estate

## Overview

**Creative North Star: "The Property Brief"**

This is a site built to read like a well-organized, trustworthy briefing document, not a sales brochure. Off-white paper, near-black ink, a single confident blue used sparingly, and sharp, undecorated rectangles throughout — the visual system gets out of the way of the facts (benchmark prices, due-diligence checklists, FAQs written the way people actually search). Every corner on the site is a hard 90°; there is no radius token in use anywhere in the codebase, and that is deliberate, not an oversight.

The palette was explicitly pared down from an earlier two-tone red/blue, warm/cool scheme — the client found it busy — and a later pitch for a SaaS-style dark navy/indigo/gold identity was proposed and then declined. Both departures were considered and rejected in favor of the current restraint. That history makes the single-accent rule a confirmed decision, not an unexplored option.

Dark sections (hero, nav, footer, closing CTAs) alternate with light and raised sections through every page for rhythm — a page that stays one shade for its whole length is a defect, not a style (see Why Manan page fix, this session).

**Key Characteristics:**
- One accent blue, used deliberately and sparingly — never a second hue competing for attention
- Hard, sharp corners everywhere — no `border-radius` anywhere in the stylesheet
- Off-white paper over pure white for body backgrounds; pure white reserved for raised cards/forms sitting on a gray or dark section
- Alternating light/raised/dark section rhythm down every page
- One typeface (General Sans) for everything, including what a legacy `--serif` variable name still calls "serif" — it isn't; the alias is legacy naming, not a real serif face
- No monospace anywhere — removed site-wide per explicit client request; never reach for one on new digit-heavy elements (phone numbers, calculator results, stats)

## Colors

A near-monochrome neutral palette (off-white paper, near-black ink) with exactly one accent hue in two weights, plus a third accent step reserved for text-on-dark contexts where the base accent fails contrast.

### Primary
- **Signal Blue** (`#1E5FD9` / `--accent`): solid button fills, large heading accent spans, theme-color meta. The brand's one moment of color.
- **Signal Blue, Deep** (`#164FB8` / `--accent-deep`): hover state for solid buttons; also the default link/icon color on light and raised backgrounds, where the base Signal Blue runs slightly light.

### Neutral
- **Ink** (`#121212` / `--ink`): primary text color; also the fill for dark sections (hero, nav, footer, closing CTA bands).
- **Ink, Soft** (`#4A4A4A` / `--ink-soft`): secondary/supporting text on light backgrounds.
- **Paper** (`#FAFAF8` / `--paper`): default page background. Off-white, not pure white — pure white is reserved for raised elements.
- **Paper, Raised** (`#FFFFFF` / `--paper-raised`): cards, forms, and any element that needs to lift off the paper background or off a gray `raised` section.
- **Line** (`#E4E2DD` / `--line`): borders, dividers, card outlines.
- **Line, Soft** (`#EDEBE6` / `--line-soft`): the fill for `.raised` section backgrounds and light-mode icon tiles.
- **Signal Blue, On Dark** (`#5B8AF0` / `--accent-on-dark`): a lighter accent step for text and links that must sit directly on an ink-black background, where the base Signal Blue's contrast runs too low for small text.

### Named Rules
**The One Accent Rule.** Signal Blue is the only hue on the site besides neutrals. It was chosen after two more colorful alternatives were built and rejected by the client as "too busy" — do not propose a second accent color without that context in mind.

**The Off-White Rule.** Page backgrounds are `--paper` (#FAFAF8), never pure white. Pure white (`--paper-raised`) is reserved for elements that need to visually lift off the page.

## Typography

**Display / Body Font:** 'General Sans', sans-serif (the only typeface on the site)

**Character:** A single confident grotesque doing every job — headlines, body copy, labels, and (via a legacy CSS variable name, `--serif`) even where "serif" is referenced in code. There is no second typeface anywhere, and no monospace font anywhere; digit-heavy content (phone numbers, calculator results, price stats) uses the same sans as everything else.

### Hierarchy
- **Display** (700, 2.5rem, drops to 1.9rem under 700px): hero `<h1>` on subhero/hero sections, white on dark backgrounds.
- **Headline** (700, 1.9rem): standard `<h2>` inside content sections.
- **Body** (400, 16px base, 1.55 line-height): running paragraph text.
- **Label/Eyebrow** (500, 0.78rem, uppercase, 0.02em letter-spacing): the small badge-style label above a heading — see the Eyebrow Badge component below.

### Named Rules
**The No-Mono Rule.** IBM Plex Mono was fully removed site-wide per explicit client request, who called it "ugly digital style." Never reach for a monospace font on any new UI element, however digit-heavy.

## Layout

Sections stack vertically at `80px` top/bottom padding (`.content-section`), or `56px` for a `.tight` variant. Each section is full-bleed with its own background color; content is constrained by a `.wrap` max-width container. Two-column layouts (`.two-col`) use a `56px` gap grid, collapsing to one column under ~860px.

Section backgrounds alternate deliberately down a page: dark (`.dark`, `--ink` fill, white text) → light (default `--paper`) → raised (`.raised`, `--line-soft` fill, for visual separation from a plain section without going fully dark) → back to dark for closing CTAs. A page that stays one background for its entire length breaks this rhythm and should be treated as a defect.

Grid layouts use CSS Grid with `fr` units; any grid item containing an `<img>` with HTML `width`/`height` attributes must carry `min-width:0` (a blanket rule already covers `[class*="grid"] > *` and a short list of named grid classes) or the image's intrinsic size can blow out the track — this has caused two real, shipped bugs on this site.

## Elevation & Depth

Mostly flat. The system does not use shadows as a general elevation language — most cards, buttons, and sections rely on background color and hairline borders (`--line`) for separation, not drop shadows. The few `box-shadow` uses on the site are narrow exceptions for floating/overlay-like elements (a sticky search-note tooltip, the mega-menu dropdown, the Google-follow card, the mobile menu panel) — not a general card-elevation pattern. Depth elsewhere comes from tonal layering: paper → raised (`--line-soft`) → white card, each a half-step lighter or more separated than its container.

### Named Rules
**The Flat-Card Rule.** Cards and content boxes are distinguished by a hairline `--line` border and/or a background shift, not a shadow. Reserve `box-shadow` for genuinely floating UI (menus, tooltips, sticky bars).

## Shapes

Every corner on the site is a hard 90°. A `--radius: 2px` custom property exists in `:root` but is not referenced by a single rule in the stylesheet — it's effectively dead and should not be treated as the site's real corner value. Buttons, cards, forms, tiles, chips, images: all sharp rectangles, no exceptions found.

### Named Rules
**The Sharp Corner Rule.** Do not add `border-radius` to any new component. The absence of rounding is a confirmed, site-wide visual choice, not an inconsistency to "fix."

## Components

### Buttons
- **Shape:** sharp rectangle, no radius.
- **Primary** (`.btn-solid-warm`): `--accent` fill, white text, 600 weight, `14px 24px` padding, hover darkens to `--accent-deep`.
- **Secondary/Outline** (`.btn-outline-light`, for dark backgrounds): `1px solid rgba(255,255,255,0.5)` border, white text, hover fills `rgba(255,255,255,0.1)`.
- **Outline, dark-on-light** (`.btn-outline-dark`): mirrors the outline treatment for use on light/raised sections, hover inverts to a solid ink fill.
- **Block/form submit** (`.btn-block-dark`): full-width ink-filled button used as the submit action inside `.consult-form`.
- CTA hierarchy is a live design decision, not just a style choice: the higher-commitment action (a phone call) is deliberately styled as the *secondary* outline button, and the lower-friction action (a form, a text message) gets the solid primary treatment — this was a conversion-driven fix made this session and should be preserved in any new CTA pairing.

### Eyebrow Badge
- A small uppercase label badge (`.eyebrow`) used above headings site-wide: `0.78rem`, 500 weight, uppercase, `0.02em` letter-spacing, `7px 14px` padding, `1px solid` border.
- **Light-mode default:** white (`--paper-raised`) fill, `--line` border, `--ink-soft` text — this is the base rule now; it was previously missing entirely and rendered invisibly outside the hero, a real bug fixed this session.
- **Dark-context override** (inside `.subhero`, `.content-section.dark`, or the page-specific `.why-dark-section`): translucent white fill (`rgba(255,255,255,0.08)`), translucent white border, white text.

### Cards / Containers
- **Corner style:** sharp, no radius.
- **Simple card** (`.simple-card`, `.community-card`, etc.): `1px solid --line` border, `--paper-raised` or `--paper` background depending on context, no shadow.
- **Internal padding:** roughly `18px–30px` depending on card density.

### Inputs / Fields (`.consult-form`)
- White (`--paper-raised`) card background, `1px solid --line` on each field, `12px 14px` field padding.
- No focus-ring or border-color-shift treatment is currently defined — a real gap worth closing if forms get another pass (nothing to describe here yet; do not invent one).
- A small uppercase-free trust line (`.form-trust`, `--accent-deep`, `0.78rem`, 600 weight) sits directly under the form heading — added this session as a credibility signal, real credentials only (REALTOR® designation, degree), never the brokerage name.

### Navigation
- Dark (`--ink`) fixed-height bar, logo + wordmark left, links + mega-menu trigger center, a persistent CTA button top-right.
- Mega-menu dropdown opens via CSS `:hover` on desktop, a click-toggled panel on mobile (`≤760px`), each item showing a small blue line-icon + label + one-line description.
- Mobile also gets a sticky bottom CTA bar (`.mobile-cta-bar`, `≤760px` only) — two buttons, always visible regardless of scroll position, added this session specifically so a contact path is never more than one tap away on long pages.

### Icons
- Custom-built inline SVG line icons: `24×24` viewBox, `1.75px` stroke, round linecaps/linejoins, `currentColor` stroke, sized via `width/height:1em` so they inherit the surrounding text's font-size by default.
- Colored `--accent-deep` wherever used as a UI icon (nav bullets, card icons, form trust markers) — this replaced a full site-wide emoji icon system this session; never reintroduce emoji as UI icons.

## Do's and Don'ts

### Do:
- **Do** keep every new section's background alternating with its neighbors (dark/light/raised) rather than letting two-plus sections in a row share the same background.
- **Do** use the Eyebrow Badge's light-mode default (white fill, `--ink-soft` text) on any plain or raised section, and only reach for the dark override inside an actual dark-background section.
- **Do** make the lowest-friction contact action (text/form) the visually primary button, and the highest-friction one (phone call) secondary, in any CTA pairing.
- **Do** use the established SVG icon set (`icons.py`) and its blue/line-icon convention for any new icon need.

### Don't:
- **Don't** add `border-radius` to any element. The sharp-corner language is confirmed, site-wide, and deliberate.
- **Don't** introduce a second accent hue. One blue, in up to three lightness steps for contrast reasons, is the ceiling.
- **Don't** reach for a monospace font for any digit-heavy content — explicitly banned per client request.
- **Don't** add a drop-shadow-based card style as a general pattern; shadows are reserved for genuinely floating/overlay UI only.
- **Don't** use emoji as UI icons — the site standardized on custom blue SVG line icons this session specifically to replace them.
