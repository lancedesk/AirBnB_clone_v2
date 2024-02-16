#!/usr/bin/python3
"""
This script starts a Flask web application
"""

from models import storage
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """
    Route handler for the '/hbnb' endpoint.
    Fetches data from storage engine & renders the '100-hbnb.html' template.

    Returns:
    HTML template rendering the data fetched from the storage engine.
    """
    states = storage.all("State")
    amenities = storage.all("Amenity")
    places = storage.all("Place")
    return render_template("100-hbnb.html",
                           states=states, amenities=amenities, places=places)


@app.teardown_appcontext
def teardown(exc):
    """
    Teardown method to remove current SQLAlchemy Session after each request.
    """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
