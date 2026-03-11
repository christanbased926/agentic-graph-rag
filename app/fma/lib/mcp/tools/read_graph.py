from ..mcp_registry import mcp_manager
from ...db.neo4j import run_query
from ...log.log_read_graph import log_read_graph

@mcp_manager.tool(
    name="read_graph",
    description="Führt eine beliebige Cypher-Abfrage gegen die Neo4j-Datenbank aus. "
                "Nutze dies für komplexe Graph-Analysen oder spezifische Suchen."
                "Beachte, dass der Graph read-only ist.",
    schema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string", 
                "description": "Das vollständige Cypher-Statement (z.B. MATCH (n) RETURN n LIMIT 5)"
            }
        },
        "required": ["query"]
    }
)
async def read_graph(args):
    query = args.get("query")
    
    try:
        result = await run_query(query)
        
        if not result:
            log_read_graph(f"SUCCESS: 0 Results", query)
            return "Abfrage erfolgreich, aber keine Ergebnisse gefunden."

        length = len(result)
        log_read_graph(f"SUCCESS: {length} Results", query)
            
        return str(result)
        
    except Exception as e:
        log_read_graph(f"ERROR: {type(e).__name__}", query)
        return f"Datenbank-Fehler: {str(e)}"