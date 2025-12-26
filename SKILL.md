---
name: openai-responses-api
description: Build or update Python integrations that call the OpenAI Responses API, including create/stream/retrieve/cancel/delete, input_items, input_tokens counting, response compaction, tool use (web search, code interpreter, file search, function, MCP, image generation, computer use), reasoning controls, and structured outputs.
---

# OpenAI Responses API

## Overview
Use this skill to implement or review Python code that calls the OpenAI Responses API with full feature coverage and correct request/response handling.

## Quick start
- Read `references/responses-api.md` for endpoint coverage and parameter semantics.
- Read `references/tools.md` for tool definitions and tool_choice rules.
- Read `references/streaming.md` for streaming event handling and reasoning summaries.
- Read `references/python-sdk.md` for SDK method usage and patterns.
- Run scripts in `scripts/` for one-shot examples. They default to dry-run; set `OPENAI_API_KEY` and `OPENAI_RUN_LIVE=1` to execute live calls.

## Core workflow
1. Choose the endpoint and model, then build the request payload with `input`, `instructions`, `reasoning`, `text`, and optional `tools` and `tool_choice`.
2. If tools are used, inspect `response.output` for tool call items and send tool outputs back as new input items (usually with `previous_response_id`).
3. If streaming, handle SSE events and assemble the final response using the SDK stream manager.
4. For long-running threads, use `previous_response_id` or `conversation` plus optional compaction when needed.

## Resources
- `references/responses-api.md`
- `references/tools.md`
- `references/streaming.md`
- `references/python-sdk.md`
- `scripts/` runnable examples
