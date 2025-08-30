#Ans. the use of __name & __species and get and setter will identify encapsulation. The methods could not accessed publicly within the class.

class Animal:
    def __init__(self, name, species):
        self.__name = name       # private attribute
        self.__species = species # private attribute
    
    # Getter for name
    def get_name(self):
        return self.__name
    
    # Setter for name
    def set_name(self, name):
        if isinstance(name, str) and len(name) > 0:
            self.__name = name
        else:
            print("Invalid name. It must be a non-empty string.")
    
    # Getter for species
    def get_species(self):
        return self.__species
    
    # Setter for species
    def set_species(self, species):
        if isinstance(species, str) and len(species) > 0:
            self.__species = species
        else:
            print("Invalid species. It must be a non-empty string.")
    
    def display_info(self):
        print(f"Animal Name: {self.__name}, Species: {self.__species}")


# Example usage
if __name__ == "__main__":
    # Creating an animal
    lion = Animal("Leo", "Lion")
    
    # Display info using encapsulated attributes
    lion.display_info()
    
    # Access through getter
    print("Current Name:", lion.get_name())
    
    # Update using setter
    lion.set_name("Simba")
    lion.set_species("African Lion")
    
    # Display updated info
    lion.display_info()
    
    # Trying invalid update
    lion.set_name("")   # This should print an error

