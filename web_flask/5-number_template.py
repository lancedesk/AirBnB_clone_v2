#!/usr/bin/python3
"""
This script starts a Flask web application
"""

from flask import Flask, render_template
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def hello_hbnb():
    """
    Route that displays "Hello HBNB!"
    """
    return "Hello HBNB!"


@app.route('/hbnb')
def hbnb():
    """
    Route that displays "HBNB"
    """
    return "HBNB"


@app.route('/c/<text>')
def c_text(text):
    """
    Route that displays "C " followed by the value of the text variable
    """
    return "C {}".format(text.replace('_', ' '))


@app.route('/python')
@app.route('/python/<text>')
def python_text(text="is cool"):
    """
    Route that displays "Python " followed by the value of the text variable
    """
    return 'Python {}'.format(text.replace('_', ' '))


@app.route('/number/<int:n>')
def text_if_int(n):
    """
    Route that displays "n is a number" only if n is an integer
    """
    return "{:d} is a number".format(n)


@app.route('/number_template/<int:n>')
def template_int(n):
    """
    Route that displays an HTML page if n is an integer
    """
    return render_template('5-number.html', number=n)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
