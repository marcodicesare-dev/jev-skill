# Find the decisions your agent should stop writing prose to make

Most coding agents can find a place to call a new model. The harder question is whether that call improves the workflow. Paste the prompt below into an agent that can inspect your repository. It asks for a **shadow test**, so the current path keeps running until you have evidence.

> Read https://github.com/marcodicesare-dev/jev-skill/blob/main/SKILL.md and inspect this repository's real AI workflow. Find at most three repeated steps where a model currently returns a bounded decision: a yes/no, one of known options, or a score with defined levels. Quote the actual callsite and output contract for each.
>
> Rank those steps by their likely effect on this workflow. Use observed call counts, token usage and latency if available; write “unknown” where they are not. Exclude writing, open-ended reasoning, arithmetic, permission grants and any step where an incorrect answer has no review or rollback path. Do not assume Jev saves money just because its price per token is lower.
>
> For the best candidate, show the exact state a human would inspect, one focused Jev question, the code that would consume its answer, and the fallback when the API fails or the answer is uncertain. Check TypeSafe's current documentation before writing an integration.
>
> Prepare a shadow-mode comparison on at least 20 examples from this workflow: existing path and Jev see the same relevant evidence, but Jev changes no production result. Include clear easy, ambiguous and bad cases. Use existing human or objectively verifiable labels. If none exist, prepare the examples for human labelling and mark accuracy as unmeasured; do not let the same model invent its own answer key. Report accuracy or agreement where measurable, errors, p50 latency, actual provider cost, and what the human reviewer would have to read. Keep the per-item results so I can inspect failures. Do not replace the existing path until I have reviewed the comparison.
>
> Keep credentials out of prompts, logs and the repo. Follow this project's data-sharing rules before any provider call.

## What to expect back

| Decision | Current path and callsite | Frequency and cost | Jev question and evidence | Failure cost | Verdict |
|---|---|---:|---|---|---|
| One real step from your repo | File and function | Measured or unknown | Concrete state and typed answer | What breaks when wrong | Shadow-test, keep, or reject |

The most useful result may be **“keep the current path.”** In our own work, using Jev to narrow a writer's already readable source material made 20 ads worse; using it to search a transcript archive too large to read helped. The difference was the job, not a magic prompt.

## Three decisions from our own workflow

| Decision we considered | What the comparison showed | Result |
|---|---|---|
| Choose which of 44 notes an ad writer may read | On 20 ads, full context won 13 comparisons, filtered context won 3, and 4 tied | **Reject** the filter when the writer can read everything. |
| Classify whether a search term names one hotel or a kind of stay | With top search results in the state, Jev reached 98.7% on 300 labelled keywords versus 88.3% from the keyword alone | **Candidate** for a measured keyword workflow; the search results cost more than Jev. |
| Check whether an extracted value appears in its saved source page | In a small incident test, 3 invented values were flagged and 2 true controls passed | **Candidate** for a per-value receipt check, with human review; not yet a universal production guarantee. |

These outcomes are specific to our data and model version. They show why the audit asks for your callsites, labels and failure costs before suggesting a replacement.
