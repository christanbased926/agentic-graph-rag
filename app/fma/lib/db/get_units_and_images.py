from .neo4j import db
from .tools.load_cypher_file import load_cypher_file

async def get_units_and_images():
    """Sucht alle Units and their images."""
    
    query = load_cypher_file("get_units_and_images")
    print(query)
    result = await db.run_statement(query)

    return result