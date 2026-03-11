from mcp.server import Server

from .mcp_registry import mcp_manager
from . import tools

mcp_server = Server("graph-rag-server")

# Alle Tools, die in 'app/tools/' definiert wurden, 
# sind jetzt automatisch im mcp_manager bekannt.
mcp_manager.register_to_server(mcp_server)