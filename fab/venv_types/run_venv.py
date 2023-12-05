import argparse
import subprocess
import sys
import os
import venv

def install_package(package,projec_path):
    subprocess.run([sys.executable, "-m", "pip", "install", package], check=True,cwd=projec_path)

def check_and_install_tools(project_path):
    required_tools = ["flake8", "black", "mypy", "pylint", "isort"]
    for tool in required_tools:
        try:
            result = subprocess.run([tool, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, cwd=project_path)
            version_output = result.stdout.decode("utf-8").strip()
            print(f"{tool} version: {version_output}")
        except subprocess.CalledProcessError:
            print(f"{tool} is not installed. Installing...")
            install_package(tool, project_path)

def run_isort(project_path):
    print("Running isort...")
    subprocess.run(["isort", "."], check=False, cwd=project_path)

def run_flake8(project_path):
    print("Running flake8...")
    subprocess.run(["flake8", "."], check=False, cwd=project_path)

def run_black(project_path):
    print("Running black...")
    subprocess.run(["black", "."], check=False, cwd=project_path)

def run_mypy(project_path):
    print("Running mypy...")
    subprocess.run(["mypy", "."], check=False, cwd=project_path)

def run_pylint(project_path):
    print("Running pylint...")
    subprocess.run(["pylint", "./src"], check=False, cwd=project_path)

def run_fab(project_path):
    check_and_install_tools(project_path)
    run_isort(project_path)
    run_black(project_path)
    run_flake8(project_path)
    run_mypy(project_path)
    run_pylint(project_path)

def create_virtual_environment():
    user_response = input("No virtual environment found. Do you want to create one? (yes/no): ").lower()
    return user_response == "yes"

def create_and_run_virtual_environment(project_path):
    
    venv_dir = os.path.join(project_path, "venv")
    if not os.path.exists(venv_dir):
        venv.create(venv_dir, with_pip=True)
    run_fab(venv_dir)

def main():
    parser = argparse.ArgumentParser(description="Run fab commands in a Python project.")
    parser.add_argument("project_path", help="Path to the Python project")

    args = parser.parse_args()
    project_path = args.project_path

    venv_exists = os.path.exists(os.path.join(project_path, "venv"))

    if venv_exists:
        create_and_run_virtual_environment(project_path)
    else:
        create_venv = create_virtual_environment()
        
        if create_venv:
            create_and_run_virtual_environment(project_path)
        else:
            run_fab(project_path)

if __name__ == "__main__":
    main()
