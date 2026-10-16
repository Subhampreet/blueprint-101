# Blueprint 101: Product Requirements

Status: living document. Last updated October 2026.

## 1. Problem

Engineers preparing for system design interviews at product companies juggle scattered resources: long GitHub primers, paid courses, blog posts and whiteboard tools. They lack one place that combines depth (how things really work), practice (realistic interview walkthroughs and questions), intuition (seeing trade-offs move) and a plan (what to study, in what order, for the time they have).

## 2. Goal

A free, self-hostable, one-stop system design preparation site that takes someone from "where do I start" to "I can lead a 45 minute design round", built from Markdown notes in this repository.

Inspiration: the structure of GreatFrontEnd's "Get Started" page (study plans, recommended path, company guides, focus areas, progress) and fanout.sh (concepts, case studies, builds, labs).

## 3. Users

| Persona | Need | What they use most |
|---|---|---|
| Interview soon (1 to 2 weeks) | Highest-yield material, fast | 1 Week plan, Interview Framework, flashcards |
| Planned prep (1 to 3 months) | Structured, complete coverage with progress | Study plans, focus areas, case studies, labs |
| Senior / staff candidate | Depth for follow-ups: failures, consistency, scale, cost | Advanced topics, deep dives in case studies |
| Company-targeted | Practice the products a company is known for | Company practice sets |
| Visual learner | See architectures and trade-offs | Diagrams, interactive labs |

## 4. Scope

### In scope (shipped)

- **Notes**: 96 Markdown notes in 14 sections with front matter (`title`, `summary`, `tags`, `level`, `time`, optional `lab`). Every note ends with interview Q&A in `<details>` blocks.
- **Diagrams**: hand-drawn (Excalidraw style) SVGs generated from Python definitions, each with an editable `.excalidraw` source.
- **Builds**: runnable from-scratch implementations with self-checks, embedded into notes via `tools/sync_builds.py`.
- **Reader site** (`site/`, static, no framework):
  - Get Started dashboard: hero with stats, resume cards, recommended 4-step path, study plans, company practice sets, focus areas, practice formats.
  - Study plans (1 Week, 1 Month, 3 Months) and company practice sets, each a list page with progress and a Continue button.
  - Section pages, note pages (TOC, prev/next, mark complete, Excalidraw downloads, lightbox), search (`/` or Cmd+K), flashcards (Leitner boxes), diagram gallery, 10 interactive labs.
  - Local learner profile (see section 4a): name, progress, flashcard boxes, bookmarks, personal notes and daily streak, all in `localStorage`.
  - "Your progress" page (`#/profile`): stats, activity heatmap, saved and recently completed notes, per-section progress, export/import/reset.
  - Light and dark themes; responsive down to 360px.
- **Tooling**: `tools/build_site.py` (content.js, site assets, README index), `tools/check_notes.py` (lint, links, no long dashes), CI workflow.

### 4a. Learner profile and local persistence

Many people use the site, each with their own progress, but there are no accounts and no backend. Decision: keep everything in the browser's `localStorage`.

| Option | Survives refresh and restart | Effort | Verdict |
|---|---|---|---|
| `localStorage` | Yes (until site data is cleared) | Synchronous key/value, about 5 MB per origin | **Chosen**: our data is tens of KB, reads are instant, no async plumbing |
| `sessionStorage` | No (dies with the tab) | Same API | Rejected |
| IndexedDB | Yes | Async, transactions, more code | Overkill for small JSON; revisit only if we store large blobs |
| Cookies | Yes | 4 KB limit, sent with every request | Rejected |
| Cache API / service worker | Yes | Built for HTTP responses | Wrong tool (could later power offline reading) |
| Backend DB + accounts | Across devices | Auth, hosting, privacy work | Out of scope; export/import covers moving devices |

Rules:

- **Keys** (all prefixed `bp-`): learner data `profile`, `done`, `boxes`, `saved`, `activity`, `memo`, `last`; preferences `theme`, `open`, `fc-scope`. Export, import and reset act on learner data only.
- **Name prompt**: a "Track your progress" card on Get started, and a one-time dialog the first time someone marks a note complete without a profile. "Not now" records an empty name so we never ask twice.
- **Say where data lives**: every place that collects the name states that progress is saved only in this browser on this device, and the profile page explains what erases it (clearing site data, private windows, another browser).
- **Never throw**: every storage call is wrapped; if storage is blocked the site works and the profile page shows a warning.
- **Eviction**: after a name is saved we call `navigator.storage.persist()` so the browser keeps the data under storage pressure where supported.
- **Backup format**: `{ app: "blueprint-101", version: 1, exported, data: {...} }`. Import validates and drops unknown notes, malformed values and unknown keys, then replaces local data after a confirmation.
- **Multi-tab**: a `storage` event listener reloads state so progress made in one tab shows up in the others.
- **Privacy**: nothing is sent anywhere; the name is only shown back to the learner.

### Out of scope (for now)

- Accounts, server-side progress sync, payments.
- User-generated content or comments.
- A full in-browser whiteboard (link to Excalidraw instead).

## 5. Requirements

### Functional

1. Every note is reachable from the sidebar, its section page, search, and at least one of: a study plan, a company set, or the recommended path.
2. Marking a note complete updates progress everywhere (sidebar, cards, plans, companies, sections) without reload.
3. Images and downloads work when the deployment root is `site/` (Vercel) and when the repo root is served (local, GitHub Pages).
4. Links inside notes to other notes stay inside the reader; links to code (`builds/`, `tools/`) open on GitHub.
5. Labs run fully client-side and stop their animation loops on navigation.
6. Flashcards are generated automatically from note Q&A; no manual deck maintenance.
7. Progress, bookmarks, notes and streaks persist across refreshes and browser restarts in the same browser, and can be exported and imported as a JSON file.

### Non-functional

- Static: deployable by copying `site/`. No build step on the host.
- Fast: first load is one HTML, one CSS, three small scripts and the content bundle (about 2 MB uncompressed, compresses well). Diagrams lazy-load.
- Works offline-ish: if the `marked` CDN fails, a built-in Markdown renderer takes over.
- Accessible: keyboard navigation, visible focus, ARIA labels on icon buttons, respects `prefers-reduced-motion`, text contrast AA in both themes.
- Content style: no em dashes or en dashes anywhere (enforced by `check_notes.py`).

## 6. Information architecture

```text
Get started (#/)
  Study plans (#/plans) -> plan (#/plan/<id>) -> note
  Company practice sets (#/company/<id>) -> note
  Focus areas = sections (#/section/<id>) -> note (#/note/<section>/<slug>[~anchor])
  Labs (#/labs) -> lab (#/lab/<id>)
  Flashcards (#/flashcards[/<section or slug>])
  Diagram gallery (#/diagrams)
  Your progress (#/profile): profile, stats, backup
```

Routing is hash-based so it works on any static host and from `file://`.

## 7. Content model

| Source | Becomes |
|---|---|
| `notes/<NN-section>/<NN-slug>.md` | a note page, sidebar entry, search entry, README index row |
| `## Interview questions` `<details>` blocks | flashcards |
| front matter `lab: <id>` | "Open the lab" button and lab back-links |
| `tools/diagrams/defs/*.py` | `assets/diagrams/*.svg` + `.excalidraw`, copied to `site/assets/` |
| `PLANS`, `COMPANIES` in `tools/build_site.py` | study plans and company sets (validated against note slugs at build time) |

## 8. Success measures

- A new reader can find "what to study first" within 10 seconds of landing (recommended path above the fold on desktop).
- Zero broken links or images (CI-enforced).
- Every case study has a diagram and at least 3 interview questions.

## 9. Roadmap ideas

1. Shipped: export/import progress (JSON). Next: optional sync through a share code or a user-owned file (e.g. a GitHub gist) without running our own backend.
2. Timed mock mode: pick a case study, 45 minute timer, structured self-review rubric.
3. Per-company question frequency notes once sourced from public interview reports.
4. More labs: consistent hashing with bounded load, Raft leader election, CDN cache hit ratio, Little's law.
5. Prerendered static HTML per note for SEO and link previews.
