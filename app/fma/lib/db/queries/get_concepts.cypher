MATCH (n:Concept)
RETURN 
  [label IN labels(n) WHERE label <> 'Concept'] AS sublabels,
  n.slug AS slug,
  COALESCE(n.ancestor_slugs, []) AS ancestor_slugs