import random
import sys

from State import State

vowels = ["a", "e", "i", "o", "u"]
size, max_guesses = 5, 6
english_words = []
state = State([], [])


def load_words(size):
    with open('words_alpha.txt') as word_file:
        five_letter_words = []
        for word in word_file.read().split():
            if len(word) == size:
                five_letter_words.append(word)

        global english_words
        english_words = five_letter_words


def first_words():
    max = 0
    results = []
    for word in english_words:
        score = 0
        for letter in word:
            if letter in vowels:
                score += 1
            elif letter == "y":
                score += .5

        if score == max:
            results.append(word)
        elif score > max:
            max = score
            results = [word]

    return results


def filter_words():
    filtered_words = []
    for word in english_words:
        if contains_no_forbidden_letters(word, state.not_letters, state.cells):
            if contains_all_known_letters(word, state.letters):
                filtered_words.append(word)

    return filtered_words


def contains_all_known_letters(word, letters):
    result = True
    for letter in letters:
        if letter not in word:
            result = False
            break

    return result


def contains_no_forbidden_letters(word, not_letters, cells):
    result = True
    for index, letter in enumerate(word):
        if not matches_cell_input(letter, cells[index], not_letters):
            result = False
            break

    return result


def matches_cell_input(letter, cell, not_letters):
    if letter in not_letters:
        result = False
    elif not cell:
        result = True
    elif cell.is_known():
        result = letter == cell.letter
    else:
        result = letter not in cell.not_letters

    return result


def init_game():
    global size, max_guesses, state
    size = int(input("What is the size of the word?"))
    state = State([],[],size)
    load_words(size)

    print(random.choices(first_words(), k=3))


def collect_input():
    result = input("Did we win? y/N") == "y"
    if result:
        return result

    guess = input("What was our guess?")
    for index, cell in state.cells.items():
        if cell.is_known():
            print("Letter " + str(index + 1) + " is already known")
        else:
            prompt = "Was '" + guess[index] + "' Correct(1), Misplaced(2), or Wrong(3)"
            letter_result = int(input(prompt))
            if letter_result == 1:
                state.add_hit(guess[index])
                cell.known(guess[index])
            elif letter_result == 2:
                state.add_hit(guess[index])
                cell.known_not(guess[index])
            else:
                state.add_miss(guess[index])

    return result


if __name__ == '__main__':
    init_game()

    for guess in range(max_guesses):
        we_won = collect_input()
        if we_won:
            print("Hooray!")
            sys.exit()

        filtered_words = filter_words()
        print("Filtered words count: " + str(len(filtered_words)))
        print(random.choices(filtered_words, k=min(5, len(filtered_words))))
