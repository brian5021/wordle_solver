import random
import sys

from State import State

vowels = ["a", "e", "i", "o", "u"]
size, max_guesses = 5, 5
english_words = []
common_words = []
state = State([], [])
guess = ""


def load_words(size):
    with open('words_alpha.txt') as word_file:
        five_letter_words = []
        for word in word_file.read().split():
            if len(word) == size:
                five_letter_words.append(word)

        global english_words
        english_words = five_letter_words

    with open('wordlist.10000.txt') as word_file:
        five_letter_words = []
        for word in word_file.read().split():
            if len(word) == size:
                five_letter_words.append(word)

        global common_words
        common_words = five_letter_words


def first_words():
    max = 0
    results = dict()
    for word in english_words:
        score = 0
        distinct_letters = set()
        for letter in word:
            if letter in distinct_letters:
                continue

            distinct_letters.add(letter)
            if letter in vowels:
                score += 1
            elif letter == "y":
                score += .5
            else:
                score += .25

        if word in common_words:
            score += 5

        if score == max:
            results[word] = int(score)
        elif score > max:
            max = score
            results.clear()
            results[word] = int(score)

    return sorted(results, key=results.get, reverse=True).pop(0), len(results.keys())


def filter_words():
    global english_words
    filtered_words = {}
    for word in english_words:
        if contains_no_forbidden_letters(word, state.not_letters, state.cells):
            if contains_all_known_letters(word, state.letters):
                filtered_words[word] = int(distinct_score(word))

    english_words = filtered_words
    return sorted(filtered_words, key=filtered_words.get, reverse=True).pop(0), len(filtered_words.keys())


def distinct_score(word):
    score = 0
    distinct_letters = set()
    for letter in word:
        if letter not in distinct_letters:
            if letter in vowels:
                score += .5
            else:
                score += 1
            distinct_letters.add(letter)

    if word in common_words:
        score += 100
    return score


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
    global size, state, guess
    size = int(input("What is the size of the word?"))
    state = State([], [], size)
    load_words(size)

    guess = first_words()[0]
    print(guess)


def collect_input():
    global english_words, max_guesses
    result = int(input("What happened on our guess?\n (1) We won!\n (2) Word was wrong\n (3) Word was invalid"))
    if result == 1:
        return True
    elif result == 3:
        del english_words[guess]
        max_guesses += 1
        return False

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

    return False


if __name__ == '__main__':
    init_game()
    while max_guesses > 0:
        we_won = collect_input()
        if we_won:
            print("Hooray!")
            sys.exit()

        guess, total_potentials = filter_words()

        if total_potentials == 1:
            print("We win! The word is: " + str(guess))
            sys.exit()

        print("Filtered words count: " + str(total_potentials))
        print(guess)
        max_guesses -= 1

    print("Boo! :(")
    sys.exit()
