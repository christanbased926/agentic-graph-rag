from .neo4j import db
from .tools.load_cypher_file import load_cypher_file

import json
from collections import defaultdict

# Rekursive Definition für ein multidimensionales Dictionary
def tree():
    return defaultdict(tree)

def build_and_print_taxonomy(neo4j_data):
    # 1. Baum-Struktur initialisieren
    taxonomy = tree()

    # 2. Flache Daten in den multidimensionalen Baum überführen
    for record in neo4j_data:
        sublabels = record.get("sublabels", [])
        slug = record.get("slug")
        ancestor_slugs = record.get("ancestor_slugs", [])

        top_level = sublabels[0] if sublabels else "Uncategorized"
        current_node = taxonomy[top_level]

        # --- HIER IST DER FIX ---
        # Wir drehen die Liste um, damit wir mit dem höchsten Vorfahren (Root) beginnen 
        # und uns nach unten zum direkten Elternknoten vorarbeiten.
        for ancestor in reversed(ancestor_slugs):
            current_node = current_node[ancestor]

        # Den eigentlichen Slug als Endknoten dieses Pfads einfügen
        current_node = current_node[slug]

    # 3. Rekursive Funktion für die Markdown-Generierung
    def generate_markdown(current_tree, depth=0):
        md_lines = []
        
        # Alphabetisches Sortieren auf der aktuellen Ebene
        for key in sorted(current_tree.keys()):
            # Einrückung berechnen (2 Leerzeichen pro Tiefe)
            indent = "  " * depth
            
            if depth == 0:
                # Top-Level-Einträge bekommen den Prefix ":Concept: "
                md_lines.append(f"{indent}* **:Concept:{key}**")
            else:
                # Alle tieferen Ebenen bekommen nur das Sternchen
                md_lines.append(f"{indent}* {key}")
            
            # Rekursiv die Kinder anhängen
            md_lines.extend(generate_markdown(current_tree[key], depth + 1))
            
        return md_lines

    # 4. Markdown erstellen und ausgeben
    markdown_lines = generate_markdown(taxonomy)
    markdown_lines.insert(0, "Available Concept Nodes and `slug`-properties\n")
    
    return "\n".join(markdown_lines)

async def get_ontology():
    """Reads the ontology of the graph"""
    
    query = load_cypher_file("get_concepts")
    result = await db.run_statement(query)

    return build_and_print_taxonomy(result)