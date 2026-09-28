# jev-skill

**A skill that teaches your coding agent to use Jev, measured on real work.**

[Jev](https://docs.typesafe.ai) is TypeSafe's decision model. It never writes: it answers closed questions about a text (a choice among options, a score on described levels, a yes/no) with a probability, in about a quarter of a second, for $0.042 per million input tokens.

We put Jev to work on a real hotel-marketing stack in September 2026: ads, reviews, keywords, call transcripts, a hotel directory. This skill is what we learned, written for Claude Code, Codex and any agent that reads skills. Say **"use Jev"** and the agent knows how to call it, what it is good and bad at (with numbers), which question sets are already tested, and which mistakes we already made for you.

## Install

```bash
git clone https://github.com/marcodicesare-dev/jev-skill ~/.claude/skills/jev     # Claude Code
git clone https://github.com/marcodicesare-dev/jev-skill ~/.agents/skills/jev     # Codex and others
export LLMAPI_API_KEY=...        # or OPENROUTER_API_KEY for a pinned model version
```

## What is inside

| File | What it gives your agent |
|---|---|
| `SKILL.md` | when to use Jev and when not, six rules, a one-minute call |
| `reference/api.md` | the request, the three question types, what a call really costs, the errors we met |
| `reference/capabilities.md` | what Jev did on each job, with the numbers |
| `reference/patterns.md` | designs that worked (and one that failed), and how to test a new use |
| `reference/pitfalls.md` | thirteen mistakes that cost us time or a wrong conclusion |
| `recipes/` | tested question sets: keyword intent, review stars with an injection guard, ad quality, instructions in call transcripts, claims against their source |
| `tools/jev.py` | a small CLI: `ask`, `batch`, `--via openrouter` |

## Five things we measured that we have not seen published elsewhere

1. Letting Jev choose what a writer model reads made the writing worse when everything fit (13 losses to 3), and found 51 of 54 needles when it could not fit (30,143 utterances, 7 % read).
2. Packing several texts into one call changes 8–34 % of answers; packing many questions about one text changes nothing.
3. Jev reads your option names: a name that contradicts its description cut exact star ratings from 27 to 15 of 40.
4. Jev orders good, flat, poor and broken versions of an ad right 30 times out of 30, but picks at chance among versions that are all good.
5. Probabilities are overconfident by 3–20 points on every task we measured: recalibrate before any threshold.

## Honest limits

Our tests are ours: hotel marketing, English and Italian, jev-1.13, September 2026. Treat every threshold as a starting point for your own labelled cases. Not affiliated with TypeSafe.

Maintained by Marco Di Cesare ([Lumina](https://www.luminafrontier.ai)). MIT licence.
