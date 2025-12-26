import json
import os

from openai import OpenAI


def main() -> None:
    json_schema = {
        "name": "task_brief",
        "schema": {
            "type": "object",
            "properties": {
                "summary": {"type": "string"},
                "priority": {"type": "string", "enum": ["low", "medium", "high"]},
            },
            "required": ["summary", "priority"],
            "additionalProperties": False,
        },
        "strict": True,
    }

    payload = {
        "model": "gpt-4.1",
        "input": "Summarize the task 'Finish quarterly report' and set priority.",
        "text": {
            "format": {
                "type": "json_schema",
                "json_schema": json_schema,
            }
        },
    }

    if os.getenv("OPENAI_RUN_LIVE") != "1" or not os.getenv("OPENAI_API_KEY"):
        print("DRY RUN: set OPENAI_API_KEY and OPENAI_RUN_LIVE=1 to execute.")
        print(json.dumps(payload, indent=2))
        return

    client = OpenAI()
    response = client.responses.create(**payload)
    data = json.loads(response.output_text())
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
