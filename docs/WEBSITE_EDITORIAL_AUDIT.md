# Website Editorial Audit

This is the editing log for the GitHub Pages site.

## Pass 1 - Source And Style Mismatch

Problem found:

- The HTML had moved to a stronger project-brief structure.
- The CSS was still built for the older page, so many new sections were not properly styled.
- The look was too close to the plain newspaper version.
- The page needed a clear visual identity without falling back to the repeated cool-color style.

Changes made:

- Replaced the stylesheet.
- Built a warmer field-report layout with ink, paper, teal, copper, moss, red, and ochre.
- Removed unused old selectors.
- Styled the new hero, run ledger, dashboard frame, build cards, output grid, tools list, limits band, and file links.

## Pass 2 - Visual Rhythm And Evidence Density

Problem found:

- The first fold was readable but too restrained.
- The page still leaned too much on black rules and warm paper.
- The strongest proof points were not visible fast enough.

Changes made:

- Added a three-item evidence strip below the scope note:
  - data work,
  - modelling,
  - business output.
- Added color-coded labels and ledger rows.
- Added a stronger left-side field marker to separate the page from the older flat version.
- Kept the color palette varied without turning it into the repeated cool-color style.

## Pass 3 - Editorial Tightening And Responsive Fixes

Problem found:

- The headline was longer than it needed to be.
- The run ledger created dead space on desktop.
- A narrow headless preview exposed horizontal clipping risk around the hero area.

Changes made:

- Rewrote the headline to be shorter and clearer:
  - "I rebuilt this pharma analytics project so the work can be checked."
- Tightened the lead copy.
- Reduced hero padding and ledger stretch.
- Added grid min-width guards so text and chart areas do not force horizontal overflow.
- Fixed mobile navigation wrapping and narrow-width spacing.
- Kept text in first person and simple vocabulary.

## Final Editorial Rule

Every section should answer one question:

> What did I do, what file proves it, and what am I not claiming?
