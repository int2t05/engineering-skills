# Motion Design System

Motion is a design system, not decoration. This reference defines the token scale,
easing catalog, choreography patterns, and the canonical scroll-animation skeletons.
Load when `MOTION_INTENSITY > 3` or when building any scroll-driven, pinned, or
staggered animation.

## When to load this

- Building scroll-driven animations (sticky-stack, horizontal-pan, scroll-reveal stagger).
- Defining a motion token system for a project (duration, easing, distance scales).
- Any animation that needs to be justified, reduced-motion-safe, and performant.

## Duration token scale

| Token | Duration | Use |
|---|---|---|
| `instant` | 0ms | State flips, no transition |
| `quick` | 80–120ms | Micro-interactions: hover, press, toggle, focus ring |
| `short` | 150–200ms | Small UI transitions: tooltip, dropdown, chip appear |
| `base` | 200–300ms | Standard transitions: modal, drawer, sheet, tab switch |
| `long` | 300–500ms | Page-level: route transition, large card expand |
| `cinematic` | 500–800ms | Hero reveals, scroll-pinned sequences, brand moments |

Never exceed 800ms for a single animation — it feels broken. Chain animations instead
of lengthening one.

## Easing catalog

| Token | cubic-bezier | Use |
|---|---|---|
| `linear` | `cubic-bezier(0,0,1,1)` | Scrub-driven only (scroll progress, progress bars) |
| `ease-out` | `cubic-bezier(0,0,0.2,1)` | Entering elements (appear, slide-in, scale-up) |
| `ease-in` | `cubic-bezier(0.4,0,1,1)` | Exiting elements (dismiss, fade-out) |
| `ease-in-out` | `cubic-bezier(0.4,0,0.2,1)` | Position changes within view |
| `spring` | `cubic-bezier(0.34,1.56,0.64,1)` | Playful micro-interactions (slight overshoot) |
| `emphasis` | `cubic-bezier(0.16,1,0.3,1)` | Premium / cinematic reveals (strong deceleration) |

Rules:
- **Exit faster than enter** — exiting elements use a shorter duration (×0.6) than entering.
- **One easing per category** — don't mix 5 different eases on the same page. Pick 2–3.
- `linear` is only for scrub-driven (scroll-tied) animations. Never for time-based.

## Distance scale

| Token | Distance | Use |
|---|---|---|
| `shift-xs` | 4px | Micro: icon wiggle, badge bounce |
| `shift-sm` | 8–12px | Small: button press, chip settle |
| `shift-base` | 16–24px | Standard: card lift, drawer slide |
| `shift-lg` | 32–48px | Page: modal rise, panel expand |
| `shift-xl` | 64–96px | Cinematic: hero parallax, full-section reveal |

## Choreography patterns

### Stagger

Reveal a group of elements with a delay between each — not all at once.

- Stagger interval: 60–100ms (quick), 80–120ms (standard), 120–180ms (cinematic).
- Cap total stagger duration at 600ms — if 10 items × 100ms = 1000ms, reduce interval.
- Stagger by DOM order, not random — predictability reads as intentional.

### Shared element transition

An element animates from one position/size to another across a route or state change
(e.g., a card thumbnail expanding into a detail view).

- Use `layoutId` (Motion) or `View Transitions API` (native).
- The element is the anchor — everything else fades around it.

### Cross-fade

Replace one element with another by fading opacity in parallel.

- Duration: 200–300ms. Shorter feels abrupt; longer feels sluggish.
- Never cross-fade large images — they flash. Use a loaded state first.

## Scroll-driven animation skeletons

### Sticky-stack (pin cards on scroll)

Cards pin at the viewport top as you scroll; the previous card shrinks and dims as the
next arrives.

Critical points:
- `start: "top top"`, `pin: true`, `pinSpacing: false`.
- Every card except the last is pinned.
- The scale/opacity transform is driven by the **next** card's scroll trigger — so the
  previous card shrinks as the next one arrives.
- Use `gsap.context()` with cleanup (`ctx.revert()`) to avoid memory leaks.
- Wrap in `useReducedMotion()` — skip all animation if the user prefers reduced motion.

### Horizontal-pan (scroll vertically, move horizontally)

A horizontal track moves left as the user scrolls down. The track width is translated
by the scroll delta.

Critical points:
- Pin the wrapper for the duration of the horizontal scroll.
- Calculate `end` from the track width: `-=` the track's horizontal overflow.
- `scrub: true` ties animation progress to scroll position.
- Reduced motion: render the track as a vertical stack instead.

### Scroll-reveal stagger (lighter alternative)

Elements fade/slide in as they enter the viewport, one by one. No pinning.

- Use `IntersectionObserver` or `whileInView` (Motion) — no ScrollTrigger needed.
- Stagger by 80–120ms within a group.
- Threshold: trigger at 15–25% visible (not 0%, not 50% — too early or too late).

## Forbidden animation patterns

- **No `window.addEventListener('scroll')`** — use `useScroll()` / ScrollTrigger /
  IntersectionObserver / CSS scroll-driven animations. Scroll listeners cause jank.
- **No `useEffect` without cleanup** — every animation must clean up on unmount
  (`ctx.revert()`, `cancelAnimationFrame`, `observer.disconnect()`).
- **No `h-screen`** — use `min-h-[100dvh]` for viewport stability on mobile.
- **No GSAP-for-show** — every animation must be justifiable in one sentence
  (hierarchy / storytelling / feedback / state transition).
- **No two horizontal marquees** on the same page.
- **No infinite-loop micro-animations everywhere** — reserve motion for meaning.

## Reduced motion (mandatory)

Everything with `MOTION_INTENSITY > 3` must be wrapped in a reduced-motion check:

- Use `useReducedMotion()` (Motion) or `@media (prefers-reduced-motion: reduce)`.
- Reduced motion does NOT mean zero motion — it means: no parallax, no scroll-pinned
  sequences, no auto-playing carousels. Quick transitions (opacity, small shifts) are
  fine and often preferred over instant snaps.
- Test with reduced motion ON before delivering.

## Performance guardrails

- **Hardware acceleration** — animate `transform` and `opacity` only. Never animate
  `width`, `height`, `top`, `left`, `margin`, `padding` (they trigger layout).
- **`will-change` sparingly** — only on elements actively animating, removed after.
- **Containment** — use `contain: layout style paint` on heavy animation containers.
- **DOM cost** — keep animated element count under 50 per page. Each animated element
  is a compositor layer.
- **Z-index restraint** — animated overlays use a documented z-index scale, not
  ad-hoc `z-[9999]`.

## Verify

- Every animation is justifiable in one sentence.
- Duration, easing, and distance use the token scale (not ad-hoc values).
- Reduced-motion fallback tested and working.
- No scroll-event listeners — using ScrollTrigger / useScroll / IntersectionObserver.
- All animations clean up on unmount.
- `transform` and `opacity` only animated (no layout-triggering properties).
