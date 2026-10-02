# Why dozens of facts were not kept

2 October 2026. Counts are from `comparison.json`. The keep rule is in `ClefFace/cloudflare/src/engine/normalize.ts`.

## Expectation

`doc2use.md` is a fact sheet. Nearly every sentence in the note states a fact: what the organism is, how often it causes brain abscess, the mortality range, where it lives, what imaging shows, how it is diagnosed, and how it is treated.

A `[1]` or `[2]` at the end of a sentence is the source of that fact. It does not stop the sentence from being a fact.

The reference list at the bottom is titles, authors, and journal names. Those are not the facts.

The page should have kept the facts. Headings can be skipped. The reference-list scraps can be skipped. A kept sentence whose reading is backwards is a bad keep.

## What happened

The splitter cut the file into 121 pieces.

- 64 pieces are the note.
- 57 pieces are the reference list, broken into titles and author lines.

On the note, the models called these Facts:

| Model | Facts it called in the note | Facts the page kept |
| --- | ---: | ---: |
| Local Clef | 43 | 0 |
| Jev | 50 | 3 |
| Mercury | 42 | 4 |
| Liquid | 48 | 6 |

That is dozens of facts in, and 0 to 6 kept. No fact was kept by three or four models. All 57 reference scraps were called No label, which is fine. They are not the missing facts.

The nine sentences anyone kept were all facts with no citation bracket left on that piece. The facts that still had `[1]` on them were not kept by anyone.

One bad keep: Mercury kept “fluconazole is poorly active” as “says no.” The sentence states that fact. The other three read it as “says yes” and did not keep it.

## Causes

### 1. A citation throws the fact out

The page adds a wait whenever a model says the sentence relies on a citation or an outside source. On 24 note pieces that at least three models called Fact, every model raised that flag, and the page kept none of them.

Those 24 are facts. The brackets are why they were dropped.

**Change.** A citation may be shown on the fact. It must not, by itself, remove the fact from the kept set.

**Check.** Those 24 come back as kept facts, with the citation still visible.

### 2. The score is the weakest side question

For a Fact, the score is the lowest of several answers: the category, the reading, whether it is “stated as a fact,” the time scope, and whether a number is present. The keep line is 0.72. One unsure side answer pulls a sure fact under the line.

Local’s highest score on the whole note was 0.7159, and that was on a figure caption, not on a fact. None of its 43 facts reached 0.72.

This run saved only the final score. It did not save each question’s score, so we cannot yet name the side question that failed.

**Change.** Save every question score. Then let the keep score be the category and the reading. Leave the other answers on the record for a person to see.

**Check.** Uncited facts such as the culture description, “CSF cultures are mostly negative,” surgery in about 89% of cases, and repeat surgery in about 20% are kept when the category and the reading are both at least 0.72.

### 3. Local Clef never reached the line, and the larger model was not called

Local kept nothing. The model that answered was the small 4-bit Clef on this computer. The code’s own test said all 121 answers should be asked of a larger Clef. That address was not set, so the small model’s answer stood. It took 620.357 seconds.

**Change.** Keep the small model as the on-this-computer path. Say plainly that, on this note, it kept nothing. Add a larger Clef only when that model is actually available.

**Check.** The report names which file answered. If a larger model is run, its keep count sits beside the small model’s zero.

### 4. A muddled reading blocks a fact, and a backwards reading can be kept

If a Fact’s reading is “not sure,” the page holds it. Mercury did that on 15 facts the other three read as “says yes.” On the culture sentence Mercury’s score was 0.86 and the page still held it because the reading was “not sure.”

The fluconazole sentence is the opposite fault: a high score and the wrong reading, and the page kept it.

**Change.** “Not sure” still holds the fact. A reading that reverses the sentence does not get kept when the other models read it the other way.

**Check.** “Fluconazole is poorly active” is not kept as “says no.” The culture sentence is kept as “says yes” if its category score clears 0.72.

### 5. The models did not keep the same facts

Even among facts with no citation bracket, the kept lists do not match. Four facts were kept by two models. Five were kept by one. None were kept by three or four. Jev and Liquid agreed most often on the note: same category on 50 of 64 pieces, same category and reading on 46 of 64.

Each score is that model’s own certainty. The same 0.72 line is four different rulers.

**Change.** Do not crown a winner from this run. After the citation gate and the score formula are fixed, compare the four kept lists again on this same note.

**Check.** A later run reports, for each fact in the note, which models kept it.

### 6. Some pieces are not facts

Six markdown headings, figure captions, and the closing question are inside the 64. The 57 reference scraps are a separate pile. They make “121 pieces” look like 121 facts. The missing facts are the ones in the note, not the bibliography.

**Change.** Count the note’s facts separately from headings and from the reference list.

**Check.** The next report says how many note facts were kept, not only how many of 121 pieces were kept.

## Order for a mitigation plan

1. Stop a citation from throwing out a fact.
2. Save each question’s score, then stop side questions from vetoing a fact.
3. Block a backwards reading from being kept.
4. Report note facts separately from headings and the reference list.
5. Leave local Clef as the empty result until a larger model is actually connected.
6. Compare the four models again on this same note before picking a default.
