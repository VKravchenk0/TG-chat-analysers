This is a flask app. Entry point is `app.py`.
Contains two pages/sub-apps:
1. Language usage counter (see `src/blueprints/langugage_count_blueprint.py`, http://localhost:5000/language)
2. Most active members counter (see `src/blueprints/most_active_members_blueprint.py`, http://localhost:5000/most-active-members)

Quickstart:
1. (Optional) Create virtual environment.
2. Install dependencies: `pip install requirements.txt`
3. Run the app: `flask run` or `python app.py`
4. Go to http://localhost:5000

How to use:
1. Using Telegram desktop, export telegram chat in json format with text only (without pictures/videos).
2. Go to the respective page (`/language` or `/most-active-members`).
3. Fill the form if needed and pick a file from the previous step. Submit the form.
4. Wait until the processing is over, and open the provided link.