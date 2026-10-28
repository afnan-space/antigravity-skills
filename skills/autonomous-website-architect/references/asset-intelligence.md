# Asset Intelligence & Matching Protocol

## Overview
Reconstructing a website with high visual fidelity requires identifying, categorizing, and mapping the original assets to their corresponding UI components before writing markup or styling.

## 1. Asset Discovery Checklist
Run the helper script `python scripts/asset_analyzer.py <path_to_assets>` to catalog all assets:
- **Formats**: PNG, WebP, AVIF, JPG, JPEG, SVG, GIF, WebM, MP4, WOFF2, TTF.
- **Dimensions & Aspect Ratios**: Note exact widths and heights. Avoid CSS distortion.
- **Alpha Channels**: Differentiate transparent cutout graphics (characters, coins, floating badges) from opaque backgrounds (hero scenery, cards).
- **Sprite Sheets**: Flag images with extreme aspect ratios ($\ge 3:1$ or $\le 0.33:1$) or frame strips. Compute frame width:
  $$\text{Frame Width} = \frac{\text{Image Width}}{\text{Number of Frames}}$$
  or read accompanying JSON/metadata (`sprites.json`).

## 2. Asset Matching Rules
1. **Never substitute matching original assets** with generic shapes, AI-generated art, or third-party stock icons when the local asset exists.
2. **Preserve Transparency**: Transparent PNG/WebP files must be served as-is with proper alpha channel preservation. Never add white or black box backgrounds behind transparent cutout characters.
3. **SVGs vs Font Icons**:
   - Check if custom SVGs exist for icons before falling back to generic Lucide / FontAwesome icons.
   - For icons defined via CSS masks (`-webkit-mask: url(...)`), verify the mask URL and ensure `background: currentColor` or the intended theme color is applied.
4. **CSS Backgrounds vs `<img>` tags**:
   - Use `<img>` with `object-fit: cover` and relative positioning inside overflow-hidden wrappers when parallax or layered scaling is needed.
   - Use CSS background properties (`background-image`, `background-size: cover`, `background-position: center`) when the image functions purely as decorative texture or tiling pattern.
5. **Deduplication**: Match files by SHA-256 hash. If asset files have duplicate suffixes (`_1.webp`, `.jpg.jpeg`), resolve which is the background scene vs the character cutout by checking dimensions and transparency.

