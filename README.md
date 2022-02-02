# RCPY_Boilerplate

**WARNING: WORK IN PROGRESS**

A Python boilerplate inspired from the Maven Standard Directory Layout

## Project organization
Warning on resources package name (avoid conflict whith python folder)

## Pipenv (Pipfile) versus requirements.txt project

## Run tests

## Build

>```sh
>python setup.py clean --all \
>   && rm -rf dist \
>   && rm -rf *.egg-info \
>   && python setup.py bdist_wheel sdist
>```

## Delivery *(on https://pypi.org/)*

### Prerequisite

`twine` is required for this part
>```sh
> pip install twine
>```
***Note:** As it is a common delivery tool, you can install it on your global python environment. 
However you can also install it on your pipenv virtual environment*

### Delivery command

>```sh
>twine upload dist/*
>```

***Note:** Obviously, this command must be run after the [Build](#build) one*

pip install -e .

