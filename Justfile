# run once to install deps from requirements.txt
install:
    pip install -r requirements.txt



# opens a jupyter notebook
notebook:
    jupyter notebook 2> /dev/null &


test:
    pytest test


check:
    mypy aft test
    flake8 --max-line-length=100 aft test
    just test
    black --check --diff --color aft test


# ~~~~~~~~~~~~~~~~~~ Clean up ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# formats any python file
format PYTHON-FILE:
    isort {{PYTHON-FILE}}
    docformatter --in-place {{PYTHON-FILE}}
    black {{PYTHON-FILE}}


format-dir DIR:
    find {{DIR}} -iname '*.py' -exec just format {} \;

format-aft:
    just format-dir aft

format-tests:
    just format-dir test

format-all:
    just format-aft
    just format-tests
