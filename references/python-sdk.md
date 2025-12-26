# Python SDK usage

## Setup
```python
from openai import OpenAI

client = OpenAI()  # uses OPENAI_API_KEY
```

## Core methods
- client.responses.create(...)
- client.responses.stream(...)
- client.responses.retrieve(response_id, include=[...])
- client.responses.cancel(response_id)
- client.responses.delete(response_id)
- client.responses.input_items.list(response_id, limit=20, order="desc", after=None)
- client.responses.input_tokens.count(model=..., input=...)
- client.responses.compact(model=..., input=..., previous_response_id=...)

## Response helpers
- response.output_text(): aggregate output_text blocks into a single string.
- response.output: list of items (messages, tool calls, tool outputs, reasoning items).

## Structured outputs
Use text.format.json_schema to force structured JSON:
```python
response = client.responses.create(
    model="gpt-4.1",
    input="Return a summary and score.",
    text={
        "format": {
            "type": "json_schema",
            "json_schema": {
                "name": "summary_score",
                "schema": {
                    "type": "object",
                    "properties": {
                        "summary": {"type": "string"},
                        "score": {"type": "number"}
                    },
                    "required": ["summary", "score"],
                    "additionalProperties": False
                },
                "strict": True
            }
        }
    },
)
data = response.output_text()
```

## Runnable examples
Scripts in `scripts/` are one-shot examples and default to dry-run. Set `OPENAI_API_KEY` and `OPENAI_RUN_LIVE=1` to run live calls.
