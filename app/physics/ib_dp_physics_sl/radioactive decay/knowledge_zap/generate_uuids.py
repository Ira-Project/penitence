import json
import uuid

def generate_uuid():
    return str(uuid.uuid4()).replace('-', '')[:21]

# Read the JSON file
with open('knowledge_zap.json', 'r') as f:
    data = json.load(f)

# Generate UUIDs for multiple choice questions
for mcq in data['multipleChoiceQuestions']:
    mcq['id'] = generate_uuid()
    for variant in mcq['variants']:
        variant['id'] = generate_uuid()

# Generate UUIDs for matching questions
for mq in data['matchingQuestions']:
    mq['id'] = generate_uuid()
    for variant in mq['variants']:
        variant['id'] = generate_uuid()

# Generate UUIDs for ordering questions
if 'orderingQuestions' in data:
    for oq in data['orderingQuestions']:
        oq['id'] = generate_uuid()
        for variant in oq['variants']:
            variant['id'] = generate_uuid()

# Write back to file
with open('knowledge_zap.json', 'w') as f:
    json.dump(data, f, indent=2)
