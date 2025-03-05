from .llm_parameters import *

def extract_concepts(passage):

    messages = [
        {"role": "system", "content": extract_concepts_instructions + "\n\n" + extract_concepts_response_format + "\n\n" + extract_concepts_pointers},
        {"role": "user", "content": passage}
    ]
        