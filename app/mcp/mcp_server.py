import os
import asyncio
from mcp.server import Server
import mcp.types as types
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.responses import Response
import uvicorn
from neo4j import GraphDatabase

# 1. MCP Server Setup
# --- 1. Neo4j Konfiguration & Driver ---
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

# Hier wird der Driver global definiert
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

app = Server("test-mcp-server")

@app.list_tools()
async def handle_list_tools():
    return [
        types.Tool(
            name="get_status",
            description="Prüft die Verbindung zwischen ADK und MCP Server.",
            inputSchema={
                "type": "object",
                "properties": {"request": {"type": "string"}},
            },
        ),
        types.Tool(
            name="query_graph",
            description="Führt eine Cypher-Abfrage in der Neo4j-Datenbank aus.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Die Cypher-Abfrage"}
                },
                "required": ["query"]
            },
        )
    ]

def is_read_only(cypher: str) -> bool:
    """
    Prüft, ob die Query potenziell gefährlich ist.
    In einem kuratierten Axiom-Graphen erlauben wir NUR das Suchen.
    """
    cmd = cypher.strip().upper()
    
    # Erlaubte Start-Keywords für reines Lesen
    allowed_starts = ("MATCH", "WITH", "RETURN", "UNWIND", "OPTIONAL")
    
    # Verbotene Keywords irgendwo in der Query (um Schreib-Subqueries zu verhindern)
    forbidden = ["CREATE", "MERGE", "SET", "DELETE", "REMOVE", "DROP", "DETACH", "CALL"]
    
    if not cmd.startswith(allowed_starts):
        return False
    
    if any(word in cmd for word in forbidden):
        return False
        
    return True

@app.call_tool()
async def handle_call_tool(name: str, arguments: dict | None):
    if name == "get_status":
        user_input = arguments.get("request", "keine Eingabe")
        return [types.TextContent(type="text", text=f"MCP Echo: {user_input}")]
        pass
    
    if name == "query_graph":
        cypher = arguments.get("query", "")
    
        if not is_read_only(cypher):
            return [types.TextContent(
                type="text", 
                text="Validation Error: This Graph is read-only."
            )]

        try:
            with driver.session() as session:
                result = session.run(cypher)
                data = [record.data() for record in result]
                return [types.TextContent(type="text", text=f"Ergebnis: {data}")]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Fehler: {str(e)}")]
            
    raise ValueError(f"Tool nicht gefunden: {name}")

# 2. SSE Transport Setup
# Wir nutzen "/messages" als Pfad für POST-Requests
sse = SseServerTransport("/messages")

# 3. ASGI Handler (Die Brücke zwischen Starlette und MCP)
async def handle_sse(scope, receive, send):
    """Behandelt den GET /sse Stream"""
    async with sse.connect_sse(scope, receive, send) as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

async def handle_messages(scope, receive, send):
    """Behandelt die POST /messages Aufrufe"""
    await sse.handle_post_message(scope, receive, send)

# 4. Die Starlette App ohne Umwege
async def starlette_app(scope, receive, send):
    """
    Ein einfacher ASGI-Router, der die 'NoneType' Fehler umgeht.
    """
    path = scope.get("path")
    if path == "/sse":
        await handle_sse(scope, receive, send)
    elif path == "/messages":
        await handle_messages(scope, receive, send)
    else:
        # 404 für alles andere
        response = Response("Not Found", status_code=404)
        await response(scope, receive, send)

if __name__ == "__main__":
    uvicorn.run(starlette_app, host="0.0.0.0", port=8001)