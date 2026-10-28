# Mode B: Autonomous Original Website Creation Runbook

## Trigger Conditions
Activate Mode B when the user provides:
- A business concept, startup pitch, or product idea
- A list of features or requirements
- A prompt like *"Build me an e-commerce site for coffee"*, *"Create a modern landing page for an AI agent platform"*, *"Screenshot chara nijer moto design koro"*, *"Build a website from scratch"*
- Any request without a reference URL, screenshot, or pre-existing design.

---

## Autonomous Step-by-Step Procedure

### 1. Synthesize the Visual Specification
Act as the principal product designer and UI/UX architect. Create an internal specification:
1. **Target Audience & Value Proposition**: Who is this site for, and what primary action should they take?
2. **Archetype Selection**: Choose from Gaming, Web3, SaaS, E-Commerce, Portfolio, Dashboard, or Business.
3. **Color Palette**: Establish 6 core tokens:
   - `--bg`: Dark/light background
   - `--surface`: Card and modal background
   - `--line`: Subtle border color
   - `--primary`: Hero CTA and brand color
   - `--accent`: Secondary badges, highlights, or gradients
   - `--text`: High-contrast readable copy
4. **Typography Hierarchy**: Pair an expressive display typeface for headings with a clean geometric sans for UI and body text.
5. **Component Blueprint**: Plan 6–9 core sections tailored to the business goal.

### 2. Autonomous Asset Creation Strategy
Do not pause or ask the user to supply image files. Generate or assemble all needed visual assets:
- **Hero & Feature Graphics**:
  - If the `image-generator` subagent is available, invoke it with a detailed brief matching the palette.
  - If SVG/CSS is preferred, generate custom vector illustrations, layered isometric cards, or decorative gradient meshes.
  - For dynamic backgrounds, write lightweight canvas particle generators (stars, matrix rain, floating embers, or grid lines).
- **Icons**:
  - Write custom SVGs or use clean, modern inline icons (Lucide / custom SVG paths).
  - Never use raw emojis as product icons.
- **Data & Charts**:
  - Build responsive SVG charts (sparklines, bar charts, area charts) with realistic mock data.

### 3. Architecture & Code Implementation
- Set up a clean **React + Vite + TypeScript** structure.
- Scaffold design tokens using `scripts/design_token_generator.py <archetype>`.
- Build modular components:
  - `Header`: Sticky navbar with logo, nav links, theme toggle (if appropriate), and CTA.
  - `Hero`: Clear headline, subheadline, interactive preview or illustration, social proof badges.
  - `FeaturesGrid`: Interactive cards with icon graphics, titles, and descriptions.
  - `InteractiveWidget`: A live working feature (e.g. calculator, product configurator, live code playground, or pricing comparison toggle).
  - `SocialProof`: Customer testimonials with avatars, logos, or metric callouts.
  - `Pricing`: Tiered plans with "Popular" highlight badge and monthly/annual billing toggle.
  - `FAQ`: Clean expandable accordion.
  - `FinalCTA`: High-impact closing pitch with action button.
  - `Footer`: Links, copyright, and social icons.

### 4. Interactive Quality Standards
Every control must have real frontend functionality:
- Tabs change displayed content.
- Sliders and inputs update calculations in real time.
- Modals and drawers open and trap focus cleanly.
- Filtering and sorting controls dynamically update rendered lists.

### 5. Self-Evaluation Against Visual Criteria
Evaluate the generated site against these criteria:
- **Distinctive Identity**: Does this look custom-designed for this specific business, rather than a generic template?
- **Hierarchy & Contrast**: Does the headline dominate? Are CTAs immediately noticeable?
- **Responsiveness**: Does it look completely intentional on a 390px mobile viewport?

