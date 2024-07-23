import os
import shutil


def merge_files(source_dir, output_file, exclude_dirs, script_name):
    # Ensure the output directory exists
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        # Traverse the source directory
        for root, dirs, files in os.walk(source_dir):
            # Exclude specified directories from being traversed
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            # Process files
            for file_name in files:
                file_path = os.path.join(root, file_name)

                # Skip the script file itself and non-Python files
                if file_name == script_name or not file_name.endswith('.py'):
                    continue

                # Skip files in the output directory
                if output_dir in file_path:
                    continue

                print(f'Merging file: {file_path}')
                with open(file_path, 'r', encoding='utf-8') as infile:
                    content = infile.read()
                    outfile.write(f'# Content from {file_path}\n')
                    outfile.write(content)
                    outfile.write('\n\n')


def copy_img_folder(source_img_dir, target_img_dir):
    if os.path.exists(source_img_dir):
        if os.path.exists(target_img_dir):
            shutil.rmtree(target_img_dir)
        shutil.copytree(source_img_dir, target_img_dir)
        print(f'Copied {source_img_dir} to {target_img_dir}')
    else:
        print(f'Source img folder {source_img_dir} does not exist.')


if __name__ == "__main__":
    source_directory = '../../'  # Adjust this relative path as needed
    output_directory = 'com'
    output_filename = 'output.py'
    script_name = 'merge_code.py'  # Name of this script

    # Directories to exclude
    exclude_directories = [output_directory, 'venv']  # Add other directories to exclude if needed

    # Define the path for the output file
    output_file_path = os.path.join(source_directory, output_directory, output_filename)

    # Run the merge operation
    merge_files(source_directory, output_file_path, exclude_directories, script_name)
    print(f'All files have been merged into {output_file_path}')

    # Copy the img folder
    source_img_dir = os.path.join(source_directory, 'img')
    target_img_dir = os.path.join(source_directory, output_directory, 'img')
    copy_img_folder(source_img_dir, target_img_dir)
