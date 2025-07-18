from setuptools import setup, find_packages

setup(
    name="maikol-utils",
    version="0.0.1",
    packages=find_packages(), #find_packages(where="src"),
    author="Miquel Gómez",
    description="Python module with some utils for every day code that I've usefull lately while working. Print, print colors, print warnings, print errors, save files, load files, clear bash",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=[
    ]
)
