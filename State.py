from Cell import Cell


class State:
    def __init__(self, letters, not_letters, size=5):
        self.not_letters = not_letters
        self.letters = letters
        self.size = size
        self.cells = dict()
        for x in range(size):
            self.cells[x] = Cell()

    def is_first_input(self):
        return not self.letters and not self.not_letters

    def add_hit(self, letter):
        if letter not in self.letters:
            self.letters.append(letter)

    def add_miss(self, letter):
        if letter not in self.not_letters and letter not in self.letters:
            self.not_letters.append(letter)
