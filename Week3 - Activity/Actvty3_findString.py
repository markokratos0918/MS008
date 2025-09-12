class StringManipulator:
    def __init__(self, text):  # used to initialize object attributes
        self.text = text

    def find_character(self, char):
        return self.text.find(char)

    def get_length(self):
        """Return the length of the string."""
        return len(self.text)

    def to_uppercase(self):
        """Return the string in uppercase."""
        return self.text.upper()


def main():
    # Create an instance of the StringManipulator class
    name = StringManipulator("example")

    # Call the find_character method
    result = name.find_character('x')
    print("Index of 'x':", result)  # Output: 1

    # Call the get_length method
    length = name.get_length()
    print("Length of string:", length) 

    # Call the to_uppercase method
    uppercase_text = name.to_uppercase()
    print("Uppercase string:", uppercase_text) 


if __name__ == "__main__":
    main()