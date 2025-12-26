import json
import os

from openai import OpenAI


def main() -> None:
    payload = {
        "model": "gpt-4.1",
        "input": "Summarize the Apollo program in two sentences.",
    }

    if os.getenv("OPENAI_RUN_LIVE") != "1" or not os.getenv("OPENAI_API_KEY"):
        print("DRY RUN: set OPENAI_API_KEY and OPENAI_RUN_LIVE=1 to execute.")
        print(json.dumps(payload, indent=2))
        return

    client = OpenAI()
    response = client.responses.create(**payload)
    print(response.output_text())


if __name__ == "__main__":
    main()
