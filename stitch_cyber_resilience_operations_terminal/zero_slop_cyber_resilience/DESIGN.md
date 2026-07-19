---
name: Zero-Slop Cyber Resilience
colors:
  surface: '#141313'
  surface-dim: '#141313'
  surface-bright: '#3a3939'
  surface-container-lowest: '#0e0e0e'
  surface-container-low: '#1c1b1b'
  surface-container: '#201f1f'
  surface-container-high: '#2a2a2a'
  surface-container-highest: '#353434'
  on-surface: '#e5e2e1'
  on-surface-variant: '#c4c7c8'
  inverse-surface: '#e5e2e1'
  inverse-on-surface: '#313030'
  outline: '#8e9192'
  outline-variant: '#444748'
  surface-tint: '#c6c6c6'
  primary: '#fdfdfc'
  on-primary: '#2f3131'
  primary-container: '#e0e0e0'
  on-primary-container: '#626363'
  inverse-primary: '#5d5f5f'
  secondary: '#c8c6c6'
  on-secondary: '#303030'
  secondary-container: '#474747'
  on-secondary-container: '#b6b5b4'
  tertiary: '#fffbff'
  on-tertiary: '#342f2d'
  tertiary-container: '#e7deda'
  on-tertiary-container: '#67615e'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#e2e2e2'
  primary-fixed-dim: '#c6c6c6'
  on-primary-fixed: '#1a1c1c'
  on-primary-fixed-variant: '#454747'
  secondary-fixed: '#e4e2e1'
  secondary-fixed-dim: '#c8c6c6'
  on-secondary-fixed: '#1b1c1c'
  on-secondary-fixed-variant: '#474747'
  tertiary-fixed: '#eae1dd'
  tertiary-fixed-dim: '#cdc5c1'
  on-tertiary-fixed: '#1f1b19'
  on-tertiary-fixed-variant: '#4b4643'
  background: '#141313'
  on-background: '#e5e2e1'
  surface-variant: '#353434'
typography:
  display-lg:
    fontFamily: JetBrains Mono
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: JetBrains Mono
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-sm:
    fontFamily: JetBrains Mono
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
  body-lg:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  code-table:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: '400'
    lineHeight: 14px
  label-caps:
    fontFamily: JetBrains Mono
    fontSize: 10px
    fontWeight: '700'
    lineHeight: 12px
spacing:
  unit: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  gutter: 1px
  margin: 16px
---

## Brand & Style

The design system is built on **Utilitarian Brutalism**, optimized for high-stakes Security Operations Centers (SOC). The brand personality is clinical, unforgiving, and hyper-efficient. It treats the interface as a precision instrument rather than a consumer product, eliminating "slop"—unnecessary decorative elements, soft edges, and organic transitions.

The target audience consists of cybersecurity analysts and system architects who require maximum information density and zero visual latency. The emotional response is one of absolute control and situational awareness. The aesthetic draws directly from terminal emulators and mainframe readouts, utilizing a strict 1px grid-based logic.

## Colors

The palette is strictly functional. The background is a true black (`#000000`) to minimize eye strain in low-light SOC environments and maximize the contrast of active elements. 

- **Primary Text:** `#E0E0E0` provides high legibility without the harshness of pure white.
- **Borders/Structure:** `#333333` defines the grid and containers.
- **Status Colors:** These are used exclusively for data state and alerting. 
    - `CRITICAL`: `#FF0000` (Red)
    - `WARNING`: `#FFFF00` (Yellow)
    - `SECURE`: `#00FF00` (Green)

Interactive states (hover/active) should be represented by color inversion or solid fills rather than glows or gradients.

## Typography

This design system utilizes **JetBrains Mono** across all levels to maintain a rigid, monospaced vertical rhythm. Monospace is selected for its superior character differentiation (0 vs O, 1 vs l) and its ability to align data perfectly across columns.

- **Vertical Rhythm:** All line heights must be multiples of 4px to snap to the layout grid.
- **Alignment:** Numbers must always be tabular to ensure vertical alignment in data tables.
- **Scale:** High density is prioritized. The primary body size is 12px, with 11px used for dense log data.
- **Emphasis:** Use weight shifts (Bold) or color changes (Primary to Status) rather than italics.

## Layout & Spacing

The layout is a **strict fluid grid** based on a 4px module. Elements are separated by 1px solid borders (`#333333`) rather than whitespace, creating a "tiled" effect reminiscent of a terminal multiplexer (like tmux).

- **Grid:** A 12-column layout is used for top-level organization, but sub-containers use nested flexbox/grid layouts that must snap to the 4px increment.
- **Gutters:** Gutters are effectively 1px (the border itself). No additional gap is used between adjacent borders.
- **Density:** Padding inside containers is kept to a minimum (typically 8px or 16px) to maximize the amount of visible data.
- **Mobile:** On small screens, columns stack vertically, and the 1px borders become the primary visual separators.

## Elevation & Depth

This design system is strictly **2D and flat**. There is no concept of physical elevation, light sources, or shadows.

- **Hierarchy via Tiers:** Depth is communicated through nested borders and background shifts. A "raised" element (like an active tab) is shown by inverting the colors (Background: `#E0E0E0`, Text: `#000000`).
- **Overlays:** Modals or dropdowns are defined by thick 2px solid borders to distinguish them from the background grid. They do not have shadows or background blurs; they are opaque.
- **Focus:** The active element or focused input is indicated by a high-contrast color shift or a solid 2px border.

## Shapes

The shape language is **strictly rectangular**. 

- **Corners:** Every element (buttons, cards, inputs, tags) must have a `border-radius` of `0`.
- **Lines:** Borders are 1px solid. Use 2px borders only for active/focused states or top-level modal containers.
- **Symbols:** Use raw Unicode characters (e.g., `[+]`, `[-]`, `[!]`, `▲`, `▼`, `█`) or simple, un-stroked geometric SVG shapes for icons.

## Components

### Buttons
- **Default:** 1px border `#333333`, text `#E0E0E0`, background `#000000`.
- **Hover/Active:** Background `#E0E0E0`, text `#000000`.
- **Action Indicators:** Use brackets to frame text, e.g., `[ RUN QUERY ]`.

### Inputs
- **Text Fields:** 1px border `#333333`. Placeholder text in `#666666`. 
- **Focus:** Border becomes 1px `#E0E0E0` or `#00FF00`.
- **Checkboxes:** Square boxes `[ ]` for unchecked, `[X]` or `[█]` for checked. No animation.

### Data Tables
- **Header:** Background `#333333`, text `#000000` (inverted) or bold `#E0E0E0`.
- **Rows:** 1px bottom border. No zebra striping. Use color-coded text for status columns.
- **Selection:** Full row background becomes `#333333`.

### Cards / Containers
- Every module must have a 1px border. 
- **Title Bar:** A header section within the card with a 1px bottom border, often containing the title in `label-caps`.

### Chips / Tags
- Inline text wrapped in brackets, e.g., `[TAG:VALUE]`. 
- For alerts: `[!! CRITICAL !!]` in `#FF0000`.

### Symbols & Icons
- Avoid illustrative icons. Use standard CLI conventions:
    - Search: `[ / ]`
    - Close: `[ X ]`
    - Expand: `[ + ]`
    - Critical: `[ ! ]`