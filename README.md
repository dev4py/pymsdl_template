# RCPY_Boilerplate

# **WARNING: WORK IN PROGRESS**

A Python boilerplate inspired from
the [Maven Standard Directory Layout](https://maven.apache.org/guides/introduction/introduction-to-the-standard-directory-layout.html)
without any dependency.

***Since there are some existing limitations, it is strongly advised to read
the [Project organization](#project-organization) part before the [Project commands](#project-commands) one***

> ***Note:** By default, this boilerplate is configured in order to work with [pipenv](https://pipenv.pypa.io/). However, if
> you are not using pipenv you can easily configure this boilerplate to work a
> [requirements.txt file](https://pip.pypa.io/en/stable/user_guide/#requirements-files).*
>
> *See [Pipenv (Pipfile) versus requirements.txt project](#pipenv-pipfile-versus-requirementstxt-project)...*

## Table of content

* [Project organization](#project-organization)
    + [setup.py & project.ini files](#setuppy--projectini-files)
    + [Pipenv (Pipfile) versus requirements.txt project](#pipenv-pipfile-versus-requirementstxt-project)
    + [Maven Standard Directory Layout with python](#maven-standard-directory-layout-with-python)
        - [Sources & Resources directories configuration](#sources--resources-directories-configuration)
        - [<span style='color: orange'><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Warning.svg/25px-Warning.svg.png" alt="warning-icon" width="20px" height="20px"/> WARNING: Limitations</span>](#-warning-limitations)
            * [A. Use root package names with suffix](#a-use-root-package-names-with-suffix)
            * [B. Use namespace package as root package](#b-use-namespace-package-as-root-package)
            * [C. Don't fully respect the Maven Standard Directory Layout](#c-dont-fully-respect-the-maven-standard-directory-layout)
* [Project commands](#project-commands)
    + [Clean project](#clean-project)
    + [Run module](#run-module)
    + [Run tests](#run-tests)
    + [Build](#build)
    + [Delivery *(on https://pypi.org/)*](#delivery-on-httpspypiorg)
        - [Prerequisite](#prerequisite)
        - [Delivery command](#delivery-command)

## Project organization

### setup.py & project.ini files

The `setup.py` file is used in order to build & deliver correctly your project.

When you start a new project from this boilerplate, ***YOU DON'T HAVE TO UPDATE SETUP.PY FILE***

In order to set your project properties, you just have to update the [project.ini](./project.ini) file:

> Configuration example:
> ```ini
> ###############################
> ###### PROJECT PROPERTIES #####
> ###############################
> [PROJECT]
> name = hellopysdl
> version = 1.0.0
> author = author
> email = author@mail.com
> description = A Python boilerplate inspired from the Maven Standard Directory Layout
> url = https://github.com/St4rG00se/${name}
> license = MIT
> 
> [ENTRY_POINT]
> console_scripts = hello = ${PROJECT:name}.__main__:hello
> # ...
> ```

> ***Note:** Environment variables are available from `ENV` section.*
>
> **Environment variable example:**
> ```ini
> # Set name from `ProjectName` environment variable
> name=${ENV:ProjectName}
> # ...
> ```
>
> *Trick: If you define an `ENV` section in your [project.ini](./project.ini) file, each variable which exists in your
> environment variable set will be overridden otherwise it will be used. It means that you can define an `ENV` section
> in order to set default environment variable values*
>
> **Environment variable default value example:**
> ```ini
> # Set ProjectName environment variable default value:
> [ENV]
> ProjectName=My default project name (will be used if ProjectName environement variable doesn't exists)
> # ...
> ```

### Pipenv (Pipfile) versus requirements.txt project

By default, this boilerplate if configured in order to work with [pipenv](https://pipenv.pypa.io/) (ie: `Pipfile` &
`Pipfile.lock`).

However, you can easily use it without `pipenv` by using a `requirements.txt` file. To do that, you just have to update
the `project.ini` file like this:

> ```ini
> # ...
> 
> # use_pipenv: (default: True)
> #      True -> use Pipfile.lock for setup install_requires
> #      False -> Use requirements.txt for setup install_requires
> use_pipenv = False
> 
> # ...
> ```

> ***Note:** `Pipfile.lock` or `requirements.txt` must be located in the same directory as `setup.py` (ie: the project
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

**However, if you don't want to configure your PYTHONPATH, you can use the provided [Run module](#run-module) command**

> ***Note:** if you are using IDE like **[<img src="https://upload.wikimedia.org/wikipedia/commons/1/1d/PyCharm_Icon.svg" alt="Pycharm-icon" width="17px" height="17px"/>
Pycharm](https://www.jetbrains.com/pycharm/)**
> , it means `src/main/python` and `src/main/resources` must be marked as **Sources Root**
> `(Right click on these directories > Mark directory as > Sources Root)`
> and `src/test/python` and `src/test/resources` must be marked as **Test Sources Root**
> `(Right click on these directories > Mark directory as > Test Sources Root)`*

> ***Note:** Due to a setuptools limitation ([issue-230](https://github.com/pypa/setuptools/issues/230)), using
> installation with edit mode (`pip install -e .`) in order to avoid the *PYTHONPATH* configuration will not work if you
> want to use resources directories (=> it will work only with `src/main/python` content).*

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
* *<My_Root_Package_Name>`_rsrc`* for resources (in `src/main/resources`)
* *<My_Root_Package_Name>`_test`* for test sources (in `src/test/python`)
* *<My_Root_Package_Name>`_test_rsrc`* for test resources (in `src/test/resources`)

> **Project structure example:**
>
> ```sh
> <My_Project>
>  |- ...
>  |- src
>      |- main
>      |   |- python
>      |   |   |- <MY_ROOT_PACKAGE_NAME>
>      |   |       |- __init__.py
>      |   |       |- ...
>      |   |- resources
>      |       |- <MY_ROOT_PACKAGE_NAME>_rsrc
>      |           |- __init__.py
>      |           |- ...
>      |- test
>          |- python
>          |   |- <MY_ROOT_PACKAGE_NAME>_test
>          |       |- __init__.py
>          |       |- ...
>          |- resources
>              |- <MY_ROOT_PACKAGE_NAME>_test_rsrc
>                  |- __init__.py
>                  |- ...
> ```

> ***Note:** since root package names are different (`_rsrc`, `_test`, `_test_rsrc` suffixes) it cannot exist conflict
> between packages in `src/main/python`, `src/main/resources`, `src/test/python` and `src/test/resources`*

> ***Note:** `_rsrc`, `_test`, `_test_rsrc` are just suggested suffixes you can use your own suffixes*

##### B. Use namespace package as root package

If you really want a common root package name, you can use a `namespace package` as root. This `namespace package` must
contain packages without conflict between sources and resources directories.

> *Reminder: A namespace package doesn't contain any source or `__init__.py` file*

> **Project structure with namespace package as root package example:**
>
> ```sh
> <My_Project>
>  |- ...
>  |- src
>      |- main
>      |   |- python
>      |   |   |- <MY_ROOT_NAMESPACE_PACKAGE_NAME>
>      |   |       |- <MY_PACKAGE_NAME>
>      |   |       |   |- __init__.py
>      |   |       |   |- ...
>      |   |       |- ...
>      |   |- resources
>      |       |- <MY_ROOT_NAMESPACE_PACKAGE_NAME>
>      |           |- <MY_PACKAGE_NAME>_rsrc
>      |           |   |- __init__.py
>      |           |   |- ...
>      |           |- ...
>      |- test
>          |- python
>          |   |- <MY_ROOT_NAMESPACE_PACKAGE_NAME>
>          |       |- <MY_PACKAGE_NAME>_test
>          |       |   |- __init__.py
>          |       |   |- ...
>          |       |- ...
>          |- resources
>              |- <MY_ROOT_NAMESPACE_PACKAGE_NAME>
>                  |- <MY_PACKAGE_NAME>_test_rsrc
>                  |   |- __init__.py
>                  |   |- ...
>                  |- ...
> ```

##### C. Don't fully respect the Maven Standard Directory Layout

If you are not agree with the previous suggestions, you can remove the `src/main/resources`, `src/test/python`
and `src/test/resources` directories and put your resources and tests directly into the `src/main/python` directory.

> **Note:** in this case you will also avoid the `pip install -e .` limitation explained before
> (see [Sources & Resources directories configuration](#sources--resources-directories-configuration) part)
>
> However, if you do that, your tests will be included during your project/package installation (not only in the source
> distribution as it is suggested in the best practices)

## Project commands

### Clean project

> ```sh
> python setup.py clean
> ```

> ***Note:** It doesn't use the default `clean` command*. This one remove `build`, `dist` and/or `.egg-info` directories
> ```sh
> Options for 'CleanCommand' command:
>  --build (-b)     Remove the 'build' directory
>  --dist (-d)      Remove the 'dist' directory
>  --egg-info (-e)  Remove the '.egg-info' directory
>  --all (-a)       (default) remove all directories
> ```

### Run module

RCPY boilerplate allow you to run a python module (even in the **Maven Standard Directory Layout**) without having to
configure your **[PYTHONPATH](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONPATH)**

> ```sh
> python setup.py run -m <MODULE_NAME>
> ```

>**Run *module* example:**
> ```sh
> python setup.py run -m hellopysdl.__main__
> ```
> Run the __main__.py module from hellopysdl package
> 
> **Run *package* example:**
> ```sh
> python setup.py run -m hellopysdl
> ```
> ***Note:** your package MUST contains a __main__.py module*


### Run tests

> ```sh
> python setup.py test
> ```

> ***Note:** It doesn't use the deprecated `test` command*

> ***Note:** This project is configured to execute tests with
> [**unittest**](https://docs.python.org/3/library/unittest.html). If you want to use another runner you have to update
> the `TestCommand` class from `setup.py` or not use the `setup.py test` command*

### Build

> ```sh
> python setup.py clean \
> && pip wheel --wheel-dir=dist/ .
> ```

or if you need a source distribution (sdist) archive:

> ```sh
> python setup.py clean sdist
> ```

> ***Reminder:** Using `python setup.py bdist_wheel` in order to create your `wheel` archive directly is deprecated (It
> should work however you will have a warning message)*

### Delivery *(on https://pypi.org/)*

#### Prerequisite

`twine` is required for this part
> ```sh
> pip install twine
> ```

> ***Note:** As it is a common delivery tool, you can install it on your global python environment. However you can also
> install it on your pipenv virtual environment*

#### Delivery command

> ```sh
> twine upload dist/*
> ```

> ***Note:** Obviously, this command must be executed after the [Build](#build) one*

# TODO:

* Test with namespace
* Run module with args
* (delivery install) explain python -m pkgname
* explain entrypoint
* best practice dependencies
* quickstart
* add docker (mb docker-compose)
* project.py project command wrapper
