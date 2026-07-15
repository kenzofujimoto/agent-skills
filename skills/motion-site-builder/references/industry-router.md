# Industry and experience router

The project must be classified on two independent axes before design generation:

1. **Industry profile** — domain semantics, content, trust, regulation, product media and motion limits.
2. **Experience archetype** — the job the website must perform, such as configurator, booking,
   product launch, service portal, catalog or editorial story.

## Required output

Create `industry-profile.json` before `motion-plan.json` with:

- primary industry ID;
- optional secondary industry IDs;
- subindustry;
- target audience;
- business objective;
- selected experience archetypes;
- content priorities;
- motion metaphors;
- recommended media;
- conversion pattern;
- risk/trust mode;
- motion intensity range;
- anti-patterns;
- selected references and why each is relevant.

## Routing rules

- Read `industry-profiles.json` and run `scripts/industry_router.py` with the project brief.
- Use a primary profile and at most two secondary profiles.
- Do not average conflicting risk rules. The strictest trust/accessibility rule wins.
- A project can borrow patterns across niches only when the experience archetype matches.
  Example: an aircraft configurator may borrow product-viewer principles from automotive,
  while retaining aviation accuracy and safety constraints.
- Market references establish expected information architecture and conversion.
- Creative references establish possible motion, visual rhythm and technology.
- Do not treat a visually impressive campaign as the default UX for routine tasks.
- Revalidate every reference URL in the browser before relying on it.
- If a reference is unavailable, record it as unavailable and choose another from the same
  industry or archetype. Do not fabricate observations.

## Interaction with ui-ux-pro-max

Pass the resolved industry, subindustry, archetypes, audience, risk level and motion range to
`ui-ux-pro-max --design-system`. Its design system remains the source of truth for typography,
color, layout and accessibility. This skill then converts those decisions into motion and
media contracts.
