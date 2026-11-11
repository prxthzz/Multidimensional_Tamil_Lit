import json


INPUT_FILE = "tests/retrieval_reviewed_results.json"


def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        cases = data["cases"]

    total_results = 0
    direct = 0
    indirect = 0
    irrelevant = 0

    for case in cases:
        query = case["query"]
        results = case["results"]

        print("\n" + "=" * 60)
        print("QUERY:", query)
        print("=" * 60)

        for result in results:
            relevance = result["relevance"]

            if relevance == 2:
                direct += 1
            elif relevance == 1:
                indirect += 1
            elif relevance == 0:
                irrelevant += 1

            total_results += 1

        relevant_or_related = sum(
            1
            for result in results
            if result["relevance"] > 0
        )

        direct_count = sum(
            1
            for result in results
            if result["relevance"] == 2
        )

        print("Directly relevant:", direct_count)
        print("Related:", relevant_or_related)
        print("Not relevant:", len(results) - relevant_or_related)

        print(
            "Reviewed relevance rate:",
            round(relevant_or_related / len(results), 3)
        )

    print("\n" + "=" * 60)
    print("OVERALL REVIEW")
    print("=" * 60)

    print("Total results reviewed:", total_results)
    print("Directly relevant:", direct)
    print("Indirectly relevant:", indirect)
    print("Not relevant:", irrelevant)

    print(
        "Direct relevance rate:",
        round(direct / total_results, 3)
    )

    print(
        "Related-or-direct relevance rate:",
        round((direct + indirect) / total_results, 3)
    )


if __name__ == "__main__":
    main()