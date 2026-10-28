#!/usr/bin/env python3
"""
Asset Analyzer Utility for Pixel-Perfect Website Reconstruction.
Inspects local asset folders, extracts dimensions, aspect ratios, transparency,
identifies sprite sheets, computes SHA-256 hashes, and matches assets against reference references.
Zero external dependencies (uses standard library).
"""

import os
import sys
import json
import struct
import hashlib
import re

def get_image_info(filepath):
    """Extract dimensions, format, and transparency hint from image binary headers."""
    ext = os.path.splitext(filepath)[1].lower()
    size_bytes = os.path.getsize(filepath)
    info = {
        'path': filepath,
        'filename': os.path.basename(filepath),
        'ext': ext,
        'size_bytes': size_bytes,
        'size_kb': round(size_bytes / 1024, 1),
        'width': None,
        'height': None,
        'aspect_ratio': None,
        'is_transparent': False,
        'is_spritesheet': False,
    }

    try:
        with open(filepath, 'rb') as f:
            head = f.read(64)

            # PNG
            if head.startswith(b'\x89PNG\r\n\x1a\n'):
                w, h = struct.unpack('>II', head[16:24])
                info['width'] = w
                info['height'] = h
                color_type = head[25]
                # Color types 4 (greyscale + alpha) and 6 (RGBA) have alpha
                info['is_transparent'] = color_type in (4, 6)

            # JPEG
            elif head.startswith(b'\xff\xd8'):
                f.seek(0)
                data = f.read()
                i = 2
                while i < len(data) - 9:
                    marker, length = struct.unpack('>HH', data[i:i+4])
                    if marker in (0xffc0, 0xffc1, 0xffc2):
                        h, w = struct.unpack('>HH', data[i+5:i+9])
                        info['width'] = w
                        info['height'] = h
                        break
                    i += 2 + length

            # WebP
            elif head.startswith(b'RIFF') and head[8:12] == b'WEBP':
                chunk = head[12:16]
                if chunk == b'VP8 ':
                    w, h = struct.unpack('<HH', head[26:30])
                    info['width'] = w & 0x3fff
                    info['height'] = h & 0x3fff
                elif chunk == b'VP8L':
                    b1, b2, b3, b4 = struct.unpack('BBBB', head[21:25])
                    info['width'] = 1 + (((b2 & 0x3f) << 8) | b1)
                    info['height'] = 1 + (((b4 & 0x0f) << 10) | (b3 << 2) | ((b2 & 0xc0) >> 6))
                    info['is_transparent'] = bool(b4 & 0x10)
                elif chunk == b'VP8X':
                    info['width'] = 1 + struct.unpack('<I', head[24:27] + b'\x00')[0]
                    info['height'] = 1 + struct.unpack('<I', head[27:30] + b'\x00')[0]
                    flags = head[20]
                    info['is_transparent'] = bool(flags & 0x10)

            # GIF
            elif head.startswith(b'GIF87a') or head.startswith(b'GIF89a'):
                w, h = struct.unpack('<HH', head[6:10])
                info['width'] = w
                info['height'] = h
                info['is_transparent'] = True

            # SVG
            elif ext == '.svg' or b'<svg' in head.lower():
                f.seek(0)
                content = f.read(2048).decode('utf-8', errors='ignore')
                viewbox = re.search(r'viewBox=["\']([0-9\.\s\-]+)["\']', content, re.IGNORECASE)
                if viewbox:
                    parts = viewbox.group(1).strip().split()
                    if len(parts) >= 4:
                        try:
                            info['width'] = float(parts[2])
                            info['height'] = float(parts[3])
                        except ValueError:
                            pass
                if info['width'] is None:
                    wm = re.search(r'width=["\']([0-9\.]+)px?["\']', content, re.IGNORECASE)
                    hm = re.search(r'height=["\']([0-9\.]+)px?["\']', content, re.IGNORECASE)
                    if wm and hm:
                        try:
                            info['width'] = float(wm.group(1))
                            info['height'] = float(hm.group(1))
                        except ValueError:
                            pass
                info['is_transparent'] = True

        if info['width'] and info['height'] and info['height'] > 0:
            info['aspect_ratio'] = round(info['width'] / info['height'], 2)
            # A strip where width is >= 3x height or height is >= 3x width is likely a sprite sheet
            if info['aspect_ratio'] >= 3.0 or info['aspect_ratio'] <= 0.33:
                info['is_spritesheet'] = True

    except Exception:
        pass

    return info

def compute_hash(filepath):
    """Compute SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def scan_directory(directory):
    """Recursively scan directory and return asset inventory."""
    results = []
    supported_exts = {'.png', '.webp', '.jpg', '.jpeg', '.svg', '.gif', '.webm', '.mp4', '.woff', '.woff2', '.ttf'}
    
    for root, _, files in os.walk(directory):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in supported_exts:
                fpath = os.path.join(root, file)
                info = get_image_info(fpath)
                info['sha256'] = compute_hash(fpath)
                info['rel_path'] = os.path.relpath(fpath, directory)
                results.append(info)
    return results

def main():
    if len(sys.argv) < 2:
        print("Usage: python asset_analyzer.py <asset_directory> [--json]")
        sys.exit(1)

    target_dir = sys.argv[1]
    if not os.path.isdir(target_dir):
        print(f"Error: {target_dir} is not a valid directory.")
        sys.exit(1)

    assets = scan_directory(target_dir)

    if '--json' in sys.argv:
        print(json.dumps(assets, indent=2))
        return

    print(f"\n=======================================================")
    print(f" Asset Inventory for: {target_dir}")
    print(f" Total files analyzed: {len(assets)}")
    print(f"=======================================================\n")
    print(f"{'Filename':<32} {'Format':<8} {'Dimensions':<14} {'Ratio':<8} {'Transparent':<12} {'Spritesheet'}")
    print("-" * 85)

    spritesheets = []
    for a in sorted(assets, key=lambda x: x['filename']):
        dims = f"{int(a['width'])}x{int(a['height'])}" if a['width'] and a['height'] else "vector/n/a"
        ratio = str(a['aspect_ratio']) if a['aspect_ratio'] else "-"
        trans = "Yes" if a['is_transparent'] else "No"
        sprite = "YES (Sprite)" if a['is_spritesheet'] else "No"
        print(f"{a['filename'][:30]:<32} {a['ext']:<8} {dims:<14} {ratio:<8} {trans:<12} {sprite}")
        if a['is_spritesheet']:
            spritesheets.append(a)

    if spritesheets:
        print(f"\n[!] Detected {len(spritesheets)} potential spritesheets:")
        for s in spritesheets:
            print(f"    - {s['filename']}: {int(s['width'])}x{int(s['height'])} (Aspect Ratio {s['aspect_ratio']})")

if __name__ == '__main__':
    main()

