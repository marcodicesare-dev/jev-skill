# My AI cited a page that proved nothing. I made Jev check it.

![A quiet shoreline between a rust cliff and a bright distant island](../docs/assets/guides/show-the-receipt.jpg)

Your agent gives you a precise number and a source link. You open the link. The page doesn't say the number.

That happened in my own work. A hotel-directory pipeline extracted an Expedia rating of **9.5/10 from 120 reviews**. The saved source was a **223-character bot check**, not a review page. In the same week, it attached **2** MICHELIN claims to a hotel missing from the list page it cited.

I asked Jev to read each saved page and choose among 3 answers: **the page supports this fact; the page contradicts it; the page doesn't address it**. On those actual mistakes it flagged **3 of 3** invented values and accepted **2 of 2** real controls. Then I tried the broader idea of checking a whole article. That version missed **3 of 5** known errors. The boundary matters: a small check against the right source helped; a vague “fact-check everything” job did not.

## Why this matters outside a hotel directory

Any agent that reads the web can produce this failure. A founder asks it for competitor prices. A student asks it to collect citations. A team asks it to fill a spreadsheet from supplier pages. The answer can look trustworthy because it carries a URL, even when the page is blocked, belongs to another company or never states the value.

The first question is not “Is this fact true somewhere on the internet?” It is much simpler: **does the saved page that produced this fact actually say it about this subject?** That is a question Jev can answer quickly when it sees the claim and the page together.

| Claim my pipeline wanted to save | What the supposed source contained | Jev's result |
| --- | --- | --- |
| Hotel A has **9.5/10** on Expedia from **120** reviews | A **223-character bot challenge** | Flagged: not addressed |
| Hotel B has a **19.2/20** MICHELIN score | A list that did not name Hotel B | Flagged: not addressed |
| Hotel B holds **MICHELIN Keys** | The same list did not name Hotel B | Flagged: not addressed |

The full Expedia page showed **9.8/10 from 103 reviews**. Jev accepted that real value. It also accepted a true score for a different hotel on the MICHELIN list. Those 2 controls matter: an alarm that flags every value would catch lies but be useless. The [public pattern note](https://github.com/marcodicesare-dev/jev-skill/blob/main/reference/patterns.md) records both the narrow success and the whole-page failure.

## The smallest Jev check

I save **the claim, its source URL, the page text as fetched and the fetch time**. If the page is long, I split its text into short chunks. Jev receives 1 chunk and a question about 1 precise claim. [The public recipe](https://github.com/marcodicesare-dev/jev-skill/blob/main/recipes/claim-vs-source.json) uses a Choice with these answers:

```json
{
  "supported": "The page states the claim or clearly implies it",
  "contradicted": "The page states something incompatible",
  "not_addressed": "The page does not say whether the claim is true"
}
```

The real question contains the full sentence, including the subject and the value: “Does this Expedia page say Hotel A has a guest score of 9.5/10 from 120 reviews?” Asking whether “9.5” appears anywhere on a page of many hotels would be too loose.

My code's rule for the test was: **accept only if at least 1 chunk supports the claim at 0.5 or above, and no chunk contradicts it at 0.5 or above**. Otherwise send the fact to a person with the source excerpt attached. The exact threshold was chosen for this small test; it needs a new labelled check before use in another workflow.

Put a simpler check ahead of Jev. If a scraper receives a tiny bot-challenge page, reject the fetch. Code would have caught that **223-character** page without asking any model. Jev earns its place when a real page exists but the extracted value may belong to another item or not appear there at all.

## I tried to expand it. That failed.

I also ran Jev over **124** sentences of an entire hotel page. I asked whether each sentence was supported by a collection of official source pages. Before the test I set 2 targets: catch all **5** errors I knew about and flag no more than **40%** of the page for review.

It caught **2 of 5** errors and flagged **57%** of sentences. Both targets failed. Some sentences came from reviews, competitor pages and travel-time data that I had not included in the receipts. Jev couldn't confirm a sentence against a page that was never its source.

A subtler wording error passed too. My text said the hotel was *above* Barga; the official page said it was *in* Barga. The hotel sits across the valley. Jev treated that loose paraphrase as supported. A model that checks whether text sounds similar is not a map.

That gives me a stricter design: check **each extracted field against the exact page it came from**. Do not point a whole article at a pile of vaguely related pages and call the result fact-checking.

## Give this job to your agent

The [Jev skill](https://github.com/marcodicesare-dev/jev-skill) contains the claim-versus-source question I used. Here is the assignment I would give an agent working on my own pipeline:

> Find every step where my workflow copies a fact from a page into a record or draft. For 1 important field, save the value, subject, URL, fetch time and raw page text together. Reject blocked, empty or clearly invalid fetches in code. Ask Jev whether that exact page supports, contradicts or does not address the complete claim. Show me 5 known correct values and 5 known incorrect or mismatched values before adding an automatic gate. Keep the page excerpt beside every flag. If a sentence draws on another source, check that source instead. Do not treat this as a general truth test or as permission to publish.

You could start with prices, dates or ratings. Pick the field whose mistake would most embarrass your product. A real receipt check is small enough to test on last week's records.

## The habit that survives the test

In my small extraction test, Jev flagged **3 of 3** invented values and passed **2 of 2** real ones. That is enough to justify testing a per-field check, not enough to claim “Jev eliminates hallucinations.” The whole-page version failed, and a misleading place description slipped through.

When an AI gives you a fact with a link, keep the source text with the fact and ask whether **that source** says **that fact** about **that subject**. Let code reject broken fetches, let Jev flag clear source mismatches, and let a person inspect what remains uncertain. A URL is a direction to evidence, not evidence by itself.
