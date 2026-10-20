# Tailor-made resumes

A Claude Code skill that works like a paid personal resume tailor. Give it your resume or LinkedIn PDF and a job link. For each job you get three documents:

- **A two-page interview cheat sheet.** It says what the job really is, walks the core metrics through one working day, tells one story with real arithmetic, gives interview answers with the reasoning shown, adds cold drills and questions to ask. Every point is tagged KNOW (you already do this, in their words), LEARN (new, taught here) or TRAP (the gotcha interviewers use).
- **A human resume**, one page, in one of three layouts.
- **An ATS resume**, one page, single column, keyword-rich, built so applicant tracking systems read every word.

Everything comes from one fact file you approve, so nothing is invented. That means no made-up metrics and no certifications you do not hold.

## Install

```bash
git clone https://github.com/luffy2095/tailor-made-resumes ~/.claude/skills/tailor-made-resumes
```

Then tell Claude Code: "tailor my resume for this job: <link>".

On the first run the skill installs a small LaTeX distribution, TinyTeX, into your user folder. It needs about 200 MB and no admin rights. Then it asks for your resume and a few questions with options. You never touch LaTeX.

| OS | Status | Notes |
|---|---|---|
| macOS | tested | nothing extra needed |
| Linux | supported | needs `perl` (full, not perl-base) and `xz`. Setup names what is missing. |
| Windows | supported, untested | setup prints the TinyTeX installer command for PowerShell, or use `choco install tinytex`. |

Optional: `pdftoppm` and `pdftotext` from poppler for PNG previews and the ATS text check (`brew install poppler`, `apt install poppler-utils`).

## See it first

`examples/ria-kapoor/` is a complete run for a fictional backend engineer applying to a fictional payments company:

- [Per-job cheat sheet](examples/ria-kapoor/jobs/ledgerline-senior-backend-payments/cheatsheet.pdf)
- [Topic cheat sheet: double-entry ledgers](examples/ria-kapoor/topics/cheatsheet_ledgers.pdf)
- [Human resume](examples/ria-kapoor/jobs/ledgerline-senior-backend-payments/human.pdf) and [ATS resume](examples/ria-kapoor/jobs/ledgerline-senior-backend-payments/ats.pdf)
- [The dossier they came from](examples/ria-kapoor/profile/dossier.md) and [the gap map](examples/ria-kapoor/jobs/ledgerline-senior-backend-payments/gapmap.md)

## Layouts

| Classic | Modern | Two-column |
|---|---|---|
| ![classic](templates/previews/classic.png) | ![modern](templates/previews/modern.png) | ![two-column](templates/previews/twocol.png) |

## Tracks

A track sets the keyword bank, the proof to ask for, the default layout and what the cheat sheet focuses on. Two ship today:

- Software engineering
- Hospitality revenue management

Add a track by adding a file to `references/tracks/`, following the shape of the existing two.

## What the build checks

- Each document has its exact page count: two for a cheat sheet, one for a resume.
- No unfilled placeholder reaches a PDF.
- The ATS PDF's text layer has no ligature characters. A parser that reads "Office" as "O" plus one glyph misses the keyword.
- Each job folder records which version of your fact file it was built from.

## Licence

MIT.
