#!/usr/bin/env python3
"""jev — call Jev (TypeSafe System One) from any agent session without writing a harness.

  jev.py ask     --state '{"text":"..."}' | state.json   --questions '{...}' | questions.json   [--via llmapi|openrouter|typesafe]
  jev.py batch   --states items.jsonl --questions questions.json --out answers.jsonl [--state-field text] [--workers 20] [--via ...]
                 one state per input line; resumable (ids already in --out are skipped); prints cost and speed at the end
  jev.py credits                                  LLM API balance

Routes (keys come from the environment):
  llmapi      (default) https://api.llmapi.ai/v1/systemone, model jev-latest
  openrouter  https://openrouter.ai/api/v1/systemone, model typesafe/jev-1.13
  typesafe    official https://api.typesafe.ai/v1/systemone, model jev-latest; requires a TypeSafe API key

Question shapes (Choice / Score / Noul), limits and errors: reference/api.md. Every call's answering version is in `model`.
"""
import argparse, concurrent.futures as cf, json, os, pathlib, sys, time

ROUTES = {
    "llmapi": ("LLMAPI_API_KEY", "https://api.llmapi.ai/v1/systemone", "jev-latest"),
    "openrouter": ("OPENROUTER_API_KEY", "https://openrouter.ai/api/v1/systemone", "typesafe/jev-1.13"),
    "typesafe": ("TYPESAFE_API_KEY", "https://api.typesafe.ai/v1/systemone", "jev-latest"),
}

def _direct(state, qs, via):
    """Standard-library call to Jev, retried on 429, 5xx and timeouts → (status, data, latency_s, cost_usd)."""
    import random, urllib.request, urllib.error
    var, url, model = ROUTES[via]
    key = os.environ.get(var) or sys.exit(f"jev: set {var} in the environment first (export {var}=...)")
    body = json.dumps({"model": model, "state": state, "questions": qs}).encode()
    for attempt in range(8):
        req = urllib.request.Request(url, body, {"Authorization": f"Bearer {key}", "Content-Type": "application/json", "User-Agent": "jev-cli/1"})
        t0 = time.perf_counter()
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                status, data = r.status, json.loads(r.read())
        except urllib.error.HTTPError as e:
            status, data = e.code, {"error": e.read().decode(errors="replace")[:500]}
        except Exception as e:
            status, data = -1, {"error": repr(e)[:200]}
        lat = time.perf_counter() - t0
        if status not in (429, 500, 502, 503, 504, 529, -1): break
        time.sleep(min(20, 2 ** attempt + random.random()))
    u = (data or {}).get("usage") or {}
    return status, data, lat, u.get("cost") if u.get("cost") is not None else (u.get("input_tokens") or 0) * 0.042e-6

def call(state, questions, via="llmapi", exp=None, tag=None):
    """Call Jev and return (HTTP status, response, latency seconds, estimated USD cost).

    ``exp`` and ``tag`` are accepted for compatibility with earlier versions of
    this CLI. They are not sent to the provider or logged by this public client.
    """
    if via not in ROUTES:
        raise ValueError(f"Unknown Jev route: {via}")
    return _direct(state, questions, via)

def load_json(arg):
    try:
        p = pathlib.Path(arg); is_file = p.exists()
    except OSError:             # inline JSON longer than a file name (macOS, Python < 3.13)
        is_file = False
    return json.loads(p.read_text()) if is_file else json.loads(arg)

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("ask"); a.add_argument("--state", required=True); a.add_argument("--questions", required=True)
    a.add_argument("--via", choices=list(ROUTES), default="llmapi")
    b = sub.add_parser("batch"); b.add_argument("--states", required=True); b.add_argument("--questions", required=True); b.add_argument("--out", required=True)
    b.add_argument("--state-field", default=None, help="use only this field of each line as the state (default: the whole line minus `id`)")
    b.add_argument("--workers", type=int, default=16); b.add_argument("--via", choices=list(ROUTES), default="llmapi")
    sub.add_parser("credits")
    args = ap.parse_args()
    if args.cmd == "credits":
        import urllib.request
        key = os.environ.get("LLMAPI_API_KEY") or sys.exit("jev: set LLMAPI_API_KEY before checking credits")
        req = urllib.request.Request("https://api.llmapi.ai/v1/credits", headers={"Authorization": f"Bearer {key}", "User-Agent": "jev-cli/1"})
        print(json.dumps(json.loads(urllib.request.urlopen(req, timeout=30).read()), indent=1)); return
    qs = load_json(args.questions)
    via = args.via
    if args.cmd == "ask":
        status, data, lat, cost = _direct(load_json(args.state), qs, via)
        print(json.dumps({"status": status, "via": via, "latency_s": round(lat, 3), "cost_usd": cost, **(data or {})}, indent=1, ensure_ascii=False))
        sys.exit(0 if status == 200 else 1)
    out = pathlib.Path(args.out); done = set()
    if out.exists():
        done = {json.loads(l)["id"] for l in out.read_text().split("\n") if l.strip()}
    items = []
    for i, line in enumerate(pathlib.Path(args.states).read_text().split("\n")):
        if not line.strip(): continue
        item = json.loads(line); iid = item.get("id", i)
        if iid in done: continue
        items.append((iid, item[args.state_field] if args.state_field else {k: v for k, v in item.items() if k != "id"}))
    t0 = time.time(); n = 0; failures = 0; cost = 0.0; lats = []
    def one(x):
        iid, state = x
        return iid, _direct(state, qs, via)
    with cf.ThreadPoolExecutor(max(1, args.workers)) as ex:
        for iid, (status, data, lat, c) in ex.map(one, items):
            if status != 200:
                print(f"ERR {iid} {status} {str(data)[:200]}", file=sys.stderr); failures += 1; continue
            with open(out, "a") as f:
                f.write(json.dumps({"id": iid, "via": via, "model": (data or {}).get("model"), "answers": data["answers"], "usage": (data or {}).get("usage")}, ensure_ascii=False) + "\n")
            n += 1; cost += c or 0; lats.append(lat)
    lats.sort()
    print(f"wrote {n} new lines to {out} · {failures} failed · {time.time() - t0:.1f} s wall · median call {lats[len(lats) // 2] if lats else 0:.2f} s · ${cost:.5f}", file=sys.stderr)
    if failures:
        sys.exit(1)

if __name__ == "__main__":
    main()
