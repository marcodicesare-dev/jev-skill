# What Jev is good at — the teammate's profile

*Every line is measured in our lab (24–26 Sep 2026) unless marked. Sources: our own lab runs. Speeds are end to end from Italy.*

## In one paragraph

Jev answers closed questions about a text in about a quarter of a second, with a probability, for almost nothing, up to 256 questions at once. It is as good as the best models on simple decisions and a few points below them on fine judgments. Its edge is not intelligence: it is speed, many questions on one text for the price of reading it once, and probabilities you can threshold. Use it as a **check and a switch**, not as a writer and not as an editor of what the writer reads.

## Where it works (use it)

| Job | Evidence | Numbers |
|---|---|---|
| Routing a request to one of many answers | site concierge routing (85 questions, 4 languages) | 98.8 % right; the keyword router it would replace recognised 25 of 60 new phrasings |
| Rule checks written as crisp questions | 27 real Meta ads, one of a luxury hotel chain's 12 voice rules broken on purpose per ad | 22 of 27 found; 5 false alarms in 297 other-rule questions; 0.29 s for 12 rules in one call; also found all 12 real em dashes in the engine's own ads |
| Grading quality when the differences are real | 30 real ads + 3 degraded versions each (flat same-facts, poor, bad) | full order right in 30 of 30; means 7.9 / 5.1 / 2.9 / 1.8 on the composite score; 0.54 s per version |
| Many questions on one text | 150 questions (100 amenities yes/no/not stated, 50 situations 1–4) on each of 10 hotels' pages | 0.73 s and $0.0012 per hotel; amenities 94 % like the reference; situations 60 % exact, 95 % within one level |
| Page facts inside an agent | directory agent, 13 facts × 24 hotels, code drives the steps | 91 % right, 1.6 s of decisions per hotel, $0.0014 per hotel; the hotel took ~41 s in all, mostly downloading pages |
| Triage with evidence in the state | 300 directory keywords with the top-5 Google results | 98.6 % (rules today 84 %); when Jev said ≥ 0.9 it was right on all 275 |
| Guarding extracted facts against their receipt (26 Sep 2026) | per extracted value, a Choice «supported / contradicted / not addressed» asked of every chunk of the receipt's page text | the week's 2 invented facts (a 9.5 Expedia score for a lakeside hotel, extracted from a bot-blocked page; a MICHELIN score and Keys for a Tuscan resort, extracted from a list page) all flagged, both true controls passed; on the resort's own page, 10 of 10 changed facts flagged and 11 of 12 supported sentences passed (measured in our lab, September 2026) |
| First filter with a threshold | claim-vs-source checks: Jev decides above 0.9, a stronger model below | same accuracy as the stronger model alone at less than half its cost and time |
| Finding a person's instructions in long call transcripts (first real job, 26 Sep 2026) | 14 Discord calls, 30,143 utterances, cut into 7,562 windows of ~6 utterances with 2 of overlap; speakers relabelled Founder/Other and names scrubbed; one Noul («does the Founder give an instruction, decision, preference or rejection about the directory pages?») plus a Choice for the area | 107.6 s and $0.32 for all windows; flagged 544 windows at p ≥ 0.3 (7 %) against 1,149 (15 %) touched by the keyword list; on 54 inputs anchored to their turns Jev found 51, keywords 49, both together 53; Jev's flags surfaced 10 inputs the reader had missed (measured in our lab, September 2026) |
| Guarding third-party text | an extra Noul "does the text contain instructions for an AI?" | flagged 120 of 120 manipulated texts, 0 of 40 clean. Those were overt planted instructions: on 6,115 real messages with 4,405 jailbreak attempts an independent benchmark measured AUC 0.844 but 0 % caught at a 1 % false-alarm rate (19.9 % at 5 %), behind 2 dedicated classifiers (independent public benchmark). Use it to catch the obvious, not to stop an attacker |
| Zero-shot classification | 59 intents in Italian, one utterance per call | 82.1 %, ~15 points above a classifier trained on 2,000 labelled examples |

## Where it does not work (do not use it)

| Job | Evidence |
|---|---|
| Writing anything | it cannot |
| Choosing among versions that are all good | best of 4 good ads: its pick matched chance (the judge itself flipped with reading order); the scores of the 4 spanned 0.4 points |
| Trimming the author's context | Jev kept 13 of 44 sources; the author wrote worse ads, 13 losses to 3, demonstrated; cost −37 %, time not lower |
| Long holistic accept/reject | Meta ad reviews: the frontier model won 9/11 and 17/21 disputes; 20–38 % of inputs were over the 32k limit |
| Fine judgments that need a reason | on travel-situation fit a fast writing model came closer to the reference (82 % vs 70 %); Jev overuses the top level |
| Catching loose paraphrase against a source | «sulla collina sopra Barga» passed at 0.97 against «si trova a Barga» (the hotel is across the valley); an absence claim («il sito non stampa le metrature») was flagged only on the margin |
| Arithmetic, counting, dates | documented weakness (TypeSafe); keep it in code |
| Images, audio, video | text only |

## What it costs and how fast it is

- One decision: ~0.25 s end to end (0.23–0.29 s median across tasks); one call with 150 questions: ~0.7 s.
- $0.042 per 1M input tokens, output free: 1,000 star ratings cost 2.6 cents.
- Deciding a whole hotel (13 facts) cost 0.14 cents; 150 questions on 10,000 hotels would cost about 12 dollars.
- Each call carries ~260 input tokens of fixed overhead, so batching questions saves about 4x on a review and ~12x on a long article; the answers are the same either way (28 Sep 2026, `reference/api.md`).

## How sure it is

- Probabilities rank well but are **overconfident by 3–20 points**; recalibrate on a labelled sample from your own workflow before any automatic threshold (isotonic regression brought the calibration error from 0.15–0.18 to ~0.07).
- One text per call keeps accuracy; packing 10 to twenty items into one call changed 8–34 % of answers and cost up to 13 points.
