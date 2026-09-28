# Jev skill for Claude Code, Codex and other coding agents

**We ran Jev more than 19,000 times. This is the guide we wish we had before call one.** The [research tally](reference/research-scope.md) records 19,367 successful Jev API responses and 90.4M metered input tokens in 4 days of experiments. The useful part is what survived those tests: 5 copyable recipes, a CLI, failures, and the conditions under which each result held.

Start with [**The Ultimate Guide to Jev (After 19,367 Calls and 90M Tokens)**](https://marcodicesare-dev.github.io/jev-skill/) if you want the full story, an honest decision map and a first workflow you can run. The [Markdown version](GUIDE.md) lives here in the repo.

[Jev](https://docs.typesafe.ai/) takes a `state` and focused questions and returns typed answers: **Choice** (one option), **Score** (a described scale), or **Noul** (yes/no). It does not write prose. Your code decides what to do with its answers. This repository adds a standard-library Python CLI, 5 tested question sets, and measurements from real work. It is an independent community project, [not TypeSafe's official skill](https://github.com/typesafe-ai/skills).

## Install the Jev agent skill

```bash
git clone https://github.com/marcodicesare-dev/jev-skill.git ~/.claude/skills/jev  # Claude Code
git clone https://github.com/marcodicesare-dev/jev-skill.git ~/.agents/skills/jev  # Codex and others
export LLMAPI_API_KEY=...  # or OPENROUTER_API_KEY for the optional pinned route
```

Do not put keys in prompts or source control. Then ask your agent: **“Use the Jev skill to find one repeated, bounded decision in this workflow. Show me the question, the state, and a small labelled test before changing the workflow.”** Python 3 and an API key are enough to use the CLI; there are no package dependencies.

## First Jev API call

```bash
J=~/.claude/skills/jev  # adjust to your install path
python3 "$J/tools/jev.py" ask \
  --state '{"review":"The room was quiet, but breakfast was cold."}' \
  --questions '{"noise":{"type":"noul","instructions":"Does `review` complain about noise?","criteria":{"true":"A noise complaint is present","false":"No noise complaint is present"}}}'
```

The response includes `answers.noise.noul`, the model name, latency and estimated cost. The CLI uses the LLM API gateway by default because that is where most of our experiments ran. `--via typesafe` uses the official endpoint with a TypeSafe API key (**live tested: HTTP 200, jev-1.13.0, 28 September**). `--via openrouter` selects a version-pinned route. TypeSafe [reopened new signups on 28 September](https://x.com/typesafeai/status/2104337822350221795) after a temporary pause. Read [API and route details](reference/api.md) before integrating Jev into an application; check [TypeSafe's live documentation](https://docs.typesafe.ai/) for current contracts and limits.

## Choose the right job

| Good candidate | Keep elsewhere |
|---|---|
| Route a ticket, classify a review, score a defined quality dimension, check whether a source supports a claim | Write copy, explain a judgment, calculate an exact value, grant permissions or choose what a writer reads when all source material fits |

**The operating shape:** collect the evidence a person would inspect → ask narrow questions about one item → let code apply the answer → send uncertain or consequential cases to review. Read [patterns](reference/patterns.md) for the design and [pitfalls](reference/pitfalls.md) before setting thresholds.

If you already have an AI agent, copy the [workflow audit prompt](AUDIT-YOUR-AGENT.md). It finds candidate decisions in your code and sets up a shadow comparison before any replacement.

## What we tested

These are **our September 2026 results on our tasks**, not general Jev benchmarks. Denominators and limits are in [capabilities](reference/capabilities.md), the [recipe index](recipes/README.md), and the [research tally](reference/research-scope.md).

| Finding | Measured result | Practical lesson |
|---|---:|---|
| Let Jev select source notes for an ad writer when the writer could read them all | Full-context ads won 13 comparisons; filtered ads won 3, with 4 ties | Do not filter a writer's material by default. |
| Search 30,143 call utterances for known founder instructions | 51 of 54 found with Jev while reading 7% of windows; keyword search found 49 | Use Jev alongside search when the corpus is too large to read whole. |
| Give keyword classification the top 5 search results | 88.3% → 98.7% accuracy on 300 labelled keywords | Put the evidence a human would check into the state. |
| Reword a Score option so its name contradicted its description | Exact star ratings fell from 27 to 15 of 40 | Option names are part of the question. |
| Compare 4 quality levels of the same ad | Correct ordering on 30 of 30; near chance among 4 good variants | Test with real contrasts before calling a judge useful or useless. |
| Check probability against observed accuracy | Top band: 98.6% stated, 84.8% right across 138 claim checks | Calibrate on labelled cases before automatic pass lines. |

The [5 recipes](recipes/README.md) cover keyword intent, review stars and an injection flag, ad quality, transcript search, and claim-versus-source checks. Each recipe declares its required state and test. The injection flag caught simple planted strings, but it is **not** a security boundary.

## Jev guide by task

- **Jev API and Python example:** [request and response shape, routes, limits](reference/api.md)
- **Jev with Claude Code or Codex:** [skill instructions](SKILL.md) and the install command above
- **Where Jev belongs in an existing agent:** [copyable workflow audit](AUDIT-YOUR-AGENT.md)
- **Choice, Score and Noul questions:** [API reference](reference/api.md) and [tested recipes](recipes/README.md)
- **Classification, routing, scoring and LLM-as-judge:** [capabilities](reference/capabilities.md) and [patterns](reference/patterns.md)
- **RAG evidence checks and hallucinated extracted facts:** [claim-versus-source recipe](recipes/claim-vs-source.json) and its [measured limits](recipes/README.md)
- **Cost, latency, confidence and calibration:** [API notes](reference/api.md), [field results](reference/capabilities.md), [pitfalls](reference/pitfalls.md)

For new model versions, providers and SDK features, prefer [TypeSafe's official docs](https://docs.typesafe.ai/) and [official skill](https://github.com/typesafe-ai/skills). Our dated experiments are useful evidence, not a substitute for checking current behavior.

## Who made this

Built and maintained by [Marco Di Cesare](https://x.com/marcodice_ai) while working on [Lumina, an AI-native platform for hotel marketing](https://www.luminafrontier.ai/?utm_source=github&utm_medium=readme&utm_campaign=jev_skill). I share the visual side of the work on [Instagram](https://www.instagram.com/marcodice.ai/) and the experiments on [X](https://x.com/marcodice_ai).

This is independent research, not affiliated with TypeSafe. MIT licensed. If a recipe fails on your labelled cases, open an issue with the state shape, question, expected outcome and model version; remove private data first.
