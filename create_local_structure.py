import os

# Base folder 
BASE_DIR = "LOCAL_WORK"

# Folder structure 
folders = [ 
    "downloads_temp",  # this folder is only for raw unprocessed data
    "current_batch/SAFE", 
    "current_batch/HARDNEG", 
    "current_batch/VIOLENCE"
    "cleaned_batch/SAFE", 
    "cleaned_batch/HARDNEG", 
    "cleaned_batch/VIOLENCE",
    "logs" 
]

def create_structure():
    for folder in folders:
        path=os.path.join(BASE_DIR,folder)
        os.makedirs(folder,exist_ok=True) # if folder didnt exist then it gets created and if it is present already then will not do anything also will not throw any error 

        print(f"\nCreated: {path}")

if __name__ == "__main__": 
    create_structure()
    print("\n local structure created successfully!")
