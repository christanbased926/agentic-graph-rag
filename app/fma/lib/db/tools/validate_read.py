def is_read_only(statement: str) -> bool:
    """
    Prüft, ob die Query potenziell gefährlich ist.
    In einem kuratierten Axiom-Graphen erlauben wir NUR das Suchen.
    """
    cmd = statement.strip().upper()
    
    # Erlaubte Start-Keywords für reines Lesen
    allowed_starts = ("MATCH", "WITH", "RETURN", "UNWIND", "OPTIONAL")
    
    # Verbotene Keywords irgendwo in der Query (um Schreib-Subqueries zu verhindern)
    forbidden = ["CREATE", "MERGE", "SET", "DELETE", "REMOVE", "DROP", "DETACH", "CALL"]
    
    if not cmd.startswith(allowed_starts):
        return False
    
    if any(word in cmd for word in forbidden):
        return False
        
    return True