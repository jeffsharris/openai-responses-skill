# Tools and tool_choice

## tools[] (tool definitions)
Use the `tools` array to grant the model access to built-in tools, MCP
connectors, or your own functions.

### Function tool (custom)
- type: "function"
- name: function name
- description: optional
- parameters: JSON Schema object describing args
- strict: boolean, defaults to true (enforces schema)

### Custom tool
- type: "custom"
- name: tool name
- description: optional
- input_format: format for tool input (defaults to unconstrained text)
  - {type: "text"} for free-form text
  - {type: "grammar", syntax: "lark"|"regex", grammar: "..."} for constrained input

### Web search tool
- type: "web_search" | "web_search_2025_08_26"
- filters.allowed_domains: list of allowed domains (optional)
- user_location: approximate location object
  - type: "approximate"
  - country: ISO 3166-1 code (e.g., "US")
  - region: free text (e.g., "California")
  - city: free text
  - timezone: IANA timezone (e.g., "America/Los_Angeles")
- search_context_size: "low" | "medium" | "high" (default "medium")

### Web search preview tool
- type: "web_search_preview" | "web_search_preview_2025_03_11"
- user_location: approximate location object (same shape as web_search)
- search_context_size: "low" | "medium" | "high" (default "medium")

### File search tool
- type: "file_search"
- vector_store_ids: list of vector store ids (required)
- max_num_results: integer 1–50
- ranking_options:
  - ranker: "default-2024-11-15"
  - score_threshold: number 0–1
  - hybrid_search:
    - embedding_weight: number
    - text_weight: number
- filters: comparison filter
  - operator: eq|ne|gt|gte|lt|lte|in|nin
  - key, value

### Code interpreter tool
- type: "code_interpreter"
- container: container id or {type: "auto", file_ids?, memory_limit?}

### Computer use tool
- type: "computer_use_preview"
- environment: windows | mac | linux | ubuntu | browser
- display_width, display_height: integers

### Image generation tool
- type: "image_generation"
- model: "gpt-image-1" | "gpt-image-1-mini" (default gpt-image-1)
- quality: low | medium | high | auto
- size: 1024x1024 | 1024x1536 | 1536x1024 | auto
- output_format: png | webp | jpeg
- output_compression: integer (default 100)
- moderation: auto | low | medium | high (default auto)
- background: transparent | opaque | auto (default auto)
- input_fidelity: controls prompt fidelity (see image guide)

### MCP tool
- type: "mcp"
- server_label: label used in tool calls
- server_url or connector_id (one required)
  - connector_id values: connector_dropbox, connector_gmail,
    connector_googlecalendar, connector_googledrive, connector_microsoftteams,
    connector_outlookcalendar, connector_outlookemail, connector_sharepoint
- authorization: OAuth access token (optional, required for many connectors)
- server_description: optional
- headers: optional HTTP headers for MCP server
- allowed_tools: list of tool names or filter:
  - tool_names: allowed tool names
  - read_only: filter by read-only hint
- require_approval: always | never | filter object (same shape as allowed_tools)

### Environment-specific tools
- type: "shell", "local_shell", "apply_patch" (available only in supported environments).

## tool_choice
Controls which tool (if any) the model must call.
Options:
- "none" | "auto" | "required"
- {"type": "allowed_tools", "mode": "auto"|"required", "tools": [ ... ]}
- {"type": "function", "name": "get_weather"}
- {"type": "custom", "name": "my_custom_tool"}
- {"type": "mcp", "server_label": "my_server", "name": "tool_name"}
- {"type": "file_search"} | {"type": "web_search_preview"} | {"type": "code_interpreter"}
- {"type": "computer_use_preview"} | {"type": "image_generation"}
- {"type": "apply_patch"} | {"type": "shell"} (where supported)

Related controls:
- parallel_tool_calls: allow tool calls in parallel.
- max_tool_calls: cap total built-in tool calls in a response.

## Tool outputs in responses
- Tool call items appear in response.output with types like function_call,
  file_search_call, web_search_call, code_interpreter_call, mcp_call,
  image_generation_call, custom_tool_call.
- MCP approval flow items appear as mcp_approval_request and mcp_approval_response.
- For function/MCP/custom tools, execute the tool in your code and send a
  corresponding *_call_output input item in a follow-up response (often with
  previous_response_id). Custom tools use custom_tool_call_output.
- Use include[] to request extra tool details:
  web_search_call.action.sources, web_search_call.results,
  code_interpreter_call.outputs, file_search_call.results,
  computer_call_output.output.image_url.
