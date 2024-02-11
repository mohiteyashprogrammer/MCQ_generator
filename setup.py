from setuptools import setup,find_packages
from typing import List

NAME = "MCQ Generator"
VERSION = "0.1"
AUTHOR = "yash mohite"
AUTHOR_EMAIL = "mohite.yash@gmail.com"
HYPHAN_E_DOT = "-e ."

def get_requirements(filepath:str)->[str]:
    requirements = []

    with open(filepath) as file_obj:
        requirements = file_obj.readlines()
        requirements = [i.replace("\n","") for i in requirements]

        if HYPHAN_E_DOT in requirements:
            requirements.remove(HYPHAN_E_DOT)

    return requirements

setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    packages=find_packages(),
    install_required =    get_requirements("requirements.txt")
)