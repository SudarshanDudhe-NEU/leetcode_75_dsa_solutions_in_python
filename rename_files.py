import os
import re


def rename_files(directory):
    # Walk through the directory and its subdirectories
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Get the full path of the file
            old_file_path = os.path.join(root, file)

            # Split the file name and extension
            file_name, file_extension = os.path.splitext(file)

            # Replace spaces with underscores and remove dots (except for the extension)
            new_file_name = file_name.replace(
                " ", "_").replace(".", "") + file_extension

            # Extract the problem number from the file name (if it exists)
            problem_number_match = re.search(r"^\d+", new_file_name)
            if problem_number_match:
                problem_number = problem_number_match.group(0)
                # Remove any duplicate problem number prefix
                new_file_name = re.sub(
                    rf"^{problem_number}_*", "", new_file_name)
                # Prepend the problem number to the file name (only once)
                new_file_name = f"{problem_number}_{new_file_name}"

            # Construct the new file path
            new_file_path = os.path.join(root, new_file_name)

            # Rename the file
            if old_file_path != new_file_path:
                os.rename(old_file_path, new_file_path)
                print(f"Renamed: {old_file_path} -> {new_file_path}")


# Specify the directory to process
directory_to_process = "LeetCode_Solutions"

# Run the renaming script
rename_files(directory_to_process)
