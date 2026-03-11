import mcp.types as types
from mcp.server import Server

class McpToolManager:
    def __init__(self):
        self.tools = {}
        self.prompts = {}

    def tool(self, name: str, description: str, schema: dict):
        def decorator(func):
            self.tools[name] = {"func": func, "description": description, "schema": schema}
            return func
        return decorator

    def prompt(self, name: str, description: str):
        """Decorator für MCP Prompts."""
        def decorator(func):
            self.prompts[name] = {"func": func, "description": description}
            return func
        return decorator

    def register_to_server(self, server: Server):
        @server.list_tools()
        async def handle_list_tools():
            return [types.Tool(name=n, description=t["description"], inputSchema=t["schema"]) 
                    for n, t in self.tools.items()]

        @server.call_tool()
        async def handle_call_tool(name: str, arguments: dict | None):
            if name not in self.tools: raise ValueError(f"Tool {name} unknown")
            result = await self.tools[name]["func"](arguments or {})
            return [types.TextContent(type="text", text=str(result))]

        @server.list_prompts()
        async def handle_list_prompts():
            return [
                types.Prompt(name=n, description=p["description"])
                for n, p in self.prompts.items()
            ]

        @server.get_prompt()
        async def handle_get_prompt(name: str, arguments: dict | None):
            if name not in self.prompts:
                raise ValueError(f"Prompt {name} nicht gefunden")
            
            # Hier rufen wir die Prompt-Funktion auf
            content = await self.prompts[name]["func"](arguments or {})
            return types.GetPromptResult(
                description=self.prompts[name]["description"],
                messages=[
                    types.PromptMessage(
                        role="user",
                        content=types.TextContent(type="text", text=content)
                    )
                ]
            )

# Die zentrale Instanz
mcp_manager = McpToolManager()