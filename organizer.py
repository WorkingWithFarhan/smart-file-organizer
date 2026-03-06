"""
Smart File Organizer
Version: V0.2

This project automatically organizes files in a folder
based on their file extensions.

New in V0.2:
A logging system that records every file movement with
a timestamp so users can track what the program did.

Author: Farhan
"""

import os
import shutil
import json
from datetime import datetime


# ---------------------------------------------------
# FUNCTION: load_config()
#
# This function reads the config.json file which
# contains the mapping of file extensions to
# folder categories.
#
# Example inside config.json:
#
# {
#   "Images": [".png", ".jpg"],
#   "Documents": [".pdf", ".txt"]
# }
#
# This allows the program to remain flexible.
# If users want to add more file types later,
# they only need to modify config.json.
# ---------------------------------------------------

def load_config():

    with open("config.json", "r") as file:
        config = json.load(file)

    return config


# ---------------------------------------------------
# FUNCTION: write_log()
#
# This function writes a log entry to logs.txt
#
# Each entry contains:
# - timestamp
# - file name
# - destination folder
#
# Logs are appended instead of overwritten so
# users can keep a full history of operations.
# ---------------------------------------------------

def write_log(message):

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = f"[{current_time}] {message}\n"

    with open("logs.txt", "a") as log_file:
        log_file.write(log_entry)


# ---------------------------------------------------
# FUNCTION: create_folder_if_missing()
#
# This checks whether a folder already exists.
# If not, the folder will be created.
#
# This prevents errors when moving files into
# directories that do not yet exist.
# ---------------------------------------------------

def create_folder_if_missing(path):

    if not os.path.exists(path):
        os.makedirs(path)


# ---------------------------------------------------
# FUNCTION: organize_files()
#
# This is the main engine of the program.
#
# Steps performed:
#
# 1. Load configuration rules
# 2. Scan all files in the target folder
# 3. Detect file extension
# 4. Match extension with category
# 5. Create category folder if needed
# 6. Move file to correct folder
# 7. Record the action in logs.txt
# ---------------------------------------------------

def organize_files(folder_path):

    config = load_config()

    files = os.listdir(folder_path)

    for file in files:

        full_path = os.path.join(folder_path, file)

        # Skip folders
        if os.path.isdir(full_path):
            continue

        extension = os.path.splitext(file)[1].lower()

        moved = False

        for category in config:

            if extension in config[category]:

                category_folder = os.path.join(folder_path, category)

                create_folder_if_missing(category_folder)

                destination = os.path.join(category_folder, file)

                shutil.move(full_path, destination)

                message = f"Moved {file} → {category}"

                print(message)

                write_log(message)

                moved = True

                break

        # If extension not found in config
        if not moved:

            other_folder = os.path.join(folder_path, "Others")

            create_folder_if_missing(other_folder)

            destination = os.path.join(other_folder, file)

            shutil.move(full_path, destination)

            message = f"Moved {file} → Others"

            print(message)

            write_log(message)


# ---------------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------------

if __name__ == "__main__":

    print("\nSmart File Organizer V0.2\n")

    folder = input("Enter the folder path you want to organize:\n")

    if not os.path.exists(folder):

        print("Error: Folder does not exist.")

    else:

        organize_files(folder)

        print("\nOrganization completed successfully.")