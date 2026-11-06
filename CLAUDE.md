# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Static portfolio site hosted on GitHub Pages at flashlopez.dev. No build pipeline — pure HTML/CSS/JS.

## Development

No build tools or package manager. To preview locally:

```bash
python3 -m http.server 8080
# or
npx serve .
```

Then open http://localhost:8080.

## Architecture

Everything lives in `index.html` — a single-file SPA with embedded CSS and JavaScript. No external JS dependencies.

- **Styles**: CSS custom properties for theming, `clamp()` for fluid typography, CSS animations (`fadeUp`, `pulse`, `fadeLeft`) for entrance effects
- **Palette**: `#c8956c` (copper accent), `#d4a96a` (amber secondary), near-black background (`#0a0a0f`)
- **Fonts**: Fraunces (display/serif), Inter (body/mono) via Google Fonts
- **Analytics**: GA4 embedded in `<head>`

## Deployment

Push to `main` → GitHub Pages auto-deploys. Custom domain set via `CNAME` (flashlopez.dev).

## Advisor Strategy (Opus)

Spawn an Opus advisor before:
- Any significant copy/positioning change (hero, about, section headers) — wrong framing changes how the site reads
- Design direction decisions (palette, layout, typography)
- Adding or removing content sections

Call pattern:
```
Agent(
  model="opus",
  description="Opus advisor — [decision in 5 words]",
  prompt="Context: personal portfolio site for a senior DevOps engineer.\nProblem: [specific decision]\nOptions: [list]\nQuestion: [single crisp question]\nRespond under 150 words. Plan only."
)
```

Skip advisor for: typo fixes, metadata updates, PDF/DOCX swaps, CSS micro-tweaks that don't change visual direction.

## Resume PDF (must stay readable by hiring software)

The PDF is made by Claude: open the `.docx` in Pages (Apple's word processor), export PDF. Pages joins letter pairs ("fl", "tf", "ti") into single glyphs that resume parsers drop — Lever read the email as `michael@ashlopez.dev` (2026-10-22). After every new export, run:

```bash
python3 tools/fix_resume_ligatures.py export.pdf Michael-Lopez-Resume.pdf
pdftotext Michael-Lopez-Resume.pdf - | head -3   # must show michael@flashlopez.dev
pdftotext Michael-Lopez-Resume.pdf - | grep -cE 'Pla orm|produc on'   # must be 0
```
