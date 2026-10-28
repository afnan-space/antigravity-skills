# Browser Verification & Quality Audit Protocol

## Viewport Test Matrix
Every website (whether replicated in Mode A or created in Mode B) must pass inspection across 5 standard viewports:

| Viewport | Dimensions | Key Elements to Verify |
| :--- | :--- | :--- |
| **Desktop** | 1440 × 900 | Full multi-column grid, horizontal nav, side-by-side hero composition |
| **Laptop** | 1280 × 800 | Container constraint, spacing consistency, font line wrapping |
| **Tablet** | 768 × 1024 | 2-column card reflow, navigation threshold, touch targets |
| **Mobile** | 390 × 844 | Single-column cards, hamburger drawer, sticky action bar, zero horizontal overflow |
| **Small Mobile** | 360 × 740 | Extreme narrow text scaling, input padding, modal full-width fitting |

---

## Zero Horizontal Overflow Verification
Run this JavaScript snippet in Playwright or browser evaluation:
```javascript
const isOverflowing = document.documentElement.scrollWidth > window.innerWidth;
if (isOverflowing) {
  const badElements = Array.from(document.querySelectorAll('*'))
    .filter(el => el.getBoundingClientRect().right > window.innerWidth)
    .map(el => ({ tag: el.tagName, class: el.className, right: el.getBoundingClientRect().right }));
  console.error('Horizontal Overflow Detected:', badElements);
}
```

---

## Console Zero-Error Guarantee
1. Check browser console logs after loading and interacting with the page.
2. Ensure:
   - Zero uncaught JavaScript errors.
   - Zero missing image / asset `404 Not Found` requests.
   - Zero React property or hydration mismatches (e.g. `class` instead of `className`).

---

## Production Build Verification
Always execute:
```bash
npm run build
```
Verify that TypeScript compiles without errors and Vite emits clean production bundles in `dist/`.

