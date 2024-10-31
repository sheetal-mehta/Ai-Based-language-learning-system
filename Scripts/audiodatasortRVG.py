import pandas as pd
import os
import shutil

# Reading the name of the words to create respective folder of the name.
folders_name = pd.read_excel("D:/SRH Study Data/SEM 04/Master's Thesis/audio data/dt.xlsx",sheet_name="RVG")

def make_folders(folders_name,parent_dir):
    
    # Making it a list to loop through it.
    folders = list(folders_name['suffix'])
    #folders = list(folders_name['Words'])

    # Parent Directory path.
    # parent_dir = "D:/SRH Study Data/SEM 04/Master's Thesis/Wasep_Sorted"

    # Creating folders of the words in folders list.
    for i in folders:
        path = os.path.join(parent_dir, i)
        os.mkdir(path)

    return "Folders are created"


def copy_files_matching_folders(source_dir, destination_dir):
    # Get list of folders in the source directory
    source_folders = os.listdir(source_dir)
    
    # Get list of folders in the destination directory
    destination_folders = os.listdir(destination_dir)
    
    # Iterate through each source folder
    for source_folder in source_folders:
        # Construct the full path of the source folder
        source_folder_path = os.path.join(source_dir, source_folder)
        
        # Check if it's a directory
        if os.path.isdir(source_folder_path):
            # Iterate through each file in the source folder
            for file in os.listdir(source_folder_path):
                # Construct the full path of the file
                file_path = os.path.join(source_folder_path, file)
                
                # Check if it's a file (not a directory)
                if os.path.isfile(file_path):
                    # Iterate through each folder in the destination directory
                    for destination_folder in destination_folders:
                        #print(file)
                        # Check if the folder name matches any component of the file name
                        if ".wav" in file or "PAR" in file or "DEO" in file:
                            file = file[-6:-4]
                        if "_annot" in file:
                            file = file[-13:-11]
                        if destination_folder in file:
                            # Construct the full path of the destination folder
                            destination_folder_path = os.path.join(destination_dir, destination_folder)
                            
                            # Copy the file to the corresponding destination folder
                            shutil.copy(file_path, destination_folder_path)

path_wasep_new = "D:/SRH Study Data/SEM 04/Master's Thesis/RVG_sorted"
make_folders(folders_name,path_wasep_new)


source_directory = "D:/SRH Study Data/SEM 04/Master's Thesis/audio data/all.RVG-J.2.cmdi.25584.1711213590/RVG-J"
destination_directory = "D:/SRH Study Data/SEM 04/Master's Thesis/RVG_sorted"

copy_files_matching_folders(source_directory, destination_directory)





