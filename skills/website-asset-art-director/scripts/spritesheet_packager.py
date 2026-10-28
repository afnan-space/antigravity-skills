"""
spritesheet_packager.py - Animation Frame to Spritesheet Stitcher & CSS Generator
Part of the website-asset-art-director Antigravity skill.

Takes a folder of sequential frames (PNGs) and stitches them into a horizontal
or grid spritesheet with alpha transparency preserved. Emits copy-paste CSS
and HTML5 Canvas animation code.
"""

import os
import sys
import argparse
from pathlib import Path

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


def package_spritesheet(frames_dir, output_path, fps=12, layout="horizontal"):
    if not PIL_AVAILABLE:
        print("Error: PIL (Pillow) is required for spritesheet packaging.")
        return False
        
    p = Path(frames_dir)
    if not p.exists() or not p.is_dir():
        print(f"Error: Directory '{frames_dir}' does not exist.")
        return False
        
    # Gather image files sorted naturally
    valid_exts = [".png", ".webp", ".jpg", ".jpeg"]
    files = sorted([f for f in p.iterdir() if f.suffix.lower() in valid_exts], key=lambda x: x.name)
    
    if not files:
        print(f"No valid image frames found in '{frames_dir}'.")
        return False
        
    images = []
    max_w, max_h = 0, 0
    
    for f in files:
        im = Image.open(f).convert("RGBA")
        images.append(im)
        max_w = max(max_w, im.width)
        max_h = max(max_h, im.height)
        
    num_frames = len(images)
    print(f"Loaded {num_frames} frames. Frame dimensions: {max_w}x{max_h} px.")
    
    if layout == "horizontal":
        sheet_w = max_w * num_frames
        sheet_h = max_h
        sheet = Image.new("RGBA", (sheet_w, sheet_h), (0, 0, 0, 0))
        
        for idx, im in enumerate(images):
            # Center frame within cell if dimensions differ slightly
            ox = idx * max_w + (max_w - im.width) // 2
            oy = (max_h - im.height) // 2
            sheet.paste(im, (ox, oy), im)
            
    out_file = Path(output_path)
    sheet.save(out_file, "PNG")
    print(f"\n✅ Spritesheet created: {out_file} ({sheet_w}x{sheet_h} px)")
    
    # Calculate animation duration
    duration_sec = round(num_frames / fps, 2)
    anim_name = out_file.stem.replace("-", "_")
    
    css_code = f"""
/* ========================================================== */
/* CSS Steps Animation for Spritesheet: {out_file.name}       */
/* ========================================================== */

.sprite-{anim_name} {{
  width: {max_w}px;
  height: {max_h}px;
  background-image: url('/assets/sprites/{out_file.name}');
  background-repeat: no-repeat;
  background-position: 0 0;
  animation: play_{anim_name} {duration_sec}s steps({num_frames}) infinite;
  image-rendering: pixelated; /* Optional: for pixel art */
}}

@keyframes play_{anim_name} {{
  from {{
    background-position: 0 0;
  }}
  to {{
    background-position: -{sheet_w}px 0;
  }}
}}
"""
    
    canvas_code = f"""
// HTML5 Canvas Sprite Animator
const spriteImg = new Image();
spriteImg.src = '/assets/sprites/{out_file.name}';
let currentFrame = 0;
const totalFrames = {num_frames};
const frameWidth = {max_w};
const frameHeight = {max_h};
let lastTick = performance.now();
const fpsInterval = 1000 / {fps};

function drawSprite(ctx, x, y) {{
  const now = performance.now();
  const elapsed = now - lastTick;
  if (elapsed > fpsInterval) {{
    lastTick = now - (elapsed % fpsInterval);
    currentFrame = (currentFrame + 1) % totalFrames;
  }}
  ctx.drawImage(
    spriteImg,
    currentFrame * frameWidth, 0, frameWidth, frameHeight,
    x, y, frameWidth, frameHeight
  );
}}
"""
    
    print("\n--- GENERATED CSS CODE ---")
    print(css_code)
    
    css_out_path = out_file.with_suffix(".css")
    with open(css_out_path, "w", encoding="utf-8") as f:
        f.write(css_code + "\n/* Canvas Reference:\n" + canvas_code + "\n*/")
    print(f"CSS saved to: {css_out_path}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Animation Frame to Spritesheet Packager")
    parser.add_argument("frames_dir", help="Directory containing sequential PNG frames")
    parser.add_argument("--out", default="spritesheet.png", help="Output spritesheet filename (default: spritesheet.png)")
    parser.add_argument("--fps", type=int, default=12, help="Target frames per second (default: 12)")
    
    args = parser.parse_args()
    package_spritesheet(args.frames_dir, args.out, fps=args.fps)


if __name__ == "__main__":
    main()
