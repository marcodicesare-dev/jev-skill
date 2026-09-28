# My AI read 14 team calls and missed 10 things I asked for. Jev found them.

![A small figure looking over a dark sea at a coral horizon](../docs/assets/guides/lost-decisions.jpg)

I had **14** recorded team calls. They contained **30,143** things people said. Some of my instructions for work in progress were buried in there, and the first agent reading the calls had missed **10** of them.

I gave Jev a smaller job: look at a few lines at a time and tell me whether I was giving an instruction, making a decision, expressing a preference or rejecting something. Jev marked **7%** of the short passages for a full read. The scan took **108 seconds** and cost **$0.32**. Reading those marked passages surfaced the **10** missed instructions.

If your startup records calls, this is the useful part: you don't need another summary of everything everyone said. You need a reliable way back to the moment someone said the thing your agent must now obey. Jev helped me build that reading queue. It did not decide what the instructions meant.

## Why search missed them

Keyword search is good when you know the words to type. It is less helpful when a decision was spoken in different words, between many mentions of the same topic.

In my calls, words such as “video,” “photo” and “keyword” appeared again and again. A keyword hit sent my first reader to plenty of relevant talk, but it did not reliably pick out the sentence where I actually made a decision.

Jev asked a different question of each short passage: **is the person I care about making a decision here?** It could mark a rejection even if I never said the project's usual keyword.

| Search method | Share of passages sent for full reading | Known instructions it touched |
| --- | ---: | ---: |
| Keyword list | **15%** | **49 of 54** |
| Jev | **7%** | **51 of 54** |
| Both together | The union of both reading lists | **53 of 54** |

The methods did not find exactly the same things. Keywords alone found **2** Jev missed; Jev alone found **4** keywords missed; **1** needed a full-call read. So I would keep both reading lists. I published [the measured pattern and its limits](https://github.com/marcodicesare-dev/jev-skill/blob/main/reference/capabilities.md) with the Jev skill.

## How to give Jev a meeting archive

A whole meeting is too much for 1 narrow question. I cut the transcripts into **7,562** overlapping passages. Each held about **6** consecutive utterances, roughly **40 seconds**, and shared **2** utterances with the next passage. The overlap kept a decision from falling between 2 cuts.

Before sending them to an external model, I relabelled speakers as `Founder` and `Other` and scrubbed personal names. The saved input looked like this:

```json
{"id":"call-07#103","passage":"Other: ...\nFounder: I want the next page to show the video library.\nOther: ..."}
```

That line is a **format example**, not a verbatim transcript. The real inputs were scrubbed and remain private.

Jev answered a focused yes/no question about each passage:

```json
{
  "decision_here": {
    "type": "noul",
    "instructions": "Does Founder give an instruction, make a decision, express a preference, or reject a proposal about <the project>?"
  }
}
```

Replace `<the project>` with a short description of your own topic. The [public transcript recipe](https://github.com/marcodicesare-dev/jev-skill/blob/main/recipes/founder-inputs-from-transcripts.json) also asks Jev which part of my directory the passage concerns. Rewrite those options for your work. Do not copy my hotel categories into your product.

## What I read, and what Jev read

Jev evaluated all **7,562** passages. I selected passages scoring at least **0.3**, merged neighboring hits and read the original transcript around them. That gave **544** marked passages, about **7%** of the total. Among passages my first reader had not yet read, Jev's flags led to **10** missed instructions.

The **0.3** line was chosen to catch more possible decisions, even if it meant reading extra passages. It is not a universal “safe” score. On a different archive, I would first mark a few decisions I know are present and check that the chosen line finds them.

There is another detail hidden in the cost claim. Jev still read **all** the short passages. The saving was in **human or agent reading time**: a reader examined the marked sections in full instead of trying to reread every call. The $0.32 was the measured Jev input cost for this run, not a promise that your archive will cost the same.

## Hand this to your agent

The [Jev skill and transcript recipe](https://github.com/marcodicesare-dev/jev-skill) give your agent the question shape and CLI. This is the job I would give it:

> I have an archive of calls, tickets or chats and need to recover decisions on one topic. First identify the speaker or role whose decisions matter. Build overlapping passages of about 6 utterances, with 2 utterances shared between neighbors. Scrub names and secrets before sending anything to Jev. Ask 1 yes/no question per passage about a decision, instruction, preference or rejection on the topic. Keep a low review threshold, then read every flagged passage in its original context. Run keyword search alongside Jev and read the union. Before reporting coverage, check both methods against at least 5 decisions I already know are in the archive. Give me the exact source passage for every recovered instruction. Do not turn a model label into an instruction without reading the passage.

The output I want is a ledger: **decision, exact passage, date, speaker role, current status**. A list of “themes discussed” would not tell my agent what to do next.

## Where this result stops

This was **1 archive about 1 project**. The same first reader who built the reference list of **54** instructions had already used keyword search, so the benchmark is not a clean independent contest. The source also does not establish whether the **10** newly surfaced instructions are included in those **54**. I report them as 2 observations, not as numbers to add together.

Automatic transcripts contain recognition errors. A model can miss a decision because the words were transcribed badly. Jev also missed **2** instructions the keywords found. The combined list found **53 of 54**, and the last one required reading the whole call.

## Why I would save this pattern

The next time an agent tells me “I read the meetings,” I want proof that it found the decisions that matter, with links back to the exact moment they were spoken. On this archive, Jev turned **30,143** utterances into a much smaller reading queue in **108 seconds** for **$0.32**, and that queue surfaced **10** instructions an earlier pass missed.

Start with a question you can recognize in a short passage, keep the original words attached, and test recall against decisions you already know. Jev can help you find where to look. Your agent or a person still has to understand what was decided and whether it is still current.
