import os
import requests
import asyncio
from google.adk.agents.llm_agent import Agent
from mcp import ClientSession
from mcp.client.sse import sse_client
#from google.adk.tools.openapi_tool import OpenAPIToolset
#from google.adk.tools.openapi_tool.auth.auth_helpers import token_to_scheme_credential

# 1. Konfiguration des MCP-Servers
# Wichtig: Innerhalb von Docker nutzen wir den Service-Namen 'mcp' aus der docker-compose.yml
MCP_SERVER_URL = "http://idea-agent-mcp:8001/sse"

async def check_mcp_connection(message: str) -> str:
    """
    Ruft das get_status Tool vom MCP-Server auf.
    """
    async with sse_client(MCP_SERVER_URL) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            # Wir rufen das Tool auf dem MCP-Server auf
            result = await session.call_tool("get_status", arguments={"request": message})
            # Wir geben den Textinhalt zurück
            return result.content[0].text

async def query_graph(query: str) -> str:
    """
    Führt eine Cypher-Abfrage in der Neo4j-Datenbank aus.
    Nutze dies, um Daten zu suchen, Knoten zu erstellen oder Beziehungen zu finden.
    """
    async with sse_client(MCP_SERVER_URL) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            # Wir rufen exakt den Namen auf, den wir im mcp_server.py definiert haben
            result = await session.call_tool("query_graph", arguments={"query": query})
            return result.content[0].text

async def get_mcp_tools():
    """
    Diese Funktion verbindet sich mit dem MCP-Server und holt die verfügbaren Tools.
    """
    async with sse_client(MCP_SERVER_URL) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Initialisierung der Verbindung
            await session.initialize()
            # Liste der Tools vom MCP-Server abrufen
            tools = await session.list_tools()
            return tools

# 2. ADK Agent Definition
# Wir erstellen einen Agenten, der später die MCP-Tools nutzen soll.
root_agent = Agent(
    model="gemini-2.5-flash",
    name="Curator",
    description="An Expert Agent for Reasoning based on GraphRAG.",
    instruction=(
        "Du bist ein Agent, der via MCP mit einer Neo4j-Instanz verbunden ist."
    ),
    tools=[check_mcp_connection, query_graph]
)

# 3. ADK App Setup
#app = App(agents=[agent])

# Hier würden wir normalerweise die Tools registrieren.
# Da ADK (Python-Version) oft über Dekoratoren arbeitet, 
# ist der einfachste Weg für einen Test, ein lokales ADK-Tool zu bauen, 
# das als Proxy zum MCP fungiert – oder die MCP-Tools direkt zu mappen.

if __name__ == "__main__":
    # Dieser Teil wird von 'adk web' übernommen, 
    # kann aber für lokales Debugging genutzt werden.
    pass

