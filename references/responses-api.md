# OpenAI Responses API (reference summary)

## Overview
The Responses API is the primary interface for generating text or structured
JSON outputs from text, image, or file inputs. It supports conversation state,
reasoning configuration, tool calls, and streaming via SSE.

## Endpoints
- POST /v1/responses: create a response.
- GET /v1/responses/{response_id}: retrieve a response (optionally stream).
- POST /v1/responses/{response_id}/cancel: cancel a response (background).
- DELETE /v1/responses/{response_id}: delete a stored response.
- GET /v1/responses/{response_id}/input_items: list input items for a response.
- POST /v1/responses/input_tokens: count input tokens for a request body.
- POST /v1/responses/compact: compact a conversation into an encrypted summary.

## Create response request body
Required:
- model: model ID used to generate the response.
- input: string or array of input items. (If using prompt templates, include
  prompt + variables and provide input as required by that template.)

Optional (grouped):
- prompt: {id, version?, variables?}
  - id: prompt template id.
  - version: optional prompt template version.
  - variables: map of substitution values (strings or input item shapes like
    images/files). See reusable prompts in the text guide.
- instructions: system/developer message inserted into the model context.
  - When used with previous_response_id, instructions are not carried over.
- reasoning: {effort, summary}
  - effort: none|minimal|low|medium|high|xhigh (model-specific defaults).
    - gpt-5.1 defaults to none (supports none/low/medium/high).
    - models before gpt-5.1 default to medium and do not support none.
    - gpt-5-pro defaults to and only supports high.
    - xhigh supported after gpt-5.1-codex-max.
  - summary: auto|concise|detailed.
    - concise supported for computer-use-preview and reasoning models after gpt-5.
  - generate_summary: deprecated alias for summary.
- text: {format, verbosity}
  - format.type: text | json_schema | json_object
  - json_schema format fields:
    - name: required; must match [A-Za-z0-9_-], max length 64.
    - description: optional; describes the response format for the model.
    - schema: required JSON Schema object.
    - strict: boolean; if true, model must match schema exactly. Only a subset
      of JSON Schema is supported in strict mode.
    - Practical guardrail: with strict=true, include every property key in
      required and use nullable types for optional fields to avoid API
      validation errors.
  - json_object: legacy JSON mode (not recommended for gpt-4o and newer).
  - verbosity: low | medium | high.
- tools: array of tool definitions (see tools.md).
- tool_choice: none | auto | required, or a specific tool choice object.
- parallel_tool_calls: allow the model to run tool calls in parallel.
- max_tool_calls: max total built-in tool calls for the response.
- max_output_tokens: upper bound on visible + reasoning tokens.
- stream: true to stream SSE events.
- stream_options.include_obfuscation:
  - default true; adds obfuscation to delta events to normalize payload sizes.
  - set false to reduce overhead if you trust the network link.
- include: additional output data to include (see include values below).
- store: store response for later retrieval (default true).
- background: run the response in the background (default false).
- truncation: auto | disabled (default).
  - auto: if input exceeds context, truncate oldest items to fit.
  - disabled: request fails with 400 if input exceeds context.
- previous_response_id: continue a stateless thread (cannot use with conversation).
- conversation: conversation id/object; conversation items are prepended to input.
  Output items are added to the conversation after response completes.
- metadata: up to 16 key-value pairs; keys max 64 chars, values max 512 chars.
- temperature, top_p: sampling controls (do not tune both).
- top_logprobs: 0–20, number of most likely tokens to return with logprobs.
- safety_identifier: stable identifier for safety monitoring.
- prompt_cache_key: cache bucketing key (replaces deprecated user).
- prompt_cache_retention: in-memory | 24h.
- user: deprecated; use safety_identifier and prompt_cache_key.
- service_tier: auto | default | flex | scale | priority; response returns actual service tier used.

## Input shapes
- String: treated as a user text input.
- Array of input items:
  - Message items: {role, content} where role is user|assistant|system|developer.
  - Content parts include input_text, input_image, input_file (and model outputs).
  - Images: {type: "input_image", image_url: "...", detail?} (data URL or https).
  - Files: {type: "input_file", file_url|file_data, filename?}.
  - Tool outputs: function_call_output or built-in tool call outputs.
- Conversation state: use previous_response_id or conversation for multi-turn.

Example input (text + image):
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
- id, status (completed, in_progress, failed, incomplete)
- output: list of items (messages, tool calls, tool outputs, reasoning items)
- usage: input/output/total tokens and reasoning token counts
- fields echoed from request: reasoning, tool_choice, tools, text, truncation,
  store, parallel_tool_calls, metadata
- SDK convenience: response.output_text (aggregated output_text content, SDK-only).

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
- Use previous_response_id for stateless threading.
- Use conversation for server-side state; do not combine with previous_response_id.
- For zero data retention, set store=false and include reasoning.encrypted_content
  if you must carry reasoning items forward.

## Token counting and compaction
- /responses/input_tokens: estimate input tokens for a model + input.
- /responses/compact: compact long conversations into encrypted content.
