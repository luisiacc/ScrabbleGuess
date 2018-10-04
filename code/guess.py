spanish_dict = 'dicts/spanish.txt'


class Guesser:
    alllet = 'qwertyuiopñlkjhgfdsazxcvbnmáéíóú'

    def __init__(self, let: str, dictionary, strict_len=False,
                 min_matches=0, min_len=0, max_len=15):

        self.let = let.lower()
        self.strict = strict_len
        self.min_matches = min_matches
        self.min_len = min_len
        self.max_len = max_len
        self.dictionary = [self.word_filter(i) for i in dictionary if self.word_filter(i)]

        for i in dictionary:
            i = self.word_filter(i)
            if i: self.dictionary.append(i)

    def word_filter(self, word: str):
        word = word.strip('\n')
        for char in word:
            if char not in self.alllet:
                word = word.replace(char, '')

        if self.strict:
            if len(self.let) == len(word):
                return word
            else:
                return 0
        else:
            if self.min_len <= len(word) <= self.max_len:
                return word
            else:
                return 0

    def counter(self, word):
        count = 0
        for char in self.let.lower():
            if char in word:
                count += 1
        return count

    def match_strict(self, word: str):
        for i in self.let:
            if self.let.count(i) != word.count(i):
                return False

        return True

    def get_matches(self):
        matches = []

        def append(wo):
            if wo not in matches:
                matches.append(wo)

        for word in self.dictionary:
            if word:
                count = self.counter(word)

                if not self.strict:
                    if count == len(self.let):
                        append(word)

                    if self.min_matches:
                        if count >= self.min_matches:
                            append(word)
                else:
                    if self.match_strict(word):
                        append(word)

        return matches

    @property
    def combination_matches(self):
        matches = []

        # :type word: str

        def append(wo):
            if wo not in matches:
                matches.append(wo)

        if self.let.endswith('-'):
            for word in self.dictionary:
                word = self.word_filter(word)
                if word.startswith(self.let[:-1]):
                    append(word)
        elif self.let.startswith('-'):
            for word in self.dictionary:
                word = self.word_filter(word)
                if word.endswith(self.let[1:]):
                    append(word)
        else:
            for word in self.dictionary:
                if self.let in word and not word.startswith(self.let) \
                    and not word.endswith(self.let):
                    append(word)
        return matches
