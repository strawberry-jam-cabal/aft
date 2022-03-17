# run once to install deps from requirements.txt
install:
    pip install -r requirements.txt



# opens a jupyter notebook
notebook:
    jupyter notebook 2> /dev/null &


test:
    pytest test

