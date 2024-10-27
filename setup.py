#setup.py
from setuptools import setup, find_packages

setup(
    name="myllput",
    version="1.0",
    description="a simple (and bad) input listener and sender helper for pynput",
    author="Fightingpainter",
    author_email="lechimnorepe@gmail.com",
    packages=find_packages(),
    install_requires=["pynput"],
)
