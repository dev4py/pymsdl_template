import json
import os
import sys
import unittest
from configparser import ConfigParser, ExtendedInterpolation
from typing import Final, Type
from unittest import TestSuite

from setuptools import setup, find_namespace_packages, Command
from setuptools.errors import DistutilsError

# CONSTANTS
# - project / sources / test paths
PROJECT_PATH: Final[str] = os.path.dirname(__file__)
MAIN_FOLDER: Final[str] = 'src/main'
SRC_FOLDER: Final[str] = f'{MAIN_FOLDER}/python'
RESOURCES_FOLDER: Final[str] = f'{MAIN_FOLDER}/resources'
TEST_FOLDER: Final[str] = 'src/test'
TEST_SRC_FOLDER: Final[str] = f'{TEST_FOLDER}/python'
TEST_RESOURCES_FOLDER: Final[str] = f'{TEST_FOLDER}/resources'

# - ini file consts
PROJECT_INI_FILE_PATH: Final[str] = 'project.ini'
INIT_ENV_VAR_SECTION: Final[str] = 'ENV'
INI_PROJECT_SECTION: Final[str] = 'PROJECT'
INI_ENTRY_POINT_SECTION: Final[str] = f'{INI_PROJECT_SECTION}.ENTRY_POINTS'

# - properties default values
DEFAULT_TEST_FILE_PATTERN: Final[str] = '*[Tt]est*.py'
DEFAULT_USE_PIPENV: Final[bool] = True
DEFAULT_LONG_DESCRIPTION_FILE: Final[str] = 'README.md'
DEFAULT_LONG_DESCRIPTION_CONTENT_TYPE: Final[str] = 'text/markdown'


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


def load_project_ini_file(project_ini_file_path: str, environment_section: str) -> ConfigParser:
    esc_env_vars: Final[dict[str, str]] = {k: v.replace('$', '$$') for k, v in dict(os.environ).items()}
    config_parser: Final[ConfigParser] = ConfigParser(interpolation=ExtendedInterpolation())
    config_parser.read(project_ini_file_path)
    if config_parser.has_section(environment_section):
        config_parser[environment_section] = dict(config_parser[environment_section], **esc_env_vars)
    else:
        config_parser[environment_section] = esc_env_vars
    return config_parser


def find_resources_packages(resources_folder: str, excluded_packages: list[str]) -> list[str]:
    return [pkg for pkg in find_namespace_packages(where=resources_folder) if pkg not in excluded_packages]


def to_packages_dir(folder_path: str, packages: list[str]) -> dict[str, str]:
    return {pkg: f"{folder_path}/{pkg.replace('.', '/')}" for pkg in packages}


def load_entry_points(config_parser: ConfigParser, entry_point_section: str) -> dict[str, list[str]] | None:
    if not config_parser.has_section(entry_point_section):
        return None

    return {k: v.splitlines() for k, v in config_parser.items(entry_point_section)}


def test_command_class_factory(project_path: str, test_src_folder: str, test_file_pattern: str) -> Type[Command]:
    class TestCmd(TestCommand):
        def __init__(self, dist, **kw):
            super().__init__(project_path, test_src_folder, test_file_pattern, dist, **kw)

    return TestCmd


# SETUP CLASSES
# - COMMAND CLASSES
# -- Test command
class TestCommand(Command):
    user_options = []

    def __init__(self, project_path: str, test_src_folder: str, test_file_pattern: str, dist, **kw):
        self.__project_path: str = project_path
        self.__test_src_folder: str = test_src_folder
        self.__test_file_pattern: str = test_file_pattern
        super().__init__(dist, **kw)

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    # noinspection PyMethodMayBeStatic
    def run(self):
        # Prepare tests
        test_loader = unittest.defaultTestLoader
        test_suite: TestSuite = test_loader.discover(
            os.path.join(self.__project_path, self.__test_src_folder),
            pattern=self.__test_file_pattern
        )

        # Run tests
        test_result = unittest.TextTestRunner().run(test_suite)

        if not test_result.wasSuccessful():
            raise DistutilsError('Test failed: %s' % test_result)


# SETUP MAIN
if __name__ == '__main__':
    # Configure sys.path for commands execution
    sys.path.append(os.path.join(PROJECT_PATH, SRC_FOLDER))
    sys.path.append(os.path.join(PROJECT_PATH, RESOURCES_FOLDER))
    sys.path.append(os.path.join(PROJECT_PATH, TEST_SRC_FOLDER))
    sys.path.append(os.path.join(PROJECT_PATH, TEST_RESOURCES_FOLDER))

    # Sources and resources packages & package_dir configuration
    src_packages: Final[list[str]] = find_namespace_packages(where=SRC_FOLDER)
    resources_packages: Final[list[str]] = find_resources_packages(RESOURCES_FOLDER, src_packages)
    #   --> {'': SRC_FOLDER} workaround for pip install -e but resources & tests will not work
    #   --> see: https://github.com/pypa/setuptools/issues/230
    src_packages_dir: Final[dict[str, str]] = {'': SRC_FOLDER}
    resources_packages_dir: Final[dict[str, str]] = to_packages_dir(RESOURCES_FOLDER, resources_packages)

    # Configurable properties parser (ConfigParser)
    cfg_parser: Final[ConfigParser] = load_project_ini_file(PROJECT_INI_FILE_PATH, INIT_ENV_VAR_SECTION)

    # Execute setup
    setup(
        name=cfg_parser.get(INI_PROJECT_SECTION, 'name', fallback=None),
        version=cfg_parser.get(INI_PROJECT_SECTION, 'version', fallback=None),
        author=cfg_parser.get(INI_PROJECT_SECTION, 'author', fallback=None),
        url=cfg_parser.get(INI_PROJECT_SECTION, 'url', fallback=None),
        author_email=cfg_parser.get(INI_PROJECT_SECTION, 'email', fallback=None),
        description=cfg_parser.get(INI_PROJECT_SECTION, 'description', fallback=None),
        long_description=read_file(
            cfg_parser.get(INI_PROJECT_SECTION, 'long_description_file', fallback=DEFAULT_LONG_DESCRIPTION_FILE)
        ),
        long_description_content_type=cfg_parser.get(
            INI_PROJECT_SECTION, 'long_description_content_type', fallback=DEFAULT_LONG_DESCRIPTION_CONTENT_TYPE
        ),
        license=cfg_parser.get(INI_PROJECT_SECTION, 'license', fallback=None),
        packages=src_packages + resources_packages,
        package_dir=dict(resources_packages_dir, **src_packages_dir),
        package_data={'': ['*']},
        include_package_data=True,
        install_requires=get_deps(
            cfg_parser.getboolean(INI_PROJECT_SECTION, 'use_pipenv', fallback=DEFAULT_USE_PIPENV)
        ),
        entry_points=load_entry_points(cfg_parser, INI_ENTRY_POINT_SECTION),
        cmdclass={
            'test': test_command_class_factory(
                PROJECT_PATH,
                TEST_SRC_FOLDER,
                cfg_parser.get(INI_PROJECT_SECTION, 'test_file_pattern', fallback=DEFAULT_TEST_FILE_PATTERN)
            )
        }
    )
