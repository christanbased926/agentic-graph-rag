import re
import glob
import os

# Konfiguration
INPUT_DIR = './input_scripts'    # Ordner mit den Arrows.app .cypher Dateien
OUTPUT_FILE = '../99_data.cypher' # Zieldatei

# Regex für Knoten: (alias:Labels {props}) oder (alias)
# Nutzt {[^{}]*} um sicherzustellen, dass wir nur die direkten Properties des Knotens matchen
NODE_REGEX = re.compile(r'\(\s*(?P<alias>[a-zA-Z0-9_]+)?\s*(?P<labels>(?::[a-zA-Z0-9_]+)*)?\s*(?P<props>\{[^{}]*\})?\s*\)')

# Regex für die ..._id Property (z.B. unit_id: "unit-apple-tomato")
ID_PROP_REGEX = re.compile(r'(?P<key>[a-zA-Z0-9_]+_id)\s*:\s*"(?P<val>[^"]+)"')

# Globale States für das Master-File
global_node_registry = {}  # Mappt "unit-apple-tomato" -> "gn1" (Global Alias)
global_node_counter = 1    # AutoIncrement für temp_id
all_processed_paths = []   # Sammelt alle bearbeiteten Pfade aller Dateien

def generate_slug(val):
    """
    Entfernt den semantischen Präfix aus der ID.
    Beispiel: "unit-apple-tomato" -> "apple-tomato"
    """
    parts = val.split('-', 1) # Splittet beim ERSTEN Bindestrich
    if len(parts) > 1:
        slug = re.sub(r"^\d+.*?-(.+)", r"\1", parts[1])
        return slug
    return val

def process_file(filepath, file_index):
    global global_node_counter
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Entferne das initialie "CREATE " von Arrows.app (wir bauen ein eigenes großes am Ende)
    content = re.sub(r'^\s*CREATE\s+', '', content, flags=re.IGNORECASE)

    # Lokales Mapping für diese Datei (z.B. mappt lokales 'n1' auf globales 'gn4')
    local_alias_map = {}

    def node_replacer(match):
        global global_node_counter
        
        alias = match.group('alias')
        labels = match.group('labels') or ''
        props_str = match.group('props')

        if props_str:
            # Suche nach der ..._id Property im Knoten
            id_match = ID_PROP_REGEX.search(props_str)
            if id_match:
                key = id_match.group('key')
                val = id_match.group('val')

                if val not in global_node_registry:
                    # 1. Fall: Knoten ist komplett NEU
                    temp_id = global_node_counter
                    global_node_counter += 1
                    
                    g_alias = f"gn{temp_id}"
                    global_node_registry[val] = g_alias
                    
                    if alias:
                        local_alias_map[alias] = g_alias

                    slug = generate_slug(val)

                    # Ersetze die String-ID durch int und füge den slug hinzu
                    # z.B. unit_id: "unit-apple" => unit_id: 1, slug: "apple"
                    new_props_str = ID_PROP_REGEX.sub(f'{key}: {temp_id}, slug: "{slug}"', props_str)

                    return f"({g_alias}{labels} {new_props_str})"
                else:
                    # 2. Fall: Knoten wurde bereits in einer anderen (oder dieser) Datei definiert
                    g_alias = global_node_registry[val]
                    if alias:
                        local_alias_map[alias] = g_alias
                    
                    # Da er im Master-File schon existiert, referenzieren wir ihn nur noch per Global-Alias.
                    # Cypher wirft sonst einen Fehler, wenn man Properties mehrfach deklariert.
                    return f"({g_alias})"
            else:
                # Knoten hat Properties, aber keine _id. Um Kollisionen zu vermeiden, 
                # namespacen wir den Alias (z.B. n1 -> n1_f0)
                if alias:
                    new_alias = f"{alias}_f{file_index}"
                    local_alias_map[alias] = new_alias
                    return f"({new_alias}{labels} {props_str})"
                return match.group(0)

        else:
            # 3. Fall: Knoten ist nur eine Referenz (z.B. "(n1)")
            if alias and alias in local_alias_map:
                return f"({local_alias_map[alias]})"
            elif alias:
                # Alias referenziert, aber ohne ID (namespace fallback)
                new_alias = f"{alias}_f{file_index}"
                local_alias_map[alias] = new_alias
                return f"({new_alias}{labels})"
            return match.group(0)

    # Wende den Replacer auf alle Knoten im File an
    processed_content = NODE_REGEX.sub(node_replacer, content)
    
    # Füge den verarbeiteten String zur Gesamtliste hinzu
    all_processed_paths.append(processed_content.strip())

def main():
    if not os.path.exists(INPUT_DIR):
        print(f"Create directory '{INPUT_DIR}' - put .cypher files there.")
        os.makedirs(INPUT_DIR)
        return

    cypher_files = glob.glob(os.path.join(INPUT_DIR, '*.cypher'))
    if not cypher_files:
        print(f"No .cypher files found in '{INPUT_DIR}'.")
        return

    print(f"\nFound: {len(cypher_files)} Files. Start Processing...")

    for idx, filepath in enumerate(sorted(cypher_files)):
        print(f"\tProcessing: {filepath}")
        process_file(filepath, idx)

    # Master-Statement zusammenbauen
    # Verbindet alle Paths mit einem Komma für ein einzelnes großes CREATE-Statement
    master_cypher = "CREATE\n" + ",\n".join(all_processed_paths) + ";"

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(master_cypher)

    print(f"Done! Unique Nodes: {global_node_counter - 1}")

if __name__ == "__main__":
    main()