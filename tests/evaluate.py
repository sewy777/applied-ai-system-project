"""
Test harness for the Music Recommender Simulation.

Runs a fixed set of test cases and prints a pass/fail summary
with scores and confidence ratings.

Run with:
    python -m tests.evaluate
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.recommender import load_songs, recommend_songs, validate_user_prefs

SONGS = load_songs("data/songs.csv")

TEST_CASES = [
    {
        "name": "Pop/happy profile returns a pop song first",
        "prefs": {"genre": "pop", "mood": "happy", "energy": 0.85},
        "check": lambda results: results[0][0]["genre"] == "pop",
    },
    {
        "name": "Lofi/chill profile returns a lofi song first",
        "prefs": {"genre": "lofi", "mood": "chill", "energy": 0.38},
        "check": lambda results: results[0][0]["genre"] == "lofi",
    },
    {
        "name": "Rock/intense profile returns a rock song first",
        "prefs": {"genre": "rock", "mood": "intense", "energy": 0.92},
        "check": lambda results: results[0][0]["genre"] == "rock",
    },
    {
        "name": "Results are sorted highest score first",
        "prefs": {"genre": "pop", "mood": "happy", "energy": 0.8},
        "check": lambda results: all(
            results[i][1] >= results[i + 1][1] for i in range(len(results) - 1)
        ),
    },
    {
        "name": "Top result has confidence above 50%",
        "prefs": {"genre": "lofi", "mood": "chill", "energy": 0.4},
        "check": lambda results: results[0][3] > 50.0,
    },
    {
        "name": "Returns exactly 5 results by default",
        "prefs": {"genre": "rock", "mood": "intense", "energy": 0.9},
        "check": lambda results: len(results) == 5,
    },
    {
        "name": "Invalid energy raises ValueError (guardrail check)",
        "prefs": {"genre": "pop", "mood": "happy", "energy": 1.5},
        "check": "expect_error",
    },
    {
        "name": "Missing genre raises ValueError (guardrail check)",
        "prefs": {"genre": "", "mood": "happy", "energy": 0.8},
        "check": "expect_error",
    },
]


def run_harness():
    passed = 0
    failed = 0

    print("\n" + "=" * 55)
    print("  MUSIC RECOMMENDER — EVALUATION HARNESS")
    print("=" * 55)

    for i, case in enumerate(TEST_CASES, 1):
        name = case["name"]
        prefs = case["prefs"]
        check = case["check"]

        try:
            if check == "expect_error":
                # These cases should raise a ValueError
                try:
                    validate_user_prefs(prefs)
                    print(f"[FAIL] {i}. {name}")
                    print(f"       Expected a ValueError but none was raised.")
                    failed += 1
                except ValueError:
                    print(f"[PASS] {i}. {name}")
                    passed += 1
            else:
                results = recommend_songs(prefs, SONGS, k=5)
                if check(results):
                    top = results[0]
                    print(f"[PASS] {i}. {name}")
                    print(f"       Top: '{top[0]['title']}' | Score: {top[1]:.2f} | Confidence: {top[3]:.1f}%")
                    passed += 1
                else:
                    top = results[0]
                    print(f"[FAIL] {i}. {name}")
                    print(f"       Top: '{top[0]['title']}' | Score: {top[1]:.2f} | Confidence: {top[3]:.1f}%")
                    failed += 1

        except Exception as e:
            print(f"[FAIL] {i}. {name}")
            print(f"       Error: {e}")
            failed += 1

    total = passed + failed
    avg_conf = 0.0
    try:
        normal_cases = [c for c in TEST_CASES if c["check"] != "expect_error"]
        confs = []
        for case in normal_cases:
            try:
                results = recommend_songs(case["prefs"], SONGS, k=5)
                confs.append(results[0][3])
            except Exception:
                pass
        if confs:
            avg_conf = sum(confs) / len(confs)
    except Exception:
        pass

    print("\n" + "-" * 55)
    print(f"  Results : {passed}/{total} tests passed")
    print(f"  Avg top-result confidence : {avg_conf:.1f}%")
    print("-" * 55 + "\n")


if __name__ == "__main__":
    run_harness()
