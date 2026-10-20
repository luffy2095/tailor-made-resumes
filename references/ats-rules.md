# ATS rules

The ATS version has one fixed layout (`templates/ats.tex`). Do not offer layout choices for it.

- Single column. No tables, columns, photos, icons or graphics.
- Contact details in the body, never in a page header or footer.
- Standard headings, exactly: Professional Summary, Core Competencies, Professional Experience, Education, Certifications, Professional Development.
- Left-aligned, never justified. Hyphenation off, so keywords stay whole.
- Ligatures off. A parser that reads "Office" as "O" plus one ligature character misses the keyword. `build.py` fails any `ats*.tex` whose text layer has ligatures.
- A Core Competencies block of JD keywords, and a "Systems:" line of tools, both in the JD's exact spelling.
- Keyword-rich summary and bullets, using the JD's words where the dossier supports them.
- One page. Reduce to 9.5pt and tighten margins to 0.45in vertical before cutting content.
- Dates as "Mon YYYY -- Mon YYYY" or "Present".
- File name: `<First>_<Last>_<Company>_<Role>_ATS.pdf`.
