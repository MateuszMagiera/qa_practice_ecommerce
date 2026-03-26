import os

correct = {
    "email": os.environ["CORRECT_EMAIL"],
    "password": os.environ["CORRECT_PASSWORD"],
}

incorrect = {
    "email": os.environ["INCORRECT_EMAIL"],
    "password": os.environ["INCORRECT_PASSWORD"],
}