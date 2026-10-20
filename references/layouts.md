# Human resume layouts

Three layouts, one page each. The ATS version is separate and fixed.

| Layout | File | Look | Default for |
|---|---|---|---|
| Classic | `templates/human_classic.tex` | XCharter serif, small-caps headings, hairline rules | software engineering, finance |
| Modern | `templates/human_modern.tex` | Carlito sans, name in the accent colour over a thin rule | marketing, product, sales |
| Two-column sidebar | `templates/human_twocol.tex` | Open Sans, warm grey sidebar with contact, skills, education | hospitality, client-facing roles |

Previews built from the fictional example are in `templates/previews/`. Show them at intake question 8.

- **Accent**: `\setaccent{navy|forest|wine|slate}` in the preamble.
- **Photo**: two-column only. `\phototrue` and a square `profile/photo.jpg`. Off unless the user turns it on.
- **Never offered**: fonts, margins, section order. The track decides them. A user who wants a different order for one job gets it as a conversational fix after the preview.
- If the uploaded resume's own structure clearly works, say so and keep that structure inside the chosen layout.
- Reduce font size before cutting content. Cut the oldest role's weakest bullet first.
