# Run once to install deps from requirements.txt
install:
    pip install -r requirements.txt


# Open a jupyter notebook
notebook:
    jupyter notebook 2> /dev/null &


# Run unit tests
test:
    pytest test


# Runs all validation done in CI
check:
    # type check
    mypy aft test
    # lint
    flake8 --max-line-length=100 aft test
    # unit test
    just test
    # Enforce formatting
    isort --check aft test
    docformatter --check --recursive aft test
    black --check --diff --color aft test


# Format a python file or directory
format WHAT:
    isort {{WHAT}}
    docformatter --recursive --in-place {{WHAT}}
    black {{WHAT}}


# Format all code
format-all:
    just format aft
    just format test
