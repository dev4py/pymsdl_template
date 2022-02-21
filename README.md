# PYMSDL_Template

A Python [Poetry](https://python-poetry.org/) template inspired from
the [Maven Standard Directory Layout](https://maven.apache.org/guides/introduction/introduction-to-the-standard-directory-layout.html)

**<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Warning.svg/25px-Warning.svg.png" alt="warning-icon" width="20px" height="20px"/>
WARNING Prerequisites:**

* `Poetry >= 1.1.0`

***Since there are some existing limitations, it is strongly advised to read
the [Project organization](#project-organization) part before the [Project commands](#project-commands) one***

> ***Note:** this template is configured in order to work with [Poetry](https://python-poetry.org/).*
>
> *if you want to use another layout than [Maven Standard Directory Layout](https://maven.apache.org/guides/introduction/introduction-to-the-standard-directory-layout.html),
> you can change the **project structure** as explained in the
> [pyproject.toml & project.py files](#pyprojecttoml--projectpy-files) part*

## Table of contents

* [Project organization](#project-organization)
    + [pyproject.toml & project.py files](#pyprojecttoml--projectpy-files)
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
        - [Wheel archive](#wheel-archive)
        - [Source Distribution](#source-distribution-archive)
    + [Delivery *(on https://pypi.org/)*](#delivery-on-httpspypiorg)

## Project organization

### pyproject.toml & project.py files

The [pyproject.toml](./pyproject.toml) file is used in order to describe and deliver correctly your project.

See:

* [PEP 517](https://www.python.org/dev/peps/pep-0517/)
* [PEP 518](https://www.python.org/dev/peps/pep-0518/)
* [PEP 621](https://www.python.org/dev/peps/pep-0621/)
* [PEP 660](https://www.python.org/dev/peps/pep-0660/)
* [Poetry pyproject.toml details](https://python-poetry.org/docs/pyproject/)

Moreover, this template provides the [project.py](./project.py) file which is a command line wrapper in order to
simplify the project evolution (see [Project commands](#project-commands))

When you start a new project from this template, ***YOU DON'T HAVE TO UPDATE THE [PROJECT.PY](./project.py) FILE***,
until you switch from [Poetry](https://python-poetry.org/) to another tool.

In order to set your project properties, you just have to update the [pyproject.toml](./pyproject.toml)

> **Note:** If you don't want to use the [Maven Standard Directory Layout](https://maven.apache.org/guides/introduction/introduction-to-the-standard-directory-layout.html),
> you can reconfigure the project structure in the `[tool.poetry]` section > `packages` option

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

> ***Note:** Due to a [Poetry](https://python-poetry.org/) limitation, using  installation with edit mode
> (`pip install -e .`) in order to avoid the
> [PYTHONPATH](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONPATH) configuration will not work and fail
> with:*
>
> `build backend is missing the 'build_editable' ... Consider using a build backend that supports PEP 660.`

#### <span style='color: orange'><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Warning.svg/25px-Warning.svg.png" alt="warning-icon" width="20px" height="20px"/> WARNING: Limitations</span>

Python resources MUST be located in a python package (ie: directory containing an `__init__.py` file. (You can see that
like a java classpath).

Since a package sources cannot be split in several directories, each package in `src/main/python`,
`src/main/resources`, `src/test/python` and `src/test/resources` directories must be different. In case of conflict, the
package from the first directory found in
your **[PYTHONPATH](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONPATH)** will be used.

So if you want to respect the
*[Maven Standard Directory Layout](https://maven.apache.org/guides/introduction/introduction-to-the-standard-directory-layout.html)*
there are several suggestions:

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

> **Note:** if you do that, your tests will be included during your project/package installation (not only in the source
> distribution as it is suggested in the best practices)

## Project commands

Project commands are available from the [project.py](./project.py) python file.

If you take a look at this file, you will see that it contains:

* **A shared `project_properties` variable** which contains all project properties.

* **A command line wrapper:** this wrapper is designed in order to be used locally and in your deployment scripts (like
  CI/CD).

  Indeed, by using it, if you want to update you "project tools" (sample: switching from poetry to setuptools) you just
  have to update this script but not all your pipeline.

  Moreover, this wrapper manage the project [PYTHONPATH](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONPATH)
  for you

  > **Command wrapper man:**
  > ```sh
  > PROJECT COMMANDS WRAPPER:
  > 
  > Usage: python project.py <COMMAND_1> <arg1_1 ...> ... <COMMAND_N> <argN_1 ...>
  >         Note: In order to get the wrapped command help, you can try python project.py <command> --help
  > 
  > Available commands are:
  >   clean         Remove directories generated by the "build" commands (like 'sdist' or 'wheel')
  >   run           Run module which can be in the project structure without having to configure the PYTHONPATH
  >   test          Run configured unit tests
  >   wheel         Build Wheel archive
  >   sdist         Build sdist archive
  >   upload        Upload available deliveries
  > ```

  > ***Note:** Using `--help` argument on a command or if an error occurs, the message will be from the wrapped command
  > line*

### Clean project

> ```sh
> ./project.py clean
> ```
or
> ```sh
> python project.py clean
> ```

> ***Note:** Remove dist directory and test cache directories*

### Run module

PYMSDL template provides you a run python module command line (even in the **project packages**) without having to
configure your **[PYTHONPATH](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONPATH)**

> ```sh
> ./project.py run -m <MODULE_NAME>
> ```
or
> ```sh
> python project.py run -m <MODULE_NAME>
> ```

> ***Note:** the `run` command is like opening python in your poetry virtual environment and the project structure
> configured in your **[PYTHONPATH](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONPATH)***
>
> *Moreover, your opened `python` will work from the current directory (not from the `project.py` one).*

> **Examples:**
>
> **- Open a *python console* from the current directory:**
> ```
> ./project.py run
> ```
> ***Note:** `<PATH_TO_PROJECT.PY> run` will open a python console in your current directory not in the `project.py`
> one*
>
> **- Run *module* example:**
> ```sh
> ./project.py run -m hellopymsdl.__main__
> ```
> Run the `__main__.py` module from `hellopymsdl` package
>
> **- Run *package* example:**
> ```sh
> ./project.py run -m hellopymsdl
> ````
> ***Note:** your package MUST contains a `__main__.py` module*
>
> **- Run *module* from path example:**
> ```sh
> ./project.py run src/main/python/hellopymsdl/__main__.py
> ```
> Run the `__main__.py` module from `hellopymsdl` package
> **WARNING: the path is from the command `CWD` if not absolute**
>
> **- Run *package* from path example:**
> ```sh
> ./project.py run src/main/python/hellopymsdl
> ```
> ***Note:** your package MUST contains a `__main__.py` module*
> **WARNING: the path is from the command `CWD` if not absolute**
>
> **- Run *module* with arguments example (using --args string parameter):**
> ```sh
> ./project.py run -m hellopymsdl.__main__ --arg1 --arg2=my_arg2 ...
> ```

### Run tests

This project is configured to execute tests with [**Pytest**](https://docs.pytest.org/):

> ```sh
> ./project.py test
> ```
or
> ```sh
> python project.py test
> ```

> ***Note:** If you change the project structure, don't forget to update the `[tool.pytest.ini_options]` section from
> the [pyproject.toml](./pyproject.toml) file*

### Build

#### Wheel archive

> ```sh
> ./project.py wheel
> ```
or
> ```sh
> python project.py wheel
> ```

#### Source Distribution archive

If you need a source distribution (sdist) archive:

> ```sh
> ./project.py sdist
> ```
or
> ```sh
> python project.py sdist
> ```


### Delivery *(on https://pypi.org/)*

> ```sh
> ./project.py upload
> ```
or
> ```sh
> python project.py upload
> ```

> ***Note:** Obviously, this command must be executed after the [Build](#build) one*


# TODO:

* quickstart
* add docker (mb docker-compose)
