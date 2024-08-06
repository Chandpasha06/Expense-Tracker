# Expense Tracker

A simple web application for tracking expenses using Flask, SQLAlchemy, and Chart.js. The application allows users to register, log in, add expenses, view summaries, and visualize expense data.

## Features

- User registration and login
- Add and categorize expenses
- View expense summaries by category
- Visualize expenses using a pie chart
- Responsive design

## Technologies Used

- **Flask**: Web framework for building the application
- **SQLAlchemy**: ORM for database management
- **WTForms**: Form handling
- **Chart.js**: JavaScript library for rendering charts
- **Bootstrap**: CSS framework for styling

## Installation

### Prerequisites

- Python 3.8 or higher
- `pip` (Python package installer)

### Create a virtual environment:
- python -m venv venv
### Activate the virtual environment:
- On Windows
- - venv\Scripts\activate
- On macOS/Linux
- - source venv/bin/activate
### Install the required packages:
- pip install -r requirements.txt

### Create the database:
- FLASK_APP=app.py
- flask db init
- flask db migrate -m "Initial migration"
- flask db upgrade

### Run the application:
- flask run

The application should be accessible at http://127.0.0.1:5000.


### Explanation:

- **Introduction**: Brief description of the project and its features.
- **Technologies Used**: Lists the technologies and libraries used in the project.
- **Installation**: Steps to set up the development environment and run the project.
- **Usage**: Basic instructions on how to use the application.
- **Contributing**: Guidelines for contributing to the project.
- **License**: Licensing information.
- **Contact**: Contact details for feedback or questions.

Feel free to modify the links and contact information as needed.


