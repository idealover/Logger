# setup.py

from setuptools import setup, find_packages

setup(
    name='chatlogger',
    version='0.1.0',
    description='Log your OpenAI conversations locally',
    author='Esha Manideep',
    author_email='esha@giga.do',
    packages=find_packages(),
    install_requires=[
        #No third party dependencies
    ],
)
