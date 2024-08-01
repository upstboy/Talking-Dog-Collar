rooms = {
    "entrance": {
        "description": "You are at the entrance of a dark house.",
        "exits": ["living room"],
        "items": [],
        "objects": []
    },
    "living room": {
        "description": "You are in a cozy living room. There's a door to the kitchen.",
        "exits": ["entrance", "kitchen"],
        "items": ["Golden key"],
        "objects": ["Computer"]
    },
    "kitchen": {
        "description": "You are in a small kitchen. There's a door to the bedroom.",
        "exits": ["living room", "bedroom"],
        "items": ["password paper"],
        "objects": []
    },
    "bedroom": {
        "description": "You are in a quiet bedroom. You see a locked chest.",
        "exits": ["kitchen", "Locked Door"],
        "items": [],
        "objects": ["Locked Chest"]
    },
    "Locked Door": {
        "description": "You are in a dimly lit room, you see a broken drill.",
        "exits": ["bedroom"],
        "items": ["Tape"],
        "objects": ["Broken Drill"]
    }
}

inventory = {
    
}

def handle_move(currentLocation):
    requestedLocation = input("Where do you want to go? ")
    if requestedLocation not in rooms[currentLocation]["exits"]:
        print("You are too far to go here! Enter a different value")
    elif requestedLocation == "Locked Door":
        item = "Sd Card"
        if item in inventory: # Check whether user has SD card in inventory, only then enter locked door.
            currentLocation = requestedLocation
            del inventory["Sd Card"]
        else:
            print("You cannot enter this room!")
    else: 
        currentLocation = requestedLocation
    
    return currentLocation


def handle_takeItem(currentLocation):
    item = input("Which item do you want to take? ")
    if item in rooms[currentLocation]["items"]:
        if item in inventory:
            inventory[item] += 1
            rooms[currentLocation]["items"].remove(item)
    
        else:
            inventory[item] = 1
            rooms[currentLocation]["items"].remove(item)
            print(f"{item} has been added to your inventory.")
    else:
        print("That item is not here.") 
        

def handle_Object(currentLocation):
    desiredObject = input("Which object do you want to interact with? ")
    if desiredObject in rooms[currentLocation]["objects"]:
        if desiredObject == "Locked Chest":
            if "Golden key" in inventory: 
                print("You unlocked the chest!")
                print("You got a new item, the Hammer!")
                item = "Hammer"
                inventory[item] = 1
                del inventory["Golden key"]
                rooms[currentLocation]["objects"].remove(desiredObject)
            else: 
                print("You do not have the item required to open this chest!") 
        if desiredObject == "Computer":
            if "password paper" in inventory:
                print("You unlocked the computer!")
                print("You got a new item, the Sd Card!")
                item = "Sd Card"
                inventory[item] = 1
                del inventory["password paper"]
                rooms[currentLocation]["objects"].remove(desiredObject)
            else:
                print("You do not have the item required to open this computer!")
    else: 
        print("Invalid Object!")



def theAdventureGame():
    
    currentLocation = "entrance"
    while currentLocation != "exit":
        print(rooms[currentLocation]["description"])
        print("Exits: ")
        print(rooms[currentLocation]["exits"])
        print("Items: ")
        print(rooms[currentLocation]["items"])
        print("Objects: ")
        print(rooms[currentLocation]["objects"])

        requestedAction = input("What do you want to do? [move, take item, object]: ").lower()

        if requestedAction == "move":

            currentLocation = handle_move(currentLocation)

        elif requestedAction == "take item":

           handle_takeItem(currentLocation)

        elif requestedAction == "Inventory": 
            print(inventory)
        
        elif requestedAction == "object":

            handle_Object(currentLocation)
        
        else: 
            print("Invalid action")
       

theAdventureGame()