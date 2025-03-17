import json
import random

# Load your JSON data from a file (or you can use a JSON string directly)
with open('data.json', 'r') as file:
    data = json.load(file)  # Assuming your JSON is a list of objects

# Shuffle the list of objects
random.shuffle(data)

# Save the shuffled JSON back to a file, or just use the shuffled data
with open('shuffled_data.json', 'w') as file:
    json.dump(data, file, indent=4)  # Indent for pretty printing

# Now the data is shuffled and saved in shuffled_data.json

