#
# flask_app.py
#
# A spike for testing the usage of the Flask framework for hosting an HTTP server using Python.
#
# Author: Kays Beslen
# Last modified: 29/03/25
#

from flask import Flask


def create_app() -> Flask:
    """
        Initialises a Flask HTML web server.

        :return Flask: the Flask server application
    """
    app = Flask(__name__)

    @app.route('/')
    def index() -> str:
        """
            Defines what will be presented in the root directory of the webpage exported by the Flask server.

            :return str: the string to be displayed on the webpage at the specified route
        """
        return "Flask test."

    return app


if __name__ == '__main__':
    flask_app = create_app()
    flask_app.run()
