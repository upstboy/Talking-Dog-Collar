def adventureGame():
    rooms = {
        "entrance": {
            "description": "You are at the entrance of a dark house.",
            "exits": ["living room"],
            "items": []
        },
        "living room": {
            "description": "You are in a cozy living room. There's a door to the kitchen.",
            "exits": ["entrance", "kitchen"],
            "items": ["Golden key"]
        },
        "kitchen": {
            "description": "You are in a small kitchen. There's a door to the bedroom.",
            "exits": ["living room", "bedroom"],
            "items": ["note"]
        },
        "bedroom": {
            "description": "You are in a quiet bedroom. You see a locked chest.",
            "exits": ["kitchen"],
            "items": []
        }
    }

    inventory = {
        
    }

    location = "entrance"
    print (rooms[location]['description'])
    print (rooms[location]['exits'])
    print (rooms[location]['items'])
    for i in (rooms[location]["items"]):
        if i in inventory:
            inventory[i] = inventory[i] + 1
        else: 
            inventory[i] = 1
    print(inventory)
adventureGame()