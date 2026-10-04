# Entity types and their required/optional attributes
ENTITY_TYPES = {
    'College': {'required': ['name'], 'optional': ['code', 'established', 'type', 'affiliation', 'approval', 'accreditation', 'autonomous', 'recognition', 'ranking', 'campus_area', 'society', 'address', 'phone', 'email', 'website']},
    'Department': {'required': ['name', 'id'], 'optional': ['short', 'hod', 'intake', 'description', 'highlights']},
    'Faculty': {'required': ['name', 'department_id'], 'optional': ['designation', 'qualification', 'experience', 'research_areas']},
    'Subject': {'required': ['name', 'department_id'], 'optional': ['code', 'credits', 'semester', 'type']},
    'Lab': {'required': ['name'], 'optional': ['department_id', 'equipment', 'capacity', 'icon', 'description']},
    'Course': {'required': ['name'], 'optional': ['duration', 'level', 'branches', 'total_intake', 'specializations', 'intake_per_spec', 'intake', 'eligibility']},
    'Fee': {'required': [], 'optional': ['btech', 'mtech', 'mba', 'hostel', 'transport']},
    'Admission': {'required': [], 'optional': ['btech', 'mtech', 'mba']},
    'Facility': {'required': ['name'], 'optional': ['icon', 'description']},
    'Placement': {'required': [], 'optional': ['highest_package', 'average_package', 'median_package', 'students_placed_2024_25', 'job_offers_2024_25', 'companies_visited_2024_25', 'training', 'top_recruiters']},
    'Recruiter': {'required': ['name'], 'optional': []},
    'Scholarship': {'required': ['name'], 'optional': ['description', 'eligibility']},
    'Event': {'required': ['name'], 'optional': ['type', 'description']},
    'Club': {'required': ['name'], 'optional': []},
    'HOD': {'required': ['name', 'department'], 'optional': ['designation']},
    'Management': {'required': [], 'optional': ['governing_body_chairman', 'chairman', 'secretary', 'ceo', 'director', 'principal']},
    'ResearchArea': {'required': ['name'], 'optional': []},
    'Notice': {'required': [], 'optional': []},
    'PlacementDrive': {'required': [], 'optional': []},
    'AcademicSystem': {'required': [], 'optional': ['type', 'semesters_per_year', 'evaluation', 'curriculum']},
    # ── New entity types for formal ER model ─────────────────────────────────
    'Building': {'required': ['name', 'id'], 'optional': ['type', 'floors', 'description', 'year_built', 'departments']},
    'Floor': {'required': ['name', 'building_id'], 'optional': ['floor_number']},
    'Room': {'required': ['name', 'building_id'], 'optional': ['room_number', 'type', 'capacity', 'floor', 'id']},
    'Semester': {'required': ['name', 'number'], 'optional': ['year']},
    'Program': {'required': ['name', 'code'], 'optional': ['duration', 'level', 'total_credits', 'department_id']},
}

# Relationship types with source -> target entity types
RELATIONSHIP_TYPES = {
    'has_department': ('College', 'Department'),
    'has_management': ('College', 'Management'),
    'has_facility': ('College', 'Facility'),
    'offers_course': ('College', 'Course'),
    'has_hod': ('Department', 'HOD'),
    'has_faculty': ('Department', 'Faculty'),
    'offers_subject': ('Department', 'Subject'),
    'has_lab': ('Department', 'Lab'),
    'teaches': ('Faculty', 'Subject'),
    'belongs_to': ('Faculty', 'Department'),
    'researches': ('Faculty', 'ResearchArea'),
    'has_qualification': ('Faculty', 'str'),
    'has_fee': ('College', 'Fee'),
    'has_admission': ('College', 'Admission'),
    'has_placement': ('College', 'Placement'),
    'recruited_from': ('Recruiter', 'Department'),
    'has_recruiter': ('Placement', 'Recruiter'),
    'has_scholarship': ('College', 'Scholarship'),
    'has_event': ('College', 'Event'),
    'has_club': ('College', 'Club'),
    'mentors': ('Faculty', 'Club'),
    'organized_by': ('Event', 'Department'),
    'conducted_in': ('PlacementDrive', 'Department'),
    'uses_lab': ('Subject', 'Lab'),
    'has_academic_system': ('College', 'AcademicSystem'),
    # ── New relationship types for formal ER model ───────────────────────────
    'has_building': ('College', 'Building'),
    'has_floor': ('Building', 'Floor'),
    'has_room': ('Building', 'Room'),
    'housed_in': ('Department', 'Building'),
    'has_semester': ('Program', 'Semester'),
    'offered_in': ('Subject', 'Semester'),
    'teaches_in': ('Faculty', 'Room'),
    'lab_in': ('Lab', 'Room'),
    'has_program': ('Department', 'Program'),
}

def validate_node(node_type, data):
    """Checks if node data has required fields for its type."""
    if node_type not in ENTITY_TYPES:
        return False, f"Unknown node type: {node_type}"
    
    required_fields = ENTITY_TYPES[node_type]['required']
    missing_fields = [f for f in required_fields if f not in data]
    
    if missing_fields:
        return False, f"Missing required fields for {node_type}: {', '.join(missing_fields)}"
    
    return True, "Valid"

def validate_edge(rel_type, source_type, target_type):
    """Checks if edge relationship is valid between source and target types."""
    if rel_type not in RELATIONSHIP_TYPES:
        return False, f"Unknown relationship type: {rel_type}"
    
    expected_source, expected_target = RELATIONSHIP_TYPES[rel_type]
    if source_type != expected_source or target_type != expected_target:
        # Note: we might want to relax string types e.g. for has_qualification
        if expected_target != 'str' and expected_target != target_type:
             return False, f"Invalid relationship {rel_type} between {source_type} and {target_type}. Expected {expected_source} -> {expected_target}."
    
    return True, "Valid"

def get_entity_types():
    return list(ENTITY_TYPES.keys())

def get_relationship_types():
    return list(RELATIONSHIP_TYPES.keys())
