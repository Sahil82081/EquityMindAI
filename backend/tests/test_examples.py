import urllib.request
import urllib.parse
import json


def test_prompt_examples():
    examples = ["Apple", "AAPL", "Microsft", "Nvidia", "Tesla"]
    print("=== Testing Prompt Specified Examples ===")

    for q in examples:
        url = f"http://127.0.0.1:8000/api/v1/company/search?q={urllib.parse.quote(q)}"
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        match = data.get("match")
        assert match is not None, f"Expected match for query '{q}', got None"
        print(f"\nQuery: '{q}' -> Resolved Normalized Company:")
        print(
            json.dumps(
                {
                    "name": match["name"],
                    "ticker": match["ticker"],
                    "exchange": match["exchange"],
                    "market": match["market"],
                },
                indent=2,
            )
        )
        print(f"Fuzzy: {data['fuzzy']}, Ambiguous: {data['ambiguous']}, Count: {data['count']}")

    print("\nAll prompt examples resolved successfully!")


if __name__ == "__main__":
    test_prompt_examples()
