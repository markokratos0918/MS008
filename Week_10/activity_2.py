"""Module for analyzing strings and lists with comprehensive character counting."""


class Analyzer:
    """Base class for analyzing strings and lists."""

    def __init__(self, data):
        """
        Initialize with string or list.

        Args:
            data: Input data (string or list) to analyze.
        """
        self.data = data

    def total_length(self):
        """
        Return the total length of the data.

        Returns:
            int: Length of data (string length or list length).
        """
        return len(self.data)

    def count_uppercase(self):
        """
        Count uppercase characters in data.

        Returns:
            int: Number of uppercase characters.

        Raises:
            ValueError: If data is not a string or list.
        """
        if isinstance(self.data, str):
            return sum(1 for char in self.data if char.isupper())
        if isinstance(self.data, list):
            return sum(1 for item in self.data
                      for char in str(item) if char.isupper())
        raise ValueError("Data must be a string or a list.")

    def count_lowercase(self):
        """
        Count lowercase characters in data.

        Returns:
            int: Number of lowercase characters.
        """
        if isinstance(self.data, str):
            return sum(1 for char in self.data if char.islower())
        if isinstance(self.data, list):
            return sum(1 for item in self.data
                      for char in str(item) if char.islower())
        return 0

    def count_digits(self):
        """
        Count digit characters in data.

        Returns:
            int: Number of digit characters (0-9).
        """
        if isinstance(self.data, str):
            return sum(1 for char in self.data if char.isdigit())
        if isinstance(self.data, list):
            return sum(1 for item in self.data
                      for char in str(item) if char.isdigit())
        return 0

    def count_special_characters(self):
        """
        Count special characters in data.

        Special characters are defined as characters that are not:
        - Alphanumeric (letters or digits)
        - Whitespace

        Returns:
            int: Number of special characters.
        """
        if isinstance(self.data, str):
            return sum(1 for char in self.data
                      if not char.isalnum() and not char.isspace())
        if isinstance(self.data, list):
            return sum(1 for item in self.data for char in str(item)
                      if not char.isalnum() and not char.isspace())
        return 0

    def count_whitespace(self):
        """
        Count whitespace characters in data.

        Returns:
            int: Number of whitespace characters.
        """
        if isinstance(self.data, str):
            return sum(1 for char in self.data if char.isspace())
        if isinstance(self.data, list):
            return sum(1 for item in self.data
                      for char in str(item) if char.isspace())
        return 0

    def get_summary(self):
        """
        Get a comprehensive summary of character counts.

        Returns:
            dict: Dictionary containing all character count statistics.
        """
        return {
            'total_length': self.total_length(),
            'uppercase': self.count_uppercase(),
            'lowercase': self.count_lowercase(),
            'digits': self.count_digits(),
            'special_characters': self.count_special_characters(),
            'whitespace': self.count_whitespace()
        }


class StringAnalyzer(Analyzer):
    """Analyzer for string data with additional string-specific methods."""

    def __init__(self, data):
        """
        Initialize with a string.

        Args:
            data: String to analyze.

        Raises:
            ValueError: If data is not a string.
        """
        if not isinstance(data, str):
            raise ValueError("Data must be a string.")
        super().__init__(data)

    def count_words(self):
        """
        Count the number of words in the string.

        Returns:
            int: Number of words (split by whitespace).
        """
        return len(self.data.split())


class ListAnalyzer(Analyzer):
    """Analyzer for list data with additional list-specific methods."""

    def __init__(self, data):
        """
        Initialize with a list.

        Args:
            data: List to analyze.

        Raises:
            ValueError: If data is not a list.
        """
        if not isinstance(data, list):
            raise ValueError("Data must be a list.")
        super().__init__(data)

    def count_items(self):
        """
        Count the number of items in the list.

        Returns:
            int: Number of items in the list.
        """
        return len(self.data)

    def get_concatenated_string(self):
        """
        Get all list items concatenated as a single string.

        Returns:
            str: Concatenated string of all list items.
        """
        return ''.join(str(item) for item in self.data)


def print_analysis_report(analyzer, data_type):
    """
    Print a formatted analysis report.

    Args:
        analyzer: Analyzer object (StringAnalyzer or ListAnalyzer).
        data_type: String describing the type of data being analyzed.
    """
    print(f"\n{'=' * 50}")
    print(f"{data_type} Analysis Report")
    print('=' * 50)

    summary = analyzer.get_summary()
    print(f"Total Length:         {summary['total_length']}")
    print(f"Uppercase Letters:    {summary['uppercase']}")
    print(f"Lowercase Letters:    {summary['lowercase']}")
    print(f"Digits:               {summary['digits']}")
    print(f"Special Characters:   {summary['special_characters']}")
    print(f"Whitespace:           {summary['whitespace']}")

    if isinstance(analyzer, StringAnalyzer):
        print(f"Word Count:           {analyzer.count_words()}")
    elif isinstance(analyzer, ListAnalyzer):
        print(f"List Items:           {analyzer.count_items()}")


# Example usage
if __name__ == "__main__":
    # Test with string data
    STRING_DATA = "Hello World! Python3.12 is #1 @2025"
    string_analyzer = StringAnalyzer(STRING_DATA)

    # Test with list data
    LIST_DATA = ["Hello", "World123", "Python3!", "@Special#"]
    list_analyzer = ListAnalyzer(LIST_DATA)

    # Print detailed reports
    print_analysis_report(string_analyzer, "STRING")
    print(f"\nOriginal String: '{STRING_DATA}'")

    print_analysis_report(list_analyzer, "LIST")
    print(f"\nOriginal List: {LIST_DATA}")

    # Additional demonstrations
    print("\n" + "=" * 50)
    print("Quick Summary Examples")
    print("=" * 50)

    test_string = "Test123!@#"
    test_analyzer = StringAnalyzer(test_string)
    print(f"\nAnalyzing: '{test_string}'")
    print(f"Digits: {test_analyzer.count_digits()}")
    print(f"Special chars: {test_analyzer.count_special_characters()}")

