# Mistakes we made with Jev — read before designing or testing

*Each one cost us time or a wrong conclusion between 24 and 26 September 2026.*

1. **Concluding "it can't" from a test without contrast.** We wrote that Jev "has no taste" after it failed to pick the best of four good ads. Given good, flat, poor and bad versions, it ordered all four right in 30 of 30 ads. Always include items that are clearly worse or clearly violating.
2. **Packing several items into one call.** Ten reviews or twenty sentences in one state changed 8–34 % of answers and cost up to 13 points. One text per call; many questions per text is fine.
3. **Trusting raw probabilities as thresholds.** Overconfident by 3–20 points on every task. Recalibrate on a few hundred of your own labelled cases, then fix the threshold before looking at the results.
4. **Trimming the writer's context with Jev.** Cheaper and worse (13–3). Jev checks outputs; it does not decide what the writer may read. This holds when the whole context fits the writer. When it cannot fit (an archive, a whole market), something must choose, and choosing with written criteria is where TypeSafe's team reports its biggest production wins ("tune-able RAG", 25 Sep 2026; NOT TESTED by us).
5. **Vague rules as questions.** "Use the present tense" and "speak as We" were flagged on most clean ads. A rule becomes a question only when a stranger could answer it from the text alone.
6. **Sending private records to an external service.** A transcript test included names that should have been removed first. Apply the user's data-sharing rules before any provider call. Remove keys and secrets; scrub private records when required. Parse JSON before scrubbing string values so the structure stays valid. Public availability alone does not grant permission to send data.
7. **Comparing against slow settings of other models.** A frontier model with its default reasoning looks 8–15× slower than Jev; with reasoning off (`reasoning_effort: "none"`) the gap is 3–5×. Compare against the fastest honest setting.
8. **Forgetting the 32k limit.** 20–38 % of real Meta ad reviews and every strategy-concept critique (~58k tokens) were over it. Measure input sizes before designing.
9. **Assuming the version is stable.** LLM API serves only `jev-latest`, which moves. Log `response.model`; re-check thresholds when it changes; use OpenRouter `typesafe/jev-1.13` to pin.
10. **Letting Jev drive an agent.** The code owns the steps; Jev decides inside each step.
11. **Counting duplicates twice.** A Langfuse export repeated two calls; our counts were wrong until we deduplicated by id. Deduplicate every export.
12. **Blaming Jev for our harness.** Rate limits (30/min until 25 Sep) belonged to the LLM API account, not to Jev; 402s on OpenRouter came from a low balance. Check the gateway first.
13. **Testing a workflow we invented instead of the product's job.** The 26 Sep page-composition test measured our own idea (compose from the hotel's own pages) against a weak opponent (a generic homepage), while the product it was for, the directory, exists to tell a hotel with every voice. Write the job first, feed the job's real inputs, and fight the real alternative (`patterns.md`, step 0 of "How to test a new use").
