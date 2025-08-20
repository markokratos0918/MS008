#attached text file, open, read, and write the complete information for the demo.txt.


class FileProcess:

    def __init__(self, file_path):
        self.file_path = file_path
    
    def read_file(self):
        file = open(self.file_path, "r", encoding="UTF-8") #open the file 
        data = file.read()
        file.close()
        print(data) # prints contents of the file

    def write_file(self):
        file = open(self.file_path,"a") # Opens the file in append mode
        inputted_text=input("Write the text you want to append :")
        file.write(f"{inputted_text}\n")
        print("Your data has been added into the file")
        file.close()
    
    def word_count(self):
        file = open(self.file_path, "r", encoding="UTF-8")
        data = file.read()
        file.close()

        words = data.split()
        word_count = len(words)
        print(f"The file contains {word_count} words.\n")



if __name__=="__main__":
    stored_file = FileProcess(r"C:\Users\DTMAR\Downloads\demo.txt")
    
    print("Welcome to File Processor!")
    user_option = input("Do you want to read the file or write into it? Press R if you want to read, W to write, or C to count the words on the file:  ").strip().lower()
    
    if user_option.lower() == "r":   #user is given the option to choose the method
       stored_file.read_file()
    elif user_option.lower() == "w":   
       stored_file.read_file()  
    elif user_option.lower() == "c":   
       stored_file.word_count()  
    else: 
        print("Invalid method entered, please choose R, W, or C only.")
  
 