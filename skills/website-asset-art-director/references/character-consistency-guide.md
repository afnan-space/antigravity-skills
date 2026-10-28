# Character and Art Direction Consistency Engine

A master runbook for maintaining identical character facial features, equipment, art style, lighting, and proportions across dozens of independent visual assets.

---

## 1. The Core Problem & The Golden Rules

Diffusion models lack persistent identity memory: asking for "a dwarf miner" in 5 different prompts will generate 5 completely distinct characters with different facial structures, beard styles, clothing, and proportions.

### The 4 Golden Rules of Character Consistency:
1. **Rule 1: Always Generate a Master Turnaround Sheet First.** Never generate hero shots or action poses before having a single reference image showing the character from multiple angles.
2. **Rule 2: Anchor Specific Trademark Features.** Generic descriptions fail. Name 4 to 5 unique, immutable features in every prompt:
   - *Example:* "Rugged dwarven miner, braided fiery orange bifurcated beard with 2 silver cylindrical rings, brass welding goggles with one cracked green lens, patchwork brown leather vest with brass shoulder stud, wielding a pickaxe with an embedded glowing blue cobalt crystal."
3. **Rule 3: Use Character Reference Conditioning (`--cref` or Vision Input).**
4. **Rule 4: Keep the Art Engine / Lighting Anchor Constant.** Reuse the exact same rendering style suffix across all assets.

---

## 2. Step 1: The Master Turnaround Sheet

Before generating any individual pose, generate a 3-way or 4-way turnaround sheet in one single generation. Because it is generated in a single pass, the character is guaranteed to be consistent across angles.

### Master Turnaround Prompt (Midjourney / FLUX):
```text
Character design turnaround sheet of a fantasy dwarf miner, showing front view, three-quarter view, and side profile view. Rugged dwarven miner, braided fiery orange bifurcated beard with silver cylindrical rings, brass welding goggles on forehead, patchwork leather mining vest, holding a glowing crystal pickaxe. Solid neutral gray background, clean studio lighting, 3D character sheet, Disney Pixar meets Blizzard cinematics, model sheet, high detail, sharp focus --ar 16:9 --v 6.1 --no background scenery, text
```

Save the best output as `public/assets/branding/master-character-reference.png`.

---

## 3. Step 2: Pose & Action Propagation Across Tools

### Workflow A: Midjourney v6.1 (`--cref`)
Midjourney features native Character Reference (`--cref`):
1. Upload `master-character-reference.png` to Discord or get its public image URL.
2. Copy the image link: `https://.../master-character.png`.
3. Generate new poses using the `--cref` parameter:
   ```text
   The dwarf miner swinging his glowing crystal pickaxe into a wall of gold ore, dynamic action pose, flying rock sparks, intense heroic expression --cref https://.../master-character.png --cw 100 --ar 4:5 --v 6.1
   ```
   - `--cw 100` (default): Copies face, hair, and clothing.
   - `--cw 0` to `--cw 20`: Copies only facial features, allowing clothing to change.

### Workflow B: ChatGPT / DALL-E 3 (Vision Reference Workflow)
1. In ChatGPT Plus, click the attachment (+) button and upload `master-character-reference.png`.
2. Enter the prompt:
   ```text
   Look closely at the dwarf miner in the attached reference image. Replicate this EXACT SAME character with identical facial features, orange braided beard with silver rings, brass goggles, and patchwork leather vest. 
   
   Render him in a celebratory victory pose, holding up a giant glowing gold nugget with both hands and winking at the camera. Solid white background (#ffffff) for clean cutout. Maintain the exact same 3D animated cinematic rendering style.
   ```

### Workflow C: Stable Diffusion (IP-Adapter & ControlNet)
In ComfyUI or Automatic1111:
1. Pass `master-character-reference.png` into **IP-Adapter Face / Plus** (weight: `0.75 - 0.85`).
2. Use **ControlNet OpenPose** to force the desired body posture without altering the character's facial structure.
3. Keep the prompt focused on lighting and action.

---

## 4. Color Palette and Material Locking

To ensure assets feel like they belong to the exact same universe, define a **Style Lock String** and append it to every asset prompt:

```text
[Style Lock]: stylized 3D cinematic rendering, Octane Render, warm subterranean torchlight, deep umber shadows, glowing gold specular highlights, Pixar meets Blizzard fantasy aesthetic, clean silhouette, no chromatic aberration
```

### Consistency Audit Checklist
Before integrating multiple character assets into your site:
- [ ] **Facial Structure:** Jawline, eye color, nose shape match across poses.
- [ ] **Costume Details:** Belt buckles, goggles, fabric colors are identical.
- [ ] **Scale & Proportion:** Head-to-body ratio remains constant (e.g. 1:4 for stylized dwarf or chibi, 1:7 for realistic human).
- [ ] **Light Direction:** Key lighting matches the website's ambient mood (e.g. top-left warm light).
- [ ] **Edge Sharpness:** Cutout edges have identical anti-aliasing depth.
