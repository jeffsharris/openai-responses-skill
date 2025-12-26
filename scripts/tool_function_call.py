import json
import os

from openai import OpenAI


def get_weather(location: str, unit: str = "c") -> dict:
    return {
        "location": location,
        "unit": unit,
        "temperature": 18.5,
        "forecast": "Partly cloudy",
    }


def main() -> None:
    tool_def = {
        "type": "function",
        "name": "get_weather",
        "description": "Get current weather for a location.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string"},
                "unit": {"type": "string", "enum": ["c", "f"]},
            },
            "required": ["location"],
            "additionalProperties": False,
        },
        "strict": True,
    }

    first_payload = {
        "model": "gpt-4.1",
        "input": "What is the weather in Boston? Use get_weather.",
        "tools": [tool_def],
        "tool_choice": {"type": "function", "name": "get_weather"},
    }

    if os.getenv("OPENAI_RUN_LIVE") != "1" or not os.getenv("OPENAI_API_KEY"):
        second_payload = {
            "model": "gpt-4.1",
            "previous_response_id": "<RESPONSE_ID>",
            "input": [
                {
                    "type": "function_call_output",
                    "call_id": "<CALL_ID>",
                    "output": json.dumps(get_weather("Boston", "c")),
                }
            ],
        }
        print("DRY RUN: set OPENAI_API_KEY and OPENAI_RUN_LIVE=1 to execute.")
        print(json.dumps(first_payload, indent=2))
        print(json.dumps(second_payload, indent=2))
        return

    client = OpenAI()
    first = client.responses.create(**first_payload)

    call_item = next(item for item in first.output if item.type == "function_call")
    args = json.loads(call_item.arguments)
    tool_output = get_weather(**args)

    second = client.responses.create(
        model=first_payload["model"],
        previous_response_id=first.id,
        input=[
            {
                "type": "function_call_output",
                "call_id": call_item.call_id,
                "output": json.dumps(tool_output),
            }
        ],
    )
    print(second.output_text())


if __name__ == "__main__":
    main()
