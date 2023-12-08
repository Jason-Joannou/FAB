import argparse
import subprocess
import sys
import os

def install_package(package, projec_path):
    subprocess.run([sys.executable, "-m", "pipenv", "install", package], check=True, cwd=projec_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"Installed {package}")

def check_and_install_tools(project_path):
    required_tools = ["flake8", "black", "mypy", "pylint", "isort"]
    for tool in required_tools:
        try:
            result = subprocess.run(["pipenv", "run", tool, "--version"], check=True, cwd=project_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            version_output = result.stdout.decode("utf-8").strip()
            print(f"{tool} version: {version_output}\n")
        except subprocess.CalledProcessError:
            print(f"{tool} is not installed. Installing...")
            install_package(tool, project_path)

def display_section_header(header):
    print(f"\n{'='*40}")
    print(f"{header}")
    print(f"{'='*40}")

def display_tool_output(tool, output):
    print(f"{tool} suggestions:")
    print("-" * 40)
    print(output.strip())
    print("-" * 40)

def run_isort(project_path):
    display_section_header("Running isort...")
    result = subprocess.run(["pipenv", "run", "isort", "."], check=False, cwd=project_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    display_tool_output("Isort", result.stdout.decode("utf-8"))

def run_flake8(project_path):
    display_section_header("Running flake8...")
    result = subprocess.run(["pipenv", "run", "flake8", "."], check=False, cwd=project_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    display_tool_output("Flake8", result.stdout.decode("utf-8"))

def run_black(project_path):
    display_section_header("Running black...")
    result = subprocess.run(["pipenv", "run", "black", "."], check=False, cwd=project_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #display_tool_output("Black", result.stdout.decode("utf-8"))
    display_tool_output("Black", result.stderr.decode("utf-8"))

def run_mypy(project_path):
    display_section_header("Running mypy...")
    result = subprocess.run(["pipenv", "run", "mypy", "."], check=False, cwd=project_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    display_tool_output("Mypy", result.stdout.decode("utf-8"))

def run_pylint(project_path):
    display_section_header("Running pylint...")
    result = subprocess.run(["pipenv", "run", "pylint", "./src"], check=False, cwd=project_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    display_tool_output("Pylint", result.stdout.decode("utf-8"))

def run_fab(project_path):
    check_and_install_tools(project_path)
    run_isort(project_path)
    run_black(project_path)
    run_flake8(project_path)
    run_mypy(project_path)
    run_pylint(project_path)
    print("All checks have finished running!")

def create_virtual_environment():
    user_response = input("No virtual environment found. Do you want to create one? (yes/no): ").lower()
    return user_response == "yes"

def create_and_run_virtual_environment(project_path):
    # For Pipenv
    pipenv_file = os.path.join(project_path, "Pipfile")
    if os.path.exists(pipenv_file):
        run_fab(project_path)
    else:
        print("Pipfile not found. Creating a new Pipenv environment...")
        
        # Create a Pipenv environment
        subprocess.run(["pipenv", "install"], check=True, cwd=project_path)

        # Check if the environment was created successfully
        if os.path.exists(pipenv_file):
            print("Pipenv environment created successfully.")
            run_fab(project_path)
        else:
            print("Failed to create Pipenv environment. Exiting.")


def main():
    parser = argparse.ArgumentParser(description="Run fab commands in a Python project.")
    parser.add_argument("project_path", help="Path to the Python project")

    args = parser.parse_args()
    project_path = args.project_path

    # Check if a virtual environment exists
    pipenv_exists = os.path.exists(os.path.join(project_path, "Pipfile"))
    output_file = "./format.txt"

    if pipenv_exists:
        # Virtual environment exists, activate and run fab commands
        create_and_run_virtual_environment(project_path)
    else:
        # Virtual environment doesn't exist
        create_venv = create_virtual_environment()
        
        if create_venv:
            create_and_run_virtual_environment(project_path)
        else:
            print("It is strongly reccommended to create a virtual enviroment, please create and re-run.")

if __name__ == "__main__":
    main()
