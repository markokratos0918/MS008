class WordCounter:
    def __init__(self):    #initializes the sentence variable.
        self.sentence = ""

    def get_sentence(self):   #collects the user’s sentence.
        self.sentence = input("Enter a sentence: ").strip()

    def count_words(self):
        if not self.sentence:
            return 0
        return len(self.sentence.split())

    def display_result(self):
        word_count = self.count_words()
        print(f"Number of words in the sentence: {word_count}")


if __name__ == "__main__":
    counter = WordCounter()
    counter.get_sentence()
    counter.display_result()