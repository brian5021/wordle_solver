class Cell:
    def __init__(self, not_letters=None, letter=None):
        if not_letters is None:
            not_letters = []
        self.not_letters = not_letters
        self.letter = letter

    def is_known(self):
        return self.letter is not None

    def known(self, letter):
        self.not_letters = []
        self.letter = letter

    def known_not(self, letter):
        if letter and letter not in self.not_letters:
            self.not_letters.append(letter)
