def inventoryGame ():
    inventory = {}
    condition = True
    while condition: 
        print ("Welcome to the inventory")
        print ( )
        print ("Would you like to")
        print ( )
        print("1: Add items")
        print( )
        print("2: Remove items")
        print ( )
        print("3: Update items")
        print ( )
        print ("4: View Inventory")
        print ( )
        print ("5: Exit")
        print( )
        userChoice = int(input("Enter the number here: "))
        if userChoice == 1:
            itemName = input("Enter the name of the item you want to add: ")
            amount = int(input("Enter the amount of the item you want to add: "))
            value = float(input("Enter the value of the item: "))
            inventory[itemName] = (amount, value)
            print(f"{itemName} has been added to inventory")
        if userChoice == 2: 
            itemName = input("What item would you like removed: ")
            del inventory[itemName]
            print(f"{itemName} has been deleted from inventory")
        if userChoice == 3:
            itemName = input("Enter the name of the item you want to update: ")
            updatedAmount = int(input("Enter the new amount of the item: "))
            inventory[itemName] = updatedAmount
        if userChoice == 4:
            print("Inventory: ")
            for itemName, details in inventory.items():
                print(f"Item: {itemName}, Details: {details}")
        if userChoice == 5: 
            print ("You have chose to exit the inventory")
            condition = False

    







inventoryGame()