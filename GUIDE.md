# The Ultimate Guide to Jev (After 19,367 Calls and 90M Tokens)

![A small writer beneath an enormous open book, with a page lifting into the light](assets/jev-guide-cover.png)

## I tried to make my AI writer cheaper. The writing got worse.

My AI writer had 44 research notes. It could read them all at once, but every note added to the bill. I thought I could save money by asking a smaller model to pick the useful notes first.

I tried it, and then I compared the ads it wrote across 20 cases.

| What the writer could read | Comparisons it won |
|---|---:|
| All 44 notes | **13** |
| Only the notes Jev selected | **3** |
| Inconclusive because the judge changed its answer when I reversed the order | **4** |

I had made the writer cheaper by hiding things it needed to know.

I almost gave up on the smaller model. Then I gave it a different job. I had 30,143 utterances from old team calls, and I wanted to find instructions buried inside them.

The model found **51 of 54** instructions that I already knew were there. I only had to read **7% of the archive windows** it had checked. The run took **108 seconds** and cost **$0.32**.

![A person examines 1 note against a vast cliff of archived documents](assets/jev-archive.png)

The model behaved differently because I had given it a different job.

I spent 4 days testing [Jev](https://docs.typesafe.ai/), TypeSafe's decision model, while building agents at [Lumina Frontier](https://www.luminafrontier.ai/?utm_source=github&utm_medium=guide&utm_campaign=jev_skill). I wanted to know which decisions I could give it, and which ones I should leave alone. The [research tally](reference/research-scope.md) explains what the 19,367 calls in the title actually count.

## Start with a small question

Imagine that a customer sends your company this message:

> I was charged twice and need help.

What should an AI do with it? It could send the message to the billing queue.

That is a small decision. It should not decide that 2 charges really happened, because it has not seen the account. It should not issue a refund, because choosing a queue is not the same as checking a payment.

This is where Jev makes sense to me. My code supplies the possible queues. Jev reads the message and chooses 1. Then another system or a person checks the account and replies.

The same idea works in other places:

- **Before publication:** Jev can check whether a saved passage supports a claim in an article.
- **During research:** Jev can flag a passage in a large archive that may answer my question.

In each case, it answers a question about evidence that I can keep and inspect.

Jev accepts a **state**, which can be text or JSON, and questions about that state. It returns typed answers and probabilities. I can use **Choice** to select from options I provide, **Score** to place an item on a scale I describe, or **Noul** to answer a yes-or-no question with a probability. [TypeSafe's documentation](https://docs.typesafe.ai/) has the current API details.

I have not measured a complete support workflow. The customer message is an example that makes the boundary easy to see. The results below come from work I actually tested.

## Show the model what a person would look at

I asked Jev to classify 300 search terms about hotels. I tested 2 versions of the same task:

| Evidence Jev could see | Correct classifications on my labelled examples |
|---|---:|
| Only the search query | **88.3%** |
| The query and its top 5 search results | **98.7%** |

Those results gave it the same clues a person might glance at before making the call. The improvement came from showing the model the evidence it needed.

This sounds obvious until you see how often an AI is asked to judge a source it cannot really read. In another system I tested, an AI reported a hotel's rating as **9.5**. The page it had saved as its source was a **223-character bot check**. The rating was nowhere on that page.

![A small investigator finds a thin thread to a hotel behind an enormous blank source page](assets/jev-source-check.png)

In a small incident test, Jev flagged that claim and 2 other invented facts. It also passed 2 true controls. That was useful, but I should have caught the bot page with ordinary code before asking Jev anything. A page with almost no content should not be treated as a source for a hotel rating.

My rule now is simple: if code can settle a problem, I use code. If the answer depends on what a passage means, I give the model the passage and ask a precise question about it. The [claim-versus-source recipe](recipes/claim-vs-source.json) shows the question I tested and its limits.

## Ask several questions about 1 thing

1 customer message might raise 3 questions:

- Which queue should receive it?
- Is the customer asking for a refund?
- Is the message trying to give instructions to the AI agent?

All 3 questions use the same message as evidence, so I can ask them in 1 call.

I tried the opposite approach in my review experiments. I packed different texts into 1 state and asked the model to keep them straight. Depending on the setup, **8% to 34%** of the answers changed.

When I grouped several questions about 1 short text, the answers stayed stable and the calls cost about **4× less** in my setup.

I use 1 item per state and ask several questions about that item. TypeSafe allows up to **256 questions** in 1 call, although each question still costs something. If 2 questions need different evidence, I make separate calls. The [API notes](reference/api.md) explain the measured cost and question shapes.

## Check the finished work, not the price of 1 step

Here is why the writer experiment failed.

All 44 notes fit in the writer's context. Jev selected a smaller set, which saved input tokens. But the notes it removed contained details the writer needed. The writer could not use information it had never seen.

If I had measured only the cost of Jev's call, I might have celebrated. When I compared the finished ads, the writer with all the notes won **13 to 3**. The other **4 comparisons changed when the judge saw the ads in the opposite order**.

I saw a related limit when I asked Jev to judge ads. I gave it groups of ads that were clearly good, flat, poor and broken. It ordered all **30 groups** correctly in that test. Then I gave it 4 versions that were all good. Its picks were near chance.

I would use that result to catch an obviously broken draft in this setting. I would not use it to pick the best of 4 strong creative ideas.

A cheap model call is only a win if the finished job improves. I have to count mistakes, human cleanup, latency, provider cost and the quality of what someone actually uses. The [capability notes](reference/capabilities.md) give the test sizes and conditions.

## Do not treat a probability as permission

1 result made me much more careful with confidence numbers.

I looked at **138 claim checks** at the high end of 1 experiment. Jev's average stated probability was **98.6%**. The answers were correct **84.8%** of the time. Other tasks had smaller gaps, but this 1 showed why I cannot copy a threshold from a demo and let the agent act.

Before I automate a decision, I label examples from my own workflow. I include easy examples, confusing examples and examples where a mistake matters. Then I compare the model's probabilities with what actually happened. I keep permissions and irreversible actions in code.

Even the names of the options can change the answer. I once described 5 star-rating choices correctly, but I gave them names that contradicted their descriptions. Exact ratings fell from **27 to 15 out of 40**. Jev read the names as part of the question.

When a result looks strange, I check the evidence, the instructions, the option names and the criteria before I blame the model.

## Try 1 decision in your own agent

I put the [Jev skill and a Python CLI](README.md) on GitHub. The CLI needs Python 3 and a TypeSafe API key, but it has no package dependencies. After you set `TYPESAFE_API_KEY` locally, you can run this from the cloned repo:

```bash
git clone https://github.com/marcodicesare-dev/jev-skill.git jev-skill
cd jev-skill

python3 tools/jev.py ask --via typesafe \
  --state '{"message":"I was charged twice and need help."}' \
  --questions examples/message-routing.json
```

The response includes `answers.route.choice` and the probability for each route. When I tested that exact message on `jev-1.13.0`, Jev returned `billing` in **0.29 seconds**.

That is 1 illustrative call, not a support benchmark. It classified the message. It did not inspect a bank statement.

The response also reports the model version, latency and token usage. The [live API docs](https://docs.typesafe.ai/) show the current limits, while my [API notes](reference/api.md) describe the version I tested.

If you already have an agent, you can use my [audit prompt](AUDIT-YOUR-AGENT.md) to find 1 repeated decision that a large model currently makes. Run Jev beside it on labelled cases. Compare the final result before you replace the old step.

## What the 19,367 calls mean

Over 4 days, I logged **19,367 successful Jev API responses** and **90.4 million metered input tokens**. The count includes retries and reruns. It does not mean I ran 19,367 independent experiments, and it cannot tell you how many tokens your agent will save.

I published the [counting method and scope](reference/research-scope.md). The archive search, writer comparison, search-term classification, batching tests, ad judgments and confidence check were measurements on my tasks. The support inbox was an illustration. Your own labelled examples will tell you whether Jev helps your product.

I started with a simple plan to make my writer cheaper. That plan made the writing worse. When I gave Jev a narrow question and the evidence it needed, it helped me search an archive that would have been painful to read by hand.

**That is the test I would run this week:** find 1 small decision your agent makes again and again. Run both approaches on real examples. Keep Jev if the whole job gets better. If it does not, you have found another useful boundary.

- [Get the skill, CLI and test data](README.md)
- [Use the agent audit prompt](AUDIT-YOUR-AGENT.md)
- [Read TypeSafe's official skill](https://github.com/typesafe-ai/skills)

I'm [Marco Di Cesare](https://x.com/marcodice_ai). I ran these experiments while building [Lumina](https://www.luminafrontier.ai/?utm_source=github&utm_medium=guide&utm_campaign=jev_skill), a platform for hotel marketing. I also share work on [Instagram](https://www.instagram.com/marcodice.ai/).
