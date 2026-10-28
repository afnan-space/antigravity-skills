# Visual Inspection & Comparison Checklist

## Priority Order of Visual Similarity
When comparing the replica with the reference screenshot or live site, address mismatches in this strict order:

1. **Overall Page Structure & Section Order**:
   - Are all sections present in the exact order as the reference?
   - Is any section or card container accidentally missing or collapsed?
2. **Key Asset Placements & Proportions**:
   - Are hero characters, 3D emblems, and main illustrations positioned accurately?
   - Do images maintain their natural aspect ratio without stretching or squishing?
3. **Typography & Hierarchy**:
   - Primary display font (e.g., condensed bold serif or modern display sans).
   - Heading sizes, uppercase transformation, letter-spacing (`tracking`), and line-height.
   - Text color gradients (e.g., `-webkit-background-clip: text` with gold/orange gradients).
   - Body font readability and muted metadata colors.
4. **Spacing, Margins & Container Max-Widths**:
   - Check container constraint (`max-width: 1180px` or `1280px`, margin auto).
   - Section vertical paddings (`padding: 88px 0` or `130px 0` on desktop; `64px 0` on mobile).
   - Gap between cards, columns, and list items.
5. **Card Styling, Borders & Shadows**:
   - Slanted corners (`clip-path: polygon(...)`) or border-radius.
   - Subtle inner borders (`box-shadow: inset 0 0 0 1px var(--line)`).
   - Glow filters (`filter: drop-shadow(...)`), vignettes, and atmospheric radial gradients.
6. **Background Layers & Overlays**:
   - Vignette gradients (`radial-gradient` and `linear-gradient` over scenes).
   - Film grain or texture overlay (`mix-blend-mode: overlay`, SVG noise).
   - Floating particle effects (embers, stars, glows).
7. **Interactive Elements**:
   - Buttons (slanted game cuts, hover brightness, active translation).
   - Accordions (`+` rotation, details/summary smooth toggle).
   - Carousels and horizontal tracks (snap alignment, progress bars, arrow buttons).
   - Form inputs, sliders, and live calculation outputs.

## Screenshot Capture Protocol
1. Launch the local development server on a fixed port.
2. Ensure all scroll reveal animations or `.reveal` elements have triggered (e.g. scroll the page or set `.reveal.in`).
3. Capture full-page screenshots at:
   - **Desktop**: 1440 × 900
   - **Laptop**: 1280 × 800
   - **Tablet**: 768 × 1024
   - **Mobile**: 390 × 844
   - **Small Mobile**: 360 × 740
4. Inspect the image files and identify the **Top 5 Visual Differences**.
5. Adjust CSS/JSX and re-verify until differences are resolved.

