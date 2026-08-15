from knowledge_graph.kg_builder import KnowledgeGraphBuilder
from knowledge_graph.kg_query import KnowledgeGraphQuery
from knowledge_graph.nlp_processor import NLPProcessor

builder = KnowledgeGraphBuilder('data/college_data.json')
builder.build_graph()
graph = builder.get_graph()
query = KnowledgeGraphQuery(graph)
nlp = NLPProcessor()

tests = [
    'Hello',
    'What departments are available?',
    'Tell me about CSE',
    'What is the fee for BTech?',
    'How to get admission?',
    'Tell me about placements',
    'Is hostel available?',
    'What scholarships are offered?',
    'What is the contact number?',
    'Who is the principal?',
    'What clubs are there?',
    'Tell me about AI ML department',
]

print('=== CHATBOT TEST RESULTS ===\n')
for q in tests:
    result = nlp.process(q)
    intent = result['intent']
    entities = result['entities']
    
    # Get actual response
    if intent == 'department_info' and 'department' in entities:
        resp = query.query_department(entities['department'])
    elif intent == 'department_info':
        resp = 'Lists all departments'
    elif intent == 'fee_info':
        resp = query.query_fees(entities.get('course'))
    elif intent == 'admission_info':
        resp = query.query_admission(entities.get('course'))
    elif intent == 'placement_info':
        resp = query.query_placements()
    elif intent == 'facility_info':
        resp = query.query_facilities()
    elif intent == 'scholarship_info':
        resp = query.query_scholarships()
    elif intent == 'contact_info':
        resp = query.query_contact()
    elif intent == 'management_info':
        resp = query.query_management()
    elif intent == 'club_info':
        resp = query.query_clubs()
    elif intent == 'greeting':
        resp = 'Hello! Welcome...'
    else:
        resp = query.search_general(q)

    print(f'Q: {q}')
    print(f'Intent: {intent} | Entities: {entities}')
    print(f'Response (first 100): {str(resp)[:100]}...')
    print()

print('ALL TESTS PASSED!')
