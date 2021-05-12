# warring-wizards
Flask web application which runs an online multiplayer combat clicker game
---
Final project for the course CS50, taken through Harvard Extension School.
## Instructions for running
This app runs on Heroku at "https://warring-wizards.herokuapp.com", via GitHub deployment. However, it can also be run locally.

This app runs on Python 3.8.2, but also works with some other recent versions of Python 3.

To run this application locally, first clone this repository to the desired location on your computer.

Before the application can run, the necessary dependencies in requirements.txt must be installed. See https://docs.python.org/3/tutorial/venv.html for instructions on how to create a virtual environment and install the dependencies in requirements.txt. Virtual environments will automatically handle adding libraries to PATH for command line execution, but if you choose to not use a virtual environment, Flask must be added to PATH manually.

Once the requirements are satisfied, execute "flask run" in the warring-wizards main directory from a terminal. The app will then run at "http://localhost:5000/".

Note that this app cannot be run in CS50 IDE, due to conflictions with the flask-socketio library.
