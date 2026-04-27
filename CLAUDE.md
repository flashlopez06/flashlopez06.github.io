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
- **Palette**: `#4af0a8` (green accent), `#5b9fff` (blue accent), dark background
- **Fonts**: Outfit, JetBrains Mono, DM Sans via Google Fonts
- **Analytics**: GA4 embedded in `<head>`

## Deployment

Push to `main` → GitHub Pages auto-deploys. Custom domain set via `CNAME` (flashlopez.dev).
