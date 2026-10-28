# Responsive Verification Protocol

## 1. Zero Horizontal Overflow
Horizontal scrolling is the most common flaw in low-quality website clones.
Verify that horizontal overflow is strictly `0px` across all viewports:
```javascript
// Test expression:
document.documentElement.scrollWidth <= window.innerWidth
```
If `scrollWidth > clientWidth`:
- Identify offending elements:
  ```javascript
  Array.from(document.querySelectorAll('*')).filter(el => el.getBoundingClientRect().right > window.innerWidth);
  ```
- Common culprits:
  - Fixed widths (`width: 500px` without `max-width: 100%`).
  - Pre-formatted text or unconstrained tables (use `overflow-x: auto` on table wrappers).
  - Unbroken long strings/hashes (use `overflow-wrap: anywhere` or `word-break: break-all`).
  - Absolute/parallax elements protruding past screen bounds without `overflow: hidden` on the parent section.

## 2. Breakpoint Behaviors

### Desktop ($\ge 1000\text{px}$)
- Full multi-column grids (3–4 columns for feature cards, 2 columns for calculators and split layouts).
- Horizontal navigation bar visible; mobile hamburger hidden.
- Hero composition features side-by-side arrangement (headline on left, artwork on right).
- Full horizontal track for carousels with visible slide-in cards.

### Tablet ($640\text{px}$ – $999\text{px}$)
- 2-column card layouts.
- Header CTA adjusts or switches to mobile drawer.
- Sub-headings and statistics wrap into 2×2 or 4×1 blocks.

### Mobile ($< 640\text{px}$)
- Single-column card stacking.
- Sticky or fixed mobile play/action bar (`.mbar`) slides up once hero CTA leaves viewport.
- Mobile drawer navigation opens on hamburger click and traps or handles focus.
- Hero character artwork scales cleanly (e.g. positioned with top/right percentages, lower opacity behind text, or neatly stacked).
- Buttons expand to full width or 2-column grid (`1.4fr 1fr`).
- Presets and small controls use grid layouts (e.g. `repeat(6, 1fr)`).
- Touch target minimum: 44×44px for buttons and interactive controls.

