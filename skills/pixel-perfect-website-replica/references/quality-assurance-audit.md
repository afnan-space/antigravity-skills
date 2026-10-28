# Quality Assurance & Delivery Audit

## 1. Zero Broken Assets
- Check all image `src`, SVG mask URLs, and background URLs.
- No `404 Not Found` in browser network tab or console.
- Transparent PNGs must not exhibit white square artifacts or missing alpha channels.

## 2. Browser Console Verification
- Open the browser console or check Playwright console log output.
- **Zero uncaught exceptions**.
- **Zero React hydration or DOM property warnings** (e.g., `fetchpriority` vs `fetchPriority`, `class` vs `className`).

## 3. Production Build Validation
Always execute the project's production build command:
- `npm run build` or `pnpm build` or `yarn build`
- Ensure TypeScript type checking passes without errors (`tsc`).
- Verify the bundle size is reasonable and assets are properly placed into `dist/` or `build/`.

## 4. Interaction Smoke Test
Before completing:
1. **Navigation Links**: Smooth scroll to `#section-id` anchors.
2. **Mobile Drawer**: Toggles open and closed via hamburger button and Escape key.
3. **Accordions / FAQ**: Expand and collapse without layout jumps.
4. **Interactive Calculators / Sliders**: Change numbers smoothly in response to user inputs and presets.
5. **Copy Buttons**: Copy text to clipboard and display confirmation toast/label.
6. **Carousels**: Next/prev buttons advance slides; pins/dots reflect active index.

## 5. Honest Third-Party Boundaries
- Never simulate or fake successful financial transactions, wallet balances, or private backend sign-ins if real credentials/backends are missing.
- Separate demo/frontend state from live services clearly in the completion report.

