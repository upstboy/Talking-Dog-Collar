def NumberGuessingGame ():
    import random
    number = random.randint(1, 100)
    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100")
    difficulty = input("Choose a difficulty. Type 'easy' or 'hard': ").lower()
    if difficulty == "easy":
        attempts = 10
    elif difficulty == "hard":
        attempts = 5
    else:
        print("Invalid input. Please try again.")
        NumberGuessingGame()
    while attempts > 0:
        print(f"You have {attempts} attempts remaining to guess the number.")
        guess = int(input("Make a guess: "))
        if guess > number:
            print("Too high.")
            attempts -= 1
        elif guess < number:
            print("Too low.")
            attempts -= 1
        else:
            print(f"You got it! The answer was {number}.")
            break
    if attempts == 0:
        print("You've run out of guesses. You lose.")
    play_again = input("Do you want to play again? Type 'yes' or 'no': ").lower()
    if play_again == "yes":
        NumberGuessingGame()
    else:
        print("Goodbye!")

NumberGuessingGame()