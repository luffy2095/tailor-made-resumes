# The dossier

`<workspace>/profile/dossier.md` is the single source of truth. Every resume line and every cheat sheet
mapping comes from it. If a fact is not in the dossier, it does not go on a document.

Worked example: `examples/ria-kapoor/profile/dossier.md`.

## Sections, in this order

1. **Contact**: city, email, phone, links.
2. **Preferences**: track, seniority, human layout, accent, photo, confidential metrics yes or no, location, timeline.
3. **Roles**: one block per role, newest first. Title, company, city, month and year range. Bullets are facts, not resume prose: what the person owned, built, fixed, led, with numbers only when the preferences allow them.
4. **Education**.
5. **Systems actually used**: tools at the level actually used. "Go (reading level only)" is a valid entry.
6. **May not claim**: things the person has been near but must not claim. The truth rules read this list.
7. **Certifications held**: with issuer and year. Only what the person can prove.
8. **Stories for interviews**: three to six, one line each. Cheat sheets point at these by name.
9. **In progress**: skills being learned, with a start date. These feed Professional Development.

## Approval

Show the whole dossier to the user and ask for corrections. Nothing downstream runs until the user says it is right. Write the approval date at the top.

## Changelog

Every edit after approval appends one dated line to `profile/changelog.md`: what changed and why. Example: `2026-11-02: Go moved from In progress to Systems actually used. Finished the CLI project.`
