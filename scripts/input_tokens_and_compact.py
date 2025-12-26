import argparse
import json
import os

from openai import OpenAI


def main() -> None:
    parser = argparse.ArgumentParser(description="Responses API utilities")
    parser.add_argument("mode", choices=["count", "compact"], help="Operation to run")
    args = parser.parse_args()

    if args.mode == "count":
        payload = {
            "model": "gpt-4.1",
            "input": "Count tokens for this short prompt.",
        }

        if os.getenv("OPENAI_RUN_LIVE") != "1" or not os.getenv("OPENAI_API_KEY"):
            print("DRY RUN: set OPENAI_API_KEY and OPENAI_RUN_LIVE=1 to execute.")
            print(json.dumps(payload, indent=2))
            return

        client = OpenAI()
        result = client.responses.input_tokens.count(**payload)
        print(result.input_tokens)
        return

    payload = {
        "model": "gpt-4.1",
        "input": [
            {
                "role": "user",
                "content": "Summarize the last meeting in one sentence.",
            },
            {
                "id": "msg_example",
                "type": "message",
                "status": "completed",
                "role": "assistant",
                "content": [
                    {
                        "type": "output_text",
                        "text": "We discussed timelines, risks, and owners.",
                    }
                ],
            },
        ],
    }

    if os.getenv("OPENAI_RUN_LIVE") != "1" or not os.getenv("OPENAI_API_KEY"):
        print("DRY RUN: set OPENAI_API_KEY and OPENAI_RUN_LIVE=1 to execute.")
        print(json.dumps(payload, indent=2))
        return

    client = OpenAI()
    result = client.responses.compact(**payload)
    print(result.id)


if __name__ == "__main__":
    main()
