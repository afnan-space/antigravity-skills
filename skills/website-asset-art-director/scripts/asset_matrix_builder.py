"""
asset_matrix_builder.py - Website Asset Inventory & Requirements Matrix Builder
Part of the website-asset-art-director Antigravity skill.

Scans an existing asset directory or generates an archetype-based asset plan.
Inspects existing images (dimensions, aspect ratio, alpha channel, file size)
and maps them against required assets for various website archetypes.
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


ARCHETYPE_ROSTERS = {
    "gaming": [
        {"id": "GAME-01", "name": "Hero Background Atmosphere", "section": "Hero", "format": "WebP/AVIF", "dims": "1920x1080 (16:9)", "alpha": "No", "prio": "P1-Essential", "budget": "< 250 KB"},
        {"id": "GAME-02", "name": "Primary Character / Miner Cutout", "section": "Hero Foreground", "format": "PNG / WebP", "dims": "1000x1200", "alpha": "Yes (True Alpha)", "prio": "P1-Essential", "budget": "< 300 KB"},
        {"id": "GAME-03", "name": "Game Logo / Wordmark", "section": "Navbar / Hero", "format": "SVG / PNG", "dims": "512x256 (2:1)", "alpha": "Yes", "prio": "P1-Essential", "budget": "< 50 KB"},
        {"id": "GAME-04", "name": "Mining Action Spritesheet", "section": "Gameplay / Hero", "format": "PNG Spritesheet", "dims": "6-12 frames (e.g. 1536x256)", "alpha": "Yes", "prio": "P2-Important", "budget": "< 600 KB"},
        {"id": "GAME-05", "name": "Coin / Token Graphic (Rotating or 3D)", "section": "Tokenomics / Rewards", "format": "PNG / WebM / CSS", "dims": "512x512 (1:1)", "alpha": "Yes", "prio": "P1-Essential", "budget": "< 80 KB"},
        {"id": "GAME-06", "name": "Mine / Level Card Art (x4-x6)", "section": "Mines / Levels Showcase", "format": "WebP", "dims": "800x600 (4:3)", "alpha": "No", "prio": "P2-Important", "budget": "< 120 KB each"},
        {"id": "GAME-07", "name": "Stat & Action Icons (Pickaxe, Energy, Rank)", "section": "Features / Stats", "format": "SVG / PNG", "dims": "64x64 or 128x128", "alpha": "Yes", "prio": "P2-Important", "budget": "< 15 KB each"},
        {"id": "GAME-08", "name": "Particle / Spark / Glow Texture", "section": "Ambient FX", "format": "PNG (Additive Alpha)", "dims": "512x512", "alpha": "Yes", "prio": "P3-Optional", "budget": "< 40 KB"},
        {"id": "GAME-09", "name": "Favicon & App Icon", "section": "Browser / PWA", "format": "PNG / ICO / SVG", "dims": "512x512, 192x192, 32x32", "alpha": "Yes", "prio": "P1-Essential", "budget": "< 20 KB"}
    ],
    "crypto": [
        {"id": "CRYPTO-01", "name": "Hero Cyber Grid / Network Mesh", "section": "Hero", "format": "WebP / SVG", "dims": "1920x1080", "alpha": "No (Dark Theme)", "prio": "P1-Essential", "budget": "< 200 KB"},
        {"id": "CRYPTO-02", "name": "Brand Logo & Iconmark", "section": "Header", "format": "SVG", "dims": "Vector / 512x128", "alpha": "Yes", "prio": "P1-Essential", "budget": "< 30 KB"},
        {"id": "CRYPTO-03", "name": "Token / Vault Holographic 3D Element", "section": "Hero Visual", "format": "WebP / PNG / Spline", "dims": "1024x1024", "alpha": "Yes", "prio": "P1-Essential", "budget": "< 250 KB"},
        {"id": "CRYPTO-04", "name": "Ecosystem / Partner Logos (x6-x10)", "section": "Social Proof", "format": "SVG (Monochrome)", "dims": "Vector / 180x48", "alpha": "Yes", "prio": "P2-Important", "budget": "< 10 KB each"},
        {"id": "CRYPTO-05", "name": "Architecture / Protocol Diagram", "section": "How It Works", "format": "SVG / Interactive HTML", "dims": "1200x600", "alpha": "Yes", "prio": "P2-Important", "budget": "< 80 KB"},
        {"id": "CRYPTO-06", "name": "Feature Matrix Icons (x6)", "section": "Security & Features", "format": "SVG", "dims": "48x48", "alpha": "Yes", "prio": "P2-Important", "budget": "< 5 KB each"}
    ],
    "saas": [
        {"id": "SAAS-01", "name": "Product Dashboard Screenshot / Mockup", "section": "Hero Showcase", "format": "WebP / PNG", "dims": "1440x900 or 1600x1000", "alpha": "Optional (Angled or Flat)", "prio": "P1-Essential", "budget": "< 250 KB"},
        {"id": "SAAS-02", "name": "Company Logo & Inverted Variant", "section": "Navbar / Footer", "format": "SVG", "dims": "Vector / 240x60", "alpha": "Yes", "prio": "P1-Essential", "budget": "< 25 KB"},
        {"id": "SAAS-03", "name": "Feature Spotlights (x3-x4)", "section": "Feature Sections", "format": "SVG / WebP", "dims": "1000x800", "alpha": "Yes", "prio": "P1-Essential", "budget": "< 150 KB each"},
        {"id": "SAAS-04", "name": "Customer / Client Logos (x6-x12)", "section": "Logo Cloud", "format": "SVG (Grayscale)", "dims": "Vector / 160x40", "alpha": "Yes", "prio": "P2-Important", "budget": "< 8 KB each"},
        {"id": "SAAS-05", "name": "Testimonial Avatars (x3-x6)", "section": "Testimonials", "format": "WebP", "dims": "160x160 (1:1)", "alpha": "No (Circular Crop)", "prio": "P2-Important", "budget": "< 30 KB each"},
        {"id": "SAAS-06", "name": "UI Feature & Navigation Icons (x12)", "section": "Global UI", "format": "SVG (Lucide/Heroicons)", "dims": "24x24", "alpha": "Yes", "prio": "P1-Essential", "budget": "< 3 KB each"}
    ],
    "telegram_mini_app": [
        {"id": "TMA-01", "name": "Tap Character / Main Clicker Target", "section": "Game Screen", "format": "PNG / WebP", "dims": "800x800 (1:1)", "alpha": "Yes (True Alpha)", "prio": "P1-Essential", "budget": "< 180 KB"},
        {"id": "TMA-02", "name": "Tap Reaction / Burst Particles", "section": "Interactive Tap FX", "format": "PNG Spritesheet / CSS", "dims": "512x128", "alpha": "Yes", "prio": "P2-Important", "budget": "< 80 KB"},
        {"id": "TMA-03", "name": "Bottom Navigation Bar Icons (x4-x5)", "section": "Tab Navigation", "format": "SVG / PNG", "dims": "48x48", "alpha": "Yes", "prio": "P1-Essential", "budget": "< 10 KB each"},
        {"id": "TMA-04", "name": "Coin / Balance Counter Icon", "section": "Top Bar HUD", "format": "PNG / SVG", "dims": "128x128", "alpha": "Yes", "prio": "P1-Essential", "budget": "< 25 KB"},
        {"id": "TMA-05", "name": "Upgrade / Task Category Badges (x4)", "section": "Earn / Boost Screen", "format": "PNG / SVG", "dims": "256x256", "alpha": "Yes", "prio": "P2-Important", "budget": "< 40 KB each"},
        {"id": "TMA-06", "name": "Atmospheric Backdrop / Mine Vault", "section": "App Background", "format": "WebP (Mobile 9:16)", "dims": "1080x1920", "alpha": "No", "prio": "P1-Essential", "budget": "< 200 KB"}
    ]
}


def analyze_file(file_path):
    stat = file_path.stat()
    size_kb = stat.st_size / 1024
    ext = file_path.suffix.lower()
    
    info = {
        "path": str(file_path),
        "name": file_path.name,
        "extension": ext,
        "size_kb": round(size_kb, 1),
        "dimensions": "N/A",
        "aspect_ratio": "N/A",
        "has_alpha": "N/A",
        "mode": "N/A",
    }
    
    if PIL_AVAILABLE and ext in [".png", ".webp", ".jpg", ".jpeg", ".gif", ".bmp"]:
        try:
            with Image.open(file_path) as img:
                w, h = img.size
                info["dimensions"] = f"{w}x{h}"
                info["mode"] = img.mode
                
                # Aspect ratio simplification
                from math import gcd
                common = gcd(w, h)
                rw, rh = w // common, h // common
                if rw > 20 or rh > 20:
                    info["aspect_ratio"] = f"{round(w/h, 2)}:1"
                else:
                    info["aspect_ratio"] = f"{rw}:{rh}"
                    
                # Alpha check
                if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
                    # Check if actual transparent pixels exist
                    if img.mode == "RGBA":
                        alpha = img.split()[-1]
                        min_a, max_a = alpha.getextrema()
                        info["has_alpha"] = "Yes (True Alpha)" if min_a < 250 else "RGBA (Fully Opaque)"
                    else:
                        info["has_alpha"] = "Yes"
                else:
                    info["has_alpha"] = "No (Opaque)"
        except Exception as e:
            info["dimensions"] = f"Error reading: {e}"
            
    elif ext == ".svg":
        info["dimensions"] = "Vector (Scalable)"
        info["has_alpha"] = "Yes (Vector Native)"
        info["aspect_ratio"] = "Dynamic"
        
    return info


def build_audit_report(asset_dir, archetype="gaming"):
    path = Path(asset_dir)
    found_assets = []
    
    if path.exists() and path.is_dir():
        for root, _, files in os.walk(path):
            for f in files:
                ext = Path(f).suffix.lower()
                if ext in [".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif", ".webm", ".mp4", ".avif"]:
                    found_assets.append(analyze_file(Path(root) / f))
                    
    roster = ARCHETYPE_ROSTERS.get(archetype, ARCHETYPE_ROSTERS["gaming"])
    
    md = []
    md.append(f"# Website Asset Intelligence & Requirements Matrix")
    md.append(f"**Target Archetype:** `{archetype.upper()}` | **Inspected Directory:** `{asset_dir}`")
    md.append(f"**Existing Assets Detected:** {len(found_assets)}\n")
    
    if found_assets:
        md.append("## 1. Existing Assets Inventory (Scanned)")
        md.append("| Filename | Dimensions | Aspect Ratio | Alpha? | Size | Format |")
        md.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
        for a in found_assets:
            md.append(f"| `{a['name']}` | {a['dimensions']} | {a['aspect_ratio']} | {a['has_alpha']} | {a['size_kb']} KB | {a['extension'].upper()} |")
        md.append("")
    else:
        md.append("## 1. Existing Assets Inventory")
        md.append("> *No pre-existing visual assets found in the scanned path. Full asset production required from scratch.*\n")
        
    md.append(f"## 2. Standard Asset Requirements Matrix ({archetype.title()})")
    md.append("| ID | Asset Name | Target Section | Recommended Format | Target Dimensions | Alpha Needed? | Budget | Priority |")
    md.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    for item in roster:
        md.append(f"| **{item['id']}** | {item['name']} | {item['section']} | `{item['format']}` | {item['dims']} | {item['alpha']} | {item['budget']} | `{item['prio']}` |")
        
    md.append("\n## 3. Production Readiness & Gap Analysis")
    md.append("- **P1 Essential Assets:** Must be completed before frontend layout stabilization.")
    md.append("- **P2 Important Assets:** Required for feature completeness and interactive polish.")
    md.append("- **P3 Optional / Ambience:** Add particle textures, ambient glow layers, or secondary micro-animations.")
    
    return "\n".join(md)


def main():
    parser = argparse.ArgumentParser(description="Website Asset Matrix & Inventory Generator")
    parser.add_argument("dir", nargs="?", default=".", help="Directory to inspect for assets (default: current dir)")
    parser.add_argument("--archetype", choices=["gaming", "crypto", "saas", "telegram_mini_app"], default="gaming", help="Website style archetype")
    parser.add_argument("--out", help="Save output markdown to file")
    
    args = parser.parse_args()
    report = build_audit_report(args.dir, args.archetype)
    
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Matrix report saved to {args.out}")
    else:
        print(report)


if __name__ == "__main__":
    main()
