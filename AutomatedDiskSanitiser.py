####################################################################
#  Program Name :      Duplicate File Remover
#  Description :       This application scans a directory, detects
#                      duplicate files using MD5 checksum and deletes
#                      extra copies while keeping one original file.
#  Input :             Directory path
#  Output :            Displays and removes duplicate files
#  Author :            Rukmini Jayhind Gaikwad
#  Date :              18/02/2026
####################################################################

####################################################################
# import modules
####################################################################

import hashlib
import os

####################################################################
#  Function Name :      calculate_checksum
#  Description :       Calculates MD5 hash value of a file
#  Input :             file_name (string)
#  Output :            Returns hexadecimal hash value
#####################################################################


def CalculateCheckSum(FileName):

    hobj = hashlib.md5()

    try:
        with open(FileName, "rb") as fobj:
            while True:
                Buffer = fobj.read(4096)   # FIXED chunk size
                if not Buffer:
                    break
                hobj.update(Buffer)

        return hobj.hexdigest()

    except Exception:
        return None

####################################################################
#  Function Name :     find_duplicate
#  Description :       Traverses directory and finds duplicate files
#  Input :             directory_name (string)
#  Output :            Dictionary containing duplicate file paths
####################################################################

def FindDuplicate(DirectoryName):

    if not os.path.exists(DirectoryName):
        print("Directory does not exist")
        return {}

    if not os.path.isdir(DirectoryName):
        print("Path is not a directory")
        return {}

    Duplicate ={}

    for FolderName, SubFolderName, FileNames in os.walk(DirectoryName):
        for fname in FileNames:

            path = os.path.join(FolderName, fname)

            checksum = CalculateCheckSum(path)

            if checksum is None:
                continue

            Duplicate.setdefault(checksum, []).append(path)

    return Duplicate

####################################################################
#  Function Name :     display_result
#  Description :       Displays list of duplicate files
#  Input :             Dictionary
#  Output :            Prints duplicate file names
####################################################################

def DisplayResult(MyDict):

    Result = [files for files in MyDict.values() if len(files) > 1]

    if not Result:
        print("No duplicate files found")
        return

    print("\nDuplicate Files:\n")

    for group in Result:
        print("--------------------------------")
        for file in group:
            print(file)


####################################################################
#  Function Name :     delete_duplicate
#  Description :       Deletes extra duplicate files from directory
#  Input :             Path (string)
#  Output :            Deletes files and shows total count
####################################################################

def DeleteDuplicate(Path):

    MyDict = FindDuplicate(Path)

    Result = [files for files in MyDict.values() if len(files) > 1]

    if not Result:
        print("No duplicate files to delete")
        return

    confirm = input("\nDelete duplicates? (yes/no): ").lower()
    if confirm != "yes":
        print("Operation cancelled")
        return

    Deleted = 0

    for group in Result:
        original = group[0]  # keep first file

        for file in group[1:]:
            try:
                os.remove(file)
                print("Deleted:", file)
                Deleted += 1
            except Exception:
                pass

    print("\nTotal Deleted Files:", Deleted)

####################################################################
#  Function Name :     main
#  Description :       Entry point of the application
####################################################################

def main():
    path = input("Enter directory path: ")
    DeleteDuplicate(path)


if __name__ == "__main__":
    main()
