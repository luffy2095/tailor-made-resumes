# Contributing

Thank you for helping. This guide says what helps most, how to set up, and what every change must pass.

## What helps most

1. **A new track.** Marketing, finance, sales, product, data science, nursing, teaching: any field with its own vocabulary and interview style.
2. **A test report on Linux or Windows.** Setup is written from the TinyTeX documentation but has run only on macOS. A report helps even when everything works.
3. **Better cheat sheets.** A sharper rule in `references/cheatsheet-style.md`, or a second fictional example in another field.
4. **A new human resume layout.** Only when it serves a field the current three do not.
5. **Fixes to the docs.**

For anything bigger than a typo, open an issue first so we agree on the approach before you write it.

## Set up

```bash
git clone https://github.com/<you>/tailor-made-resumes
cd tailor-made-resumes
python3 -u scripts/setup.py          # installs TinyTeX if missing, about 2 to 6 minutes the first time
python3 -u scripts/selftest.py       # builds every example and checks every guard, about 1 minute
```

To try your branch inside Claude Code, link it into your skills folder:

```bash
ln -s "$PWD" ~/.claude/skills/tailor-made-resumes
```

## Rules every change must follow

- **Fictional people only.** Examples use invented names, invented companies and `example.com` addresses. Never commit a real person's resume, fact file, photo or job history, including your own.
- **Every number is computed.** Worked numbers in cheat sheets must be correct arithmetic. Check them with a tool.
- **Every link resolves.** `python3 -u scripts/selftest.py --links` checks them.
- **The build checks pass.** Run `scripts/selftest.py` before you open a pull request.
- **The truth rules hold.** Read `references/truth-rules.md`. A change must never make it easier to claim something the candidate did not do.
- **Plain writing.** Short sentences, active voice, one idea per sentence. Write for a busy job seeker.

## Add a track

1. Copy `references/tracks/software-engineering.md` to `references/tracks/<field>.md`.
2. Fill every section: Defaults, Proof to ask for in discovery, Keyword bank, Cheat sheet focus, Common LEARN gaps and topic sheets.
3. Write the keyword bank from your own knowledge of the field and from public job posts. Do not copy a real person's documents.
4. Add the track to the table in `README.md` and to intake question 1 in `references/intake.md`.
5. Optional but valuable: a fictional example in `examples/<name>/` with the same layout as `examples/ria-kapoor/`.

## Add a layout

1. Add `templates/human_<name>.tex`. Use `\ph{...}` for every slot so the build refuses an unfilled copy.
2. Load `tailor.sty` for the accent colours and shared macros.
3. Render the fictional example in it at `examples/ria-kapoor/layouts/<name>.tex`. It must fit one page.
4. Save its preview as `templates/previews/<name>.png` (`python3 scripts/build.py <file> --pages 1 --png`).
5. Add a row to `references/layouts.md`, an option to intake question 8, and a column to the layouts table in `README.md`.

## Change the cheat sheet style

The style lives in `references/cheatsheet-style.md` and the two templates. If you change a rule, update both fictional sheets to follow it and rebuild them. The sheets must stay at exactly two pages.

## Pull requests

Keep each pull request to one change. The template lists the checks.
