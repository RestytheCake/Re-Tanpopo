import subprocess
import sys


def check_and_install_requirements(requirements_file='requirements.txt'):
    """
    Check if the modules listed in the requirements file are installed.
    If not, install them using pip.

    :param requirements_file: Path to the requirements file (default is 'requirements.txt')
    """
    try:
        with open(requirements_file, 'r') as file:
            requirements = file.readlines()

        requirements = [req.strip() for req in requirements if req.strip() and not req.startswith('#')]

        for requirement in requirements:
            try:
                __import__(requirement.split('==')[0])
                print(f"'{requirement}' is already installed.")
            except ImportError:
                print(f"'{requirement}' is not installed. Installing...")
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', requirement])
                print(f"'{requirement}' installed successfully.")
    except FileNotFoundError:
        print(f"The file '{requirements_file}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage
check_and_install_requirements()
