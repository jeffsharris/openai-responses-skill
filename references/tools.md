# Tools and tool_choice

## Tools array (tools[])
Built-in tools and custom tools can be passed in the `tools` array.

Built-in tools (selected fields):
- function: {type: "function", name, description?, parameters, strict}
- web_search / web_search_2025_08_26: filters.allowed_domains, user_location, search_context_size
- web_search_preview / web_search_preview_2025_03_11: user_location, search_context_size
- file_search: vector_store_ids (required), max_num_results, ranking_options, filters
- code_interpreter: container (id or {type: "auto", file_ids?, memory_limit?})
- computer_use_preview: environment, display_width, display_height
- image_generation: model, quality, size, output_format, output_compression, moderation
- mcp: server_label, server_url or connector_id, authorization
- local_shell: {type: "local_shell"}
- shell: {type: "shell"}
- apply_patch: {type: "apply_patch"}
- custom: {type: "custom", name, description?, format}

Notes:
- For function tools, parameters is a JSON Schema object; strict defaults to true.
- For code_interpreter, use container {"type": "auto"} unless you have a container id.
- For web_search, use include[] to request sources or results.

## tool_choice
Options:
- "none" | "auto" | "required"
- {"type": "allowed_tools", "mode": "auto"|"required", "tools": [ ... ]}
- {"type": "function", "name": "get_weather"}
- {"type": "mcp", "server_label": "my_server", "name": "tool_name"}
- {"type": "custom", "name": "my_tool"}
- {"type": "file_search" | "web_search_preview" | "web_search_preview_2025_03_11" | "computer_use_preview" | "image_generation" | "code_interpreter"}
- {"type": "apply_patch"}
- {"type": "shell"}

Related controls:
- parallel_tool_calls: allow tool calls in parallel.
- max_tool_calls: cap total built-in tool calls in a response.

## Tool outputs in responses
- Tool call items appear in response.output with types like function_call, file_search_call, web_search_call, code_interpreter_call, mcp_call, image_generation_call, etc.
- For function/custom tools, execute the tool in your code and send a function_call_output/custom_tool_call_output input item in a follow-up response (often with previous_response_id).
- Use include[] to request extra tool details: web_search_call.action.sources, web_search_call.results, code_interpreter_call.outputs, file_search_call.results, computer_call_output.output.image_url.
