#attached text file, open, read, and write the complete information for the demo.txt.


class FileProcess:

    def __init__(self, file):
        self.file = file
    
    def read_file(self):
        file=open(self.file, "r")
        print(file)

    def write_file(self):
        file=open(self.file,"a") # Opens the file in append mode
        inputted_text=input("Write the text you want to append :")
        file.write(f"{inputted_text}\n")
        print("Congrats, your data has been added into the file")
        file.close()

file = FileProcess(r"C:\Users\DTMAR\Downloads\demo.txt")

def main():
    print("This is the main function")
    method_inserted_by_user=input("Please choose the method, Do you want to read the file or write into it? Press R if you want to read, else press W to write:  ")
    if(method_inserted_by_user.lower()=="r"):
        file.read_file()
    else:
        file.write_file()



if __name__=="__main__":
        main()        