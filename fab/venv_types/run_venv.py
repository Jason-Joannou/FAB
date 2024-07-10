import argparse
import os
import shutil
import subprocess
import sys
import venv

OTHER_VENVS = [".venv", "venv"]

def install_package(package, project_path):
    subprocess.run(
        [sys.executable, "-m", "pip", "install", package], check=True, cwd=project_path
    )


def check_and_install_tools(project_path):
    required_tools = ["flake8", "black", "mypy", "pylint", "isort"]
    for tool in required_tools:
        try:
            result = subprocess.run(
                [tool, "--version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                cwd=project_path,
            )
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


def is_virtual_environment_activated():
    return "VIRTUAL_ENV" in os.environ


def activate_virtual_environment(project_path, venv_name):
    print("Activating virtual environment...")
    activate_script = os.path.join(venv_name, "Scripts", "activate")
    subprocess.run(activate_script, shell=True, check=True, cwd=project_path)


def run_fab_commands(project_path):
    commands = ["isort .", "black .", "flake8 .", "mypy .", "pylint ./src"]

    for command in commands:
        subprocess.run(command, shell=True, check=False, cwd=project_path)


def create_virtual_environment(project_path, venv_name):
    venv_dir = os.path.join(project_path, venv_name)
    if not os.path.exists(venv_dir):
        print("Creating virtual environment...")
        venv.create(venv_dir, with_pip=True)


def delete_virtual_environment(project_path, venv_name):
    venv_dir = os.path.join(project_path, venv_name)
    if os.path.exists(venv_dir):
        print("Deleting virtual environment...")
        shutil.rmtree(venv_dir)


def add_to_gitignore(project_path, venv_name):
    gitignore_path = os.path.join(project_path, ".gitignore")
    venv_dir_name = f"\n{venv_name}/"

    with open(gitignore_path, "a") as gitignore_file:
        gitignore_file.write(venv_dir_name)
    print(f"Added {venv_name} to .gitignore")


def remove_from_gitignore(project_path, venv_name):
    gitignore_path = os.path.join(project_path, ".gitignore")
    venv_dir_name = f"{venv_name}/\n"

    if not os.path.exists(gitignore_path):
        return

    with open(gitignore_path, "r") as gitignore_file:
        lines = gitignore_file.readlines()

    with open(gitignore_path, "w") as gitignore_file:
        for line in lines:
            if line.strip() != venv_dir_name.strip():
                gitignore_file.write(line)
    print(f"Removed {venv_name} from .gitignore")


def run_fab(project_path, venv_name):

    if not os.path.exists(project_path):
        print(f"Project path {project_path} does not exist.")
        return

    add_to_gitignore(project_path, venv_name)
    create_virtual_environment(project_path=project_path, venv_name=venv_name)
    activate_virtual_environment(project_path=project_path, venv_name=venv_name)

    # Prepare the command to activate and run all in a subprocess
    activate_and_run = f'cmd /c "{venv_name}\\Scripts\\activate && python -m pip install --upgrade pip setuptools wheel && '
    if os.name != "nt":  # Unix-Like
        activate_and_run = f'bash -c "source {venv_name}/bin/activate && python -m pip install --upgrade pip setuptools wheel && '

    tools_install_commands = " && ".join(
        [
            f"python -m pip install {tool}"
            for tool in ["flake8", "black", "mypy", "pylint", "isort"]
        ]
    )

    OTHER_VENVS.append(venv_name)
    formatted_paths = [f"./{env}/" for env in OTHER_VENVS]
    isort_skips = " --skip ".join(OTHER_VENVS)
    black_skips = " --exclude ".join(OTHER_VENVS)
    flake_skips = ",".join(OTHER_VENVS)
    mypy_skips = " --exclude ".join(formatted_paths)
    pylint_skips = " --ignore=".join(formatted_paths)+" "
    OTHER_VENVS.pop()
    tools_commands = " && ".join(
        [
            f"isort . --skip {isort_skips}",
            f"black . --exclude {black_skips}",
            f"flake8 . --exclude {flake_skips}",
            f"mypy . --exclude {mypy_skips}",
            f"pylint ./src --ignore={pylint_skips}",
        ]
    )

    full_command = (
        activate_and_run + tools_install_commands + " && " + tools_commands + '"'
    )
    
    try:
        subprocess.run(full_command, shell=True, cwd=project_path)
    finally:
        delete_virtual_environment(project_path=project_path, venv_name=venv_name)
        remove_from_gitignore(project_path, venv_name)


def main():
    parser = argparse.ArgumentParser(
        description="Run fab commands in a Python project."
    )
    parser.add_argument("project_path", help="Path to the Python project")
    args = parser.parse_args()

    project_path = args.project_path

    run_fab(project_path=project_path, venv_name="testVenv")


if __name__ == "__main__":
    main()
