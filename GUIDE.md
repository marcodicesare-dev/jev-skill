# The Ultimate Guide to Jev (After 19,367 Calls and 90M Tokens)

![An illustrated Jev decision at the edge of a larger system](assets/jev-guide-cover.png)

I spent 4 days trying to work out where Jev actually belongs in an AI system. The count in the title is from our logs: **19,367 successful API responses and 90.4M metered input tokens**, including retries and reruns. It is the size of the investigation, not a claim that every call was a different experiment. [Here's how I counted it.](reference/research-scope.md)

The first expensive lesson was a failure. I let Jev choose which source notes an ad writer could see. The writer with *all* the notes won 13 of 20 comparisons; the writer with Jev's selection won 3, and 4 tied. The apparently clever optimization removed details the writer needed. The next day, Jev helped us search 30,143 utterances of old calls in 108 seconds for $0.32, finding 51 of 54 known instructions while we read only 7% of the windows. Same model. Different job.

So here is the useful question: **Which small decisions are you currently paying a writing model to make, and which ones should stay with the writer?** This guide gives you an answer you can test in your own workflow, plus the command, question sets and failures we wish we had seen first.

## What Jev does in one minute

Jev is TypeSafe's *decision* model. Give it one `state` (text or a JSON object) and up to 256 focused questions about that same state. It returns one of 3 typed answers:

| Ask for | Jev returns | A real use |
|---|---|---|
| **Choice** | One of the options you defined, with probabilities | Which prepared support answer fits this message? |
| **Score** | A position on levels you described in words | How strongly does this review complain about noise? |
| **Noul** | A probability for yes/no | Does this extracted rating appear in its saved source page? |

It does **not** write the support answer, explain a decision, read an image, calculate a total or grant an agent permission. Your code owns the steps and what happens when Jev is wrong. TypeSafe's [official documentation](https://docs.typesafe.ai/) is the authority for the current API; the [skill in this repo](SKILL.md) describes what we measured on our tasks.

Think about a coding agent that asks a large model “Is this request about billing?” before every reply. If the only legal outcomes are `billing`, `booking` and `other`, the agent may be buying open-ended text generation for a closed choice. Jev can answer that choice while the writing model handles the actual reply. But if the agent is deciding what evidence to show the writer, our ad test says to be careful: a fast filter can make a good writer worse.

## Get one answer before building a system

Clone the repo as an agent skill for [Claude Code](https://github.com/marcodicesare-dev/jev-skill) or Codex:

```bash
git clone https://github.com/marcodicesare-dev/jev-skill.git ~/.claude/skills/jev
# Or: git clone https://github.com/marcodicesare-dev/jev-skill.git ~/.agents/skills/jev
export LLMAPI_API_KEY=...  # set locally; never paste a key into a prompt or commit
```

Use **LLM API** for the first call if you are following our experiments: it is the route we used for most of this work and the CLI default. If you have a TypeSafe key, add `--via typesafe`; we tested that direct route live on 28 September (HTTP 200, `jev-1.13.0`). OpenRouter is available with `--via openrouter` and a pinned model version. TypeSafe [reopened signups on 28 September](https://x.com/typesafeai/status/2104337822350221795) after a temporary pause. Check its current access and billing terms before following the direct route.

```bash
J=~/.claude/skills/jev
python3 "$J/tools/jev.py" ask \
  --state '{"review":"The room was quiet, but breakfast was cold."}' \
  --questions '{"noise":{"type":"noul","instructions":"Does `review` complain about noise?","criteria":{"true":"A noise complaint is present","false":"No noise complaint is present"}}}'
```

Look at `answers.noise.noul` and `model` in the response. The question ID is for your code; the full question belongs in `instructions`. A probability near 1 means the model strongly leans yes. **It does not mean the answer is right that often on your data.** Our [API reference](reference/api.md) has exact Choice, Score and Noul shapes, limits and errors.

## The 3 places I would look first

**1. A repeated closed decision inside an agent.** Find a call that returns a category, score or yes/no, where the available moves are known before the model runs. Have code enumerate the legal options. Ask Jev to pick. Keep a fallback and compare its answers against labelled examples before replacing anything. This is the same construction behind the “Jev plays chess” demonstrations: code supplies legal moves; Jev chooses one. Jev is not calculating chess.

**2. A large collection nobody reads end to end.** Split documents, reviews or transcripts into overlapping pieces. Ask the *same* narrow question of each piece and read the flagged ones. We found 51 of 54 known instructions in our call archive that way; keyword search found 49, and their union found 53. The win was not that Jev “understood our company.” It turned an archive too big to inspect into a shorter reading queue. Keep keyword search beside it because both missed something.

**3. A claim that should point back to its source.** Save the source text beside every extracted value, then ask whether that specific value is supported, contradicted or absent. In a small incident test, this flagged 3 invented hotel facts and passed 2 true controls. One invented rating came from a saved page that was only a 223-character bot check. A simple page-length check should have caught that *before* Jev ran. The [claim-versus-source recipe](recipes/claim-vs-source.json) is a starting point, not a universal fact checker; a loose geographic paraphrase still passed in our test.

If you want your agent to find candidate callsites, [paste this audit prompt into it](AUDIT-YOUR-AGENT.md). It asks for code locations, actual frequency and cost, a bounded Jev question, and a shadow comparison. It also permits the right answer: keep the current system.

## The mistakes that mattered more than the benchmark wins

**Don't let Jev preselect a writer's readable material.** In our 20-ad comparison, the full-context writer won 13–3 with 4 ties. Jev can check a draft *after* the writer has used the sources, if the check is a narrow rule. It could help select from an archive that will never fit in the writer's context; it hurt when 44 notes already fit.

**Put the evidence you would inspect into the state.** On 300 labelled hotel search terms, keyword-only classification reached 88.3%. With the top 5 search results in the state, it reached 98.7%. Those results cost money to fetch and can be noisy. The lesson is to measure the *whole evidence path*, not celebrate the Jev call alone.

**Write option names as carefully as the descriptions.** We gave a star-rating question 5 options, then deliberately renamed the keys to contradict their descriptions. Exact answers fell from 27 to 15 of 40. Neutral keys were fine. The [API reference](reference/api.md) shows the shape; a key is not invisible metadata.

**One text per call; many questions about that text.** When we packed several reviews into one state, 8–34% of answers changed across the tested setups. Packing questions about one review preserved answers in our test and saved about 4× on short reviews. TypeSafe measured a larger saving on a long article; your text length changes the economics. [See the measurements.](reference/api.md#what-a-call-costs-and-why-batching-saves-less-on-short-texts)

**Treat confidence as a ranking until you calibrate it.** In 138 high-probability claim checks, the model's mean stated probability was 98.6%; observed accuracy was 84.8%. We also saw tasks with much smaller gaps. A `0.9` automation line copied from someone else's recipe has no warrant. Label examples from your workflow and choose the point where mistakes and human review are acceptable.

**A simple injection question is a smoke alarm, not a lock.** Our question caught 120 of 120 obvious planted instructions in reviews. An [independent test](https://backnotprop.com/blog/jev-guardrails) found 0% recall on harder attacks at a 1% false-alarm operating point. Code must retain the permission boundary regardless of Jev's answer.

## What this could unlock, if the whole workflow earns it

The interesting construction is **many cheap, typed decisions around a smaller number of writing steps**. A model writes a plan or answer; Jev checks a concrete property, chooses among approved moves, or routes the uncertain case to a person. The choices can repeat at a pace that makes some old workflows worth reconsidering:

- **An archive you can ask new questions of tomorrow.** Tag every review or document with a new semantic question, then count, group or retrieve the matching source records. For a count, calibrate first; summing overconfident probabilities can inflate rare events.
- **A brand that remembers corrections.** Turn a human correction into a narrowly worded check over future drafts, and show the reviewer the sentence that triggered it. We tested rule checks in isolation; a continuously learning brand workflow remains a product hypothesis.
- **A live interface that reacts to meaning.** A form or support desk could select a prepared next step as a person speaks or types, without waiting for a prose answer at every turn. We measured the speed of the individual decisions; we have not proved a customer interaction works better.
- **Pages assembled from approved pieces for a specific need.** We tested one version on 40 hotel searches. A blind model judge preferred 38 assembled pages to a generic hotel homepage, but about 1/3 mixed pieces poorly, the comparison was weak, and no real visitor outcome was measured. The product question remains open.

These are building hypotheses, not 4 shipped products. The speed of a brick does not prove the house is useful. Start with the customer job, the current alternative, and a test that can actually tell you the idea was wrong.

## Copy this before you change a workflow

```text
1. Name the exact decision and the code that consumes it.
2. Write the legal answers and the evidence a human would read.
3. Keep one item in each state; ask related questions together.
4. Run Jev beside the current path on labelled easy, ambiguous and bad cases.
5. Compare mistakes, human review, latency and total provider cost.
6. Change the path only when it wins on the job you actually have.
```

The [5 tested question sets](recipes/README.md) and [agent audit prompt](AUDIT-YOUR-AGENT.md) let you start today. The [capability notes](reference/capabilities.md) show denominators and limits for the numbers above. If your experiment contradicts ours, send the state shape, question, expected answer and model version in an issue, with private data removed. That would make this guide better than another round of Jev hype.

---

Written by [Marco Di Cesare](https://x.com/marcodice_ai). The experiments came from work on [Lumina](https://www.luminafrontier.ai/?utm_source=github&utm_medium=guide&utm_campaign=jev_skill), where we build tools for hotel marketing. More visual notes: [Instagram](https://www.instagram.com/marcodice.ai/). This is an independent guide, not a TypeSafe publication.
