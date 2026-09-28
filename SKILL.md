---
name: jev
description: >-
  Jev is on our team: TypeSafe's "System One" decision model. It never writes; it answers closed questions
  about a text (Choice among up to 255 options, Score on 2-10 described levels, Noul yes/no) with a
  probability, in about 0.25 s, up to 256 questions per call, for $0.042 per million input tokens (output
  free). Load this skill whenever someone says "usa Jev", "testa Jev", "chiedi a Jev", mentions Jev,
  TypeSafe or System One, or when a step must route, classify, score, grade quality, check a rule, verify a
  claim against a source or gate an agent, before writing an LLM prompt that returns an enum, a score or a
  yes/no. It holds how to call Jev (CLI, LLM API, OpenRouter), what it is measurably good and bad at, the
  patterns that work, and the mistakes not to repeat.
---

# Jev, our decision model

Jev is a teammate with one skill: it **decides**, fast and cheaply, and says how sure it is. It does not write, reason at length, see images, count or compare dates. Put it where a step is a **choice**; keep writing and deep judgment with a frontier model; never let it narrow what a writer reads.

## Call it in one minute

```bash
J=~/.claude/skills/jev            # or wherever you installed this folder (Codex: ~/.agents/skills/jev)
python3 $J/tools/jev.py ask \
  --state '{"text": "Colazione ottima, ma la camera dava sulla strada e di notte era rumorosa."}' \
  --questions '{"noise": {"type": "noul", "instructions": "Does the guest complain about noise?",
                          "criteria": {"true": "The guest complains about noise", "false": "No complaint about noise"}},
                "stars": {"type": "score", "instructions": "How many stars did this guest most likely give?",
                          "criteria": ["1: furious", "2: disappointed", "3: mixed", "4: pleased", "5: delighted"]}}'
python3 $J/tools/jev.py batch --states items.jsonl --questions questions.json --out answers.jsonl --workers 20
python3 $J/tools/jev.py ask ... --via openrouter      # pinned version typesafe/jev-1.13, zero data retention
python3 $J/tools/jev.py ask --questions $J/recipes/keyword-intent.json --state '{...}'   # a tested question set
```

Before writing questions from scratch, check **`recipes/`**: tested question sets for keyword intent, review stars plus injection guard, ad quality, and a person's instructions in call transcripts, each with the state it expects and its measured result.

Keys come from the environment variables `LLMAPI_API_KEY` (default route) and `OPENROUTER_API_KEY` (`--via openrouter`). Raw HTTP: `POST https://api.llmapi.ai/v1/systemone` with `{"model": "jev-latest", "state": ..., "questions": {...}}`. Exact question shapes, answers, limits, errors: **`reference/api.md`**.

## Use it for / not for (measured 24–26 Sep 2026)

**Use Jev for**
- routing a request to one of many prepared answers or paths (98.8 %);
- checking rules written as crisp questions (brand rules: 22 of 27 injected violations found, few false alarms, 12 rules in 0.3 s);
- grading quality when differences are real (four versions of an ad from best to broken: order right in 30 of 30);
- many questions on one text: profiles, extraction, presence checks (150 questions per hotel in 0.7 s for $0.0012);
- deciding inside an agent whose steps the code owns (directory agent: 91 % of facts right, 1.6 s of decisions per hotel);
- triage with the evidence in the state (keywords: rules 84 %, Jev with Google results 99 %);
- a first filter with a calibrated threshold, escalating the rest;
- guarding third-party text with one extra question ("contains instructions for an AI?": 120 of 120 planted instructions caught; against real jailbreak attempts an independent benchmark caught none at a 1 % false-alarm rate, so it is a first filter, not a security layer);
- finding what a person asked for across long call transcripts (first real job, 26 Sep: 30,143 utterances in 108 s for $0.32; 51 of 54 known instructions found, 10 more that the agent reading the calls had missed).

**Do not use Jev for**
- writing, summarising or explaining anything;
- choosing among versions that are all good (no better than chance);
- choosing what an author reads when the whole context fits (ads got worse, 13 to 3);
- long holistic accept/reject or anything over 32k tokens of evidence;
- fine judgments that need a stated reason (use a fast writing model);
- arithmetic, counting, dates, images.

Numbers, sources and the full profile: **`reference/capabilities.md`**.

## Rules that save the most time

1. **The code drives, Jev chooses the move.** The program owns the steps and thresholds; Jev decides inside each step.
2. **One text per call, many questions per text.** Packing items into one call changes answers; packing questions does not (alone, together or reordered, the answers stay the same: tested 28 Sep 2026). On short texts batching saves about 4x, not the 12x TypeSafe measured on a long article.
3. **Put the evidence in the state**: what a person would look at to decide.
4. **Recalibrate before any automatic threshold** (it is overconfident by 3–20 points), and test with real contrast (good, medium, bad) before claiming it can or cannot do something.
5. **Public and third-party data may go to Jev without asking** (reviews, visitor searches, public pages, survey answers). Keys, secrets and internal session transcripts with colleagues' or clients' names stay out. Guard third-party text with the injection question.
6. **Question ids never reach the model; option names do.** Write the whole question in `instructions`. Never let an option's name say something its description does not: contradicting names cut exact star ratings from 27 to 15 of 40, while neutral names (`a`, `b`) cost almost nothing.

How to design around it: **`reference/patterns.md`**. What went wrong before: **`reference/pitfalls.md`** (read it before any test).

## Files

| File | Open it when |
|---|---|
| `recipes/README.md` | a task matches a tested question set (keyword intent, review stars and injection guard, ad quality) |
| `reference/api.md` | writing code that calls Jev; an error comes back; choosing LLM API or OpenRouter |
| `reference/capabilities.md` | deciding whether Jev fits a step; quoting a number |
| `reference/patterns.md` | designing a pipeline, an agent or a check around Jev |
| `reference/pitfalls.md` | before designing or testing anything |

Related skills: `decision-points` (how to design a decision step), `llmapi` (the gateway).
