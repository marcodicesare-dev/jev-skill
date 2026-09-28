# Recipes: tested question sets, ready for the CLI

Each file is the exact question map used in a lab test, so its result holds only for the state shape shown here. Pass it with `--questions`:

```bash
J=~/.claude/skills/jev            # or wherever you installed this folder
python3 $J/tools/jev.py ask --questions $J/recipes/keyword-intent.json --state '{"keyword": "...", "destination": "...", "top_google_results": [{"title": "...", "domain": "..."}]}'
python3 $J/tools/jev.py batch --questions $J/recipes/review-stars-and-guard.json --states reviews.jsonl --out answers.jsonl
```

| File | State it expects | How to read the answer | Tested result | Source |
|---|---|---|---|---|
| `keyword-intent.json` | `{"keyword", "destination", "top_google_results": [{"title", "domain"}] }` (top 5 organic results) | `kind.choice` is `guest_need`, `specific_hotel` or `not_lodging` | 98.6 % on 300 labelled keywords; 275 of 275 right when the probability was at least 0.9; 88–91 % without the Google results | measured in our lab, September 2026 |
| `review-stars-and-guard.json` | `{"review": "..."}` | stars = `rating.score + 1`; `injection.noul` above 0.5 means the text tries to instruct an AI | injection caught in 120 of 120 planted reviews (overt, planted instructions; on 4,405 real jailbreak attempts an independent benchmark found 0 % caught at 1 % false alarms, 19.9 % at 5 %, independent public benchmark); star ratings on par with frontier models | measured in our lab, September 2026 |
| `ad-quality.json` | `{"brief_and_evidence": "...", "candidate_ad": "..."}` | for each of the nine axes take the expected level (sum of (index + 1) × probability, 1–10); overall = their mean + 2 × `publishReady.noul` | four versions of 30 real ads (original, flat, poor, broken) ranked in the right order in 30 of 30 | measured in our lab, September 2026 |
| `founder-inputs-from-transcripts.json` | `{"passage": "..."}`: ~6 consecutive utterances (or 40 s) with 2 of overlap, speakers relabelled `Founder` / `Other`, names scrubbed | read the windows with `directory_input.noul` ≥ 0.3; `area.choice` sorts them; then a person or an agent reads the flagged windows in full | on 54 known founder inputs: 51 found (keyword search 49, both 53), reading 7 % of the windows instead of 15 %; 10 more that the agent reading the calls had missed; 7,562 windows in 108 s for $0.32 | measured in our lab, 26 Sep 2026. The `area` options are specific to the hotel directory: rewrite them for another surface, keep the Noul's shape |
| `claim-vs-source.json` | `{"source": "<one chunk of the receipt's page text, ≤ 9,000 characters>"}`; one question per claim, up to 256 per call | a claim passes only if some chunk says `supported` at ≥ 0.5 and no chunk says `contradicted` at ≥ 0.5 | the week's 3 invented facts flagged, 2 true controls passed; 10 of 10 changed facts flagged (11 changes, one of which turned out true), 11 of 12 supported sentences passed; loose place paraphrase («sopra Barga» vs «a Barga») NOT caught. Checked per value against its own receipt only: the whole-page check failed both its pass marks (2 of 5 known-wrong sentences caught; 57 % of 124 sentences flagged against a ceiling of 40 %) | measured in our lab, 26 Sep 2026 |

Limits that come with them:
- `ad-quality.json` separates good from flat or broken; it does **not** pick the best among good versions (no better than chance).
- Probabilities are overconfident by 3–20 points: recalibrate on your own labelled cases before fixing an automatic threshold.
- Public and third-party text (reviews, searches, pages, survey answers) can be sent as it is (our policy); scrub only internal session transcripts, and never send keys.

A new recipe goes here only after a test with a known answer and real contrast (see `reference/patterns.md`, "How to test a new use").
