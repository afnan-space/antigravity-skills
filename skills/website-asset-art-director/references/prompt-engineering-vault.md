# Prompt Engineering Vault for Web Visual Assets

A master reference of prompt engineering formulas, parameter wrappers, and ready-to-use templates across 10 industry website archetypes.

---

## 1. Master Prompt Formula

Every production asset prompt follows this 9-part formula:

$$\text{Prompt} = \text{[Subject]} + \text{[Action / Pose]} + \text{[Framing / Angle]} + \text{[Lighting]} + \text{[Color Palette]} + \text{[Materials / Textures]} + \text{[Background Environment]} + \text{[Art Style]} + \text{[Engine / Render Details]}$$

### Tool-Specific Parameter Wrappers

| Tool | Prompt Structure | Key Flags / Settings |
| :--- | :--- | :--- |
| **Midjourney v6.1** | Concise comma-separated descriptors, artistic keywords | `--ar 16:9` (or `1:1`, `4:3`), `--v 6.1`, `--style raw`, `--stylize 150`, `--no text, watermark, logo, borders, signature` |
| **FLUX.1 (Dev/Schnell)** | Natural language, detailed descriptions of anatomy & lighting | Natural prose, specify exact camera (e.g. `shot on 35mm lens, f/1.8`), high fidelity details |
| **ChatGPT / DALL-E 3** | Strict narrative specification with explicit negative constraints | Specify `"No text or letters anywhere in the image"`, `"Render on pure white background (#ffffff) for easy cutout"` |
| **Imagen 3 (Gemini)** | Photorealistic or stylized 3D descriptive prompts | Specify materials (`matte clay`, `brushed bronze`, `subsurface scattering`), clean ambient occlusion |
| **Stable Diffusion** | Weighted tokens `(word:1.2)`, explicit negative prompt block | Negative: `text, watermark, lowres, bad anatomy, blur, cropped, out of frame, deformed` |

---

## 2. Archetype Templates & Exact Prompts

### Archetype 1: Gaming & Mining (Pickaxe, Dwarves, Steampunk)
- **Asset: Hero Atmosphere (16:9)**
  ```text
  Epic underground dwarven cavern mine, dramatic volumetric god rays beaming through cavern ceiling, glowing gold ore veins in rock walls, wooden mining scaffolds, glowing lanterns, ancient mining machinery with brass gears, drifting dust motes and glowing embers, cinematic composition, Unreal Engine 5 render, 8k resolution, deep atmospheric shadows, warm torchlight and cool ambient cavern blue --ar 16:9 --v 6.1 --no text, watermark
  ```
- **Asset: Master Miner Character Cutout (Isolated)**
  ```text
  Sturdy fantasy dwarf miner character standing confidently, holding a heavy glowing steel pickaxe with crystal inlay, leather mining apron, thick braided beard with metal rings, brass goggles on forehead, soot-dusted rugged skin, dynamic three-quarter hero pose. Rendered on solid neutral solid studio gray background, studio rim lighting, 3D character design, Pixar meets Blizzard style, sharp detailed edges, high definition --ar 4:5 --v 6.1 --no text, background scenery
  ```
- **Asset: Gold Coin / Token (1:1 Transparent Target)**
  ```text
  Chunky 3D embossed gold fantasy game coin, stamped with a crossed pickaxe insignia, heavy bevel, glistening metallic gold surface, soft warm subsurface glow, angled three-quarter isometric perspective, floating in center. Solid pure white background, studio product lighting, Octane render --ar 1:1 --v 6.1 --no text, shadow cutoff
  ```

---

### Archetype 2: Web3, Crypto & DeFi
- **Asset: Hero Holographic Visual**
  ```text
  Floating 3D holographic crypto vault node, glowing cyan and violet laser wireframes, abstract data streams and glowing glass prisms, dark futuristic cybernetic aesthetic, isometric 45 degree angle, dark minimalist background with subtle particle mesh, raytraced glass caustics, clean high-tech corporate tech --ar 16:9 --v 6.1
  ```
- **Asset: Token / Staking Emblem**
  ```text
  Minimalist 3D iridescent chrome geometric coin emblem, metallic rainbow sheen, floating in zero gravity, studio lighting with soft specular highlights, centered on solid dark slate background, Apple design aesthetic, Cinema4D render --ar 1:1
  ```

---

### Archetype 3: Modern SaaS & DevTools
- **Asset: Feature Spotlight Isometric Illustration**
  ```text
  Clean isometric 3D software pipeline diagram, modular glass floating servers, glowing data nodes connected by fiber optic cables, smooth pastel blue and deep indigo color scheme, soft ambient occlusion shadows, clean modern tech illustration, Figma 3D style --ar 4:3
  ```
- **Asset: Modern Abstract Hero Mesh Texture**
  ```text
  Subtle dark carbon wave texture, smooth flowing organic ridges, matte black and deep charcoal gray, directional studio side lighting, high-end hardware aesthetic, noise-free, minimal --ar 16:9
  ```

---

### Archetype 4: Telegram Mini App & Hyper-Casual Clicker
- **Asset: Tap Clicker Mascot (Friendly Mascot)**
  ```text
  Adorable chubby robotic golden hamster miner wearing a tiny hardhat, big expressive shiny anime eyes, holding a comically oversized gold nugget, cute chibi 3D game mascot, vibrant warm colors, smooth clay render, solid flat white background for alpha masking --ar 1:1
  ```
- **Asset: Rank Badges / Reward Chests**
  ```text
  Set of 4 progression treasure chests: Wooden, Bronze, Silver, Diamond. Cute casual mobile game UI style, vibrant saturated colors, gold trim, sparkling gem inlays, isometric front angle, clean edges, casual mobile art style --ar 16:9
  ```

---

### Archetype 5: Luxury & E-Commerce
- **Asset: Hero Product Podium**
  ```text
  Minimalist travertine stone pedestal in warm sunlight, soft linen fabric drapery, subtle olive branch shadow, architectural brutalist luxury aesthetic, neutral beige and warm ivory tones, editorial photography, high dynamic range --ar 16:9
  ```

---

## 3. Negative Prompt Master List
When using tools that support negative prompts (Stable Diffusion, Midjourney `--no`, SeaArt, etc.), always paste:
```text
text, watermark, typography, logo, lettering, signature, username, error, cropped, out of frame, blurry, low quality, pixelated, bad anatomy, deformed limbs, extra fingers, lowres, artifacts, jpeg compression artifacts, duplicate, twin
```
