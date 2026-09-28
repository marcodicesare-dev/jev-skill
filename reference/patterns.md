# Building with Jev — patterns that worked, and one that failed

*The chess lesson: Jev cannot "play", but a program that lists the legal moves and asks Jev to pick one each turn plays a whole game (an independent test: 80 games, zero illegal moves, 12 cents). The code drives; Jev chooses the move.*

## Four questions before any design

1. **What is the position?** The text Jev reads at this step (keep it ≤ 32k tokens with the question).
2. **Who produces the legal moves?** Code, a fixed list, a set of records, or a writing model. Jev only chooses among them, so it never invents one.
3. **What are the criteria?** Each criterion is one question. On one text you can ask up to 256.
4. **Who drives?** Always the code: it owns the order of steps, the thresholds and what happens after each answer. Letting Jev pick the next tool in an independent published demo made the agent take 32 % more steps and complete fewer of the required steps (0.984 → 0.921, our recount of its files).

## Patterns

**Switch (routing).** One Choice sends each input to the right path before any slow work starts. Add `none_of_these`. Example: site questions → prepared answers (98.8 %).

**Profile (many questions, one text).** Ask 50–250 questions about one page or document in a single call and store the answers as a record. Example: 150 questions per hotel in 0.7 s. This is how a whole catalogue gets a structured profile for a few dollars.

**Reflex (check after the writer).** The writer produces the whole piece; Jev asks one crisp question per rule or requirement; the code sends back only what fails, saying which rule. Examples: brand rules 22/27, quality grading 30/30. Write rules as questions a stranger could answer from the text alone ("contains a currency symbol instead of an ISO code"), not as moods ("uses the present tense" produced false alarms on 20 of 27 clean ads).

**Filter with a threshold (cascade).** Jev decides the cases where its probability clears a threshold fixed in advance; the rest go to a stronger model or a person. Recalibrate first. In an agent, escalate the doubtful answers together at the end, not step by step (a per-step escalation added latency at almost every step).

**Evidence in the state.** Put what a human would look at into the state (top search results, the page, the record). Keywords: 88 % alone, 99 % with the Google results.

**Guard.** Whenever the state is written by strangers (reviews, emails, pages, comments), add a Noul asking whether it contains instructions for an AI.

**Agent inside code.** Route → extract → route again → extract → score, each step a Jev call over the pages the code fetched. The directory agent ran this way at 1.6 s of decisions per hotel.

**Receipt guard (measured 26 Sep 2026).** When a pipeline extracts a value from a page (a score, a count, an award, an hour), ask Jev whether the page's own text states it: one Choice per value, «supported / contradicted / not addressed», over every chunk of the receipt's markdown. The value enters the record only if some chunk supports it and none contradicts it. It stopped the week's invented facts: a 9.5 extracted from a bot-blocked page of 223 characters, and a MICHELIN score and Keys extracted from a list page that never names the hotel. Both true controls passed. It does not catch loose paraphrase («sopra Barga» against «a Barga»), and it works per value against the receipt that value declares: checking a whole page against every receipt flagged 57 % of the sentences and caught only 2 of 5 known-wrong ones. Recipe: `recipes/claim-vs-source.json` (measured in our lab, September 2026).

**Ledger reader (measured 26 Sep 2026).** To find what a person asked for across long transcripts, cut them into overlapping windows of about six utterances, relabel speakers (Founder / Other), scrub names, and ask one Noul («does the Founder give an instruction, decision, preference or rejection about X?») plus a Choice for the area. Then read in full only the flagged windows. On 14 calls it found 51 of 54 known inputs against 49 for keyword search, while reading half as many windows, and reading its flags turned up 10 inputs the first reading had missed. Recipe: `recipes/founder-inputs-from-transcripts.json`.

**Speculative questions (TypeSafe's fan-out).** When a follow-up matters only for some answers ("if the guest asks about the spa, which treatment?"), ask it in the first call with its premise written into the question, and let the code use it only when the premise holds. Make a second call only when an earlier answer is needed to fetch evidence, build a new state or set the next options. Extra questions do not change the other answers (tested 28 Sep 2026), so the only price is their tokens.

**Compose in code, keep the raw answers.** Average weighted Scores only for qualities that can make up for each other. A rule such as "any serious violation blocks" needs one Noul per violation and an any-rule in code, as the receipt guard does. Store every raw answer: a new weight, threshold or filter then needs no new call (TypeSafe's skill).

**When the situation changes.** Keep what Jev inferred apart from what was observed, and ask again before acting on a situation that has changed (TypeSafe's skill; not tested by us).

**When Jev does not answer.** Write the fallback in code before the first call: a short timeout and a retry (the gateway stalls 8–35 s at times; `tools/jev.py` retries), then a behaviour chosen by what is at stake. A publishing gate stops and tells a person; a ranking or a filter falls back to the old order. Never leave the choice to an agent: one independent builder's agent, whose Jev checker stopped answering, decided silence was safer and stopped sending anything until a second agent unstuck it (X, 18 Sep 2026; reported, not measured). TypeSafe's status page showed downtime on 17, 20, 21, 23 and 24 Sep 2026.

## The pattern that failed: the eyes

Letting Jev choose what the author reads (sources, facts, photos) before the author writes. It saves money on the writer's input and makes the writing worse (13–3 against the full context). Jev can check the author's output and pick among closed options the author does not own (a destination page among real ones, a library photo), but it must not narrow the author's context.

## A worked example: the content engine

- Author (a frontier model) writes the whole asset with creative direction: unchanged.
- Reflexes after writing: brand rules as crisp Nouls, a quality grade (flat or broken drafts go back), destination URL checked against the hotel's real pages, injection guard on any third-party text.
- Not Jev: the brief-coverage report (fast alternatives wrote worse reports), long holistic reviews, choosing among good versions.
- A slow reasoning model making a closed decision elsewhere (the strategy-concept critique) was better replaced by a fast writing model with reasoning off than kept: always measure both.

## How to test a new use (do this before claiming anything)

0. **Start from the job of the product the step serves, and from why that product exists, not from an idea about using Jev.** Write the job in one sentence before designing anything, and check that the test's inputs are the inputs of that job. The opponent is the alternative people really have today, never a weak version we chose. A gap found in the market is a question, not a confirmation: find out why it exists before building on it (the `causal-research` skill). *What it cost, 26 Sep 2026:* a page-composition test on one hotel used only the hotel's own site pages and beat its generic homepage 38 of 40; but the directory it was meant to inform exists to tell a hotel with every voice (official pages, reviews, social, YouTube, blogs, how the reader wants to feel), and the real opponent was the section page Google already sends searchers to. A reviewer had to point it out.
1. Build a set with a **known answer and real contrast**: good, medium, bad, broken; clean and violated. A test on good items only cannot show that Jev "can't" judge.
2. Run the current step and Jev on the same items; for disagreements use a blind judge (both orders) or people.
3. Report quality, time and cost together, with a confidence interval (a bootstrap over the items is enough).
4. Adopt only if quality rises at equal cost and time, or cost and time fall at equal quality, and never at the expense of the writer's context.
5. For every failure, keep the state, the questions and the answers, and file it as **missing evidence** (the state lacked what a person would need), **model error**, **code error** (wrong option set, composition or threshold) or **service failure** (TypeSafe's skill). Only model errors count against Jev; the other three are ours to fix.
