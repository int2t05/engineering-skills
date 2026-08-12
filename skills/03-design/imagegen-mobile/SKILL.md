---
name: imagegen-mobile
description: Mobile app screen and flow image generation — iOS/Android/cross-platform concepts with phone mockup framing, clean hierarchy, and strong multi-screen consistency. Triggers on "mobile design image", "app screen image", "mobile mockup", "app flow", "移动端设计图", "app 屏幕图", "手机界面图", "移动端流程图".
---

# Imagegen Mobile

Generate premium mobile app screen concepts and flow images — app-native, readable, art-directed —
not generic AI mockups or phone-shaped websites. Output is images only, never code.

## When to use

- Generating mobile app screen concepts and multi-screen flow images
- iOS-native, Android-native, or cross-platform mobile products
- Onboarding, auth, home, profile, settings, chat, commerce, fintech, health, productivity, social apps
- Triggers on "mobile design image", "app screen image", "mobile mockup", "app flow", "移动端设计图", "app 屏幕图", "手机界面图", "移动端流程图"

**Not for:** web design references (use `imagegen-web`); frontend code (use `frontend-design`); brand identity (use `brandkit`).

## Steps

### 1. Set platform mode and screen count

Decide platform mode first — never mix patterns carelessly:
- **iOS-native premium** — clean top areas, tab-bar clarity, safe-area awareness, elegant spacing, restrained chrome, calm hierarchy.
- **Android-native premium** — stronger component rhythm, clear app bar, bottom navigation clarity, sheet logic, firmer framing.
- **Cross-platform premium neutral** — universal navigation patterns, less platform ornament, broadly buildable.

Then lock the screen count. **Screen-first is mandatory**: generate the screen image(s) directly,
never answer with only text or describe the app without generating it.
- 1 screen → 1 image; N screens → N images. Onboarding → multiple distinct screens; auth flow → separate sign in / sign up / recovery; app concept → a meaningful set, not one isolated mockup.
- Generate enough screens to make the flow feel real. Better to produce multiple clean readable screens than one compressed collage with tiny text. Never reduce count for convenience.
- Announce the count out loud.

### 2. Lock the design bible for multi-screen consistency

Before generating, lock an internal design bible and keep it consistent across the whole set:
platform mode, device frame style and scale, palette logic, typography mood and scale, spacing
system, corner radius, icon style, imagery treatment, texture intensity, navigation model, card/list
behavior, button styling, shadow language.

Every screen must feel like it belongs to the same product world. Allowed variation: composition,
feature emphasis, image placement, screen purpose, visual tempo. **Not allowed**: product identity,
design system, mockup quality, core spacing logic. Screen 3, 4, or 5 must not drift into a different
app. When a detail is unclear, generate a fresh standalone screen or detail render — never crop or
zoom a previously generated image.

### 3. Frame in a clean phone mockup

By default, present the UI inside a clean phone mockup with a visible device border:
- iPhone-style for iOS or neutral premium concepts; Android-style for Android-native; subtle generic premium phone for cross-platform.
- **Content-first**: the mockup supports the screen, never overpowers it. Keep visual emphasis on the UI inside the phone.
- Keep outer canvas margins visually even on all sides; the phone must not touch edges or be awkwardly cropped.
- Keep device scale and bezel consistent across all screens in the set; keep shadows soft and controlled.
- Multiple devices in one composition: same scale, equal gutter spacing, clean alignment, no random overlap.
- Only drop the visible frame if the user explicitly asks for raw screen-only output or UI sheets.

### 4. Respect safe areas and design clean first screens

**Safe-area awareness**: always account for status bar, top bar, bottom navigation, home indicator,
sheet docking zone, and gesture space. Never cram critical UI into unsafe regions; screens must feel
like real app screens, not edge-to-edge posters.

**First screen cleanliness** — the first visible screen matters most:
- One primary focal point; controlled top area; short headline (1-3 lines); one clear next action.
- No extra stats, chips, tags, or pills; no "website hero inside a phone frame"; no fake enterprise complexity.
- If imagery sits behind text, protect readability with fades, masks, or soft scrims.

**Onboarding flow**: generate multiple distinct screens; vary composition and the balance of image /
text / CTA; keep copy short; keep the first screen especially clean. Avoid 3 identical slides with
only icon and headline changes, giant abstract blobs, fake motivational filler, or early rating
prompts.

**Navigation**: believable tab bar / stack drill-down / sheets / segmented controls. Don't overload
bottom navigation or make every action equally important.

### 5. Apply art direction, readability, and anti-AI-tells

**Imagery and texture** — do not default to sterile flat backgrounds. When the category supports it
(social, commerce, travel, wellness, editorial, food, fashion), use art-directed photography,
editorial image blocks, image-backed headers, and media shelves with stable aspect ratios. Add
subtle texture (film grain, noise, paper, matte, tonal gradient fog) to make the UI feel premium and
tactile — but controlled, never overwhelming text. Image-behind-text needs clean fade-to-transparent
or soft-scrim treatments; raw image under text with no readability support is banned.

**Cleanliness over forced minimalism**: richer layered layouts are fine if they stay readable.
Sophisticated layering, controlled depth, and stronger image presence are allowed. Not always
simple — always clean. Box-in-box-in-box nesting, floating surfaces everywhere, and 5 levels of
framing are not.

**Text readability**: if text feels too small, the design is not finished — simplify the layout,
reduce content, enlarge the text, or split into another screen. Readable beats clever, dense, or
decorative small type.

**Anti-AI-tells** (ban unless explicitly requested):
- Visual: purple-blue fintech gradients, random glass cards, ambient blobs, fake neon, oversized corner radii on everything.
- Layout: fake chart dashboard spam, repeated stat cards, a homepage of 12 widgets fighting for attention, cloned screens, phone-shaped websites.
- UI clutter: too many pills/badges/tiny labels, fake system markers, meaningless avatar rows, decorative toggles.
- Copy: "elevate your life / unlock your potential / next-gen finance / seamless control / smarter than ever"; fake brands (Acme, NovaCore, Flowbit, Quantix, VeloPay).
- Icons: generic developer-tool icon packs and bland library-default line icons — prefer a clean custom-feeling icon system with consistent stroke or filled logic.

**Regenerate weak screens**: if a screen has tiny text, unclear spacing, fake navigation, website-like
layout, clutter, inconsistent framing, or lost consistency — regenerate it. Do not settle for the
first mediocre render.

## Verify

- [ ] Platform mode chosen and held coherently (iOS / Android / cross-platform — no careless mixing)
- [ ] Screen count matches the request; enough screens generated for a believable flow (not lazily collapsed)
- [ ] Each screen generated fresh — not a crop or zoom of a larger image
- [ ] Design bible held across all screens: same palette, type, spacing, radius, icon style, mockup style, imagery treatment
- [ ] Phone mockup present by default with visible clean border; content (not the device) is the hero; outer margins even on all sides
- [ ] Device scale and bezel consistent across the set; no cropped or uneven frames
- [ ] Safe areas respected — no critical UI in status bar / home indicator / gesture zones
- [ ] First screen is clean: one focal point, short headline, one clear action, no clutter
- [ ] Onboarding (if present) has distinct varied screens, not template clones
- [ ] Navigation is believable (tab bar / stack / sheets) with clear primary vs secondary actions
- [ ] Text is comfortably readable at normal viewing size — nothing feels small
- [ ] Imagery and texture are purposeful and consistent, not sterile or random filler; image-behind-text has clean fades/masks
- [ ] Layout is clean without box-in-box-in-box clutter; richer layering only where it stays readable
- [ ] No AI tells: no purple-blue gradients, no fake chart spam, no cloned screens, no generic icon-library defaults, no phone-shaped websites
- [ ] Flow is logical screen-to-screen (onboarding → auth → home, or cart → checkout → confirmation)

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — shared discipline (surface assumptions, push back, verify don't assume)
- [${CLAUDE_PLUGIN_ROOT}/references/design-principles.md](${CLAUDE_PLUGIN_ROOT}/references/design-principles.md) — design discipline (CRAP, hierarchy before decoration, design every state, accessibility non-optional, consistency from systems). The design bible in Step 2 operationalizes §6.
