# Real Estate Manager

[![Build Status](https://travis-ci.org/sirghiny/real_estate_manager.svg?branch=develop)](https://travis-ci.org/sirghiny/real_estate_manager)

[![Coverage Status](https://coveralls.io/repos/github/sirghiny/real_estate_manager/badge.svg?branch=create-more-views)](https://coveralls.io/github/sirghiny/real_estate_manager?branch=create-more-views)

***

### Set-Up:

Clone the repository at:

	https://github.com/sirghiny/real_estate_manager

Create the necessary databases as suggested in `.env.sample`.

Create `.env` in `real_estate_manager`'s root directory:

	`touch .env`

Add and source the environment variables:

	`source .env`

Create a virtual environment (this requires that one has `virtualenv` in the system's python modules):

	`virtualenv venv`

Activate the virtual environment:

	`source venv/bin/activate`

Install all requirements:

	`pip install -r requirements.txt`

Initialize the database and make migrations:

	`python manage.py init`

Everything's now set up!

To run the tests:

	`python -m pytest`

To confirm `flake8` compliance:

	`flake8`

To run the application:

	`python run.py`

The application can be accessed in the `localhost` port number `5000`

URL:
	`http://127.0.0.1:5000/`

*The commands are for Unix based systems*
