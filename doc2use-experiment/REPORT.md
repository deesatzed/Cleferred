# Four models on the Cladophialophora note

2 October 2026. Same file, same sentence split, same 14 questions as the Send page.

## In short

The note was sent through all four choices on the Send page. Each one labeled all 121 pieces. None of the calls failed.

On the reference list, all four agreed: every fragment is **No label**. On the note itself they agreed much less often. All four picked the same category on 33 of 64 pieces, and the same category plus the same yes/no reading on 16 of 64.

The page would keep very little. Local Clef kept nothing. Jev kept 3 sentences, Mercury kept 4, and Liquid kept 6. No sentence was kept by three or four models. A person has not checked these labels. Matching labels mean the models agreed with each other.

Jev finished in 5.749 seconds, Liquid in 8.810 seconds, Mercury in 38.214 seconds, and local Clef in 620.357 seconds. Those are the wall-clock times saved in each model’s file. The three cloud models ran at the same time as the local model.

## What was scored

Source file: `doc2use.md` (11,791 bytes).

SHA-256: `9dc30fc287ac08f7cbcf96c2fa0d0fba9788164937987be49f3f9831b7bd0760`

The Send page’s splitter produced **121 pieces**:

- **64** from the note, including the six section headings, the figure captions, and the closing question.
- **57** from the reference list. Titles, author lines, journal names, and years were split apart.

Every model saw the same pieces, including the previous and next piece as context, which is what the Send page sends.

The questions are the 14 yes/no and multiple-choice questions in the app. There is no free-text answer. The keep line is a score of **0.72**. A piece labeled **No label** waits for a person even when the score is high. A piece that points at a citation also waits. A larger Clef model was not called. The local column is the 4-bit model on this computer (`clef-flash-4bit` at `127.0.0.1:8010`). The answer payload names that model `clef-flash`.

Cloud text went to OpenRouter, which is the fast path you asked to try. The three cloud model ids were `typesafe/jev-1.13`, `inception/mercury-decide:free`, and `liquid/d1`. The services answered as `typesafe/jev-1.13-20260917`, `inception/mercury-decide-20260930`, and `liquid/d1-20260930`.

## How to read one label

A label has three parts.

**Category.** Fact, Theory, Concept, Step, or No label.

**Reading.** Says yes (the sentence asserts it), says no (the sentence denies it), only sometimes (it depends on a condition), or not sure.

**Score.** That model’s own certainty about its label. A 0.80 from Jev and a 0.80 from Mercury are two separate certainties. They are not marks on one shared exam.

**What the page does with it.**

- **Skipped.** The model called the piece boilerplate, such as a heading. The page drops it.
- **Kept.** The score is at least 0.72, the category is a real one, the reading is clear enough, the model did not contradict itself, and it did not flag a citation.
- **Waiting.** Anything else. A person still has to look.

## The reference list

All four models called all **57** reference fragments **No label**. They also shared the same reading on **47** of those 57. The other 10 are reading differences on pieces that all four already called No label, mostly “not sure” against “says yes” on a title or a journal name.

They differ on what the page should do with those fragments:

| Model | Skipped as boilerplate | Left waiting |
| --- | ---: | ---: |
| Local Clef | 0 | 57 |
| Jev | 35 | 22 |
| Mercury | 53 | 4 |
| Liquid | 17 | 40 |

Local was sure about many of them: **35** of 57 scored 0.72 or higher, all of them No label. The page still holds those, because No label always waits.

## The note

Of the 64 pieces in the note:

| Outcome | Pieces |
| --- | ---: |
| All four chose the same category | 33 |
| Three chose the same category | 14 |
| No category had three votes | 17 |
| Same category and the same reading | 16 |

The 33 shared categories are **32 Fact** and **1 No label**. The single shared No label is piece 64, the closing question (“Would you like to explore optimal antifungal duration…”). All four also called that one “not sure.”

Category counts on the 64 note pieces:

| Category | Local | Jev | Mercury | Liquid |
| --- | ---: | ---: | ---: | ---: |
| Fact | 43 | 50 | 42 | 48 |
| Theory | 5 | 1 | 4 | 0 |
| Concept | 0 | 1 | 3 | 4 |
| Step | 4 | 6 | 3 | 1 |
| No label | 12 | 6 | 12 | 11 |

Pairwise agreement on those 64 pieces:

| Pair | Same category | Same category and reading |
| --- | ---: | ---: |
| Jev and Liquid | 50 | 46 |
| Jev and Mercury | 46 | 23 |
| Mercury and Liquid | 50 | 24 |
| Local and Jev | 44 | 44 |
| Local and Liquid | 39 | 37 |
| Local and Mercury | 40 | 22 |

Jev and Liquid are the closest pair on this note. When local and Jev picked the same category, they also picked the same reading, on all 44 of those pieces. Mercury is the model that breaks the reading. It matches the others on category about as often as they match each other, and it matches their reading about half as often.

Across the whole 121 pieces, category agreement looks higher (90 of 121 unanimous) because the 57 reference fragments are included. The note is the comparison that matters.

## What the page would keep

| Model | Kept | Skipped | Waiting | Median score | Fact labels in the note at or above 0.72 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Local Clef | 0 | 0 | 121 | 0.42 | 0 |
| Jev | 3 | 41 | 77 | 0.30 | 6 |
| Mercury | 4 | 62 | 55 | 0.63 | 18 |
| Liquid | 6 | 24 | 91 | 0.41 | 7 |

Median score is over all 121 pieces, shown to two decimals. Mercury’s higher median means Mercury was more certain of its own labels.

Local’s highest score anywhere in the note was **0.7159**, on the Gram-stain caption (piece 38), which it called No label. None of its 43 Fact labels on the note reached 0.72. Every local answer on this document also met the app’s test for “ask a larger Clef.” That larger model is not configured, so these are the flash answers the Send page would show today.

A high score can still wait. Among pieces scored 0.72 or higher, the only reason left for waiting was a citation flag on 3 Jev pieces, 9 Mercury pieces, and 1 Liquid piece. Mercury also held high-scoring pieces because the reading was “not sure.” Piece 25 is one: Mercury scored the microscopy sentence 0.86 as Fact, read it as “not sure,” and the page held it. Jev called the same sentence Fact · says yes · 0.80 and the page kept it.

No note piece had all four scores at or above 0.72.

### Sentences the page kept

Scores below are the stored values, shown to two decimals. “Waiting” on the same row means that model picked a label and the page still held the sentence.

**Piece 10.** “The dominant manifestation is brain abscess (~97% of cerebral cases), typically a solitary lesion…”

| Model | Label | Page |
| --- | --- | --- |
| Local | Fact · says yes · 0.54 | waiting |
| Jev | Fact · says yes · 0.00 | waiting |
| Mercury | Fact · says yes · 0.88 | kept |
| Liquid | Fact · says yes · 0.83 | kept |

Jev’s 0.00 means one of the questions that make up the score was a coin toss. The category still matched.

**Piece 13.** “Reported presentations include ophthalmoplegia, ataxia, visual field defects, and progressive cognitive/motor decline.”

| Model | Label | Page |
| --- | --- | --- |
| Local | Fact · says yes · 0.30 | waiting |
| Jev | Fact · says yes · 0.34 | waiting |
| Mercury | Fact · not sure · 0.41 | waiting |
| Liquid | Fact · says yes · 0.84 | kept |

**Piece 15.** “Disease occurs about three times more often in men.”

| Model | Label | Page |
| --- | --- | --- |
| Local | Fact · says yes · 0.24 | waiting |
| Jev | Fact · says yes · 0.22 | waiting |
| Mercury | Fact · says yes · 0.89 | kept |
| Liquid | Fact · says yes · 0.81 | kept |

**Piece 20.** “Prognostically favorable features are an easily resectable, well-encapsulated mass.”

| Model | Label | Page |
| --- | --- | --- |
| Local | Fact · says yes · 0.22 | waiting |
| Jev | Fact · says yes · 0.76 | kept |
| Mercury | Fact · not sure · 0.56 | waiting |
| Liquid | Fact · says yes · 0.84 | kept |

**Piece 25.** “Direct microscopy/histopathology: KOH mount and Gram stain of aspirated pus show narrow, septate, phaeoid hyphae…”

| Model | Label | Page |
| --- | --- | --- |
| Local | Fact · says yes · 0.56 | waiting |
| Jev | Fact · says yes · 0.80 | kept |
| Mercury | Fact · not sure · 0.86 | waiting |
| Liquid | Fact · says yes · 0.47 | waiting |

**Piece 49.** “The mainstays are complete surgical excision of the abscess combined with prolonged antifungal therapy…”

| Model | Label | Page |
| --- | --- | --- |
| Local | Step · says no · 0.35 | waiting, and the model contradicted itself |
| Jev | Fact · says yes · 0.42 | waiting |
| Mercury | Fact · says yes · 0.80 | kept |
| Liquid | Fact · says yes · 0.64 | waiting |

**Piece 57.** “In vitro susceptibility supports azoles: lowest MIC90 values for posaconazole and itraconazole (0.125 µg/mL)…”

| Model | Label | Page |
| --- | --- | --- |
| Local | Fact · says yes · 0.04 | waiting |
| Jev | Fact · says yes · 0.68 | waiting |
| Mercury | Fact · says yes · 0.64 | waiting |
| Liquid | Fact · says yes · 0.83 | kept |

**Piece 58.** “Fluconazole is poorly active (MIC90 64).”

| Model | Label | Page |
| --- | --- | --- |
| Local | Fact · says yes · 0.29 | waiting |
| Jev | Fact · says yes · 0.49 | waiting |
| Mercury | Fact · says no · 0.87 | kept |
| Liquid | Fact · says yes · 0.62 | waiting |

The words assert that fluconazole is poorly active. “Says yes” means the model read the sentence as asserting that. Mercury read it as “says no,” meaning Mercury treated the sentence as a denial, and it was sure enough for the page to keep that reading. This is a reading disagreement. It is not a second medical opinion about fluconazole.

**Piece 62.** “Relapse is common, mandating extended follow-up.”

| Model | Label | Page |
| --- | --- | --- |
| Local | Fact · says yes · 0.13 | waiting |
| Jev | Fact · says yes · 0.78 | kept |
| Mercury | Fact · not sure · 0.76 | waiting |
| Liquid | Fact · says yes · 0.77 | kept |

Two models together kept pieces 10, 15, 20, and 62. The other five kept sentences were kept by one model.

## Where three models agreed

On 14 note pieces, three models shared a category and one did not. The lone model was local 8 times, and Jev, Mercury, and Liquid 2 times each.

| # | Three agreed | The other call | Piece |
| --- | --- | --- | --- |
| 9 | No label | Mercury: Fact | Clinical presentation |
| 14 | Fact | Local: No label | Frontal and parietal lobes are frequently involved. |
| 18 | No label | Local: Theory | Imaging |
| 19 | Fact | Local: Theory | MRI/CT typically shows rim-enhancing focal lesions… |
| 29 | Fact | Mercury: Step | Molecular identification: ITS sequencing/BLAST confirms species |
| 30 | Step | Liquid: Fact | Pan-fungal PCR is recommended when microscopy is positive but culture is negative… |
| 32 | Fact | Local: No label | CSF cultures are mostly negative |
| 36 | No label | Local: Fact | The following figure illustrates the typical diagnostic cascade… |
| 38 | No label | Jev: Fact | Gram-stain showing septate hyphae… under × 1000 |
| 41 | No label | Liquid: Concept | Differential diagnosis |
| 49 | Fact | Local: Step | The mainstays are complete surgical excision… |
| 50 | Fact | Local: No label | There is no clearly proven optimal regimen and mortality remains high. |
| 55 | Fact | Local: No label | Antifungal agents used (from systematic review): voriconazole (~77%)… |
| 61 | Fact | Jev: Step | Monitoring and duration: prolonged therapy with serial imaging is required |

Some of local’s lone calls match the wording. Piece 19 says “typically,” which is a hedge, and local called it a Theory. Piece 49 is a treatment recommendation, and local called it a Step. Piece 30 is a recommendation (“is recommended”), and the majority called it a Step while Liquid called it a Fact.

## Where there was no majority

17 note pieces had no category with three votes. Several are headings or captions. A few are real claims where the schema itself is easy to split.

The opening sentence (piece 1) both names the organism and states claims, including how common it is and the mortality range. Local and Jev called it Fact (0.42 and 0.52). Mercury and Liquid called it Concept. Mercury’s score was 0.92, with the reading “not sure,” so the page held it.

Piece 3, the melanin virulence sentence, split the same way: Fact, Fact, Concept, Concept.

Piece 5 says infection “is thought to occur” by inhalation or inoculation. Jev called it a Theory at 0.78. Local and Liquid called it a Fact. Mercury called it a Theory and was not sure of the reading. Jev’s category matches the hedge. The page still held Jev’s label. The wait reason on that piece was “unclear.”

Piece 7, “possibly reflecting an expanding geographic range,” went Theory (local, Mercury) against Fact (Jev, Liquid).

Piece 33, “β-D-glucan may be useful but there is no specific antigen test,” went Theory (local, Mercury) against Fact (Jev, Liquid). The word “may” is the hedge.

Piece 60, intraventricular antifungals “can be considered,” is the one piece where all four readings were “only sometimes,” while the categories still split: No label, Fact, Theory, Fact.

The other splits are headings (Microbiology, Diagnostic testing, Treatment), figure panels, the “consider:” line, two differential-diagnosis bullets, and the common-regimen sentence. Full labels and scores for every split are in `comparison.json`.

## Readings, with Mercury called out

On 17 note pieces the category matched and the reading did not. On 15 of those, Mercury said “not sure” and the other three said “says yes.” On 2, Mercury said “says no” and the other three said “says yes.”

Those two are:

- Piece 11. “Combined brain-and-meningeal involvement (~14%) and isolated meningitis (~2.5%) are much less common.” Mercury: says no, score 0.83. The page held it. The other three: says yes.
- Piece 58. “Fluconazole is poorly active (MIC90 64).” Mercury: says no, score 0.87, and the page kept it. The other three: says yes, and their scores stayed under 0.72.

## Headings

The note has six markdown headings. Jev and Liquid marked all six as boilerplate, so the page skips them. Local marked none of them as boilerplate. Local called Microbiology a Fact at 0.08, Imaging a Theory, and Treatment a Step. Mercury skipped some headings and also skipped pieces that are sentences: the molecular-identification line, the figure lead-in, one figure panel, the “consider:” line, and the closing question.

## Speed on this run

The models ran together. Local scored one piece at a time. Each cloud model scored four pieces at a time.

| Model | Wall clock | Median time per piece |
| --- | ---: | ---: |
| Jev | 5.749 s | 166 ms |
| Liquid | 8.810 s | 276 ms |
| Mercury | 38.214 s | 429 ms |
| Local Clef | 620.357 s | 5,048 ms |

Eight Mercury pieces took longer than 5 seconds. The longest Mercury piece took 12.649 seconds. The run log does not say whether those were retries. Jev’s slowest piece was 1.301 seconds. Liquid’s slowest was 0.565 seconds. Local’s slowest was 7.102 seconds, and 79 of 121 local pieces took longer than 5 seconds.

## Files

All of these are on this machine, next to the source note.

| File | What it is |
| --- | --- |
| `doc2use-experiment/local.json` | Every local label, score, and wait reason |
| `doc2use-experiment/jev.json` | Every Jev label |
| `doc2use-experiment/mercury.json` | Every Mercury label |
| `doc2use-experiment/liquid.json` | Every Liquid label |
| `doc2use-experiment/comparison.json` | Counts plus all 58 pieces where category or reading differed |
| `doc2use-experiment/run.log` | Start and finish lines from the run |
| `doc2use-experiment/REPORT.md` | This report |

Each sentence record has the quote, the category, the reading, the score, whether the page would keep it, and the wait reasons.

## What this run leaves open

A person has not marked a correct label for any sentence. The counts above are agreement and page behavior.

The local result is the small model only. The Send page would show the same local result with the current setup, because no larger Clef address is configured.

The splitter cut the bibliography into titles and author lines, and it left some list markers on the front of sentences. Every model was scored on those same pieces. A cleaner split would change the piece count, so it would be a different experiment.
