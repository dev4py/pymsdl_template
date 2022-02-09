import json
import os
import sys
import unittest
from configparser import ConfigParser, ExtendedInterpolation
from typing import Final
from unittest import TestSuite

from setuptools import setup, find_namespace_packages, Command
from setuptools.errors import DistutilsError


# SETUP CLASSES
# - CONFIGURATION CLASSES
class ProjectConfig:
    # STATIC METHODS
    @staticmethod
    def load_project_ini_file(project_ini_file_path: str) -> ConfigParser:
        config: Final[ConfigParser] = ConfigParser(interpolation=ExtendedInterpolation())
        config.read(project_ini_file_path)
        return config

    @staticmethod
    def find_resources_packages(resources_folder: str, src_packages: list[str]):
        return [pkg for pkg in find_namespace_packages(where=resources_folder) if pkg not in src_packages]

    @staticmethod
    def find_resources_packages_dir(resources_folder: str, resources_packages: list[str]):
        return {pkg: f"{resources_folder}/{pkg.replace('.', '/')}" for pkg in resources_packages}

    # PROJECT STRUCTURE CONSTS
    PROJECT_PATH: Final[str] = os.path.dirname(__file__)

    # - sources / test paths
    MAIN_FOLDER: Final[str] = 'src/main'
    SRC_FOLDER: Final[str] = f'{MAIN_FOLDER}/python'
    RESOURCES_FOLDER: Final[str] = f'{MAIN_FOLDER}/resources'
    TEST_FOLDER: Final[str] = 'src/test'
    TEST_SRC_FOLDER: Final[str] = f'{TEST_FOLDER}/python'
    TEST_RESOURCES_FOLDER: Final[str] = f'{TEST_FOLDER}/resources'

    # - sources and resources packages & package_dir configuration
    SRC_PACKAGES: Final[list[str]] = find_namespace_packages(where=SRC_FOLDER)
    RESOURCES_PACKAGES: Final[list[str]] = find_resources_packages(RESOURCES_FOLDER, SRC_PACKAGES)

    #   --> {'': SRC_FOLDER} workaround for pip install -e but resources & tests will not work
    #   --> see: https://github.com/pypa/setuptools/issues/230
    SRC_PACKAGES_DIR: Final[dict] = {'': SRC_FOLDER}
    RESOURCES_PACKAGES_DIR: Final[dict] = find_resources_packages_dir(RESOURCES_FOLDER, RESOURCES_PACKAGES)
    PACKAGES: Final[list] = SRC_PACKAGES + RESOURCES_PACKAGES
    PACKAGES_DIR: Final[dict] = dict(RESOURCES_PACKAGES_DIR, **SRC_PACKAGES_DIR)

    # PROJECT CONFIGURABLE PROPERTIES
    # - ini file consts
    PROJECT_INI_FILE_PATH: Final[str] = 'project.ini'
    INI_PROJECT_SECTION: Final[str] = 'PROJECT',
    INI_ENTRY_POINT_SECTION: Final[str] = 'ENTRY_POINT'

    # - properties default values
    DEFAULT_TEST_FILE_PATTERN: Final[str] = '*[Tt]est*.py'
    DEFAULT_USE_PIPENV: Final[bool] = True
    DEFAULT_LONG_DESCRIPTION_FILE: Final[str] = 'README.md'
    DEFAULT_LONG_DESCRIPTION_CONTENT_TYPE: Final[str] = 'text/markdown'

    # - ConfigParser
    CONFIG_PARSER: Final[ConfigParser] = load_project_ini_file(PROJECT_INI_FILE_PATH)

    # - configurable properties (project.ini file)
    USE_PIPENV: Final[bool] = CONFIG_PARSER.getboolean(INI_PROJECT_SECTION, 'use_pipenv', fallback=DEFAULT_USE_PIPENV)
    NAME: Final[str] = CONFIG_PARSER.get(INI_PROJECT_SECTION, 'name', fallback=None)
    VERSION: Final[str] = CONFIG_PARSER.get(INI_PROJECT_SECTION, 'version', fallback=None)
    DESCRIPTION: Final[str] = CONFIG_PARSER.get(INI_PROJECT_SECTION, 'description', fallback=None)
    AUTHOR: Final[str] = CONFIG_PARSER.get(INI_PROJECT_SECTION, 'author', fallback=None)
    EMAIL: Final[str] = CONFIG_PARSER.get(INI_PROJECT_SECTION, 'email', fallback=None)
    LONG_DESCRIPTION_FILE: Final[str] = CONFIG_PARSER.get(
        INI_PROJECT_SECTION,
        'long_description_file',
        fallback=DEFAULT_LONG_DESCRIPTION_FILE
    )
    LONG_DESCRIPTION_CONTENT_TYPE: Final[str] = CONFIG_PARSER.get(
        INI_PROJECT_SECTION,
        'long_description_content_type',
        fallback=DEFAULT_LONG_DESCRIPTION_CONTENT_TYPE
    )
    URL: Final[str] = CONFIG_PARSER.get(INI_PROJECT_SECTION, 'url', fallback=None)
    LICENSE: Final[str] = CONFIG_PARSER.get(INI_PROJECT_SECTION, 'license', fallback=None)
    TEST_FILE_PATTERN: Final[str] = CONFIG_PARSER.get(
        INI_PROJECT_SECTION,
        'test_file_pattern',
        fallback=DEFAULT_TEST_FILE_PATTERN
    )
    ENTRY_POINT: Final[dict[str, list[str]]]= None


# - COMMAND CLASSES
class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    # noinspection PyMethodMayBeStatic
    def run(self):
        # Prepare tests
        test_loader = unittest.defaultTestLoader
        test_suite: TestSuite = test_loader.discover(
            os.path.join(ProjectConfig.PROJECT_PATH, ProjectConfig.TEST_SRC_FOLDER),
            pattern=ProjectConfig.TEST_FILE_PATTERN)

        # Run tests
        test_result = unittest.TextTestRunner().run(test_suite)

        if not test_result.wasSuccessful():
            raise DistutilsError('Test failed: %s' % test_result)


# SETUP FUNCTIONS
def read_file(file_path: str) -> str:
    with open(file_path) as file:
        return file.read()


def get_deps_from_pipfile(section: str = "default", pipfile_path: str = "Pipfile.lock") -> list[str]:
    with open(pipfile_path) as pipfile:
        pipfile_content = json.load(pipfile)

    return [package + detail.get('version', "") for package, detail in pipfile_content.get(section, {}).items()]


def get_deps_from_requirements(requirements_path: str = "requirements.txt") -> list[str]:
    return read_file(requirements_path).splitlines()


def get_deps(use_pipfile: bool = True) -> list[str]:
    return get_deps_from_pipfile() if use_pipfile else get_deps_from_requirements()


# SETUP MAIN
if __name__ == '__main__':
    # Configure sys.path for command execution
    sys.path.append(os.path.join(ProjectConfig.PROJECT_PATH, ProjectConfig.SRC_FOLDER))
    sys.path.append(os.path.join(ProjectConfig.PROJECT_PATH, ProjectConfig.RESOURCES_FOLDER))
    sys.path.append(os.path.join(ProjectConfig.PROJECT_PATH, ProjectConfig.TEST_SRC_FOLDER))
    sys.path.append(os.path.join(ProjectConfig.PROJECT_PATH, ProjectConfig.TEST_RESOURCES_FOLDER))

    # Execute setup
    setup(
        name=ProjectConfig.NAME,
        version=ProjectConfig.VERSION,
        author=ProjectConfig.AUTHOR,
        url=ProjectConfig.URL,
        author_email=ProjectConfig.EMAIL,
        description=ProjectConfig.DESCRIPTION,
        long_description=read_file(ProjectConfig.LONG_DESCRIPTION_FILE),
        long_description_content_type=ProjectConfig.LONG_DESCRIPTION_CONTENT_TYPE,
        license=ProjectConfig.LICENSE,
        packages=ProjectConfig.PACKAGES,
        package_dir=ProjectConfig.PACKAGES_DIR,
        package_data={'': ['*']},
        include_package_data=True,
        install_requires=get_deps(ProjectConfig.USE_PIPENV),
        entry_points=ProjectConfig.ENTRY_POINT,
        cmdclass={'test': TestCommand}
    )
