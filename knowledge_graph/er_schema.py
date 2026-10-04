"""
Entity-Relationship schema utilities for the Knowledge Graph.
"""

__all__ = ['export_er_diagram', 'export_er_summary', 'validate_graph_against_schema']

from .ontology import ENTITY_TYPES, RELATIONSHIP_TYPES


def export_er_diagram():
    """
    Generates a Mermaid ER diagram string from the ontology schema.
    
    Returns:
        str: Mermaid erDiagram syntax string.
    """
    lines = ["erDiagram"]
    
    # Add relationships
    for rel_type, (source, target) in RELATIONSHIP_TYPES.items():
        if target == 'str':
            target = "StringValue"
            
        # Mermaid syntax: Source ||--o{ Target : label
        lines.append(f"    {source} ||--o{{ {target} : {rel_type}")
        
    lines.append("")
    
    # Add entities and their attributes
    for entity, fields in ENTITY_TYPES.items():
        lines.append(f"    {entity} {{")
        
        required = fields.get('required', [])
        optional = fields.get('optional', [])
        
        for field in required:
            # Determine if it's a primary/foreign key by name conventions
            if field == 'id':
                lines.append(f"        string {field} PK")
            elif field.endswith('_id'):
                lines.append(f"        string {field} FK")
            else:
                lines.append(f"        string {field} PK")
                
        for field in optional:
            if field.endswith('_id'):
                lines.append(f"        string {field} FK")
            else:
                lines.append(f"        string {field}")
                
        lines.append("    }")
        lines.append("")
        
    return "\n".join(lines)


def export_er_summary():
    """
    Returns a summary of the ER schema.
    
    Returns:
        dict: Schema summary including entity types, relationship types, and counts.
    """
    entity_types_list = []
    for name, fields in ENTITY_TYPES.items():
        entity_types_list.append({
            "name": name,
            "required_fields": fields.get('required', []),
            "optional_fields": fields.get('optional', [])
        })
        
    relationship_types_list = []
    for name, (source, target) in RELATIONSHIP_TYPES.items():
        relationship_types_list.append({
            "name": name,
            "source": source,
            "target": target
        })
        
    return {
        "entity_types": entity_types_list,
        "relationship_types": relationship_types_list,
        "total_entities": len(ENTITY_TYPES),
        "total_relationships": len(RELATIONSHIP_TYPES)
    }


def validate_graph_against_schema(graph):
    """
    Validates a NetworkX DiGraph against the ontology schema.
    
    Args:
        graph (networkx.DiGraph): The graph to validate.
        
    Returns:
        dict: Validation results including valid (bool), errors, warnings, and stats.
    """
    errors = []
    warnings = []
    
    entity_counts = {}
    rel_counts = {}
    
    # Validate nodes
    for node, data in graph.nodes(data=True):
        node_type = data.get('node_type')
        if not node_type:
            errors.append(f"Node '{node}' is missing 'node_type' attribute.")
            continue
            
        if node_type not in ENTITY_TYPES:
            errors.append(f"Node '{node}' has unknown node_type: '{node_type}'.")
            continue
            
        entity_counts[node_type] = entity_counts.get(node_type, 0) + 1
        
        # Check required fields
        required_fields = ENTITY_TYPES[node_type].get('required', [])
        missing_fields = [f for f in required_fields if f not in data]
        if missing_fields:
            errors.append(f"Node '{node}' ({node_type}) is missing required fields: {', '.join(missing_fields)}")
            
        # Optional fields check as warnings
        optional_fields = ENTITY_TYPES[node_type].get('optional', [])
        # We ignore common NetworkX or internal attributes like 'node_type' and 'label'
        extra_fields = [
            k for k in data.keys() 
            if k not in required_fields and k not in optional_fields and k not in ('node_type', 'label')
        ]
        if extra_fields:
            warnings.append(f"Node '{node}' ({node_type}) has unexpected fields: {', '.join(extra_fields)}")

    # Validate edges
    for u, v, data in graph.edges(data=True):
        rel = data.get('relationship')
        if not rel:
            errors.append(f"Edge from '{u}' to '{v}' is missing 'relationship' attribute.")
            continue
            
        if rel not in RELATIONSHIP_TYPES:
            errors.append(f"Edge from '{u}' to '{v}' has unknown relationship: '{rel}'.")
            continue
            
        rel_counts[rel] = rel_counts.get(rel, 0) + 1
        
        # Check source and target types
        u_type = graph.nodes[u].get('node_type') if u in graph else None
        v_type = graph.nodes[v].get('node_type') if v in graph else None
        
        expected_source, expected_target = RELATIONSHIP_TYPES[rel]
        
        if u_type and u_type != expected_source:
            errors.append(f"Edge '{rel}' from '{u}' to '{v}' has invalid source type. Expected '{expected_source}', got '{u_type}'.")
            
        if v_type and expected_target != 'str' and v_type != expected_target:
            errors.append(f"Edge '{rel}' from '{u}' to '{v}' has invalid target type. Expected '{expected_target}', got '{v_type}'.")

    stats = {
        "node_count": graph.number_of_nodes(),
        "edge_count": graph.number_of_edges(),
        "entity_type_counts": entity_counts,
        "relationship_type_counts": rel_counts
    }

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "stats": stats
    }
