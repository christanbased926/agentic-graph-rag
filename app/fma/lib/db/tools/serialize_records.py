from neo4j.graph import Node, Relationship

async def serialize_records(value):
    """Intelligente Konvertierung von Neo4j-Objekten in Python-Dicts."""
    
    if isinstance(value, Node):
        # Wir holen die Properties als Basis
        props = dict(value)
        
        # Wenn keine Properties da sind ODER wir im GraphRAG-Modus 
        # immer den Typ wissen wollen:
        if not props:
            return {
                "_type": "Node",
                "_labels": list(value.labels),
                "_id": value.element_id,
                "_note": "Node has no further properties"
            }
        
        # "Intelligenter" Mix: Wir geben die Props zurück, 
        # hängen aber die Labels als Metadaten an, falls sie wichtig sind
        return {
            "_labels": list(value.labels),
            **props
        }

    if isinstance(value, Relationship):
        props = dict(value)
        return {
            "_rel_type": value.type,
            "_start_node": value.start_node.element_id,
            "_end_node": value.end_node.element_id,
            **props
        }

    if isinstance(value, list):
        return [await serialize_records(v) for v in value]
    
    if isinstance(value, dict):
        return {k: await serialize_records(v) for k, v in value.items()}

    return value