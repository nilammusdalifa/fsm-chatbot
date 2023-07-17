import string

class Preprocessing:

    def __init__(self):
        pass

    def __whitespace_removal(self, text):
        res = " ".join(text.split())
        return res

    def __lower_text(self, text):
        res = self.__whitespace_removal(text).lower()
        return res

    def __symbol_removal(self, text):
        removal = str.maketrans('','', string.punctuation)
        res = self.__lower_text(text).translate(removal)
        return res

    def preprocess(self, text):
        return self.__symbol_removal(text)