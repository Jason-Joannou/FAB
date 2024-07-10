import argparse
import os
import sys

from .venv_types import run_venv


def create_virtual_environment():
    user_response = input(
        "No virtual environment found. Do you want to create one? (yes/no): "
    ).lower()
    return user_response == "yes"


def create_and_run_virtual_environment(project_path, venv_name, generate_report):
    run_venv.run_fab(project_path=project_path, venv_name=venv_name, generate_report=generate_report)


def run_fab_and_save_results(project_path, venv_name, generate_report):
    create_and_run_virtual_environment(project_path=project_path, venv_name=venv_name, generate_report=generate_report)
    print("Those looks like some FABulous suggestions!")


def main():
    parser = argparse.ArgumentParser(
        description="Run fab commands in a Python project."
    )
    parser.add_argument(
        "--project_path", help="Path to the Python project", required=True
    )
    parser.add_argument(
        "--venv_name",
        help="Virtual Enviroment Name within the project. Defaults to venv.",
        required=False,
        default="format_venv",
    )
    parser.add_argument("--generate_report", action="store_true", help="Generate formatting report", default=False)

    args = parser.parse_args()
    project_path = args.project_path
    generate_report = args.generate_report

    venv_name = args.venv_name
    run_fab_and_save_results(project_path, venv_name, generate_report)


if __name__ == "__main__":
    main()
