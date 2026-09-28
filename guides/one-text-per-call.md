# I tried to make Jev cheaper. Then 34% of its answers changed.

![A small figure crossing a ridge between pale and blue cliffs](../docs/assets/guides/one-text-per-call.jpg)

If your agent sorts thousands of messages, it is natural to ask whether you can put many of them into 1 model call. I tried it. Jev returned an answer for every message, and the bill was lower. Nothing crashed.

Then I sent the same messages separately. On my Italian test, **34%** of Jev's choices changed. On the English version, **28%** changed. The convenient batch had changed the decisions, not just the invoice.

The fix is a distinction most guides skip: **many questions about 1 message belong together; many different messages need separate inputs.** That still lets Jev save calls. In my test with **12** questions about each review, asking them together used about **4.2× fewer billed input tokens** than asking them 1 by 1, without more decision flips than simply rerunning the same request.

## The 2 things people call “batching”

Picture 1 customer message: “I paid twice and can't log in.” You might want to know which team gets it, whether it asks for a refund and whether it sounds urgent. Those are **3 questions about the same message**. Jev can answer them together because each question reads the same text.

Now picture **20 different customer messages**. They are **20 separate pieces of evidence**. Stuffing them into 1 large text asks Jev to keep track of which sentence belongs to which customer while it decides. The call can return plausible answers even when that mixing changes them.

| What I put in 1 Jev call | Result in my tests | What I would do |
| --- | --- | --- |
| **1 text, many questions** | About **4.2×** fewer billed input tokens for **12** questions on short reviews; decision flips stayed near rerun noise | Use it |
| **20 texts, questions for every text** | **28–34%** of choices changed against separate calls on the tested intent sets | Keep each text separate |

TypeSafe's [question documentation](https://docs.typesafe.ai/primitives) says questions in a request see the same state and are evaluated independently. That explains why the first pattern works: the message is sent once, then several questions look at it. It does not imply that unrelated messages should be merged into that state.

## A good call and a risky one

Here is the shape I would use for the example message. Each question below is a complete Jev question, but you would put the `questions` object in a file when using the command-line tool:

```json
{
  "state": {"message": "I paid twice and can't log in."},
  "questions": {
    "route": {
      "type": "choice",
      "instructions": "Which team should receive this message first?",
      "criteria": {
        "billing": {"what": "Charges, payments or refunds"},
        "account": {"what": "Login or account access"},
        "other": {"what": "Neither of those teams"}
      }
    },
    "refund": {
      "type": "noul",
      "instructions": "Does the message ask for a refund?"
    },
    "urgent": {
      "type": "noul",
      "instructions": "Does the message say the customer cannot use the product now?"
    }
  }
}
```

For `jev.py`, save the `questions` object in a JSON file and pass the `state` object with `--state`. The [public skill](https://github.com/marcodicesare-dev/jev-skill) shows the command. The combined JSON above is for reading, not the CLI's file format.

The risky version would put messages A through T inside the same `state`, then add question names like `route_A`, `route_B` and so on. It looks efficient because the response has all **20** answers. The test that matters is whether each answer agrees with the version where that message stood alone.

## What I actually tested

For the **20-message** test, each message was a short request and Jev faced **59** possible intents. Packing all **20** into 1 state changed **28%** of English decisions and **34%** of Italian decisions versus separate inputs. Accuracy fell by about **10** and **13** percentage points respectively on those sets.

Other packed-item tests were less dramatic: **5** reviews scored on **10** aspects changed **7.8%** of answers, while **10** reviews given star scores changed **15%**. Packing items did **not** reduce overall accuracy in every test. It did make the answer less stable, and on the larger intent choices it also made it worse.

I ran a separate test of the useful kind of batching: **40** real reviews, **12** questions per review, **480** decisions. Sending the identical combined request twice changed **5** decisions. Asking the questions separately changed **6**. Reversing their order, changing their IDs and moving their text under different IDs also stayed close to that noise floor. The combined call's median billed input-token saving was **4.16×** compared with **12** separate calls. I put the [cost method and API details](https://github.com/marcodicesare-dev/jev-skill/blob/main/reference/api.md) in the public skill.

Why not **12×**? Every separate call repeats a fixed overhead and the review, but the **12** question texts still cost tokens in the combined call. TypeSafe's published example uses a much longer document, so repeating that document is more expensive. My **4.16×** is for short reviews, not a correction to its long-document result.

## Let your agent test the shortcut

> Find a place in my workflow where Jev answers several questions. Show me the exact `state` used for each call. If it holds several independent customer messages, reviews or records, split it so each item gets its own call. Keep every question about that same item together. Replay at least 20 labelled items both ways, compare the exact choices, count flips and accuracy, and report billed input tokens and latency. Do not claim a saving until the labels still hold. Run separate-item calls concurrently if I need lower wall-clock time.

You can do this before rewriting your whole agent. Save **20** past inputs and the answers a person would give. Compare:

1. Separate item, its questions together.
2. The current packed-items version, if you have one.
3. An identical rerun, so you know how much variation exists even without changing the layout.

If the packed version saves money but moves answers you care about, the saving bought a different product behavior.

## The rule I keep

I send **1 item per Jev state** and put all useful questions about that item in the same call. That retained the answers within normal rerun variation in my **40-review** test and saved a median **4.16×** in billed input tokens against separate-question calls. Putting **20** different items into 1 state changed up to **34%** of decisions in the tests I ran.

Your text length, question count and model version can change the saving. Measure on your own inputs. The part worth remembering is the shape: **share the text across questions; don't make different texts share a decision.**
