# Intake

Run once, on the first request, after setup passes. Never ask everything in one wall of text.

## Step 1: source material, alone

Ask for one thing first:

> Send me your current resume as PDF or DOCX, or your LinkedIn profile saved as PDF (on your profile: More, then Save to PDF). Add links to a portfolio or GitHub if you have them.

LinkedIn blocks most direct profile fetches, so ask for the PDF rather than promising that a URL will work. GitHub and portfolio URLs can be fetched.

Read everything before step 2. Do not ask a question the material already answers.

## Step 2: standard questions, with options

Use the question tool, at most four questions per call, each with fixed options. The user can always pick Other. Skip any question the material already answered, and say what you inferred instead.

| # | Question | Options |
|---|---|---|
| 1 | Which track fits the jobs you want? | one per file in `references/tracks/`, plus Other |
| 2 | Seniority you are targeting? | Entry · Individual contributor · Lead or manager · Director and above |
| 3 | What kind of move is this? | Same role and level · Step up · Lateral move to a new domain · Return after a break |
| 4 | Where? | Current city only · Specific cities · Remote · Open to relocation |
| 5 | Can your employers' numbers appear on the resume? | No, keep them qualitative · Yes, numbers are fine |
| 6 | Certifications? | None · Held, with proof · In progress |
| 7 | When are you applying? | Now · Within a month · Exploring |
| 8 | Resume style for human readers? | The track default (named) · Classic · Modern · Two-column sidebar. Show `templates/previews/*.png`. |

After question 8, two quick toggles: accent colour (navy, forest, wine, slate) and photo (on or off; default off, except the two-column layout in tracks where photos are customary).

**When the photo is on, ask for the image straight away:**

> Send a photo for the resume: square or portrait, face centred, plain light background, at least 600 px. JPG, PNG, AVIF, WebP or HEIC all work. A recent professional headshot works best; a cropped phone photo against a wall is fine.

Save it as `profile/photo.<its extension>`. The build converts AVIF, WebP and HEIC to JPG itself. Look at it before using it. If it is wider than tall, the face is not centred, or it is a group or casual photo, say so in one line and ask for another. Never crop out other people or edit the person's appearance. If the user has no photo ready, turn the photo off for now and note it in the dossier preferences.

## Step 3: one open question, last

> Anything else I should know? Career gaps, visa, a role you want left off, a story you want told. Leave it empty if not.

## Then

Go to discovery: five to eight follow-ups only about gaps the material and answers left open (a role with no outcomes, a tool with no context, an uncovered period). Then write the dossier.
