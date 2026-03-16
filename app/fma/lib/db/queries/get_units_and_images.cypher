MATCH (u:Unit)-[:HAS_COMPOSITION]->(c:Composition)-[:HAS_IMAGE]->(i:Image)
// Wir sortieren die Bilder kurz, um deterministisch immer das gleiche "erste" Bild zu bekommen
WITH u, c, i ORDER BY i.src_url ASC
WITH u, c, collect(i)[0] AS first_image
// Sortierung nach composition.slug (aufsteigend)
ORDER BY c.slug ASC
// Gruppierung der Compositions als Liste von Dictionaries pro Unit
WITH u, collect({slug: c.slug, url: first_image.src_url}) AS compositions
// Abschließende Sortierung nach unit.slug (aufsteigend)
ORDER BY u.slug ASC
RETURN u.unit_id AS unit_id, u.slug AS unit_slug, u.src_url AS src_url, compositions