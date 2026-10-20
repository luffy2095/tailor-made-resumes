# Cheat sheets

The cheat sheet is the most important deliverable. The resume gets the interview. The cheat sheet gets the job.
Build it right after the gap map, before the resumes.

Templates: `templates/cheatsheet_job.tex`, `templates/cheatsheet_topic.tex`.
Worked examples: `examples/ria-kapoor/jobs/ledgerline-senior-backend-payments/cheatsheet.tex` and
`examples/ria-kapoor/topics/cheatsheet_ledgers.tex`. Read both before writing a sheet.

## Two kinds

**Per-job sheet** (`jobs/<slug>/cheatsheet.tex`), built for one interview. Sections in this order:
1. What this job actually is
2. The core metrics, through one working day
3. The rituals of the role
4. One worked story with numbers
5. The daily heartbeat
6. <Company> vocabulary: recognise, don't claim
7. Interview FAQs, reasoning shown
8. Drills: cold, out loud, before you leave home
9. Questions to ask them
10. Read next

**Topic sheet** (`topics/cheatsheet_<topic>.tex`), built once per skill gap and reused across jobs.
The one model everything runs on, then Level 1 to Level 4 or 5, gotchas, five drills, read next.
Before writing a topic sheet, check `topics/` for one that already covers the gap.

## Rules

1. **Scenario first, term second.** Every concept opens with a quoted question an interviewer would ask, in `\scenario{}`, then the answer. No glossary paragraphs.
2. **Examples use the candidate's own world.** A SQL sheet for a hotel analyst uses bookings. A ledger sheet for a food-delivery engineer uses orders and refunds. The dossier supplies the domain.
3. **Three tags.** `\K` (KNOW, green): the candidate already does this under another name, and the line maps their words to the employer's. `\LRN` (LEARN, orange): new, and the sheet teaches it. `\trapbox{}` (TRAP, red): the gotcha interviewers use to sort candidates.
4. **FAQ answers carry the reasoning.** The candidate must survive the follow-up. Put the follow-up in a TRAP under the answer.
5. **Every TRAP becomes a drill** with the expected answer in brackets.
6. **Numbers are worked arithmetic, invented and labelled.** Compute every number with a tool before writing it. Never use the candidate's confidential figures.
7. **Point at the candidate's stories by name** from the dossier: "Your Diwali-eve backlog story applies".
8. **Read next links must resolve.** Check each URL returns 200 before writing it. Give a time per item.
9. **Exactly two pages.** `python3 scripts/build.py <file> --pages 2 --png`. If it runs over, cut words, not sections. If page 2 is less than half full, the sheet is too thin: add a FAQ or a drill.
10. **Phone-readable.** 10pt, no tables wider than the column, no code lines longer than the column.

## Quality check before showing the user

- Every LEARN item in the gap map is taught somewhere on the sheet or in a linked topic sheet.
- Every KNOW item maps a dossier fact to the employer's word.
- At least three TRAPs, at least three FAQs, at least three drills.
- Look at both PNG previews. Fix overflow and orphaned headings.
