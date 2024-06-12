import tkinter as tk
import requests
import random

def draw_gallows(canvas):
    canvas.create_line(50, 350, 200, 350, fill="grey", width=4) #base
    canvas.create_line(125, 350, 125, 50, fill="grey", width=4) #pole
    canvas.create_line(125, 50, 250, 50, fill="grey", width=4) #top beam
    canvas.create_line(250, 50, 250, 100, fill="grey", width=4) #rope

def draw_head(canvas):
    canvas.create_oval(225, 100, 275, 150, outline="orange", width=4)

def draw_body(canvas):
    canvas.create_line(250, 150, 250, 250, fill="orange", width=4)

def draw_left_arm(canvas):
    canvas.create_line(250, 170, 200, 220, fill="orange", width=4)

def draw_right_arm(canvas):
    canvas.create_line(250, 170, 300, 220, fill="orange", width=4)

def draw_left_leg(canvas):
    canvas.create_line(250, 250, 200, 300, fill="orange", width=4)

def draw_right_leg(canvas):
    canvas.create_line(250, 250, 300, 300, fill="orange", width=4)

def announce_won(canvas):
    canvas.create_text(200, 400, text="You won!! Congrats", fill="green", font=("Comic Sans MS", 20))

def announce_lost(canvas):
    canvas.create_text(200, 400, text="You lost :/ the poor guy will die", fill="brown", font=("Comic Sans MS", 20))

def intro():
    print("Welcome to this game of Hangman.")
    print("A randomly-generated word of 6 to 8 letters will be given.")
    print("You have 6 chances if you guess wrong.")
    print("The game ends when you lose or when you guess the entire word within the 6 chances.")
    print("Good luck!")
    print("")

def generate_random_word(min_length=6, max_length=8):
    response = requests.get("https://api.datamuse.com/words?sp=" + "?" * random.randint(min_length, max_length) + "&max=1000")
    words = response.json()
    valid_words = [word['word'] for word in words if min_length <= len(word['word']) <= max_length and ' ' not in word['word']]
    return random.choice(valid_words) if valid_words else None

def display_dashes(word):
    word_length = len(word)
    dashed_word = '-' * word_length
    return dashed_word

def user_guess():
    guess = input("enter your guess: ")
    return guess[0].lower()

def check_guess(guess, word):
    return guess in word

def change_dashed_display(word, guess, dashed_word):
    new_dashed_word = list(dashed_word)
    for i, letter in enumerate(word):
        if letter == guess:
            new_dashed_word[i] = guess
    return ''.join(new_dashed_word)

def user_wins(dashed_word):
    return not ('-' in dashed_word)

def main():
    
    root = tk.Tk()
    root.title("Hangman Game")
    root.geometry("600x600")
    canvas = tk.Canvas(root, width=500, height=500)
    canvas.pack(pady=20)

    draw_gallows(canvas)

    draw_functions = [
        draw_head, draw_body, draw_left_arm, draw_right_arm, draw_left_leg, draw_right_leg
    ]

    intro()
    max_attempts = 6
    attempts = 0
    previous_guesses = []
    won = False
    '''
    for i in range(20):
        print(generate_random_word())
    '''
    word = generate_random_word()
    #print("Random word:", word)
    if not word:
        print("Failed to generate a random word. Please try again.")
        return
    dashed_word = display_dashes(word)
    print("Current state:",dashed_word)

    while (attempts < max_attempts) and (not won):
        guess = user_guess()
        if check_guess(guess, word):
            if guess in previous_guesses:
                print("You already guessed this letter before.")
            else:
                previous_guesses.append(guess)
                dashed_word = change_dashed_display(word, guess, dashed_word)
                if user_wins(dashed_word):
                    won = True
        else:
            if guess in previous_guesses:
                print("You already guessed this letter before.")
            else:
                previous_guesses.append(guess)
                draw_functions[attempts](canvas)
                attempts+=1
                print("Your guess:", guess, "does not exist in the word.")
                print("You have", max_attempts - attempts, "attempts left.")
        print("")
        print("Current state:", dashed_word)

    if won:
        print("Congratulations! You won the game :D")
        announce_won(canvas)
    else:
        print("Sorry, you lost :(")
        print("The word was:", word)
        announce_lost(canvas)

    root.mainloop()

if __name__ == '__main__':
    main()