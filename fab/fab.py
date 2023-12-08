import argparse
import os
import sys
from .venv_types import run_pipenv, run_venv


def create_virtual_environment():
    user_response = input("No virtual environment found. Do you want to create one? (yes/no): ").lower()
    return user_response == "yes"

def create_and_run_virtual_environment(project_path, venv_type):
    if venv_type == "venv":
        run_venv.run_fab(project_path=project_path)
    elif venv_type == "pipenv":
        run_pipenv.run_fab(project_path=project_path)
    else:
        print("Invalid virtual environment type. Using venv as default.")
        run_venv.run_fab(project_path=project_path)


def run_fab_and_save_results(project_path, output_file,venv_type, print_console):
    if print_console:
        create_and_run_virtual_environment(project_path=project_path,venv_type=venv_type)
        print("Those looks like some FABulous suggestions!")
    else:

        try:
            with open(output_file, "w") as file:
                # Redirect standard output and error to the file
                sys.stdout = file
                sys.stderr = file
                create_and_run_virtual_environment(project_path, venv_type=venv_type)

        finally:
            # Reset standard output and error to the console
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__
            print("Those looks like some FABulous suggestions!")

def choose_virtual_environment():
    print("Choose a virtual environment type:")
    print("1. venv")
    print("2. Pipenv")
    choice = input("Enter the number of your choice: ")

    if choice == "1":
        return "venv"
    elif choice == "2":
        return "pipenv"
    else:
        print("Invalid choice. Using venv as default.")
        return "venv"

def main():
    parser = argparse.ArgumentParser(description="Run fab commands in a Python project.")
    parser.add_argument("--project_path", help="Path to the Python project", required=True)
    parser.add_argument("--output_path", help="Location of the format and build suggestion text file", required=False)
    parser.add_argument("-c", help="Print results to console rather than text file", action="store_true")

    args = parser.parse_args()
    project_path = args.project_path

    # Check if a virtual environment exists
    venv_exists = os.path.exists(os.path.join(project_path, "venv"))
    pipenv_exists = os.path.exists(os.path.join(project_path, "Pipfile"))
    # Set the output file name based on the project path
    directory_name = os.path.basename(project_path)
    output_file = args.output_path if args.output_path else os.path.join(project_path, f"{directory_name}_formatting_results.txt")
    print_console = True if args.c else False

    if venv_exists:
        # Virtual environment exists, activate and run fab commands
        venv_type = "venv"
        print(f"{venv_type} found.")
        # Run fab commands and save results to the text file
        run_fab_and_save_results(project_path, output_file, venv_type, print_console)
    elif pipenv_exists:
        venv_type = "pipenv"
        print(f"{venv_type} found.")
        # Run fab commands and save results to the text file
        run_fab_and_save_results(project_path, output_file, venv_type, print_console)

    else:
        # Virtual environment doesn't exist
        create_venv = create_virtual_environment()
        
        if create_venv:
            venv_type = choose_virtual_environment()
            # Run fab commands and save results to the text file
            run_fab_and_save_results(project_path, output_file, venv_type, print_console)
        else:
            # Run fab commands system-wide
            print("It is highly recommended to create a virtual enviroment to run these packages, please re-run the script and create one. Exiting.")


if __name__ == "__main__":
    main()