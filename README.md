# WinBet - Web Betting Platform Setup Instructions

## Overview

This repository contains the WinBet platform, a web-based betting application that allows users to create and accept bets on various future events, such as sports game outcomes, election winners, or natural catastrophes. The platform simulates financial control and provides an intuitive interface for users to interact. Below are the steps to set up and run this project locally.

## Prerequisites

Ensure you have the following software installed on your machine:

- Python 3.x
- pip (Python package installer)

Additionally, you need the following Python packages:

- Flask
- sqlite3 (comes with Python standard library)
- datetime
- secure-smtplib

## Installation Guide

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Luerfel/Integrador-ll
   cd Integrador-ll
   ```

2. **Create and Activate Virtual Environment**
   It's recommended to create a virtual environment to manage dependencies.

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies**
   Install the required Python packages listed in the `requirements.txt`. If it is not provided, you can manually install the dependencies:

   ```bash
   pip install Flask secure-smtplib
   ```

   For `datetime`, this package is included in the Python standard library, so no additional installation is required.

4. **Set Up the Database**
   You can use the `bd.py` script located in the `etc/` directory to create the database:

   ```bash
   python etc/bd.py
   ```

   This script will initialize the SQLite database at `data/database.db`.

5. **Set Flask Secret Key**
   Update the secret key to ensure security. The secret key used in this code is currently `'macaco'`. You should change this to a more secure value:

   ```python
   app.secret_key = 'your_secret_key'
   ```

6. **Run the Application**
   Run the application using Flask:

   ```bash
   python app.py
   ```

   By default, the app will run at [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

## Features

- **Betting Platform**: Allows users to create and accept bets on future events.
- **Financial Simulation**: Simulates financial control for managing user bets and winnings.
- **SQLite Database**: Stores data locally in `data/database.db`.
- **Flask Flash Messages**: Used to display notifications to the user.
- **SMTP Integration**: Sends emails using the `smtplib` library.

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript for validations and functionalities related to the frontend.
- **Backend**: Python and Flask.
- **Database**: SQLite.
- **Development Environment**: Visual Studio Code (VSCode).
- **Frameworks**: None.

## Directory Structure

- `app.py`: Main application file.
- `data/`: Directory containing the SQLite database (`database.db`).
- `templates/`: Directory containing HTML files used for rendering web pages.
- `static/`: Directory containing JavaScript and CSS files for frontend functionality.
- `etc/`: Directory containing utility scripts such as `bd.py` for database creation.

## Running Tests

- Add any unit tests you may have in a separate `tests/` directory.

## Troubleshooting

- Ensure that Flask is installed and accessible in your virtual environment.
- Make sure you provide proper permissions for accessing the database (`database.db`).

## Contributing

Feel free to fork this repository and make any changes or improvements. Pull requests are welcome!

### Contributors

- Matheus Augusto Mendonça [@Luerfel](https://github.com/Luerfel)
- Felipe Zerbinati Felipe Coelho [@FelipeZerbinati](https://github.com/FelipeZerbinati)
- Fernando Furlanetto Cardoso [@Furlanets](https://github.com/Furlanets)
- Beatriz Kamien Tehzy [@beaktz](https://github.com/beaktz)
- Gustavo Ferreira Carvalho [@GutyFC](https://github.com/GutyFC)

## License

This project is open source and available under the [MIT License](LICENSE).

