import os

# Define the base directory and static image directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_img_dir = os.path.join(BASE_DIR, "public", "img")

def rename_png_files_in_subdirectories(directory):
    # Walk through all directories and files
    for root, dirs, files in os.walk(directory):
        for filename in files:
            # Check if the file has a .PNG extension
            if filename.endswith('.PNG'):
                # Create the new filename with .png extension
                new_filename = filename[:-4] + '.png'
                # Get the full path of the old and new filenames
                old_file_path = os.path.join(root, filename)
                new_file_path = os.path.join(root, new_filename)
                # Rename the file
                os.rename(old_file_path, new_file_path)
                print(f'Renamed: {old_file_path} to {new_file_path}')
            # Check if the file has a .PNG extension
            if filename.endswith('.JPG'):
                # Create the new filename with .png extension
                new_filename = filename[:-4] + '.jpg'
                # Get the full path of the old and new filenames
                old_file_path = os.path.join(root, filename)
                new_file_path = os.path.join(root, new_filename)
                # Rename the file
                os.rename(old_file_path, new_file_path)
                print(f'Renamed: {old_file_path} to {new_file_path}')

# Run the function
rename_png_files_in_subdirectories(static_img_dir)
