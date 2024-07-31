import os
import shutil

from main.modules.path import get_project_root

def merge_files(source_dir, output_file, include_dirs, script_name, include_files):
    # Ensure the output directory exists
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    print(f"Output directory: {output_dir}")

    with open(output_file, 'w', encoding='utf-8') as outfile:
        # Traverse the source directory
        for root, dirs, files in os.walk(source_dir):
            print(f"Traversing directory: {root}")
            print(f"Files in directory: {files}")
            # Include only specified directories
            for d in include_dirs:
                include_path = os.path.join(source_dir, d)
                if os.path.commonpath([root, include_path]) == include_path:
                    print(f"Directory {root} is in the include list")
                    # Process files
                    for file_name in files:
                        file_path = os.path.join(root, file_name)
                        print(f"Processing file: {file_path}")

                        relative_file_path = os.path.relpath(file_path, source_dir)
                        print(f"Relative file path: {relative_file_path}")

                        # Skip the script file itself and non-Python files
                        if file_name == script_name:
                            print(f"Skipping script file: {file_name}")
                            continue
                        if not file_name.endswith('.py'):
                            print(f"Skipping non-Python file: {file_name}")
                            continue

                        # Skip files not in the include list
                        if not any(relative_file_path.endswith(f) for f in include_files):
                            print(f"Skipping file not in include list: {relative_file_path}")
                            continue

                        # Skip files in the output directory
                        if output_dir in file_path:
                            print(f"Skipping file in output directory: {file_name}")
                            continue

                        print(f"Merging file: {file_path}")
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            content = infile.read()
                            outfile.write(f'# Content from {file_path}\n')
                            outfile.write(content)
                            outfile.write('\n\n')
                else:
                    print(f"Directory {root} is not in the include list")

def copy_img_folder(source_img_dir, target_img_dir):
    print(f"Copying img folder from {source_img_dir} to {target_img_dir}")
    if os.path.exists(source_img_dir):
        if os.path.exists(target_img_dir):
            shutil.rmtree(target_img_dir)
            print(f"Removed existing target img directory: {target_img_dir}")
        shutil.copytree(source_img_dir, target_img_dir)
        print(f"Copied {source_img_dir} to {target_img_dir}")
    else:
        print(f"Source img folder {source_img_dir} does not exist.")

if __name__ == "__main__":
    source_directory = get_project_root()  # Adjust this relative path as needed
    output_directory = 'com'
    output_filename = 'output.py'
    script_name = 'merge_code.py'  # Name of this script

    # Directories to include
    include_directories = ['main']  # Add other directories to include if needed

    # Files to include
    include_files = ['helper.py', 'refresher.py', 'AnimeViewer.py', 'globalmanager.py', 'details.py']  # Add the specific files to include

    # Print the include files list
    print(f"Files to include: {include_files}")

    # Define the path for the output file
    output_file_path = os.path.join(source_directory, output_directory, output_filename)
    print(f"Output file path: {output_file_path}")

    # Run the merge operation
    merge_files(source_directory, output_file_path, include_directories, script_name, include_files)
    print(f"All files have been merged into {output_file_path}")

    # Copy the img folder
    source_img_dir = os.path.join(source_directory, 'main/img')
    target_img_dir = os.path.join(source_directory, output_directory, 'img')
    copy_img_folder(source_img_dir, target_img_dir)