"""
SMART FILE ORGANIZER
Version: V0.1

Author: Farhan Khan
Description:
This script organizes files in a selected folder based on their file type.

Example:
Before running script:

Downloads/
    image.png
    resume.pdf
    movie.mp4
    notes.txt

After running script:

Downloads/
    Images/
        image.png
    Documents/
        resume.pdf
        notes.txt
    Videos/
        movie.mp4

This is the first version of the project. It focuses only on
basic file sorting logic without any advanced features.

Future versions will include:
- Logging system
- CLI interface
- Undo option
- GUI interface
"""

import os
import shutil
import json


# ---------------------------------------------------------
# FUNCTION: load_config()
# PURPOSE:
# Reads the config.json file which contains mapping of
# file extensions to their categories.
#
# Example:
# ".jpg" -> Images
# ".pdf" -> Documents
#
# This allows the script to understand where each file
# should be moved.
# ---------------------------------------------------------

def load_config():

    with open("config.json", "r") as file:
        config = json.load(file)

    return config


# ---------------------------------------------------------
# FUNCTION: create_folder_if_not_exists()
#
# PURPOSE:
# Checks if a folder already exists. If it does not exist,
# it creates the folder.
#
# This prevents errors when organizing files.
# ---------------------------------------------------------

def create_folder_if_not_exists(path):

    if not os.path.exists(path):
        os.makedirs(path)


# ---------------------------------------------------------
# FUNCTION: organize_files(folder_path)
#
# PURPOSE:
# This is the core logic of the project.
#
# Steps:
# 1. Read configuration file
# 2. Scan all files in the folder
# 3. Detect file extension
# 4. Find category from config
# 5. Move file to correct folder
# ---------------------------------------------------------

def organize_files(folder_path):

    config = load_config()

    # List all files inside folder
    files = os.listdir(folder_path)

    for file in files:

        full_path = os.path.join(folder_path, file)

        # Skip directories
        if os.path.isdir(full_path):
            continue

        # Extract extension
        extension = os.path.splitext(file)[1].lower()

        moved = False

        # Check which category this extension belongs to
        for category in config:

            if extension in config[category]:

                category_folder = os.path.join(folder_path, category)

                create_folder_if_not_exists(category_folder)

                destination = os.path.join(category_folder, file)

                shutil.move(full_path, destination)

                print(f"Moved: {file} -> {category}")

                moved = True
                break

        # If extension not found in config
        if not moved:

            other_folder = os.path.join(folder_path, "Others")
            create_folder_if_not_exists(other_folder)

            destination = os.path.join(other_folder, file)

            shutil.move(full_path, destination)

            print(f"Moved: {file} -> Others")


# ---------------------------------------------------------
# MAIN PROGRAM STARTS HERE
# ---------------------------------------------------------

if __name__ == "__main__":

    print("\nSmart File Organizer V0.1\n")

    folder = input("Enter the folder path you want to organize:\n")

    if not os.path.exists(folder):

        print("\nError: Folder does not exist.")

    else:

        organize_files(folder)

        print("\nAll files have been organized successfully.")