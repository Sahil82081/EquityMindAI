import urllib.request
import urllib.parse
import json
import sys


def search(q: str):
    url = f"http://127.0.0.1:8000/api/v1/company/search?q={urllib.parse.quote(q)}"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def run_tests():
    all_passed = True
    print("=" * 60)
    print("EQUITYMIND AI - COMPANY RESOLUTION VALIDATION SUITE")
    print("=" * 60)

    # 1. Exact Ticker
    res1 = search("AAPL")
    p1 = res1.get("match") is not None and res1["match"]["ticker"] == "AAPL"
    all_passed = all_passed and p1
    print("\n[TEST 1: Exact Ticker - 'AAPL']")
    print(f"Status: {'PASSED' if p1 else 'FAILED'}")
    print("Normalized Company:")
    print(json.dumps(res1["match"], indent=2))
    print(f"Fuzzy: {res1['fuzzy']} | Ambiguous: {res1['ambiguous']} | Count: {res1['count']}")

    # 2. Exact Company
    res2 = search("Tesla, Inc.")
    p2 = res2.get("match") is not None and res2["match"]["ticker"] == "TSLA"
    all_passed = all_passed and p2
    print("\n[TEST 2: Exact Company - 'Tesla, Inc.']")
    print(f"Status: {'PASSED' if p2 else 'FAILED'}")
    print("Normalized Company:")
    print(json.dumps(res2["match"], indent=2))
    print(f"Fuzzy: {res2['fuzzy']} | Ambiguous: {res2['ambiguous']} | Count: {res2['count']}")

    # 3. Partial Name
    res3 = search("Nvid")
    p3 = res3.get("match") is not None and res3["match"]["ticker"] == "NVDA"
    all_passed = all_passed and p3
    print("\n[TEST 3: Partial Name - 'Nvid']")
    print(f"Status: {'PASSED' if p3 else 'FAILED'}")
    print("Normalized Company:")
    print(json.dumps(res3["match"], indent=2))
    print(f"Fuzzy: {res3['fuzzy']} | Count: {res3['count']}")

    # 4. Typo / Minor Spelling Mistake
    res4 = search("Microsft")
    p4 = (
        res4.get("match") is not None
        and res4["match"]["ticker"] == "MSFT"
        and res4.get("fuzzy") is True
    )
    all_passed = all_passed and p4
    print("\n[TEST 4: Typo / Spelling Mistake - 'Microsft']")
    print(f"Status: {'PASSED' if p4 else 'FAILED'}")
    print("Normalized Company:")
    print(json.dumps(res4["match"], indent=2))
    print(f"Fuzzy: {res4['fuzzy']} | Count: {res4['count']}")

    # 5. No Result
    res5 = search("xyz123nonexistent")
    p5 = res5.get("count") == 0 and res5.get("match") is None
    all_passed = all_passed and p5
    print("\n[TEST 5: No Result - 'xyz123nonexistent']")
    print(f"Status: {'PASSED' if p5 else 'FAILED'}")
    print(f"Results Count: {res5['count']} | Match: {res5['match']}")

    # 6. Ambiguous Result
    res6 = search("Apple")
    p6 = res6.get("ambiguous") is True and res6.get("count") > 1
    all_passed = all_passed and p6
    print("\n[TEST 6: Ambiguous Result - 'Apple']")
    print(f"Status: {'PASSED' if p6 else 'FAILED'}")
    print(f"Ambiguous: {res6['ambiguous']} | Matches Found: {res6['count']}")
    for idx, c in enumerate(res6["results"], 1):
        print(f"  {idx}. {c['name']} ({c['ticker']}) - {c['exchange']} [{c['market']}]")

    print("\n" + "=" * 60)
    if all_passed:
        print("ALL 6 TESTS PASSED SUCCESSFULLY!")
    else:
        print("SOME TESTS FAILED!")
    print("=" * 60)
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    run_tests()
