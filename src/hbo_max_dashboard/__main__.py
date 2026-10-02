import os

from .app import create_app

if __name__ == "__main__":
    create_app().run(debug=os.getenv("DASH_DEBUG", "1") == "1")
