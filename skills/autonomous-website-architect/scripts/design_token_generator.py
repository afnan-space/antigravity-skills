#!/usr/bin/env python3
"""
Autonomous Design Token Generator
Generates cohesive, production-grade CSS variables, color palettes, typography scales,
and geometric tokens for 7 standard archetypes:
gaming, web3, saas, ecommerce, portfolio, dashboard, business.
Zero external dependencies (uses standard library).
"""

import sys
import json

ARCHETYPES = {
    'gaming': {
        'google_fonts': 'family=Bebas+Neue&family=Barlow:wght@500;600;700&family=Barlow+Condensed:wght@600;700&display=swap',
        'display_font': '"Bebas Neue", "Barlow Condensed", Impact, sans-serif',
        'body_font': '"Barlow", system-ui, -apple-system, sans-serif',
        'hud_font': '"Barlow Condensed", sans-serif',
        'bg': '#090604',
        'surface': 'rgba(18, 12, 8, 0.75)',
        'surface_solid': '#140d09',
        'line': 'rgba(255, 170, 90, 0.16)',
        'primary': '#ff8a2b',
        'accent': '#ffb547',
        'text': '#f6ead8',
        'text_muted': '#8f7c67',
        'glow': 'rgba(255, 138, 43, 0.45)',
        'cut': '14px',
        'radius': '0px',
    },
    'web3': {
        'google_fonts': 'family=Syne:wght@700;800&family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap',
        'display_font': '"Syne", "Space Grotesk", sans-serif',
        'body_font': '"Space Grotesk", system-ui, sans-serif',
        'hud_font': '"JetBrains Mono", monospace',
        'bg': '#06080e',
        'surface': 'rgba(15, 23, 42, 0.65)',
        'surface_solid': '#0f172a',
        'line': 'rgba(56, 189, 248, 0.2)',
        'primary': '#38bdf8',
        'accent': '#a855f7',
        'text': '#f8fafc',
        'text_muted': '#64748b',
        'glow': 'rgba(56, 189, 248, 0.35)',
        'cut': '0px',
        'radius': '16px',
    },
    'saas': {
        'google_fonts': 'family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap',
        'display_font': '"Plus Jakarta Sans", sans-serif',
        'body_font': '"Inter", system-ui, sans-serif',
        'hud_font': '"Plus Jakarta Sans", sans-serif',
        'bg': '#0a0d14',
        'surface': 'rgba(20, 24, 36, 0.8)',
        'surface_solid': '#121624',
        'line': 'rgba(255, 255, 255, 0.08)',
        'primary': '#6366f1',
        'accent': '#38bdf8',
        'text': '#f1f5f9',
        'text_muted': '#94a3b8',
        'glow': 'rgba(99, 102, 241, 0.25)',
        'cut': '0px',
        'radius': '12px',
    },
    'ecommerce': {
        'google_fonts': 'family=Playfair+Display:ital,wght@0,600;0,700;1,400&family=Outfit:wght@400;500;600;700&display=swap',
        'display_font': '"Playfair Display", Georgia, serif',
        'body_font': '"Outfit", system-ui, sans-serif',
        'hud_font': '"Outfit", sans-serif',
        'bg': '#0c0a09',
        'surface': 'rgba(28, 25, 23, 0.7)',
        'surface_solid': '#1c1917',
        'line': 'rgba(214, 180, 140, 0.18)',
        'primary': '#d4af37',
        'accent': '#e7c975',
        'text': '#fafaf9',
        'text_muted': '#a8a29e',
        'glow': 'rgba(212, 175, 55, 0.3)',
        'cut': '0px',
        'radius': '8px',
    },
    'portfolio': {
        'google_fonts': 'family=Clash+Display:wght@600;700&family=Satoshi:wght@400;500;700&display=swap',
        'display_font': '"Clash Display", -apple-system, sans-serif',
        'body_font': '"Satoshi", system-ui, sans-serif',
        'hud_font': '"Satoshi", sans-serif',
        'bg': '#080808',
        'surface': '#121212',
        'surface_solid': '#181818',
        'line': 'rgba(255, 255, 255, 0.12)',
        'primary': '#ffffff',
        'accent': '#ff3366',
        'text': '#f4f4f4',
        'text_muted': '#777777',
        'glow': 'rgba(255, 51, 102, 0.35)',
        'cut': '0px',
        'radius': '20px',
    },
    'dashboard': {
        'google_fonts': 'family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap',
        'display_font': '"Inter", system-ui, sans-serif',
        'body_font': '"Inter", system-ui, sans-serif',
        'hud_font': '"JetBrains Mono", monospace',
        'bg': '#0b0f19',
        'surface': '#111827',
        'surface_solid': '#1f2937',
        'line': 'rgba(75, 85, 99, 0.3)',
        'primary': '#2563eb',
        'accent': '#10b981',
        'text': '#f9fafb',
        'text_muted': '#9ca3af',
        'glow': 'rgba(37, 99, 235, 0.25)',
        'cut': '0px',
        'radius': '10px',
    },
    'business': {
        'google_fonts': 'family=Cabinet+Grotesk:wght@700;800&family=DM+Sans:wght@400;500;700&display=swap',
        'display_font': '"Cabinet Grotesk", sans-serif',
        'body_font': '"DM Sans", system-ui, sans-serif',
        'hud_font': '"DM Sans", sans-serif',
        'bg': '#090d16',
        'surface': 'rgba(17, 24, 39, 0.7)',
        'surface_solid': '#111827',
        'line': 'rgba(148, 163, 184, 0.15)',
        'primary': '#0ea5e9',
        'accent': '#38bdf8',
        'text': '#f8fafc',
        'text_muted': '#94a3b8',
        'glow': 'rgba(14, 165, 233, 0.3)',
        'cut': '0px',
        'radius': '12px',
    }
}

def generate_tokens(archetype_key):
    cfg = ARCHETYPES.get(archetype_key.lower(), ARCHETYPES['saas'])
    css = f"""/* Cohesive Design Tokens — Archetype: {archetype_key.upper()} */
@import url('https://fonts.googleapis.com/css2?{cfg['google_fonts']}');

:root {{
  /* Palette */
  --bg: {cfg['bg']};
  --surface: {cfg['surface']};
  --surface-solid: {cfg['surface_solid']};
  --line: {cfg['line']};
  --primary: {cfg['primary']};
  --accent: {cfg['accent']};
  --text: {cfg['text']};
  --text-muted: {cfg['text_muted']};
  --glow: {cfg['glow']};

  /* Typography */
  --font-display: {cfg['display_font']};
  --font-body: {cfg['body_font']};
  --font-hud: {cfg['hud_font']};

  /* Proportions & Geometry */
  --radius: {cfg['radius']};
  --cut: {cfg['cut']};
  --wrap: 1240px;
  --gutter: 24px;
  --header-height: 76px;

  color-scheme: dark;
}}
"""
    return css

def main():
    if len(sys.argv) < 2:
        print("Usage: python design_token_generator.py <archetype> (gaming, web3, saas, ecommerce, portfolio, dashboard, business)")
        sys.exit(1)

    arch = sys.argv[1].lower()
    print(generate_tokens(arch))

if __name__ == '__main__':
    main()

