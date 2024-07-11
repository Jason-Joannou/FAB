# Format and Build (FAB)

The Format and Build (FAB) module is a command-line interface (CLI) tool designed to help users format and build their repositories, ensuring good practices and smooth pull requests (PRs). FAB serves as a pre-CI (Continuous Integration) check to minimize errors that might occur during the CI pipeline build in a PR.

## How to Run FAB

To get started with FAB:

1. **Fork and Clone**: First, fork the FAB repository on GitHub, then clone it to your local machine.
2. **Navigate to the Project Root**: Ensure the root of the project is set to the FAB directory.
3. **Run the Command**: Execute the following command:
   ```
   python -m fab --project_path {project_path}
   ```

This command will run the FAB module on the specified project path. The module will:

- Create a virtual environment within the project directory.
- Download the necessary tools for code formatting.
- Run these tools on the project repository.
- Print the output to the console.
- Delete the newly created venv from your repository after the formating is complete (garbage collection)

To generate a detailed report, use the `--generate_report` argument. This will route all CLI output to a text file in the project's root directory.

For additional information on the CLI options, run:
```
python -m fab -h
```

## Tools Used in FAB

**isort**
- A Python utility for sorting imports in your Python files to maintain a consistent order.

**Black**
- An uncompromising code formatter for Python. It ensures that your code follows the PEP 8 style guide without any manual intervention.

**Flake8**
- A tool for enforcing style guide compliance. It checks your code for errors, ensures adherence to coding standards, and highlights code complexity.

**mypy**
- A static type checker for Python. It helps in ensuring that your code adheres to type hints and detects type errors early.

**pylint**
- A comprehensive source code analyzer. It checks for programming errors, enforces a coding standard, and looks for code smells.
