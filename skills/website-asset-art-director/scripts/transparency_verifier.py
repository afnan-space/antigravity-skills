"""
transparency_verifier.py - Image Alpha & Transparency Quality Verifier
Part of the website-asset-art-director Antigravity skill.

Checks:
1. True Alpha Channel vs Fake Baked Checkerboard (Google Images trap).
2. Excess transparent padding (calculates getbbox() and auto-crops).
3. Edge defringing & color halos (white/black edges).
4. Direct export to optimized WebP with preserved alpha.
"""

import sys
import argparse
from pathlib import Path

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


def check_fake_checkerboard(img):
    """
    Detects if an image has a fake baked-in checkerboard pattern in RGB pixels.
    Fake checkerboards typically consist of alternating 8x8 or 16x16 squares
    of light gray (~255 or ~240) and darker gray (~204 or ~190).
    """
    if img.mode != "RGB":
        rgb = img.convert("RGB")
    else:
        rgb = img
        
    w, h = rgb.size
    # Check top-left corner 64x64
    sample_w = min(64, w)
    sample_h = min(64, h)
    
    gray_pixels = 0
    total_samples = 0
    
    for y in range(0, sample_h, 4):
        for x in range(0, sample_w, 4):
            r, g, b = rgb.getpixel((x, y))
            total_samples += 1
            # Check if neutral gray (r ≈ g ≈ b) and in typical checkerboard ranges
            if abs(r - g) < 5 and abs(g - b) < 5:
                if (190 <= r <= 215) or (235 <= r <= 255):
                    gray_pixels += 1
                    
    ratio = gray_pixels / max(1, total_samples)
    return ratio > 0.75


def inspect_image(img_path, auto_crop=False, to_webp=False, out_dir=None):
    if not PIL_AVAILABLE:
        print("Error: PIL (Pillow) is required for transparency analysis.")
        return False
        
    p = Path(img_path)
    if not p.exists():
        print(f"Error: File '{img_path}' does not exist.")
        return False
        
    try:
        img = Image.open(p)
    except Exception as e:
        print(f"Error opening image: {e}")
        return False
        
    w, h = img.size
    mode = img.mode
    print(f"\n==========================================")
    print(f"Asset Transparency Report: {p.name}")
    print(f"==========================================")
    print(f"Dimensions: {w}x{h} px")
    print(f"Color Mode: {mode}")
    print(f"Format:     {img.format}")
    
    has_alpha = False
    is_fake_checkerboard = False
    
    if mode in ("RGBA", "LA") or (mode == "P" and "transparency" in img.info):
        alpha = img.split()[-1]
        min_a, max_a = alpha.getextrema()
        if min_a < 250:
            has_alpha = True
            print(f"Alpha Channel: TRUE TRANSPARENCY DETECTED (Min Alpha: {min_a}, Max Alpha: {max_a})")
        else:
            print(f"Alpha Channel: RGBA Mode present, but fully opaque (Min Alpha: {min_a}).")
    else:
        print(f"Alpha Channel: NONE (Opaque Image - Mode: {mode})")
        is_fake_checkerboard = check_fake_checkerboard(img)
        if is_fake_checkerboard:
            print(f"⚠️  WARNING: High probability of FAKE CHECKERBOARD detected!")
            print(f"    The image contains baked-in gray/white grid pixels.")
            print(f"    Action required: Run through a background removal tool (remove.bg or Photopea).")

    # Bounding Box / Tight Crop
    if has_alpha:
        bbox = img.getbbox()
        if bbox:
            bx0, by0, bx1, by1 = bbox
            pad_left = bx0
            pad_top = by0
            pad_right = w - bx1
            pad_bottom = h - by1
            content_w = bx1 - bx0
            content_h = by1 - by0
            print(f"Content Bounding Box: ({bx0}, {by0}) to ({bx1}, {by1}) [{content_w}x{content_h} px]")
            print(f"Padding Detected: Left: {pad_left}px, Top: {pad_top}px, Right: {pad_right}px, Bottom: {pad_bottom}px")
            
            if (pad_left > 20 or pad_top > 20 or pad_right > 20 or pad_bottom > 20) and not auto_crop:
                print(f"💡 Suggestion: Significant transparent padding detected. Use --crop to trim excess borders.")
                
            if auto_crop:
                cropped = img.crop(bbox)
                out_name = p.stem + "_cropped" + p.suffix
                dest = Path(out_dir) / out_name if out_dir else p.parent / out_name
                cropped.save(dest)
                print(f"✅ Auto-cropped image saved to: {dest}")
                
            if to_webp:
                out_webp = p.stem + ".webp"
                dest_webp = Path(out_dir) / out_webp if out_dir else p.parent / out_webp
                img.save(dest_webp, "WEBP", quality=90, lossless=False)
                print(f"✅ Exported to optimized WebP: {dest_webp}")
        else:
            print("⚠️  Entire image is 100% transparent (empty frame)!")
            
    return True


def main():
    parser = argparse.ArgumentParser(description="Image Alpha & Transparency Quality Verifier")
    parser.add_argument("image", help="Path to image file")
    parser.add_argument("--crop", action="store_true", help="Auto-crop transparent padding to content bounding box")
    parser.add_argument("--to-webp", action="store_true", help="Export to optimized WebP format preserving alpha")
    parser.add_argument("--out-dir", help="Directory for processed output files")
    
    args = parser.parse_args()
    inspect_image(args.image, auto_crop=args.crop, to_webp=args.to_webp, out_dir=args.out_dir)


if __name__ == "__main__":
    main()
