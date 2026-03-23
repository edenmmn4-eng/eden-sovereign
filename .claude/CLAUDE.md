Project Context:
You are working on the Sovereign Intelligence Terminal (v2026), an institutional-grade equity research and quantitative scoring platform. Always maintain this context during development.

Development Rules:

Universal Validation Rule: Whenever a bug or an issue is identified for a specific stock/ticker (e.g., "The logo doesn't load for AAPL"), you must automatically verify if the same issue exists for all other tickers in the system and apply a global fix. Do not wait for a separate instruction for each ticker.

Regression Prevention (Non-Destructive Editing): When implementing improvements, new features, or code refactoring, you are strictly forbidden from altering or removing existing features that are already functional unless explicitly instructed. Always perform a "Impact Analysis" before changing shared functions.

Language Consistency: All user-facing communications, comments in the UI, and responses to the developer must be in Hebrew.

Mathematical Integrity: Maintain the high-precision logic of the Quantum Scoring Engine and the Monte Carlo simulations as the core of the project.

---

## Critical Technical Rules (learned from real bugs)

### Yahoo Finance Rate Limiting
- NEVER call `fetch_data()` or `find_best_pick()` from background threads or scheduled tasks.
  These functions scan 100+ tickers and will trigger Yahoo Finance rate limits (HTTP 429).
- Background threads may ONLY fetch `yf.Ticker(t).fast_info.last_price` for a small list of tickers (price alerts only), with `time.sleep(0.3)` between each request.
- `fetch_data()` cache TTL must stay at ≥600 seconds. Do NOT lower it.
- `fetch_portfolio_prices()` cache TTL must stay at ≥600 seconds. Do NOT lower it.

### Horizon Strings
- The ONLY valid horizon values are exactly: `"30D Tactical"` and `"1Y Strategic"`.
- NEVER pass any other string (e.g., "6M", "1Y", "short") to `compute_score()` or `find_best_pick()`.
  Passing an invalid horizon silently falls into the wrong scoring branch and produces inflated/wrong scores.

### Function Signature Changes
- Before removing a parameter from any function, grep ALL call sites in app.py.
- Before renaming a variable, verify it is not used further down in the same function.
- `inject_css()` — no parameters. Do not re-add auth params.

### Background Thread Rules
- The background thread (`_bg_worker`) must only do lightweight work: fetching prices for a small set of tickers.
- Do NOT add full-market scans, news fetching, or any operation that loops over TICKER_LIST to the background thread.
- The thread sleeps 3600 seconds between runs. Do NOT reduce this interval.

### Pre-Commit Checklist
Before every commit to app.py, run: `python validate_app.py`
This script checks for the most common regression patterns.