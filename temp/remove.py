import os

def remove_meta_json_files(directory):
    """Recursively remove all _meta.json files from the given directory."""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == "_meta.json":
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"🗑️ Deleted: {file_path}")
                except Exception as e:
                    print(f"❌ Error deleting {file_path}: {e}")

# Set the base directory
base_directory = r"D:\saberprojects\kasra\kasra-docs\pages"

# Run the deletion function
remove_meta_json_files(base_directory)
