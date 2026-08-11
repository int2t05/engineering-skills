# Apple HIG Reference

Design guidance based on Apple's official Human Interface Guidelines. **Default: concise answer +
official URL.** Expand with detail only when explicitly asked. For comprehensive deep-dives,
scrape the official page on the fly — never guess.

**Base URL pattern:** `https://developer.apple.com/design/human-interface-guidelines/{topic-slug}`

## Verbosity control

| User says | Response |
|-----------|----------|
| Default (no verbosity keyword) | 1 sentence answer + official URL |
| "详细" / "展开" / "detail" / "多说点" | Key specs as table + cross-platform comparison + official URL |
| "完整" / "full" / "全部" / "所有细节" / "爬取" | Use a web-scraping tool (e.g. Firecrawl) to fetch the official page, then provide comprehensive guidance |

Never dump a wall of text by default. The full docs live on Apple's site. Your job is routing and
synthesis, not duplication.

## Quick reference: most common specs

### Touch & hit targets

| Platform | Default | Minimum |
|----------|:-------:|:-------:|
| iOS/iPadOS | 44×44 pt | 28×28 pt |
| macOS | 28×28 pt | 20×20 pt |
| tvOS | 66×66 pt | 56×56 pt |
| visionOS | 60×60 pt | 28×28 pt |
| watchOS | 44×44 pt | 28×28 pt |

### Text sizes

| Platform | Default | Minimum |
|----------|:-------:|:-------:|
| iOS/iPadOS | 17 pt | 11 pt |
| macOS | 13 pt | 10 pt |
| tvOS | 29 pt | 23 pt |
| visionOS | 17 pt | 12 pt |
| watchOS | 16 pt | 12 pt |

### 8 core design principles

Purpose, Agency, Responsibility, Familiarity, Flexibility, Simplicity, Craft, Delight.

## Routing table: official HIG URLs

### Getting started & design principles

| Topic | URL |
|-------|-----|
| All platforms overview | https://developer.apple.com/design/human-interface-guidelines/getting-started |
| Design principles (8) | https://developer.apple.com/design/human-interface-guidelines/design-principles |

### Platform-specific design

| Platform | URL |
|----------|-----|
| iOS (iPhone) | https://developer.apple.com/design/human-interface-guidelines/designing-for-ios |
| iPadOS | https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados |
| macOS | https://developer.apple.com/design/human-interface-guidelines/designing-for-macos |
| tvOS | https://developer.apple.com/design/human-interface-guidelines/designing-for-tvos |
| visionOS | https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos |
| watchOS | https://developer.apple.com/design/human-interface-guidelines/designing-for-watchos |
| Games (all platforms) | https://developer.apple.com/design/human-interface-guidelines/designing-for-games |

### Foundations

| Topic | URL |
|-------|-----|
| Foundations overview | https://developer.apple.com/design/human-interface-guidelines/foundations |
| Accessibility | https://developer.apple.com/design/human-interface-guidelines/accessibility |
| App icons | https://developer.apple.com/design/human-interface-guidelines/app-icons |
| Color | https://developer.apple.com/design/human-interface-guidelines/color |
| Icons (SF Symbols) | https://developer.apple.com/design/human-interface-guidelines/icons |
| Inclusion | https://developer.apple.com/design/human-interface-guidelines/inclusion |
| Layout | https://developer.apple.com/design/human-interface-guidelines/layout |
| Materials | https://developer.apple.com/design/human-interface-guidelines/materials |
| Motion | https://developer.apple.com/design/human-interface-guidelines/motion |
| Right to left | https://developer.apple.com/design/human-interface-guidelines/right-to-left |
| Typography | https://developer.apple.com/design/human-interface-guidelines/typography |

### Patterns

| Topic | URL |
|-------|-----|
| Patterns overview | https://developer.apple.com/design/human-interface-guidelines/patterns |
| Onboarding | https://developer.apple.com/design/human-interface-guidelines/onboarding |
| Settings | https://developer.apple.com/design/human-interface-guidelines/settings |
| Navigation | https://developer.apple.com/design/human-interface-guidelines/navigation |
| Modality | https://developer.apple.com/design/human-interface-guidelines/modality |
| Notifications | https://developer.apple.com/design/human-interface-guidelines/notifications |
| Drag and drop | https://developer.apple.com/design/human-interface-guidelines/drag-and-drop |
| File management | https://developer.apple.com/design/human-interface-guidelines/file-management |
| Privacy | https://developer.apple.com/design/human-interface-guidelines/privacy |
| Search | https://developer.apple.com/design/human-interface-guidelines/searching |

**Pattern for other topics:** Slugs use kebab-case (e.g. `launching`, `loading`,
`going-full-screen`, `managing-accounts`, `managing-notifications`, `multitasking`,
`ratings-and-reviews`, `undo-and-redo`).

### Components

| Topic | URL |
|-------|-----|
| Components overview | https://developer.apple.com/design/human-interface-guidelines/components |
| Buttons | https://developer.apple.com/design/human-interface-guidelines/buttons |
| Navigation bars | https://developer.apple.com/design/human-interface-guidelines/navigation-bars |
| Tab bars | https://developer.apple.com/design/human-interface-guidelines/tab-bars |
| Sidebars | https://developer.apple.com/design/human-interface-guidelines/sidebars |
| Toolbars | https://developer.apple.com/design/human-interface-guidelines/toolbars |
| Menus | https://developer.apple.com/design/human-interface-guidelines/menus |
| Alerts | https://developer.apple.com/design/human-interface-guidelines/alerts |
| Sheets | https://developer.apple.com/design/human-interface-guidelines/sheets |
| Text fields | https://developer.apple.com/design/human-interface-guidelines/text-fields |
| Toggles | https://developer.apple.com/design/human-interface-guidelines/toggles |
| Sliders | https://developer.apple.com/design/human-interface-guidelines/sliders |

**Pattern for other components:** Slugs use kebab-case (e.g. `progress-indicators`, `popovers`,
`scroll-views`, `search-fields`, `steppers`, `pickers`, `tables`, `split-views`, `widgets`).

### Inputs

| Topic | URL |
|-------|-----|
| Inputs overview | https://developer.apple.com/design/human-interface-guidelines/inputs |
| Gestures | https://developer.apple.com/design/human-interface-guidelines/gestures |
| Keyboards | https://developer.apple.com/design/human-interface-guidelines/keyboards |
| Pointing devices | https://developer.apple.com/design/human-interface-guidelines/pointing-devices |
| Game controls | https://developer.apple.com/design/human-interface-guidelines/game-controls |
| Apple Pencil & Scribble | https://developer.apple.com/design/human-interface-guidelines/apple-pencil-and-scribble |
| Digital Crown | https://developer.apple.com/design/human-interface-guidelines/digital-crown |

### Technologies

| Topic | URL |
|-------|-----|
| Technologies overview | https://developer.apple.com/design/human-interface-guidelines/technologies |
| Siri | https://developer.apple.com/design/human-interface-guidelines/siri |
| Apple Pay | https://developer.apple.com/design/human-interface-guidelines/apple-pay |
| HomeKit | https://developer.apple.com/design/human-interface-guidelines/homekit |
| Game Center | https://developer.apple.com/design/human-interface-guidelines/game-center |
| iCloud | https://developer.apple.com/design/human-interface-guidelines/icloud |
| CarPlay | https://developer.apple.com/design/human-interface-guidelines/carplay |
| WidgetKit | https://developer.apple.com/design/human-interface-guidelines/widgets |
| SharePlay | https://developer.apple.com/design/human-interface-guidelines/shareplay |

## URL construction rules

For topics not in the routing table, construct the URL as:

```
https://developer.apple.com/design/human-interface-guidelines/{kebab-case-topic-slug}
```

Common slug patterns:
- Multi-word: `navigation-bars`, `search-fields`, `scroll-views`
- Acronyms stay uppercase: `visionOS`, `watchOS`, `tvOS`
- Action verbs: `going-full-screen`, `managing-accounts`
- Group words: `drag-and-drop`, `undo-and-redo`

If unsure of the exact slug, scrape the overview page (e.g. `/components`) to find the correct
link, then scrape the target page.

## Response pattern

### Default (concise)
```
[1-sentence answer with key spec]
→ https://developer.apple.com/design/human-interface-guidelines/{slug}
```

### Detail level
```
[Key specs as table]
[Platform differences if relevant]
→ https://developer.apple.com/design/human-interface-guidelines/{slug}
```

### Full level
Use a web-scraping tool (e.g. Firecrawl) to fetch the relevant official page(s), then synthesize into a structured answer:
```
## [Topic]
> Source: [official URL]
```

## Critical design rules (top 10 to flag)

1. **44×44 pt minimum** touch target on iOS/iPadOS/watchOS
2. **Safe Area** must be respected on all platforms
3. **Dynamic Type** support required — never hardcode text sizes
4. **Dark Mode** must be supported — don't lock to light backgrounds
5. **tvOS Focus System** is non-optional for Apple TV apps
6. **visionOS comfort first** — no fast motion, content in field of view
7. **Never block with modals** on large screens (iPad, Mac)
8. **Contrast ratio** minimum varies by platform but always higher for tvOS
9. **Permission requests** deferred to point of need, not app launch
10. **SF Symbols** preferred over custom icons where a system symbol exists
