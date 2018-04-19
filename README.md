# Real Estate Manager

***

### Set-Up:

Clone the repository at:

	https://sirghiny@bitbucket.org/cygnetanalytics/rem.git

Rename the cloned directory to `rem` and move into it. 

Create the necessary databases as suggested in `.env.sample`.

Create `.env` in `rem`'s root directory:

	`touch .env`

Source the environment variables:

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

	`pytest`

To confirm `flake8` compliance:

	`flake8`

To run the application:

	`python run.py`

The application can be accessed in the `localhost` port number `5000`

URL:
	`http://127.0.0.1:5000/`

*The commands are for Unix based systems*
