# Initialize
friends = {
    "brandon": {
        "age": 14,
        "race": "caucasian"
    },
    "evan": {
        "age": 11,
        "race": "indian"
    }
}

# Fetch

print(friends['brandon']['age'])

print(friends['evan']['race'])

# Add
friends["evan2"] = {
    "age": 11,
    "race": "indian"
}

print(friends['evan2']['race'])

# Delete
del friends["brandon"]

# Check if exists
if "brandon" in friends:

    print(friends['brandon']['race'])

else: 
    print("not found")

friends["evan2"]["age"] = friends["evan2"]["age"] + 1

print(friends["evan2"]["age"])

friends["evan3"] = {
    "age": 12
}

print(friends["evan3"]["age"])