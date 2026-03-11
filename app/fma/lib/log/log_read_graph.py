import datetime
import os

# Pfad zur Log-Datei (im Docker-Container)
LOG_FILE_PATH = "/logs/mcp_read_graph.log"

def log_read_graph(status: str, query: str):
    """Schreibt einen Eintrag in das Log-File."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d,%H:%M:%S")
    
    # Cypher-Statement säubern: Zeilenumbrüche und Tabs durch Leerzeichen ersetzen
    clean_query = query.replace("\n", " ").replace("\r", " ").replace("\t", " ").strip()
    
    # Tab-getrennte Zeile zusammenbauen
    log_line = f"{timestamp}\t{status}\n{clean_query}\n\n"
    
    # Datei im Append-Modus öffnen und schreiben
    with open(LOG_FILE_PATH, "a", encoding="utf-8") as f:
        f.write(log_line)