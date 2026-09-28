# Jev said “99% sure.” About 15% of those answers were wrong.

![A small figure on a red plateau beneath a vast apricot sky](../docs/assets/guides/99-percent.jpg)

Imagine your agent deciding whether to publish a fact, send a message or approve a customer's request. Jev returns an answer with a number near **99%**. It is tempting to say, “That's safe enough; let it act.”

I checked what that number meant on **210** questions with known answers. Among the **138** answers in the highest probability range, Jev's average top probability was **98.6%**. It was right **84.8%** of the time. Roughly **15%** were wrong despite that impressive-looking number.

This does not make Jev useless. A higher probability often helps sort the easy cases from the hard ones. It does mean your agent should learn the difference between **“Jev prefers this answer”** and **“this answer is correct 99 times out of 100.”** Here is how I would test that difference before letting an agent act automatically.

## What the number is, in plain English

Say Jev chooses among 3 inbox folders: billing, account access and other. Its response gives a probability for each option. It also gives a separate field called `confidence`, which [TypeSafe computes from those probabilities](https://docs.typesafe.ai/confidence). The confidence field summarizes how strongly 1 option stands out. It is **not** a report of how often Jev has been correct in your inbox.

For this article, I am discussing the **top option's probability**, not that derived `confidence` field. Both can be useful for deciding what to inspect next. Neither becomes an observed accuracy rate until you compare it with answers you know are right.

Think of a weather forecaster who says “90% rain” 100 times. If it rains on 90 of those days, the percentage describes reality well. If it rains on 60, the forecast might still help you compare rainy days with dry ones, but the number is too strong. That comparison is called calibration.

## What I measured

I asked Jev whether a claim was supported by a passage and compared its answer with the labelled result. I grouped answers by their top probability:

| Jev's top-probability range | Answers | Average probability | Actually correct |
| --- | ---: | ---: | ---: |
| **90–100%** | **138** | **98.6%** | **84.8%** |
| **80–90%** | **25** | **85.8%** | **48.0%** |

The second row has only **25** examples, so it is noisy. The first is large enough to show why I would not treat a raw **0.99** as permission to publish or pay. Across **10** runs on **5** jobs, Jev's average top probability was above its measured accuracy every time, by **2.9 to 19.6 percentage points**. The [public test summary](https://github.com/marcodicesare-dev/jev-skill/blob/main/reference/capabilities.md) records the range and the recalibration result.

At the same time, probability still helped rank cases. On a separate star-rating task, accuracy was **68%** across all items, **82%** among answers above **0.9**, and **87%** above **0.95**. It was better at pointing to easier cases than at naming the exact chance of being right.

## Check your agent before you choose a threshold

You do not need a statistics degree for the first check:

1. Save the model version, question, input, chosen answer and full probabilities for each decision.
2. Collect **200–500** real examples if you can, with answers a person checked independently. Keep related versions of the same item together when you split the data.
3. Put answers into probability bands such as **0.7–0.8**, **0.8–0.9** and **0.9–1.0**. Count how many were right in each band.
4. Decide the acceptable error rate **before** moving the automatic-action line. A mistaken folder is recoverable. A wrong payment or published claim may not be.
5. Send the rest to review, and repeat the check when you change the question, evidence or model version.

If you only have **20** examples, use them to spot obvious failure, not to declare your **0.95** threshold safe. A handful of successes cannot tell you what happens in the rare wrong cases.

The [Jev skill](https://github.com/marcodicesare-dev/jev-skill) includes the API response shape and the dated limitations behind this result. Give your coding agent this job:

> Read my logged Jev decisions and the independently checked answers. Separate the top option's probability from the response's `confidence` field. For each probability band, show sample size, mean probability and actual accuracy. Find the error rate among decisions I would have automated at each proposed threshold. Keep repeated versions of the same item in the same validation group. Do not choose a threshold from the same examples and call it validated; reserve unseen cases for the final check. Tell me which errors would have affected users and which were recoverable.

## Can I repair the probabilities?

Sometimes. I tested a mapping that learns from past labelled answers. On **210** claim checks, one measure of probability error fell from **0.184** to **0.067**. On **936** answers in a multilingual routing test, it fell from **0.154** to **0.067**. I split repeated versions of an item into the same fold so the mapping could not learn from a twin of its test case.

The repair failed on a smaller **117-answer** slice: error rose from **0.108** to **0.131**. So I would not paste those improved numbers onto a new agent and assume its probabilities are fixed. Gather its own labels, keep a genuinely unseen check set, and leave uncertain or consequential actions to a person or another system.

## The decision to save

Jev can tell an agent which answer it favors and which cases look easier. In my **210-item** check, the most confident band averaged **98.6%** probability but achieved **84.8%** accuracy. That gap is big enough to change what I would automate.

Before your agent treats a probability as permission, count real errors at the threshold you plan to use. Keep the exact input and model version so you can find out why an answer failed. Use the score to prioritize review; earn automatic action with a labelled test on your own job.
