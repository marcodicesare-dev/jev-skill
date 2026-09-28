# 5 Jev jobs to test in a real agent

Use this after the [workflow audit](../AUDIT-YOUR-AGENT.md) identifies a repeated decision. Each job below links to a complete field guide and, where available, a measured recipe. The figures are results from my September 2026 work on `jev-1.13.0`, not promises for another product. Keep the old path running until a labelled comparison shows that the whole workflow improves.

## 1. Route a message before writing a reply

Give Jev the message and the destinations your code can actually use. A route such as `billing` means “send this message to billing”; it does not establish that a charge happened or authorize a refund. [`examples/message-routing.json`](../examples/message-routing.json) is a runnable illustration, checked with 1 live call, **not** a measured support classifier.

Inspect the last 20 runs of your agent. Find 1 repeated choice with short, predefined answers and evidence a person could inspect. Label 10–20 examples, including unclear ones. Run Jev beside the current path and compare mistakes before making it live. Give code an `other` route, a review path and a fallback when the provider fails. [Read the first-job guide](../guides/first-job.md).

## 2. Recover instructions from a long archive

Cut calls or chats into overlapping passages of about 6 utterances with 2 repeated between neighbors. Relabel speakers and apply the project's data-sharing rules before sending text to a provider. Ask whether the relevant person makes a decision, gives an instruction, expresses a preference or rejects a proposal on the topic. [`recipes/founder-inputs-from-transcripts.json`](../recipes/founder-inputs-from-transcripts.json) is the measured question shape; rewrite its hotel-specific topic and area options.

Set the review line using decisions you already know are in **your** archive. My 0.3 line flagged 544 of 7,562 passages and touched 51 of 54 known instructions, but it is not a universal threshold. Run keyword search too: it found 2 instructions Jev missed. Read the union in the original transcript and return an exact passage, date, speaker role and current status for every recovered decision. [Read the archive guide](../guides/lost-decisions.md).

## 3. Test a probability before it controls an action

For each decision, save the model version, input, full option probabilities, chosen answer and an independently checked label. A Choice's top probability is different from the response's derived `confidence` field; neither is an observed accuracy rate. Group repeated variants of 1 item together during validation.

Count sample size, mean top probability and actual accuracy in bands. On 138 claim checks with top probability 0.9–1.0, Jev averaged 98.6% but was right 84.8% of the time. Choose an acceptable error rate before testing a threshold, then check it on unseen items from your own task. For consequential or unclear cases, route to review. Recheck after the model, question or evidence changes. [Read the probability guide](../guides/99-percent.md).

## 4. Batch questions about 1 item, not unrelated items

Put 1 independent message, page or review in each `state`; ask all useful questions about that item together. Run separate-item calls concurrently when wall-clock time matters. In my 40-review test, 12 questions in 1 call used 4.16× fewer billed input tokens than 12 calls; decision flips were near the identical-rerun noise floor. Packing 20 independent texts into 1 state changed 28% of English decisions and 34% of Italian decisions in the tested intent sets.

Replay labelled items in both layouts and include an identical rerun. Compare the exact choices, accuracy, billed input tokens and latency. Do not infer a saving from call count alone. [Read the batching guide](../guides/one-text-per-call.md).

## 5. Check an extracted fact against its own source

Keep the complete claim, subject, source URL, fetch time and page text together. Reject blocked or empty fetches in code before asking Jev. For 1 field, ask whether **that page** supports, contradicts or does not address **that exact claim**. The tested [`claim-vs-source` recipe](../recipes/claim-vs-source.json) uses a Choice; its placeholder must be replaced for each actual claim. Read the returned source excerpt before accepting a consequential value.

In a 5-item incident test, Jev flagged 3 unsupported facts and accepted 2 true controls. A broader whole-page check caught only 2 of 5 known errors and flagged 57% of sentences. Start with a field and its receipt, not a whole article against a mixed pile of sources. Try at least 5 known good and 5 known bad values from your workflow before using it as a gate. [Read the source-check guide](../guides/show-the-receipt.md).
