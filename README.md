# RCPY_Boilerplate

**WARNING: WORK IN PROGRESS**

A Python boilerplate inspired from the Maven Standard Directory Layout

## Project organization

### Setup.py file

DON'T FORGET TO UPDATE SETUP.py FILE

### Sources & Resources

This template attempts to reach
the [Maven Standard Directory Layout](https://maven.apache.org/guides/introduction/introduction-to-the-standard-directory-layout.html)
for python.

That's why you will find the following directory structure:

* ***src/main/python:*** Should contains your application sources
* ***src/main/resources:*** Should contains your application resources
* ***src/test/python:*** Should contains your application **test** sources
* ***src/test/resources:*** Should contains your application  **test** resources

**Sources** and **resources** directories must be in
your **[PYTHONPATH](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONPATH)**

> **Note:** if you are using IDE like **Pycharm**, it means that these directories must be marked as **Sources Root**
> `(Right click on these directories > Mark directory as > Sources Root)`

### <span style='color: orange'>[!WARNING!]</span> Maven Standard Directory Layout with python limitation

Python resources MUST be placed in a python package (We can imagine this like a java classpath).

However, each package in `resources` directory must be different from those of the `python` directory otherwise they
will be overridden during the `build` step due to a `setuptool` limitation (see `setup.py` > `package_dir`
in `setuptools.setup`).

So if you want to respect the *Maven Standard Directory Layout* there are several solutions

#### A. Use a suffixed root resources name

Use a root resources package name suffixed by `_rsrc`.

> **Project structure example:**
>
> ```sh
> <My_Project>
>  |- ...
>  |- src
>      |- main
>          |- python
>          |   |- <MY_ROOT_PACKAGE_NAME>
>          |       |- <SUB_PACKAGE_1>
>          |       |- ...
>          |       |- <SUB_PACKAGE_N>
>          |- resources
>              |- <MY_ROOT_PACKAGE_NAME>_rsrc
>                  |- ...
> ```

> ***Note:** since root packages are different (`_rsrc` suffix) it cannot exist conflict between sources and resources
> packages*

#### B. Use a resources package tree without conflict

In this case you will use the same package tree between sources and resources but `resources` must be placed in specific
sub-package without conflict.

> **Project structure example:**
> ```shell
> <My_Project>
>  |- ...
>  |- src
>      |- main
>          |- python
>          |   |- <MY_ROOT_PACKAGE_NAME>
>          |       |- <SUB_PACKAGE_1>
>          |       |- ...
>          |       |- <SUB_PACKAGE_N>
>          |- resources
>              |- <MY_ROOT_PACKAGE_NAME>
>                  |- <SUB_PACKAGE_1>
>                  |    |- <SUB_PACKAGE_1_RESOURCE_PACKAGE>
>                  |    |- ...
>                  |- <SUB_RESOURCE_PACKAGE_1>
>                  |- ...
>                  |- <SUB_RESOURCE_PACKAGE_M>
> ```

> ***Note:** The most important is that a `resource (.../resources)` package **MUST NOT** exist in `source (.../python)`*

***<span style='color: orange'>!WARNING!</span> Note:** In case of conflict between sources and resources packages
everything will work but not your delivery. Indeed, resources conflicted packages will be ignored due to a `setuptool`
limitation (see `setup.py` > `package_dir`
in `setuptools.setup`)*

#### C. Don't respect the Maven Standard Directory Layout

> if you are not agree with the previous suggestions, you can remove the `src/main/resources` directory and put your
> resources directly in the `src/main/python` directory

## Pipenv (Pipfile) versus requirements.txt project

// TODO

## Run tests

// TODO

## Build

> ```shell
> python setup.py clean --all \
>   && rm -rf dist \
>   && rm -rf *.egg-info \
>   && python setup.py bdist_wheel sdist
> ```

## Delivery *(on https://pypi.org/)*

### Prerequisite

`twine` is required for this part
> ```sh
> pip install twine
> ```

> ***Note:** As it is a common delivery tool, you can install it on your global python environment. However you can also
> install it on your pipenv virtual environment*

### Delivery command

> ```shell
> twine upload dist/*
> ```

> ***Note:** Obviously, this command must be run after the [Build](#build) one*

// TODO pip install -e .
