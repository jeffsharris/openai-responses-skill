# OpenAI Responses API (condensed)

## Endpoints
- POST /v1/responses: create a response.
- GET /v1/responses/{response_id}: retrieve a response (optionally stream).
- DELETE /v1/responses/{response_id}: delete a stored response.
- POST /v1/responses/{response_id}/cancel: cancel a response (background).
- GET /v1/responses/{response_id}/input_items: list input items for a response.
- POST /v1/responses/input_tokens: count input tokens for a request body.
- POST /v1/responses/compact: compact a conversation into an encrypted summary.

## Create response parameters (key fields)
Required:
- model: Responses model id.
- input: string or array of input items.

Common optional fields:
- instructions: system/developer message for this response.
- reasoning: {effort, summary}. Effort values: none, minimal, low, medium, high, xhigh. Summary values: auto, concise, detailed.
- text: {format, verbosity}. format: text | json_schema | json_object. verbosity: low | medium | high.
- tools: array of tool definitions (see tools.md).
- tool_choice: none | auto | required, or a specific tool choice (see tools.md).
- max_output_tokens: cap on visible + reasoning tokens.
- max_tool_calls: cap on total built-in tool calls.
- stream: true to stream SSE events.
- stream_options: {include_obfuscation}.
- include: additional fields to include in the response.
- previous_response_id OR conversation (id or {id}); do not use both.
- prompt: {id, version?, variables?} to use a stored prompt template.
- background: run response in background.
- truncation: auto | disabled (default).
- store: store the response for later retrieval.
- parallel_tool_calls: allow tool calls in parallel.
- temperature, top_p, top_logprobs.
- safety_identifier, prompt_cache_key, prompt_cache_retention.
- metadata: user-defined object.

## Input shapes
- string: treated as a user text message.
- array of items: messages or tool outputs. Example user message with text + image:
```json
{
  "role": "user",
  "content": [
    {"type": "input_text", "text": "What is in this image?"},
    {"type": "input_image", "image_url": "https://example.com/image.jpg"}
  ]
}
```

## Response object (high level)
- id, object, created_at, status (completed, in_progress, failed, incomplete)
- output: list of items (assistant message, tool calls, tool outputs, reasoning items)
- usage: input/output/total tokens and reasoning token counts
- reasoning, tool_choice, tools, text, truncation, store, parallel_tool_calls, metadata

## include values
- file_search_call.results
- web_search_call.results
- web_search_call.action.sources
- code_interpreter_call.outputs
- computer_call_output.output.image_url
- message.input_image.image_url
- message.output_text.logprobs
- reasoning.encrypted_content

## Conversation state notes
- Use previous_response_id to continue a thread statelessly.
- Use conversation (id or {id}) for server-side state; do not use with previous_response_id.
- For stateless usage or zero data retention, set store=false and include reasoning.encrypted_content if you need to carry reasoning items.

## Token counting and compaction
- /responses/input_tokens: estimate input tokens for a model + input.
- /responses/compact: compact long conversations into encrypted content for reuse later.
