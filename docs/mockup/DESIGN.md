---
name: Serene Portfolio
colors:
  surface: '#f8f9fa'
  surface-dim: '#d9dadb'
  surface-bright: '#f8f9fa'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f4f5'
  surface-container: '#edeeef'
  surface-container-high: '#e7e8e9'
  surface-container-highest: '#e1e3e4'
  on-surface: '#191c1d'
  on-surface-variant: '#45474c'
  inverse-surface: '#2e3132'
  inverse-on-surface: '#f0f1f2'
  outline: '#76777c'
  outline-variant: '#c6c6cc'
  surface-tint: '#585e6c'
  primary: '#030813'
  on-primary: '#ffffff'
  primary-container: '#1a202c'
  on-primary-container: '#828796'
  inverse-primary: '#c1c6d7'
  secondary: '#4b41e1'
  on-secondary: '#ffffff'
  secondary-container: '#645efb'
  on-secondary-container: '#fffbff'
  tertiary: '#010815'
  on-tertiary: '#ffffff'
  tertiary-container: '#16202f'
  on-tertiary-container: '#7d889a'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dde2f3'
  primary-fixed-dim: '#c1c6d7'
  on-primary-fixed: '#161c27'
  on-primary-fixed-variant: '#414754'
  secondary-fixed: '#e2dfff'
  secondary-fixed-dim: '#c3c0ff'
  on-secondary-fixed: '#0f0069'
  on-secondary-fixed-variant: '#3323cc'
  tertiary-fixed: '#d9e3f7'
  tertiary-fixed-dim: '#bdc7db'
  on-tertiary-fixed: '#121c2a'
  on-tertiary-fixed-variant: '#3d4757'
  background: '#f8f9fa'
  on-background: '#191c1d'
  surface-variant: '#e1e3e4'
typography:
  display-lg:
    fontFamily: Playfair Display
    fontSize: 64px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: Playfair Display
    fontSize: 40px
    fontWeight: '700'
    lineHeight: '1.2'
  headline-md:
    fontFamily: Playfair Display
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.3'
  headline-sm:
    fontFamily: Playfair Display
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.4'
  body-lg:
    fontFamily: DM Sans
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.7'
  body-md:
    fontFamily: DM Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: '1.2'
    letterSpacing: 0.05em
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: '1.2'
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  container-max: 1280px
  gutter: 24px
  margin-mobile: 20px
  margin-desktop: 64px
  stack-sm: 16px
  stack-md: 32px
  stack-lg: 80px
---

## Brand & Style
The design system is rooted in **Minimalism** with a focus on premium editorial aesthetics. It targets a professional audience that values clarity, precision, and a high-end feel. The emotional response is one of calm confidence—evoking the atmosphere of a boutique design agency or a curated gallery. 

The visual language relies on generous whitespace (negative space) to let content breathe, ensuring that every element on the screen feels intentional. The interaction model is quiet and unobtrusive, using subtle transitions rather than loud animations to guide the user’s journey.

## Colors
The palette is built on a foundation of "Off-white" (#f9fafb) to provide a soft, non-clinical background that reduces eye strain compared to pure white. 

- **Primary:** Dark Navy/Charcoal is reserved for high-impact structural elements and deep-contrast components.
- **Accent:** Indigo is used sparingly for call-to-actions, active states, and focus indicators to maintain a professional "pop."
- **Typography:** Primary text uses Dark Gray (#374151) rather than black to maintain a softer, more sophisticated contrast ratio. Secondary text uses Gray (#6b7280) for meta-information and captions.

## Typography
This design system utilizes a high-contrast typographic pairing to reinforce the "Premium Editorial" feel. 

**Playfair Display** (Serif) is the voice of the brand, used for all headlines and display text. Its high stroke contrast brings elegance and a sense of history. 

**DM Sans** (Sans-serif) handles the bulk of body copy due to its geometric clarity and modern proportions, ensuring readability at various lengths. 

**Inter** is utilized for functional UI elements like labels, buttons, and navigation links, where its systematic nature provides a clear utilitarian counterpoint to the decorative serif.

## Layout & Spacing
The layout follows a **Fixed Grid** philosophy for desktop to maintain the integrity of the editorial composition, transitioning to a fluid model for mobile devices.

- **Desktop (1280px+):** A 12-column grid with 24px gutters. Content is centered with large 64px exterior margins to create the "gallery" effect.
- **Tablet (768px - 1279px):** An 8-column grid with 24px gutters and 40px margins.
- **Mobile (<767px):** A 4-column grid with 16px gutters and 20px margins.

Vertical rhythm is strictly 8px-based. "Stack" tokens are used to define the distance between sections, with `stack-lg` reserved for separating major portfolio projects or bio sections to emphasize the minimalist intent.

## Elevation & Depth
The design system avoids heavy shadows in favor of **Tonal Layers** and extremely **Ambient Shadows**. Depth is used to signify interactivity rather than physical height.

- **Surface Level 0:** The Off-white background (#f9fafb).
- **Surface Level 1 (Cards/Floating elements):** Pure White (#ffffff) with a very soft, diffused shadow (0px 4px 20px rgba(0, 0, 0, 0.04)).
- **Interactive State:** On hover, elements may increase shadow spread slightly or utilize a subtle 1px stroke in the Primary Navy color at low opacity (10%).
- **Outlines:** Use thin, 1px borders in a lighter shade of the secondary text color for input fields and separators to keep the interface feeling "drawn" and light.

## Shapes
The shape language is defined by "Soft-Geometric" forms. A standard radius of **12px** (represented by `rounded-md` in this system) is applied to cards, buttons, and input fields. This specific curvature strikes a balance between the precision of a sharp square and the playfulness of a pill shape, maintaining a "Modern Professional" look.

Media assets (images and videos) should always follow the 12px rounding rule to ensure they feel integrated into the UI rather than separate from it.

## Components
- **Buttons:** Primary buttons use the Indigo accent with white text. Secondary buttons use a clean 1px outline of the Primary Navy. Button padding should be generous (12px vertical, 24px horizontal).
- **Chips/Tags:** Used for "Skills" or "Categories." These should have a light gray background (#f3f4f6) and use the `label-sm` typography. 
- **Lists:** Unordered lists in body copy should use custom Indigo dot markers rather than standard bullets.
- **Input Fields:** Minimalist design with a 1px border. On focus, the border transitions to Indigo with a subtle glow. Use `body-md` for input text.
- **Cards:** White background, 12px border radius, and the Ambient Shadow defined in the Elevation section. Card titles should use `headline-sm`.
- **Icons:** Use thin-stroke (1.5px or 2px) outline icons. Avoid solid/filled icons unless used as an active state indicator.
- **Portfolio Grid Item:** A specialized component featuring a large image container (12px rounded), a `headline-sm` title, and a small `label-md` category indicator above the title.