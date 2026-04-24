# Accessibility

**When this concern applies:** The system has interfaces used by humans — web, mobile, voice, kiosk, embedded displays. Mandatory for public-sector UK systems (PSBAR 2018 and its successor), public-sector EU systems (EU Directive 2016/2102), and an enforceable baseline for private-sector systems in many jurisdictions.

**Why it matters:** Roughly 1 in 5 people live with a disability that affects their use of digital services. Inaccessible systems exclude them from services they're entitled to and expose the organisation to legal and reputational risk. Accessibility is an architectural concern because many of its requirements — semantic structure, keyboard-only operation, alternative content, high-contrast modes — are easiest to deliver when they're designed in, not retrofitted.

**Standards / references:** WCAG 2.2 (Level AA is typical baseline, AAA for public sector in some jurisdictions), EN 301 549 (European standard referencing WCAG), Section 508 (US), UK Public Sector Bodies Accessibility Regulations 2018, EAA (European Accessibility Act 2025).

## Per-view prompts

### Logical view
- Are user-facing components identified? Is each one explicitly claimed (or explicitly not-claimed) against a WCAG conformance level?
- Is there a shared **design system** or UI-component library used across interfaces — making it easier to apply accessibility fixes once and benefit everywhere?
- Is there a mechanism for users to customise accessibility settings (contrast, text size, reduced motion) that persists across sessions?

### Process view
- Where are time-bounded interactions (session timeouts, OTPs, stepped workflows)? Do they accommodate users who need more time (WCAG 2.2.1 Timing Adjustable)?
- For workflows with multiple steps, can users navigate back, review, and edit without losing progress (WCAG 2.5.7 Dragging Movements, 3.3.7 Redundant Entry)?
- Is there a clear process for users to request accommodation or report an accessibility barrier?

### Development view
- Is there a shared accessibility library / design system with accessible components by default?
- Is accessibility testing (automated and manual) part of the CI/CD pipeline?
- Are there design tokens for colour contrast, font sizing, focus indicators?

### Physical view
- For public-sector services, is the deployment environment certified against the relevant standard (e.g. GOV.UK Service Standard includes accessibility pass)?
- Is there telemetry for accessibility-relevant metrics — e.g. proportion of users using assistive technology, screen-reader error rates?

### Scenarios view
- Does at least one scenario cover **screen-reader use** — can a blind user complete the primary journey using only a screen reader?
- Does at least one scenario cover **keyboard-only use** — can a user who doesn't use a mouse complete the primary journey?
- Does at least one scenario cover **cognitive accessibility** — can a user with memory or attention difficulties complete the primary journey with reasonable accommodations (timeouts, error recovery, clear language)?
- Does at least one scenario cover a **user reporting an accessibility barrier** and the organisation's response?

## Common mitigations

- **Design-system-first** — build shared accessible components once; every team using them inherits the accessibility work.
- **Semantic HTML as a baseline** — use the right elements (`<button>`, `<nav>`, `<main>`) instead of divs with click handlers.
- **Keyboard-navigable interfaces** — every interactive control reachable and operable via keyboard; focus visible at all times.
- **Accessible-name and accessible-description for every UI control** — screen readers announce them; automated checkers verify them.
- **Sufficient colour contrast** — WCAG AA requires 4.5:1 for body text, 3:1 for large text; AAA is stricter. Don't rely on colour alone to convey information.
- **Captions, transcripts, audio descriptions** — for any time-based media.
- **Responsive and zoom-tolerant layouts** — reflow cleanly to 200% zoom, 320px viewport.
- **Reduced-motion mode** — respect `prefers-reduced-motion`; don't auto-play animation.
- **Accessibility statement** — public, maintained, reviewed at least annually, noting known limitations and alternatives.
- **Regular manual testing** — automated tools catch ~30% of issues; lived-experience testing by assistive-tech users catches the rest.

## Anti-patterns to probe for

- *"We'll make it accessible later."* Retrofitting is 5–10× more expensive than designing in.
- *Inaccessible custom components* — bespoke dropdowns, date pickers, modals reimplemented without the accessibility properties of the standard versions.
- *Time limits without extension* — forms, session timeouts, CAPTCHA with no alternative.
- *Colour-only signals* — red error / green success with no icon or text alternative.
- *PDFs as the canonical document format* without accessibility tagging.
- *"We only test on Chrome."* Many assistive technologies work better with specific browser combinations; supporting only one excludes users.

## References

- WCAG 2.2 — https://www.w3.org/TR/WCAG22/
- EN 301 549 — https://www.etsi.org/deliver/etsi_en/301500_301599/301549/
- UK PSBAR 2018 and guidance — https://www.gov.uk/guidance/accessibility-requirements-for-public-sector-websites-and-apps
- European Accessibility Act — https://ec.europa.eu/social/main.jsp?catId=1202
- GOV.UK Service Manual — accessibility — https://www.gov.uk/service-manual/helping-people-to-use-your-service/making-your-service-accessible-an-introduction
- GDS accessibility testing guidance — https://www.gov.uk/service-manual/technology/testing-for-accessibility
