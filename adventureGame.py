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
            "items": ["key"]
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
    current_room = "entrance"
    inventory = []

    while True:
        print("\nYou are in the {}.".format(current_room))
        print("You see: {}".format(", ".join(rooms[current_room]["items"]) if rooms[current_room]["items"] else "nothing"))
        print("Exits: {}".format(", ".join(rooms[current_room]["exits"])))

        command = input("\nWhat do you want to do? (move, pick up, quit): ").lower().strip()
        if command == "quit":
            print("Thanks for playing!")
            break
        elif command == "move":
            new_room = input("Where do you want to go? ").lower()
            if new_room in rooms[current_room]["exits"]:
                current_room = new_room
            else:
                print("You can't go that way!")
        elif command == "pick up":
            item = input("What do you want to pick up? ").lower()
            if item in rooms[current_room]["items"]:
                inventory.append(item)
                rooms[current_room]["items"].remove(item)
                print("Picked up {}.".format(item))
            else:
                print("There is no {} here.".format(item))
        else:
            print("Invalid command.")

adventureGame()