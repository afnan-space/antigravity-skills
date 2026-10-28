# Mode A: Reference-Based Website Replication Runbook

## Trigger Conditions
Activate Mode A when the user provides:
- A live website URL
- Full-page or partial screenshots
- A folder of downloaded assets
- An existing website repository / source files
- Exact requests like *"clone this website"*, *"recreate this screenshot"*, *"same to same banao"*.

---

## Step-by-Step Procedure

### 1. Ingest & Inspect References
- If a URL is accessible: fetch HTML, inspect stylesheets, scripts, web manifest, fonts, and assets.
- If only screenshots are available: measure visual proportions, font sizes, line heights, margins, and card grids from the image.
- Run `asset_analyzer.py` on any downloaded asset directory:
  ```bash
  python "C:/Users/User/.gemini/config/skills/autonomous-website-architect/scripts/asset_analyzer.py" "<assets_folder>"
  ```
- Map each asset to its corresponding section (Hero, Features, Character, Logos, Badges, Sprites).

### 2. Stack Evaluation
- Inspect the current working directory.
- If a project is already initialized, preserve its package manager and framework.
- If the directory is blank, initialize a clean **React + Vite + TypeScript** workspace with organized component CSS.

### 3. Structural Reconstruction
- Build every visible section:
  1. Header & Navigation (including mobile slide-out drawer)
  2. Hero banner (artwork, title gradient, lead copy, primary/secondary CTAs, stats row)
  3. Feature sections / Chapters
  4. Interactive showcases (carousels, world maps, consoles, calculators)
  5. Reward / Card grids
  6. Tokenomics / Value props
  7. Rules / Code of conduct
  8. Collapsible FAQ accordions
  9. Final CTA with social links
  10. Footer with columns and disclaimers
- Maintain true semantic HTML: never flatten text, buttons, or cards into a single static image.

### 4. Interactive Fidelity
- Wire all interactive components with real state:
  - Mobile menus open/close with backdrop and ESC key.
  - Calculators dynamically update figures, tiers, and speed.
  - Carousels scroll smoothly, sync with map pins or dot indicators, and update progress bars.
  - FAQ items expand/collapse with smooth icon rotations.
  - Clipboard copy triggers temporary toast/label confirmation.

### 5. Verification & Visual Diffing
- Start the Vite dev server.
- Capture full-page screenshots at 1440px, 1280px, 768px, 390px, 360px.
- Identify the **Top 5 Visual Mismatches** against the reference screenshot.
- Refine CSS (font weight, letter-spacing, padding, drop shadows, image crops).
- Repeat until differences are minimized to pixel precision.

