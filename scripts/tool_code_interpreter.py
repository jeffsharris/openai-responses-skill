import json
import os

from openai import OpenAI


def main() -> None:
    payload = {
        "model": "gpt-4.1",
        "input": "Compute the mean and standard deviation of [2, 4, 6, 8, 10].",
        "tools": [
            {
                "type": "code_interpreter",
                "container": {"type": "auto"},
            }
        ],
        "include": ["code_interpreter_call.outputs"],
    }

    if os.getenv("OPENAI_RUN_LIVE") != "1" or not os.getenv("OPENAI_API_KEY"):
        print("DRY RUN: set OPENAI_API_KEY and OPENAI_RUN_LIVE=1 to execute.")
        print(json.dumps(payload, indent=2))
        return

    client = OpenAI()
    response = client.responses.create(**payload)
    print(response.output_text())

    for item in response.output:
        if item.type != "message":
            print(json.dumps(item.model_dump(), indent=2))


if __name__ == "__main__":
    main()
