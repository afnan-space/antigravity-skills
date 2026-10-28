# Spritesheet and Web Motion Engine

A comprehensive architectural guide for planning, extracting, packaging, and rendering frame-by-frame 2D sprite animations and web video on the modern web.

---

## 1. Format Decision Engine: Which Animation Format to Use?

| Need / Use Case | Recommended Format | Why? | Limitation |
| :--- | :--- | :--- | :--- |
| **Character Actions (Idle, Run, Mining, Jump)** | **CSS PNG Spritesheet** | Zero video decode latency, hardware accelerated via GPU `steps()`, instant interactive response. | Higher total pixel count if frames $> 24$. |
| **Complex 3D Shaded / Particle Animation ($> 30$ frames)** | **WebM Video (VP9 with Alpha)** | Extreme compression (often 80% smaller than PNG sheets), smooth 30-60 fps playback. | Not supported on very old iOS Safari (requires MP4 fallback without alpha or APNG). |
| **Vector UI Micro-Interactions (Icons, Checkmarks)** | **Lottie JSON / CSS SVG** | Infinite resolution, tiny file size (< 10 KB), interactive state control. | Cannot render complex raster pixel art or 3D shading. |
| **Legacy Fallbacks / Simple Banners** | **Animated WebP / APNG** | Better color depth (24-bit + 8-bit alpha) than 256-color GIF. | Hard to pause, rewind, or synchronize with user input. |

> [!WARNING]
> **Never use standard 8-bit GIF** for modern web applications unless explicitly requested. GIFs have only 256 indexed colors and binary (1-bit) transparency, creating ugly jagged fringing on anti-aliased edges.

---

## 2. Planning a Spritesheet

### Standard Frame Rates & Duration:
- **Idle Breathing / Floating Animation:** 6 to 12 frames @ 10-12 fps (Duration: 0.5s – 1.0s loop).
- **Attack / Pickaxe Swing:** 8 to 14 frames @ 12-16 fps (Duration: 0.6s – 0.9s).
- **Coin Spin / Token Rotation:** 12 to 16 frames @ 12-15 fps (Duration: 1.0s seamless 360 loop).
- **Run / Walk Cycle:** 8 frames @ 12 fps (0.66s loop).

### Packaging with the Built-in Script
Place your individual frame PNGs (`frame_01.png`, `frame_02.png`, etc.) in a folder, then run:
```bash
python "C:/Users/User/.gemini/config/skills/website-asset-art-director/scripts/spritesheet_packager.py" "path/to/frames_folder" --out "public/assets/sprites/miner-mining.png" --fps 12
```
This automatically produces:
1. Stitched horizontal spritesheet with preserved alpha.
2. The exact CSS file with `@keyframes` and `steps(N)`.

---

## 3. CSS Steps Animation Implementation

```css
/* Spritesheet container */
.miner-avatar {
  width: 256px;
  height: 256px;
  background-image: url('/assets/sprites/miner-mining.png');
  background-repeat: no-repeat;
  background-position: 0 0;
  /* 12 frames @ 12fps = 1.0s duration */
  animation: minerMiningAnim 1.0s steps(12) infinite;
}

/* @keyframes moves background from 0 to negative total width */
@keyframes minerMiningAnim {
  from {
    background-position: 0px 0px;
  }
  to {
    background-position: -3072px 0px; /* 12 frames * 256px */
  }
}
```

---

## 4. Extracting Frames from Video (FFmpeg Workflow)

If you generated a 2-second video clip using an AI video tool (e.g. Runway, Pika, Kling, Luma) and want to convert it into a crisp spritesheet:

1. **Extract frames at 12 fps with transparent or green background:**
   ```bash
   ffmpeg -i input_video.mp4 -vf "fps=12,scale=512:512" frame_%03d.png
   ```
2. **If background is green chroma:**
   ```bash
   ffmpeg -i input_video.mp4 -vf "colorkey=0x00FF00:0.3:0.1,fps=12,scale=512:512" -c:v png frame_%03d.png
   ```
3. Run `spritesheet_packager.py` on the output frames folder.

---

## 5. WebM with Alpha Channel Workflow

For continuous looping background animations (e.g. floating magical dust, glowing energy orbs, spinning ton coins):

```html
<video 
  autoPlay 
  loop 
  muted 
  playsInline 
  className="w-64 h-64 pointer-events-none"
>
  <source src="/assets/videos/coin-spin.webm" type="video/webm" />
  <!-- Fallback animated WebP or PNG -->
  <img src="/assets/sprites/coin-spin.webp" alt="Rotating Coin" />
</video>
```
To encode a WebM with alpha using FFmpeg:
```bash
ffmpeg -framerate 24 -i frame_%03d.png -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 1M output_alpha.webm
```
