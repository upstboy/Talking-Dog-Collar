def NumberGuessingGame ():

    import random 

    theNumber = random.randint(1, 50)

    difficulty = input("Choose a difficulty, easy, medium, hard: ").lower()

    if difficulty == "easy":
        rem = 15 
    elif difficulty == "medium":
        rem = 10  
    elif difficulty == "hard":
        rem = 5
    else: 
        print("Not a valid difficfulty, enter again")
        NumberGuessingGame()

    while rem > 0: 

        theGuess = int(input("Give a Guess: "))

        if theGuess > theNumber: 
            print("Too high, try again")
            rem -= 1
        elif theGuess < theNumber:
            print("Too low, try again")
            rem -= 1
        else:
            print("Thats right, you guessed the right number!")
            return

NumberGuessingGame()



