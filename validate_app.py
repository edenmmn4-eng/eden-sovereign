# -*- coding: utf-8 -*-
"""
validate_app.py - Regression checks before commit
Run: python validate_app.py
"""
import ast, sys, re, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ERRORS = []
WARNINGS = []

src = open("app.py", encoding="utf-8").read()
lines = src.splitlines()

def err(msg, line=None):
    loc = f" (שורה {line})" if line else ""
    ERRORS.append(f"❌  {msg}{loc}")

def warn(msg, line=None):
    loc = f" (שורה {line})" if line else ""
    WARNINGS.append(f"⚠️  {msg}{loc}")

# ── 1. Syntax check ──────────────────────────────────────────────────────────
try:
    ast.parse(src)
except SyntaxError as e:
    err(f"Syntax error: {e}")

# ── 2. Horizon values ────────────────────────────────────────────────────────
VALID_HORIZONS = {"30D Tactical", "1Y Strategic"}
for i, line in enumerate(lines, 1):
    m = re.search(r'find_best_pick\(["\']([^"\']+)["\']', line)
    if m and m.group(1) not in VALID_HORIZONS:
        err(f"horizon לא תקין '{m.group(1)}' ב-find_best_pick() — חייב להיות אחד מ: {VALID_HORIZONS}", i)
    m2 = re.search(r'compute_score\([^,]+,[^,]+,["\']([^"\']+)["\']', line)
    if m2 and m2.group(1) not in VALID_HORIZONS:
        err(f"horizon לא תקין '{m2.group(1)}' ב-compute_score() — חייב להיות אחד מ: {VALID_HORIZONS}", i)

# ── 3. fetch_data TTL ────────────────────────────────────────────────────────
m = re.search(r'@st\.cache_data\(ttl=(\d+)[^)]*\)\s*\ndef fetch_data', src)
if m:
    ttl = int(m.group(1))
    if ttl < 600:
        err(f"fetch_data() TTL={ttl}s — חייב להיות ≥600 שניות (מניעת rate-limit)")

m2 = re.search(r'@st\.cache_data\(ttl=(\d+)[^)]*\)\s*\ndef fetch_portfolio_prices', src)
if m2:
    ttl2 = int(m2.group(1))
    if ttl2 < 300:
        warn(f"fetch_portfolio_prices() TTL={ttl2}s — מומלץ ≥300 שניות")

# ── 4. find_best_pick בתוך background thread ────────────────────────────────
bg_start = src.find("def _bg_worker")
bg_end   = src.find("\ndef ", bg_start + 1)
bg_body  = src[bg_start:bg_end] if bg_start != -1 else ""
if "find_best_pick" in bg_body:
    err("find_best_pick() נמצא בתוך _bg_worker — אסור! גורם ל-rate limit")
if "fetch_data(" in bg_body:
    err("fetch_data() נמצא בתוך _bg_worker — אסור! גורם ל-rate limit")

# ── 5. inject_css נקראת עם פרמטרים ─────────────────────────────────────────
for i, line in enumerate(lines, 1):
    if re.search(r'inject_css\(.+\)', line):
        err(f"inject_css() נקראת עם פרמטרים — הפונקציה לא מקבלת פרמטרים", i)

# ── 6. TICKER_LIST loop בתוך background thread ──────────────────────────────
if "TICKER_LIST" in bg_body:
    err("TICKER_LIST בתוך _bg_worker — אסור! גורם ל-rate limit על כל המניות")

# ── 7. sleep בין בקשות ב-background thread ──────────────────────────────────
if bg_body and "fast_info" in bg_body and "sleep" not in bg_body:
    warn("_bg_worker מבצע fast_info ללא sleep בין בקשות — מומלץ להוסיף time.sleep(0.3)")

# ── 8. בדוק ש-_bg_worker קיים ───────────────────────────────────────────────
if "_bg_worker" not in src:
    warn("_bg_worker לא נמצא — הסוכן הרקע לא מוגדר")

# ── תוצאות ──────────────────────────────────────────────────────────────────
print("\n" + "="*55)
print("  Eden Sovereign — Regression Validator")
print("="*55)

if WARNINGS:
    for w in WARNINGS:
        print(w)

if ERRORS:
    for e in ERRORS:
        print(e)
    print(f"\n✖  נמצאו {len(ERRORS)} שגיאות קריטיות — אין לבצע commit!")
    sys.exit(1)
else:
    print(f"✅  הכל תקין — {len(WARNINGS)} אזהרות, 0 שגיאות קריטיות")
    sys.exit(0)
