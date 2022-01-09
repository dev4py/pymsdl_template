import re

from setuptools import setup, find_namespace_packages


def read_file(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.read()


def get_deps_from_pipfile(section: str = "packages", pipfile_path: str = "Pipfile") -> list[str]:
    file_content = read_file(pipfile_path)
    if file_content:
        search: re.Match = re.search(r"\[\s*%s\s*\]([^\[]*)" % section, file_content, re.S | re.I)
        return [line.split('=')[0].strip() for line in search.group(1).splitlines() if line.strip()] if search else []

    return []


def to_package_dir(folder_path: str, packages: list) -> dict[str, str]:
    return {pkg: f"{folder_path}/{pkg.replace('.', '/')}" for pkg in packages}


# VAR TO SET
PROJECT_NAME: str = 'hellopysdl'
VERSION: str = '1.0.0'
AUTHOR: str = 'author'
EMAIL: str = 'author@mail.com'
DESCRIPTION: str = 'A Python boilerplate inspired from the Maven Standard Directory Layout'
URL: str = f'https://github.com/St4rG00se/{PROJECT_NAME}'
LICENSE: str = 'MIT'
ENTRY_POINT: dict[str, list[str]] = {
        'console_scripts': [
            f'serve = {PROJECT_NAME}.__main__:serve'
        ]
    }

# FIXED VAR
MAIN_FOLDER: str = 'src/main'
SRC_FOLDER: str = f'{MAIN_FOLDER}/python'
RESOURCES_FOLDER: str = f'{MAIN_FOLDER}/resources'

SRC_PACKAGES: list = find_namespace_packages(where=SRC_FOLDER)
RESOURCES_PACKAGES: list = find_namespace_packages(where=RESOURCES_FOLDER)

PACKAGES: list = list(set(SRC_PACKAGES + RESOURCES_PACKAGES))

SRC_PACKAGES_DIR: dict = to_package_dir(SRC_FOLDER, SRC_PACKAGES)
RESOURCES_PACKAGES_DIR: dict = to_package_dir(RESOURCES_FOLDER, RESOURCES_PACKAGES)
PACKAGES_DIR: dict = dict(RESOURCES_PACKAGES_DIR, **SRC_PACKAGES_DIR)

setup(
    name=PROJECT_NAME,
    version=VERSION,
    author=AUTHOR,
    url=URL,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    license=LICENSE,
    packages=PACKAGES,
    package_dir=PACKAGES_DIR,
    package_data={'': ['*']},
    include_package_data=True,
    install_requires=get_deps_from_pipfile(),
    entry_points=ENTRY_POINT
)
