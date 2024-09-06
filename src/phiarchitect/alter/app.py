"""
run the main app
"""
from .alter import Alter


def run() -> None:
    reply = Alter().run()
    print(reply)
