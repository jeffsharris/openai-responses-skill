import json
import os

from openai import OpenAI


def main() -> None:
    payload = {
        "model": "gpt-4.1",
        "input": "Explain why the sky appears blue in three short sentences.",
        "reasoning": {"effort": "medium", "summary": "concise"},
        "stream_options": {"include_obfuscation": False},
    }

    if os.getenv("OPENAI_RUN_LIVE") != "1" or not os.getenv("OPENAI_API_KEY"):
        print("DRY RUN: set OPENAI_API_KEY and OPENAI_RUN_LIVE=1 to execute.")
        print(json.dumps(payload, indent=2))
        return

    client = OpenAI()
    summary_started = False
    with client.responses.stream(**payload) as stream:
        for event in stream:
            if event.type == "response.output_text.delta":
                print(event.delta, end="", flush=True)
            elif event.type == "response.reasoning_summary_text.delta":
                if not summary_started:
                    summary_started = True
                    print("\n\n[Reasoning summary]\n", end="")
                print(event.delta, end="", flush=True)
        final = stream.get_final_response()
    print("\n\nResponse id:", final.id)


if __name__ == "__main__":
    main()
