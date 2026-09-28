# I ran Jev 19,367 times. Here's the first job I'd give it in a new AI agent.

![A painted cliff opening onto a sunlit valley](../docs/assets/guides/first-job.jpg)

You launch a startup. Messages start coming in.

- “I paid twice.”
- “Your app crashed.”
- “How much does it cost?”

Before your AI can answer, it has to make a smaller decision: **who should handle each message?**

That is a Jev job. I give Jev the message and a few possible destinations. It picks 1 and returns probabilities for the options. Code can send the message to the right place. A larger AI writes the reply when a reply is needed.

I tested Jev across **19,367 successful calls** ([here's what I counted](https://github.com/marcodicesare-dev/jev-skill/blob/main/reference/research-scope.md)). The lesson wasn't “give Jev everything.” When I let it choose which notes an AI writer could read, the writing got worse. When I asked it to find instructions buried in **14** recorded meetings, it surfaced **10** that my first search had missed.

Jev is useful for small decisions you make over and over. It can choose, flag or score. It doesn't write your answer or decide what your business should do. This guide shows how to spot the first suitable job in your own agent and test it before changing your workflow.

## The job before the job

Think of the last customer message you handled. You probably made a decision before writing a word: should I answer it, send it to billing, look up an order, or ignore it?

An agent makes those decisions too. If each decision becomes a long request to a writing model, you pay for a writer to act as a sorter. Jev is [TypeSafe's model for short, defined judgments](https://docs.typesafe.ai/primitives). You give it the information it needs and a question whose possible answers you specify. It returns an answer your code can use.

There are 3 question shapes. You don't need their names to understand the jobs:

| You ask | Jev returns | Everyday example |
| --- | --- | --- |
| Which option fits? | 1 of your options, with probabilities | Billing, account access, or something else? |
| Is this statement true of the text? | A yes probability | Does this message ask for a refund? |
| How far along a scale is it? | A position on levels you described | Is this bug minor, serious, or blocking? |

TypeSafe calls those shapes **Choice**, **Noul** and **Score**. Jev cannot verify a bank transaction just because a customer says “I paid twice.” It can say that the message belongs in the billing queue. Checking the payment belongs to the billing system.

## Run 1 small decision

My [open-source Jev skill](https://github.com/marcodicesare-dev/jev-skill) includes a command-line tool and the question below. Its README explains where to install it for each agent. To try the CLI directly, set your TypeSafe key locally and run this call:

```bash
git clone https://github.com/marcodicesare-dev/jev-skill.git jev-skill
export TYPESAFE_API_KEY=...  # set locally; never paste the real key into a prompt
J=./jev-skill
python3 "$J/tools/jev.py" ask --via typesafe \
  --state '{"message":"I was charged twice and need help."}' \
  --questions "$J/examples/message-routing.json"
```

The question gives Jev **billing**, **account** and **other** as its choices. In a live call on **28 September 2026**, it returned `billing` in **0.291 seconds** on `jev-1.13.0`. These are the relevant fields from the actual response:

```json
{
  "model": "jev-1.13.0",
  "latency_s": 0.291,
  "answers": {
    "route": {
      "choice": "billing",
      "probabilities": {"billing": 1.0, "account": 0.0, "other": 0.0}
    }
  }
}
```

That is 1 working example, not a benchmark of support accuracy. I saved the [complete response without credentials](https://github.com/marcodicesare-dev/jev-skill/blob/main/guides/evidence/first-call.json) so you can inspect the fields I omitted above.

The model's answer is only the middle of the workflow. I would let code route the message to billing. I would **not** let this answer issue a refund: Jev has not seen a payment record or received permission to move money.

## Find your own first job

Don't begin by asking, “Where can I use Jev?” Open your agent's last **20** runs and find a decision it keeps making before it does the real work. A good candidate has 4 properties:

1. **It repeats.** The agent faces it often enough that speed or cost matters.
2. **The possible answers fit in a short list.** You can write the options before the model sees an example.
3. **You can show Jev the evidence.** A message, a page, a record or a short passage contains what a person would use to decide.
4. **A wrong answer is recoverable.** Unclear or consequential cases can go to a person or a stronger system.

Here is a prompt I would give a coding agent after installing the skill:

> Inspect my current workflow and find 1 repeated decision that happens before a larger model writes or reasons. Do not change the workflow yet. Show me 10 real examples, the information a person would need to decide, the exact Jev question and options, and what my code should do with each answer. Include an “other” route. Compare Jev with the current behavior on those 10 labelled examples. Report errors, time and cost. If the decision needs open-ended writing, exact arithmetic, permission to act, or evidence you cannot provide, reject the candidate.

The important line is **“do not change the workflow yet.”** An attractive demo is not evidence that your agent will work better.

## How I learned where Jev belongs

My first money-saving idea was to put Jev in front of an AI writer. Jev chose which of **44** source notes the writer could read. The writer with all the notes won **13** comparisons; the filtered writer won **3**, with **4** inconclusive. The cheaper writing step lost information it needed.

Then I gave Jev a different job: scan an archive too large to reread and mark short passages that might contain my instructions. In **14** calls, it found passages touching **51 of 54** known instructions. Reading the passages it marked surfaced **10** instructions my earlier search had missed. That run took **108 seconds** and cost **$0.32**. I put the [question and reading method in the public skill](https://github.com/marcodicesare-dev/jev-skill/blob/main/recipes/README.md).

Those tests teach a practical boundary. If the next step must *create* an answer or understand a whole body of source material, give that material to a capable writer. If the next step asks **which of these defined things is in this text?**, Jev may be worth testing.

## So what should you build first?

Start with 1 decision, 10–20 examples and the answer you would give for each. Run Jev on the same evidence your current agent sees. Count the mistakes before discussing speed or price. If the answer is useful, put code around it: an “other” option, a review path for uncertain cases, and a rule that keeps risky actions out of Jev's hands.

The inbox example proves a call works; it does not prove a support product is ready. My **19,367** calls include retries and reruns across several tasks, not **19,367** independent experiments. What they gave me was a clearer first question: **what small choice is your agent making again and again, and can you test that choice against real answers?**
