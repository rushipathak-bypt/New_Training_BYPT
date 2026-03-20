import random

computerChoice = random.randint(1, 100)
count = 0
while True:
    try:
        userChoice = int(input("Enter a valid number between 1-100: "))
    except ValueError:
        print("Error!!! You entered non numeric value")
        print()

    else:
        if userChoice > 100 or userChoice < 1:
            print("You entered invalid integer input!")
            print()
            continue

        else:
            if userChoice == computerChoice:
                print(f"Congrats! You guessed it correctly in {count+1} attempts")
                break

            elif userChoice < computerChoice:
                print("You guessed a lower value. Try Again")
                count += 1
                continue
            elif userChoice > computerChoice:
                print("You guessed a higher value. Try Again")
                count += 1
                continue
