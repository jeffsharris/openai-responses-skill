# Streaming responses

## How to stream
- Set stream: true in responses.create.
- Or use client.responses.stream(...) for a higher-level streaming interface.
- Resume a response: GET /v1/responses/{response_id}?stream=true&starting_after=N.

## Stream options
- stream_options.include_obfuscation (default true) adds an obfuscation field
  to delta events to normalize payload sizes. Set false if you trust your
  network path and want lower overhead.

## Event families (non-exhaustive)
Lifecycle:
- response.created, response.in_progress, response.completed
- response.failed, response.incomplete, response.error

Output deltas:
- response.output_item.added, response.output_item.done
- response.content_part.added, response.content_part.done
- response.output_text.delta, response.output_text.done
- response.output_text.annotation.added
- response.refusal.delta, response.refusal.done
- response.reasoning_summary_part.added, response.reasoning_summary_part.done
- response.reasoning_summary_text.delta, response.reasoning_summary_text.done
- response.reasoning_text.delta, response.reasoning_text.done

Tool call streams:
- response.function_call_arguments.delta, response.function_call_arguments.done
- response.custom_tool_call_input.delta, response.custom_tool_call_input.done
- response.mcp_call_arguments.delta, response.mcp_call_arguments.done
- response.code_interpreter_call.*
- response.web_search_call.*
- response.file_search_call.*
- response.image_generation_call.*
- response.mcp_call.* and response.mcp_list_tools.*

Audio streams (when using audio outputs):
- response.audio.* and response.audio_transcript.*

Treat unknown events as forward-compatible and handle by logging or ignoring.

## Python streaming pattern
```python
from openai import OpenAI

client = OpenAI()

with client.responses.stream(
    model="gpt-4.1",
    input="Explain blue light in one paragraph.",
    reasoning={"summary": "concise"},
) as stream:
    for event in stream:
        if event.type == "response.output_text.delta":
            print(event.delta, end="", flush=True)
        elif event.type == "response.reasoning_summary_text.delta":
            print("\\n[Reasoning summary]", event.delta, end="", flush=True)
    final = stream.get_final_response()
    print("\\nResponse id:", final.id)
```
