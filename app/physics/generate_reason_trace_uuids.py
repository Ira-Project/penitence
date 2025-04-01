import json
import uuid


def generate_short_uuid():
    return str(uuid.uuid4()).replace('-', '')[:21]


path = "ib_dp_physics/thermal_energy_transfers/reason_trace/reason_trace.json"
# Read the JSON file
with open(path, 'r') as f:
    data = json.load(f)

# Update IDs for answer options in each reasoning question
for question in data['reasoningQuestions']:
    for option in question['answerOptions']:
        option['id'] = generate_short_uuid()

# Write back to file
with open(path, 'w') as f:
    json.dump(data, f, indent=2)
