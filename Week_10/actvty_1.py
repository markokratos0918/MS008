"""Module for analyzing strings and lists."""

class Analyzer:
    """Base class for analyzing strings and lists."""
    def __init__(self, data):
        """Initialize with string or list."""
        self.data = data

    def total_length(self):
        """Return the total length of the data."""
        return len(self.data)

    def count_uppercase(self):
        """Count uppercase characters in data."""
        if isinstance(self.data, str):
            return sum(1 for char in self.data if char.isupper())
        if isinstance(self.data, list):
            return sum(1 for item in self.data for char in str(item) if char.isupper())
        raise ValueError("Data must be a string or a list.")
class StringAnalyzer(Analyzer):
    """Analyzer for string data."""
    def __init__(self, data):
        """Initialize with a string."""
        if not isinstance(data, str):
            raise ValueError("Data must be a string.")
        super().__init__(data)
class ListAnalyzer(Analyzer):
    """Analyzer for list data."""
    def __init__(self, data):
        """Initialize for list data."""
        if not isinstance(data, list):
            raise ValueError("Data must be a list.")
        super().__init__(data) #source: https://pylint.pycqa.org/en/latest/user_guide/run.htmlurce: https://pylint.pycqa.org/en/latest/user_guide/run.html
# Example usage:
if __name__ == "__main__":
    STRING_DATA = "Hello World!"
    LIST_DATA= ["Hello", "World", "Python3"]

    string_analyzer = StringAnalyzer(STRING_DATA)
    list_analyzer = ListAnalyzer(LIST_DATA)

    print(f"String Analysis: Total Length = {string_analyzer.total_length()}, Uppercase Count = {string_analyzer.count_uppercase()}")
    print(f"List Analysis: Total Length = {list_analyzer.total_length()}, Uppercase Count = {list_analyzer.count_uppercase()}")
    

