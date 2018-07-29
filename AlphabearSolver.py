"""
AlphaBears generates letters on a grid that the player must use to create words.
Each letter starts with a number of 'lives' which reduce by one each time the
letter is not used. If the letter is allowed to reach zero lives it becomes a rock
which stops turning into letters. This reduces the number of letters available
to you for the next round and also the total number of points you will be able
to gain at the end.
"""


class AlphaBears(object):
    """
    This class takes two sets of any number of letters provided be the user
    and forms words. The letters are provided in two categories, "primary letters"
    and "secondary letters". In forming the word we will use every letter in primary,
    and as many as possible from secondary. All letters with one life left in your
    game should be included as primary, how you distribute the rest is up to you.
    """

    def __init__(self):
        """
        Request input from the user to specify which letters to use. Read in a
        file containing viable words and sort them to find the longest words that
        contain all of the provided essential letters, and as many of the optional
        letters as possible.
        """

        primary_letters = input("Please enter your essential letters: ")
        secondary_letters = input("Please enter your optional letters: ")

        self.primary_letters = primary_letters.upper()
        self.secondary_letters = secondary_letters.upper()

        # Read in a file containing all of the alphanumeric words that can be used.
        self.dictionary_corner = self.file_reader()

        # Parse through all words in the dictionary, words must contain all primary
        # letters, with a bias toward as many secondary letters as possible.
        word_list = self.word_parser()

        # Return all viable words that use the most letters. This allows the user
        # to make a decision based upon the bears they have selected prior to this game.
        self.best_word(word_list)

    def file_reader(self):
        """ Read in our dictionary of words into a list that will be searched through. """

        f = open('dictionary.txt')
        dictionary = f.read()
        dictionary_corner = dictionary.split()
        f.close()

        return dictionary_corner

    def word_parser(self):
        """
        Parse through all the words in our dictionary, choosing only words that contain all of
        our primary letters, and as many secondary letters as possible.
        """
        candidate_words = []
        # For every word in list of all words, store the word if it contains all the primary letters.
        for word in self.dictionary_corner:
            length = 0
            modified_word = word
            # Each letter in our primary_letters must exist in the word, otherwise we break the loop immediately.
            for letter in self.primary_letters:
                if letter not in modified_word:
                    break
                # Ensure these letters are removed so we don't match them twice
                modified_word = modified_word.replace(letter, '', 1)
            else:
                # If the loop didn't break, we have a candidate word with at least that many points.
                length += len(self.primary_letters)
                # Add more points for any secondary letters found.
                for letter in self.secondary_letters:
                    if letter in modified_word:
                        modified_word = modified_word.replace(letter, '', 1)
                        length += 1

                # Length is recorded so that we can verify only letters in our string have been used.
                if len(word) == length:
                    candidate_words.append(word)

        return candidate_words

    def best_word(self, word_list):
        """
        Taking a list containing a word followed by the number of points they score, scan
        through out list of candidate words, finding the first that scores the most points.

        :param word_list list A list of words and their length in the form [word, length, word, length, ...]
        """
        best_words = []

        # Look for the length of the longest word in our list. If we have not found any words,
        # max() will raise ValueError which we catch and interpret for the user.
        try:
            longest_word = len(max(word_list, key=len))
        except ValueError:
            best_words = None

        # List all words that are of equal length to the longest word in the list.
        for word in word_list:
            if len(word) == longest_word:
                best_words.append(word)

        # Display all viable words to user so that they can make the decision of which word to play.
        if best_words is None:
            print("I'm afraid no words have been found")
        else:
            print("Here are the best words you can play: %s" % best_words)


if __name__ == "__main__":
    AlphaBears()
