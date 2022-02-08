# RCPY_Boilerplate

# **WARNING: WORK IN PROGRESS**

A Python boilerplate inspired from
the [Maven Standard Directory Layout](https://maven.apache.org/guides/introduction/introduction-to-the-standard-directory-layout.html)

***Since there are some existing limitations, it is strongly advised to read
the [Project organization](#project-organization) part before the [Project commands](#project-commands) one***

> **Note:** By default, this boilerplate is configured in order to work with [pipenv](https://pipenv.pypa.io/). However, if
> you are not using pipenv you can easily configure this boilerplate to work a
> [requirements.txt file](https://pip.pypa.io/en/stable/user_guide/#requirements-files).
>
> See [Pipenv (Pipfile) versus requirements.txt project](#pipenv-pipfile-versus-requirementstxt-project)...

## Table of content

* [Project organization](#project-organization)
    + [Setup.py file](#setuppy-file)
    + [Pipenv (Pipfile) versus requirements.txt project](#pipenv-pipfile-versus-requirementstxt-project)
    + [Maven Standard Directory Layout with python](#maven-standard-directory-layout-with-python)
        - [Sources & Resources directories configuration](#sources--resources-directories-configuration)
        - [<span style='color: orange'><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Warning.svg/25px-Warning.svg.png" alt="warning-icon" width="20px" height="20px"/> WARNING: Limitations</span>](#-warning-limitations)
            * [A. Use root package names with suffix](#a-use-root-package-names-with-suffix)
            * [B. Don't fully respect the Maven Standard Directory Layout](#b-dont-fully-respect-the-maven-standard-directory-layout)
* [Project commands](#project-commands)
    + [Run tests](#run-tests)
    + [Build](#build)
    + [Delivery *(on https://pypi.org/)*](#delivery-on-httpspypiorg)
        - [Prerequisite](#prerequisite)
        - [Delivery command](#delivery-command)

## Project organization

### Setup.py file

The `setup.py` file is used in order to build & deliver correctly your project. That's why it contains each information
about the project delivery (name, version, author, description, etc.).

When you start a new project from this boilerplate, ***DON'T FORGET TO UPDATE SETUP.PY FILE***

You just have to update the `# PROJECT SPECIFIC VAR` part:

> Configuration example:
> ```python
> # PROJECT SPECIFIC VAR
> PIPENV_PROJECT: bool = True  # True -> use Pipfile.lock for *install_requires*, False -> Use requirements.txt
> PROJECT_NAME: str = 'hellopysdl'
> VERSION: str = '1.0.0'
> AUTHOR: str = 'author'
> EMAIL: str = 'author@mail.com'
> DESCRIPTION: str = 'A Python boilerplate inspired from the Maven Standard Directory Layout'
> URL: str = f'https://github.com/St4rG00se/{PROJECT_NAME}'
> LICENSE: str = 'MIT'
> ENTRY_POINT: dict[str, list[str]] = {
>     'console_scripts': [
>         f'hello = {PROJECT_NAME}.__main__:hello'
>     ]
> }
> # ...
> ```

### Pipenv (Pipfile) versus requirements.txt project

By default, this boilerplate if configured in order to work with [pipenv](https://pipenv.pypa.io/) (ie: `Pipfile` &
`Pipfile.lock`).

However, you can easily use it without `pipenv` by using a `requirements.txt` file. To do that, you just have to update
the `setup.py` file like this:

> ```python
> # PROJECT SPECIFIC VAR
> PIPENV_PROJECT: bool = False  # True -> use Pipfile.lock for *install_requires*, False -> Use requirements.txt
> # ...
> ```

>***Note:** `Pipfile.lock` or `requirements.txt` must be located in the same directory as `setup.py` (ie: the project 
> root directory)*

### Maven Standard Directory Layout with python

#### Sources & Resources directories configuration

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

> **Note:** if you are using IDE like **[<img src="https://upload.wikimedia.org/wikipedia/commons/1/1d/PyCharm_Icon.svg" alt="Pycharm-icon" width="17px" height="17px"/>
Pycharm](https://www.jetbrains.com/pycharm/)**
> , it means `src/main/python` and `src/main/resources` must be marked as **Sources Root**
> `(Right click on these directories > Mark directory as > Sources Root)`
> and `src/test/python` and `src/test/resources` must be marked as **Test Sources Root**
> `(Right click on these directories > Mark directory as > Test Sources Root)`

> **Note:** Due to a setuptools limitation ([issue-230](https://github.com/pypa/setuptools/issues/230)), using
> installation with edit mode (`pip install -e .`) in order to avoid the *PYTHONPATH* configuration will not work if you
> want to use resources directories (=> it will work only with `src/main/python` content).

#### <span style='color: orange'><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Warning.svg/25px-Warning.svg.png" alt="warning-icon" width="20px" height="20px"/> WARNING: Limitations</span>

Python resources MUST be located in a python package (We can imagine this like a java classpath).

Since a package sources cannot be splitted in several directories, each package in `src/main/python`,
`src/main/resources`, `src/test/python` and `src/test/resources` directories must be different. In case of conflict, the
package from the first directory found in
your **[PYTHONPATH](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONPATH)** will be used.

So if you want to respect the *Maven Standard Directory Layout* there are several suggestions:

##### A. Use root package names with suffix

Use root package names with suffixes like this:

* *<My_Root_Package_Name>* for sources (in `src/main/python`)
* *<My_Root_Package_Name>`_rscr`* for resources (in `src/main/resources`)
* *<My_Root_Package_Name>`_test`* for test sources (in `src/test/python`)
* *<My_Root_Package_Name>`_test_rscr`* for test resources (in `src/test/resources`)

> **Project structure example:**
>
> ```sh
> <My_Project>
>  |- ...
>  |- src
>      |- main
>      |   |- python
>      |   |   |- <MY_ROOT_PACKAGE_NAME>
>      |   |       |- ...
>      |   |- resources
>      |       |- <MY_ROOT_PACKAGE_NAME>_rsrc
>      |           |- ...
>      |- test
>          |- python
>          |   |- <MY_ROOT_PACKAGE_NAME>_test
>          |       |- ...
>          |- resources
>              |- <MY_ROOT_PACKAGE_NAME>_test_rsrc
>                  |- ...
> ```

> ***Note:** since root package names are different (`_rsrc`, `_test`, `_test_rsrc` suffixes) it cannot exist conflict
> between packages in `src/main/python`, `src/main/resources`, `src/test/python` and `src/test/resources`*

> ***Note:** `_rsrc`, `_test`, `_test_rsrc` are just suggested suffixes you can use your own suffixes*

##### B. Don't fully respect the Maven Standard Directory Layout

If you are not agree with the previous suggestion, you can remove the `src/main/resources`, `src/test/python`
and `src/test/resources` directories and put your resources and tests directly into the `src/main/python` directory.

> **Note:** in this case you will also avoid the `pip install -e .` limitation explained before
> (see [Sources & Resources directories configuration](#sources--resources-directories-configuration) part)
> 
> However, if you do that, your tests will be included during your project/package installation (not only in the source 
> distribution as it is suggested in the best practices)

## Project commands

### Run tests

// TODO

### Build

> ```shell
> python setup.py clean --all \
>   && rm -rf dist \
>   && find . -name \*.egg-info -type d -exec rm -rf {} + \
>   && python setup.py bdist_wheel sdist
> ```

### Delivery *(on https://pypi.org/)*

#### Prerequisite

`twine` is required for this part
> ```sh
> pip install twine
> ```

> ***Note:** As it is a common delivery tool, you can install it on your global python environment. However you can also
> install it on your pipenv virtual environment*

#### Delivery command

> ```shell
> twine upload dist/*
> ```

> ***Note:** Obviously, this command must be executed after the [Build](#build) one*



// TODO:

* (delivery install) explain python -m pkgname
* explain entrypoint
* best practice dependencies
* quickstart
* add docker (mb docker-compose)
