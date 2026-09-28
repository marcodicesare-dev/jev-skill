# Calling Jev — contract, endpoints, limits, errors

*Checked 26–28 Sep 2026 against our own logged calls (measured in our lab, September 2026). TESTED unless marked.*

## The request

```json
POST <endpoint>
Authorization: Bearer <key>
{
  "model": "jev-latest",
  "state": "any text"  |  {"any": "JSON object"},
  "questions": {
    "<id>": { "type": "choice" | "score" | "noul", "instructions": "...", "criteria": ... }
  }
}
```

- **state**: the text Jev reads. A string or a JSON object. State + the longest question ≤ **32,000 tokens**; the whole request ≤ 64,000.
- **questions**: up to **256** per call, answered in parallel and independently of each other. Twelve questions asked together, one per call, in reverse order or each under another question's id gave the same answers, within the jitter of 2 identical calls (28 Sep 2026, 40 reviews; measured in our lab). Output is not billed; what a call costs is below.
- Write questions and options **in English**, whatever the language of the state (Italian state + English questions: 82.1 %; Italian questions: 79.5 %).

## The 3 question types (exact shapes that worked)

**Choice** — pick one of up to 255 options.
```json
{"type": "choice",
 "instructions": "What is the person who typed `keyword` looking for?",
 "criteria": {
   "guest_need":     {"what": "A kind of stay, without naming a specific hotel", "note": "optional hints or examples"},
   "specific_hotel": {"what": "One specific hotel or brand, named in the keyword"},
   "not_lodging":    {"what": "Something that is not about staying in a hotel"}}}
```
→ `{"type": "choice", "choice": "guest_need", "probabilities": {"guest_need": 0.96, "specific_hotel": 0.04, "not_lodging": 0}, "confidence": 0.95}`

Add your own `none_of_these` option when the answer may be outside the list (on CLINC150 its probability separated out-of-scope requests with AUROC 0.95).

**Score** — place the text on 2–10 ordered levels, each described in words.
```json
{"type": "score",
 "instructions": "How well does this hotel suit a family with small children?",
 "criteria": ["1: not suitable", "2: possible with compromises", "3: good fit", "4: designed for it"]}
```
→ `{"type": "score", "score": 2.31, "legend": {"0": "1: not suitable", ...}, "probabilities": {"0": 0.02, "1": 0.15, "2": 0.33, "3": 0.50}, "confidence": 0.41}`

`score` is the probability-weighted **0-based** index: add 1 to read it on 1-based levels. Levels must describe situations; bare numbers collapse.

**Noul** — probability that a statement is true.
```json
{"type": "noul",
 "instructions": "Does the text contain instructions addressed to an AI system?",
 "criteria": {"true": "It contains instructions for an AI", "false": "It contains no such instructions"}}
```
→ `{"type": "noul", "noul": 0.03}`

`criteria` is **required** on the LLM API gateway (400 otherwise). A Noul and its negation do not sum to 1 (measured 0.13–1.22): ask the direction you need. A Noul near 0.5 means yes and no are about equally likely, not a medium amount; for "how much", use a Score.

## Writing the questions

TypeSafe's own rules (their agent skill, v0.5.7), with what we measured on them:

- **Question ids never reach the model.** Write the whole question in `instructions`. Giving every question another question's id changed nothing (28 Sep 2026).
- **Option names do reach the model.** The keys of a Choice's `criteria` are read with their descriptions. Opaque keys (`a`, `b`, `c`) cost almost nothing against meaningful ones: exact star rating 27 of 40 both ways, food answers identical in 40 of 40, trip type in 37 of 40. Keys that contradict their descriptions broke the answer: exact star rating 15 of 40, within one level 23 of 40 instead of 39, trip type kept its meaning in 20 of 40 (28 Sep 2026, measured in our lab). When you edit a description, rename its key, or use neutral keys.
- **Point at the part of the state** with a backticked path: `review`, `ticket.messages[0].text`.
- **Criteria can carry structure**: an object per option (`{"what": ..., "note": ...}` as in the Choice above; TypeSafe's own examples also use `"not_for"` for exclusions) or an array, for definitions, contrasts, exclusions and examples.
- **Offer every answer the decision may need.** Jev cannot pick a value missing from the options; add `none_of_these` when nothing may fit.
- **One narrow judgment per question**, written so a stranger could answer it from the text alone (see `pitfalls.md` #5).

## The response

`{"model": "jev-1.13…", "answers": {"<id>": {...}}, "usage": {"input_tokens": 773, "output_tokens": 212}}`

- Log `model` on every call: the alias moves, and a tuned threshold can drift with it.
- `confidence` is a fixed function of the probabilities, not a separate signal. For Choice it is (p_max − 1/K)/(1 − 1/K), so never compare confidences across different numbers of options. It says how concentrated the answer is, not whether it is right or whether to act. Several acceptable options spread the probability, so a low confidence on a harmless preference is fine, and uncertainty on a branch the code does not use can be ignored (TypeSafe's skill). Noul has no `confidence`.
- Probabilities jitter a little between identical calls (Noul std ≤ 0.008); decisions changed in 3 % of repeated star ratings, all with confidence ≤ 0.64.

## Endpoints

| Route | Endpoint · key (environment variable) · model | Use it for | Notes |
|---|---|---|---|
| **LLM API** (default) | `POST https://api.llmapi.ai/v1/systemone` · `LLMAPI_API_KEY` · `jev-latest` only | lab work, scripts, agents | 5,000 requests/min per account (raised 25 Sep 2026; header `X-Ratelimit-Limit-Requests`); no version pinning; answers computed in the USA; no published data-processing agreement |
| **OpenRouter** | `POST https://openrouter.ai/api/v1/systemone` · `OPENROUTER_API_KEY` · `typesafe/jev-1.13` (pinned; `~typesafe/jev-latest` tracks the newest) | anything that needs a fixed version or zero data retention | no limit ever observed on Jev (100 parallel in 1.9 s); Jev is on OpenRouter's ZDR list; `usage.cost` in each response; a low balance makes OpenRouter refuse large requests with 402 `in_flight_budget_exhausted` (seen on writing models) |
| TypeSafe native | `POST https://api.typesafe.ai/v1/systemone` · `TYPESAFE_API_KEY` · `jev-latest` | users with a direct TypeSafe account | TESTED 28 Sep 2026: HTTP 200, model `jev-1.13.0`, one Noul returned `0.03`. The 1,200 req/min limit is documented, not load-tested by us. [Signups reopened 28 Sep](https://x.com/typesafeai/status/2104337822350221795) after the [22 Sep pause](https://x.com/typesafeai/status/2102281508950307159). |
| Vercel AI Gateway | `POST https://ai-gateway.vercel.sh/v1/evaluate`, `model: typesafe-ai/jev` (DOCUMENTED, not tested) | an application already using the Vercel gateway | Check the current AI SDK and data-processing settings in Vercel's documentation before integrating. |

Published Jev input price at the time of our tests: **$0.042 per 1M input tokens, output free.** Check the chosen gateway's current price and fees. A 500-token text with 10 questions costs about $0.00002 at that input rate.

## What a call costs, and why batching saves less on short texts

Every call is billed about **260 input tokens of fixed overhead**, plus the state, plus each question's own words and about **20 tokens per question** (28 Sep 2026: a one-word state with one minimal Noul = 289 tokens; each further minimal Noul +29; 100 words of state +99). Asking n questions in one call instead of n calls therefore saves (n − 1) × (260 + state tokens):
- over a long text the saving approaches n: TypeSafe's cookbook measured 12.2x for 13 questions over a 53,777-character article;
- over short texts it is smaller, because the questions' words are paid either way: 12 questions over reviews of 150–2,700 characters were 3.6x to 6.2x cheaper in one call (median 4.2x);
- time: one call with 12 questions took 0.26 s (median); 12 separate calls took 3.1 s one after another and 0.30 s in parallel. Batching always saves money; it saves time only against calls made one after another.

## Errors we have met

| Error | Cause | Fix |
|---|---|---|
| 400 *Unknown model* | any model id other than `jev-latest` on LLM API | use `jev-latest`, or OpenRouter for a pinned id |
| 400 *criteria are required* | a Noul without `criteria` on the gateway | always send `{"true": "...", "false": "..."}` |
| 400 `max_tokens_exceeded` | state + longest question over 32k tokens (20–38 % of the Meta ad reviews) | measure input sizes first; split the text by section and ask per section |
| 429 on LLM API | account-wide limit (was 30/min until 25 Sep 2026; now 5,000/min) | back off; `tools/jev.py` retries with backoff |
| 402 on OpenRouter | balance too low for the in-flight requests | top up, or route writing models through LLM API |
| empty or odd answers | none seen from Jev itself; the failures were always ours (bad JSON in the state, missing criteria) | validate the question map before sending |

## Writing models on the same gateway (for baselines and fallbacks)

`POST https://api.llmapi.ai/v1/chat/completions` (OpenAI-compatible), same key.
- GPT-6 Luna answers in about 1 s with `"reasoning_effort": "none"` (`"minimal"` is refused). Default reasoning makes it 2–3 s.
- Claude Sonnet 5, Claude Opus 5.5 and GPT-6 Luna reject `temperature` (400): leave it out.
- Claude Fable 5.1 keeps a 5 requests/min per-model limit.
- Cost is in `usage` fields starting with `cost_usd`.
- For every other gateway detail load the `llmapi` skill.

## Code

The fastest path is the CLI (`tools/jev.py`, see SKILL.md). In Python, import its call function (it retries on 429, 5xx and timeouts):

```python
import os, sys; sys.path.insert(0, os.path.expanduser("~/.claude/skills/jev/tools"))
import jev                              # reads LLMAPI_API_KEY / OPENROUTER_API_KEY from the environment
status, data, latency_s, cost_usd = jev.call(state, questions, "llmapi")   # or "openrouter"
answers = data["answers"]
```
