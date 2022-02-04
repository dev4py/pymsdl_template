# RCPY_Boilerplate

# **WARNING: WORK IN PROGRESS**

A Python boilerplate inspired from
the [Maven Standard Directory Layout](https://maven.apache.org/guides/introduction/introduction-to-the-standard-directory-layout.html)

***As there are some existing limitations it is strongly advised to read
the [Project organization](#project-organization) part before the [Project commands](#project-commands) one***

> **Note:** By default, this boilerplate is configured in order to work with [pipenv](https://pipenv.pypa.io/). However, if
> you are not using pipenv can easily configure this boilerplate to work a
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
            * [A. Use a suffixed root resources name](#a-use-a-suffixed-root-resources-name)
            * [B. Use a resources package tree without conflict](#b-use-a-resources-package-tree-without-conflict)
            * [C. Don't respect the Maven Standard Directory Layout](#c-dont-respect-the-maven-standard-directory-layout)
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
> , it means these directories must be marked as **Sources Root** `(Right click on these directories > Mark directory as > Sources Root)`

> **Note:** Due to a setuptools limitation ([issue-230](https://github.com/pypa/setuptools/issues/230)), using
> installation with edit mode (`pip install -e .`) in order to avoid the *PYTHONPATH* configuration will not work if you
> want to use resources directories (=> it will work only with `src/main/python` content).

#### <span style='color: orange'><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Warning.svg/25px-Warning.svg.png" alt="warning-icon" width="20px" height="20px"/> WARNING: Limitations</span>

Python resources MUST be located into a python package (We can imagine this like a java classpath).

However, each package in `resources` directory must be different from those of the `python` directory, otherwise they
will be overridden during the `build` step due to a `setuptools` limitation (see `setup.py` > `package_dir`
in `setuptools.setup`).

So if you want to respect the *Maven Standard Directory Layout* there are several suggestions:

##### A. Use a suffixed root resources name

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

##### B. Use a resources package tree without conflict

In this case you will use the same package tree between sources and resources but `resources` must be located in
specific sub-package without conflict.

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

> ***Note:** The most important is that a `resource (in 'src/main/resources')` package **MUST NOT** exist in
> `source (in 'src/main//python')`* directory


> ***<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Warning.svg/25px-Warning.svg.png" alt="warning-icon" width="17px" height="17px"/>
> <span style='color: orange'>!WARNING!</span> Note:** In case of conflict between sources and resources packages
> everything will work but not your delivery. Indeed, resources conflicted packages will be ignored due to a `setuptools`
> limitation (see `setup.py` > `package_dir`
> in `setuptools.setup`)*

##### C. Don't respect the Maven Standard Directory Layout

if you are not agree with the previous suggestions, you can remove the `src/main/resources` directory and put your
resources directly into the `src/main/python` directory.

> **Note:** in this case you will also avoid the `pip install -e .` limitation explained before
> (see [Sources & Resources directories](#sources--resources-directories) part)

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



// TODO (delivery install) explain python -m pkgname // TODO explain entrypoint // TODO best practice dependencies
