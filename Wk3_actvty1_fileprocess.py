#attached text file, open, read, and write the complete information for the demo.txt.


class FileProcess:

    def __init__(self, file_path):
        self.file_path = file_path
    
    def read_file(self):
        file = open(self.file_path, "r", encoding="UTF-8")
        data = file.read()
        file.close()
        print(data)

    def write_file(self):
        file = open(self.file_path,"a") # Opens the file in append mode
        inputted_text=input("Write the text you want to append :")
        file.write(f"{inputted_text}\n")
        print("Your data has been added into the file")
        file.close()



if __name__=="__main__":
    stored_file = FileProcess(r"C:\Users\DTMAR\Downloads\demo.txt")
    
    print("Welcome to File Processor!")
    user_option = input("Do you want to read the file or write into it? Press R if you want to read, else press W to write:  ").strip().lower()
    
    if user_option.lower()== "r":
       stored_file.read_file()
    else:
        stored_file.write_file() 
 