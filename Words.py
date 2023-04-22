
class Word:

    def __init__(self , word):
        self.word = word
        spaces = 0

    def word_to_letter(self):
        letters = []

        for letter in self.word:
            letters.append(letter)

        return letters

    def space_count(self):
        return self.word_to_letter().__len__() 

    def __str__(self):
        return self.word