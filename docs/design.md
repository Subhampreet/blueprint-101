# Blueprint 101: Design System

The reader's visual language is modelled on GreatFrontEnd (Geist type, near-black neutrals, lime brand accent, calm bordered cards) with Excalidraw-style diagrams as the signature illustration. Tokens live at the top of `site/styles.css`; this file explains them and the rules for using them.

## 1. Principles

1. **Content first.** Notes are long; typography, spacing and contrast serve reading. Chrome stays quiet (thin borders, no heavy shadows).
2. **One accent.** Lime is reserved for the primary action on a page, progress, completion and the brand mark. Everything else is neutral. Indigo/violet appear only in decorative gradients and the "senior" chip.
3. **Dark first, light equal.** Every token has a light and a dark value. Never hardcode a color in a component.
4. **Progress is visible.** Wherever notes are listed, show completion (status dots, x/y counts, bars).
5. **Diagrams look hand-drawn.** Architecture is shown as sketches, so it feels like a whiteboard interview, not a vendor brochure.

## 2. Typography

| Role | Font | Size / weight | Tracking |
|---|---|---|---|
| UI and body | Geist (Google Fonts) | 15px / 400, line-height 1.6 | normal |
| Note prose | Geist | 16px / 400, line-height 1.75 | normal |
| Hero title | Geist | 32 to 48px / 600 | -0.035em |
| Page title | Geist | 30 to 40px / 600 | -0.03em |
| Section heading (h2 in blocks) | Geist | 22px / 600 | -0.02em |
| Card title | Geist | 16px / 600 | -0.01em |
| Meta, chips, captions | Geist | 12 to 13px / 500 | normal |
| Code, numbers in labs | Geist Mono | 12.5 to 13.5px | normal |

Use `font-variant-numeric: tabular-nums` for counts and percentages.

## 3. Color tokens

| Token | Dark | Light | Use |
|---|---|---|---|
| `--bg` | `#070708` | `#fafafa` | page background |
| `--bg-elev` | `#0e0e10` | `#ffffff` | hover state of rows/cards |
| `--surface` | `#131316` | `#ffffff` | cards, panels |
| `--surface-2` | `#1b1b1f` | `#f4f4f5` | subtle fills, active nav, table headers |
| `--surface-3` | `#27272a` | `#e4e4e7` | progress track |
| `--border` | `#232327` | `#e4e4e7` | default 1px borders |
| `--border-strong` | `#3f3f46` | `#d4d4d8` | hover borders, kbd |
| `--text` | `#fafafa` | `#18181b` | primary text |
| `--text-2` | `#a1a1aa` | `#52525b` | secondary text, descriptions |
| `--text-3` | `#71717a` | `#71717a` | meta, captions, placeholders |
| `--brand` | `#eafe7c` | `#e4fe71` | primary buttons, brand mark, done states, progress fill |
| `--brand-ink` | `#0a0a0b` | `#0a0a0b` | text/icons on `--brand` |
| `--brand-text` | `#eafe7c` | `#4d7c0f` | brand as text on the page background (contrast-safe in light) |
| `--brand-soft` / `--brand-line` | lime at 9% / 35% | `#f4fcd2` / `#bef264` | brand chips, callouts, active note |
| `--accent-2`, `--accent-3` | `#818cf8`, `#c084fc` | `#6366f1`, `#a855f7` | gradients, "senior" chip only |
| `--series-1..5` | stepped for dark | validated light set | lab charts (categorical, fixed order) |

The brand lime comes from GreatFrontEnd's `hsl(69 98% 74%)`. Never put white text on lime; always `--brand-ink`.

## 4. Spacing, radius, elevation

- Spacing scale (px): 4, 6, 8, 10, 12, 14, 16, 18, 20, 24, 36, 56. Blocks on the Get Started page are separated by 56px.
- Radius: 6 (code, small chips), 8 to 10 (buttons, inputs), 12 (`--radius`, panels, tables), 16 (`--radius-lg`, cards, lists), 20 (hero, flashcard).
- Elevation: borders do the work. `--shadow` only for floating layers (search modal, mobile sidebar).
- Hero and flashcard use `--glow`: two soft radial gradients (lime top-left, indigo top-right) over `--surface`.

## 5. Layout

- Top bar: 64px, sticky, translucent `--bg` with blur, 1px bottom border.
- Desktop: 268px sticky sidebar + content. Content pages cap at 1120px; note pages use a 760px reading column plus a 220px sticky TOC.
- Below 1200px the TOC hides. Below 1080px the sidebar becomes an off-canvas drawer with a scrim and the top links hide. Below 720px grids collapse to one column and the hero stats become 2x2.

## 6. Components

| Component | Class | Notes |
|---|---|---|
| Primary button | `.btn.primary` | lime fill, `--brand-ink` text, one per view |
| Secondary button | `.btn` | surface fill, border, `.small` variant |
| Card | `.card` | 16px radius, 20px padding, border hover only |
| Icon tile | `.icon-tile` (`.brand` variant) | 40px square holding a 20px stroke icon |
| Chip | `.chip` (`.brand`, `.violet`) | 12px pill for tags, levels, status |
| Pill | `.pill` (`.brand`) | 13px stat pill in page headers |
| Progress bar | `.bar > span` | 6px, lime fill on `--surface-3` |
| Status dot | `.status` (`.done`) | empty ring or lime filled with a check |
| Timeline step | `.timeline > .step` | number, icon tile, title + chip, description, chevron |
| Resume card | `.card.resume` | big percent, title, x/y, bar, Resume button |
| List row | `.list > .row-item` | status, title + 2-line summary, section chip + time |
| Company card | `.card.company` | colored monogram `.logo` (no third-party logos) |
| Note prose | `.prose` | tables with rounded border, Q&A `<details>` with lime "Q" badge |
| Diagram figure | `figure.diagram > .frame` | white frame; dark mode inverts the SVG (`--diagram-filter`), like Excalidraw's dark mode |
| Avatar | `.avatar` (`.lg`, `.xl`) | lime circle with initials; user icon when no name |
| Welcome strip | `.card.welcome` | name form for new visitors; streak, counts and Continue for returning ones |
| Local-storage note | `.local-note`, `.callout.local` | lock icon + "saved only in this browser"; shown wherever we collect the name |
| Dialog | `.modal > .modal-box` | 460px, icon tile, title, text, input, actions right aligned |
| My notes | `.memo` | textarea under the note body, saves every keystroke, status on the right |
| Activity heatmap | `.heat` (`.l0` to `.l4`) | 13px day squares, 26 weeks, shades of `--brand-text` so it reads in both themes |
| Danger button | `.btn.danger` | red text; only for destructive actions behind a confirm |
| Lab panel / KPI | `.panel`, `.kpi`, `.seg`, `.field` | segmented controls use lime for the selected option |

Icons: 24px viewBox, 1.75 stroke, round caps and joins (Lucide style), defined in `ICONS` in `site/app.js`. Add new icons there; do not import an icon font.

## 7. Charts (labs)

Follow the data-viz rules used in `labs.js`: one categorical palette in fixed order (`--series-1..5`), thin bars with 4px rounded ends and 2px gaps, recessive grid, a legend whenever there are two or more series, hover tooltips on every mark, no dual axes, text in text colors (never series colors).

## 8. Diagrams

- Generated by `tools/diagrams/sketch.py`: double-stroke jittered lines, pastel Excalidraw fills, handwritten font stack (Virgil, Excalifont, Comic Sans, Chalkboard), white rounded background.
- Vocabulary: `box`, `stack` (N instances), `db` (cylinder), `queue`, `user`, `cloud`, `zone` (dashed group), `note` (sticky), `arrow`/`line`, `lifeline`/`msg` (sequence diagrams).
- Colors by role: blue = services, green = data stores, yellow = queues and notes, violet = gateways/LBs, orange = workers/pipelines, red = caches or failure, cyan = edge/storage, gray = external/idle.
- Each diagram gets a title, at most about 12 nodes, and labels on arrows only where they add meaning.

## 9. Writing style

- Plain, direct sentences; numbers over adjectives.
- No em dashes or en dashes (use colons, commas, parentheses or "to" for ranges). CI enforces this.
- Notes end with `## Interview questions` and `## Related`.

## 10. Accessibility checklist

- Icon-only buttons have `aria-label`.
- Focus ring: 2px `--brand-text` outline.
- Progress bars expose `role="progressbar"` with `aria-valuenow`.
- Color is never the only signal: done states also show a check, chips carry text.
- `prefers-reduced-motion` disables transitions.
