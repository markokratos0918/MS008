class StringManipulator:
    def find_character(self, text, char):
        # Modified to accept text as a parameter
        return text.find(char)

    def get_length(self, text):
        """Return the length of the string."""
        # Modified to accept text as a parameter
        return len(text)

    def to_uppercase(self, text):
        """Return the string in uppercase."""
        # Modified to accept text as a parameter
        return text.upper()


def main():
    # Create an instance of the StringManipulator class without arguments
    manipulator = StringManipulator()
    
    # Store the text in a variable
    example_text = "example"

    # Call the find_character method, passing the text as an argument
    result = manipulator.find_character(example_text, 'x')
    print("Index of 'x':", result)  # Output: 1

    # Call the get_length method, passing the text as an argument
    length = manipulator.get_length(example_text)
    print("Length of string:", length) 

    # Call the to_uppercase method, passing the text as an argument
    uppercase_text = manipulator.to_uppercase(example_text)
    print("Uppercase string:", uppercase_text) 


if __name__ == "__main__":
    main()