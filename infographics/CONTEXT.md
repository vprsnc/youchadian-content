# Infographics — Context and Design System

## Design tokens (all infographics share this)

```css
--bg:       #f0e8d8;   /* warm parchment page background */
--card-bg:  #faf5ec;   /* card surface */
--coral:    #d95f3b;   /* primary accent (headers, badges) */
--teal:     #2a9d8f;   /* secondary accent (titles, links) */
--ink:      #1e1a16;   /* body text */
--muted:    #7a6e63;   /* secondary text, tags */
--border:   #ddd5c5;   /* dividers, card borders */
--tag-bg:   #ede5d5;   /* small pill/tag backgrounds */
```

Font: `Inter` from Google Fonts (400 / 500 / 600).  
Card width: `1100px`, `border-radius: 16px`.  
Entry animation: `@keyframes up` — fade + translateY(10px), staggered 50 ms per column.

## Per-category color palette (tea categories infographic)

```css
--c-green:  #3d8c5c;
--c-white:  #7d9fa8;
--c-yellow: #c49a1a;
--c-oolong: #2a9d8f;
--c-red:    #b83225;
--c-dark:   #6b4c3b;
```

## Oolong process step colors

```css
--sc-1: #3d8c5c;   /* picking      — fresh green  */
--sc-2: #c49a1a;   /* withering    — golden sun   */
--sc-3: #2a9d8f;   /* tossing      — teal         */
--sc-4: #d95f3b;   /* kill-green   — flame/coral  */
--sc-5: #7a6042;   /* rolling      — earth brown  */
--sc-6: #b87333;   /* drying       — copper amber */
```

Applied to `.stage-num` (circle bg), `.stage-icon` (SVG color), `.stage-chinese` (label).

## Infographic status

| Slug | Article | Status | Notes |
|---|---|---|---|
| `oolong-overview` | `oolong-overview__tea_oolong-dark` | ✅ done | 6-stage process, per-step colors, photo-traced schematic icons (80×80) |
| `chinese-tea-categories` | `chinese-tea-categories__guide` | ✅ done | 6-category oxidation spectrum, per-category colors, inline SVG icons |
| `water-for-tea` | `water-for-tea__guide` | 🔜 planned | needs pictures — see below |
| `gongfu-brewing-guide` | `gongfu-brewing-guide__guide` | 🔜 planned | needs pictures — see below |

## Picture requirements

### `water-for-tea`

Core visual concept: **vertical thermometer / temperature scale** with boiling stage illustrations.

Needed shots:
- Close-up of glass kettle at shrimp-eye stage (75–80 °C) — tiny bubbles just forming on glass
- Crab-eye stage (80–85 °C) — small pearls rising
- Fish-eye / rolling boil (95–100 °C) — full turbulence
- Ideally natural light, glass kettle on dark surface

Alt if no photos available: CSS-drawn bubbles of increasing size at each temperature band.  
The thermometer scale itself (75 °C → 100 °C with tea-type labels) can be built in pure CSS.

### `gongfu-brewing-guide`

Core visual concept: **step-by-step process strip** (like oolong-overview) + a parameter reference grid (tea type × water temp × steep time × leaf ratio).

Needed shots:
- Hero shot of gaiwan with tea being poured (arc shot)
- Dry leaf in gaiwan (overhead)
- Cup lineup on a tea tray

The existing hero `https://upload.wikimedia.org/wikipedia/commons/8/89/Gong_fu_cha.jpg` is a Wikipedia commons image — usable for reference but low resolution. Better to use our own shots or inline SVG for the step icons.

Alt if no photos: pure emoji + CSS icons work for the process steps (we already do this in oolong-overview). The parameter grid can be a clean HTML table with colored cells.

## Icon system

`infographics/icons.svg` — canonical sprite sheet, inline-embedded in each HTML.  
All symbols use `currentColor` so CSS `color` property themes them.  
ViewBox: **48×48** for tea category icons, **80×80** for oolong process step icons.

Process step icons traced from real 采茶/晒青/做青/杀青/揉捻/烘焙 reference photos:
- picking: bud + two broad wing leaves (V silhouette)
- solar-withering: round bamboo sieve with thick rim + small sun
- tossing: wide barrel/drum + two X-crossing paddle handles
- kill-green: top-view wooden frame ring + wok rim + two hands inside
- rolling: bamboo sieve + two hands pressing from above
- drying: tall 焙笼 bamboo basket + sieve top + thermometer gauge

## Layout patterns used

- **6-column equal grid**: `grid-template-columns: repeat(6, 1fr)` — used in oolong-overview and categories
- **Oxidation spectrum bar**: `linear-gradient` spanning card width above category columns
- **Process step strip**: numbered circles + connector line (`::before` pseudo-element)
- **No eyebrow tag, no footer** — stripped from categories to match oolong style
- **Parameter grid**: will be used in water-for-tea and gongfu

## File naming

```
infographics/en/<slug>.html
infographics/ru/<slug>-ru.html
infographics/bg/<slug>-bg.html
```
