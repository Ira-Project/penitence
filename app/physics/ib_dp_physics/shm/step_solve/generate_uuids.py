import json
import uuid

def generate_short_uuid():
    return str(uuid.uuid4()).replace('-', '')[:21]

# Read the JSON file
with open('step_solve.json', 'r') as f:
    data = json.load(f)

# Update question and step IDs
for question in data['questions']:
    question['id'] = generate_short_uuid()
    for step in question['steps']:
        step['id'] = generate_short_uuid()

# Write back to file
with open('step_solve.json', 'w') as f:
    json.dump(data, f, indent=2)
