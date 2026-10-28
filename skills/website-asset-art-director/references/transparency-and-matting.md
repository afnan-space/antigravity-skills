# Transparency, Matting, and Edge Cleansing Runbook

A production guide for generating, inspecting, cleaning, and optimizing transparent PNG and WebP assets for websites.

---

## 1. The Fake Checkerboard Trap

Many users download images from search engines or amateur repositories expecting transparency, only to discover that the gray-and-white checkerboard pattern is **permanently baked into the RGB pixel data**.

### How to Tell:
1. **File Extension Check:** JPG files **never** support transparency. If an image is `.jpg` or `.jpeg`, it is 100% opaque.
2. **Channel Check:** Inspect the color channels. An image with true transparency has an **Alpha channel** (`RGBA` or `LA`).
3. **Automated Verification:** Run the skill's built-in inspector:
   ```bash
   python "C:/Users/User/.gemini/config/skills/website-asset-art-director/scripts/transparency_verifier.py" "path/to/image.png"
   ```
   If it warns `High probability of FAKE CHECKERBOARD detected`, the image must be rematted.

---

## 2. Generating True Alpha from AI Tools

Most diffusion models (Midjourney, DALL-E, FLUX) generate solid backgrounds by default. To make background removal seamless:

### Prompt Strategy for Clean Cutouts
- **Request a Uniform Solid Background:**
  - For dark/metallic subjects: Specify `"solid pure white background (#ffffff), no shadows on ground"`
  - For light/white subjects: Specify `"solid neutral studio green (#00ff00) or chroma key background"`
- **Avoid Natural Shadows on the Floor:** Specify `"floating subject, no floor shadow, studio cutout lighting"` so the AI doesn't blend semi-transparent ground dirt with the background.

---

## 3. Removing Backgrounds (Free & Pro Workflows)

### Workflow A: Automated Free AI Cutout
1. **remove.bg** (Web / API): Instant high-quality edge detection for human and character cutouts.
2. **Clipdrop Background Removal** (Free tier): High-resolution cutout.
3. **Photopea (100% Free Browser Photoshop Clone at photopea.com):**
   - Open image in Photopea.
   - Go to `Select` $\rightarrow$ `Remove BG` (built-in AI model runs locally in your browser).
   - Alternatively: Use `Magic Wand (W)` with `Tolerance: 15`, select the solid background, press `Delete`.

### Workflow B: Edge Defringing & Halo Elimination
When a cutout was extracted from a white background, a 1-pixel light halo often remains around dark hair or edges. When placed over a dark website hero, this halo looks amateur.

#### To Defringe in Photopea / Photoshop:
1. Hold `Ctrl` and click the Layer thumbnail to select the cutout's opacity mask.
2. Go to `Select` $\rightarrow$ `Modify` $\rightarrow$ `Contract` by `1 px`.
3. Go to `Select` $\rightarrow$ `Modify` $\rightarrow$ `Feather` by `0.5 px`.
4. Invert selection (`Ctrl + Shift + I`) and press `Delete` to shave off the dirty outer fringe.
5. In Photoshop: Layer $\rightarrow$ Matting $\rightarrow$ **Defringe (1px)** or **Remove White Matte**.

---

## 4. Bounding Box & Tight Cropping

AI generators frequently center a small 400px character in the middle of a 1024x1024 transparent canvas. When developers import this into CSS, layout alignment and sizing becomes unpredictable because 60% of the image is invisible empty space.

### Solution: Auto-Crop
Run the skill's cropping tool:
```bash
python "C:/Users/User/.gemini/config/skills/website-asset-art-director/scripts/transparency_verifier.py" "public/assets/character.png" --crop --to-webp
```
This automatically:
1. Computes `image.getbbox()`.
2. Trims all surrounding empty transparent pixels.
3. Exports a tight-cropped asset and an optimized WebP variant.

---

## 5. Web Verification Checklist
Before approving any transparent asset:
- [ ] Tested over a **pure black background (`#000000`)**: No white edge halos or crust.
- [ ] Tested over a **pure white background (`#ffffff`)**: No dark boundary lines.
- [ ] Tested over a **colorful gradient**: Alpha gradient is smooth and not jagged/aliased.
- [ ] Excess transparent margins trimmed tightly to content edges.
- [ ] Exported as PNG-24 with alpha or Lossless/Near-lossless WebP.
