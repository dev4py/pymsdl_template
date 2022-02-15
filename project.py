from configparser import ConfigParser, ExtendedInterpolation
from io import TextIOWrapper
from json import load as json_load
from os import environ as os_environ, pathsep as os_pathsep
from pathlib import Path
from subprocess import run as subprocess_run
from sys import executable as sys_executable, argv as sys_argv, stderr as sys_stderr, stdin as sys_stdin, \
    stdout as sys_stdout
from typing import Final

# CONSTANTS
# - ini file consts
PROJECT_INI_FILE_PATH: Final[str] = 'project.ini'
INI_ENV_VAR_SECTION: Final[str] = 'ENV'
INI_PROJECT_SECTION: Final[str] = 'PROJECT'
INI_ENTRY_POINTS_SECTION: Final[str] = f'{INI_PROJECT_SECTION}.ENTRY_POINTS'
INI_STRUCTURE_SECTION: Final[str] = f'{INI_PROJECT_SECTION}.STRUCTURE'

# - sources / test default paths
PROJECT_PATH: Final[Path] = Path(__file__).parent.absolute()
DEFAULT_MAIN_PATH: Final[str] = 'src/main'
DEFAULT_SRC_PATH: Final[str] = f'{DEFAULT_MAIN_PATH}/python'
DEFAULT_RESOURCES_PATH: Final[str] = f'{DEFAULT_MAIN_PATH}/resources'
DEFAULT_TEST_PATH: Final[str] = 'src/test'
DEFAULT_TEST_SRC_PATH: Final[str] = f'{DEFAULT_TEST_PATH}/python'
DEFAULT_TEST_RESOURCES_PATH: Final[str] = f'{DEFAULT_TEST_PATH}/resources'
DEFAULT_BUILD_PATH: Final[str] = 'build'
DEFAULT_DIST_PATH: Final[str] = 'dist'

# - properties default values
DEFAULT_TEST_FILE_PATTERN: Final[str] = '*[Tt]est*.py'
DEFAULT_USE_PIPENV: Final[bool] = True
DEFAULT_LONG_DESCRIPTION_FILE: Final[str] = 'README.md'
DEFAULT_LONG_DESCRIPTION_CONTENT_TYPE: Final[str] = 'text/markdown'


# CLASSES
# - Project Configuration class
class ProjectProperties:

    def __init__(
            self,
            ini_file_path: str = PROJECT_INI_FILE_PATH,
            env_var_section: str = INI_ENV_VAR_SECTION,
            project_section: str = INI_PROJECT_SECTION,
            entry_points_section: str = INI_ENTRY_POINTS_SECTION,
            structure_section: str = INI_STRUCTURE_SECTION
    ):
        self.__ini_file_path: Final[str] = ini_file_path
        self.__env_var_section: Final[str] = env_var_section
        self.__project_section: Final[str] = project_section
        self.__entry_points_section: Final[str] = entry_points_section
        self.__structure_section: Final[str] = structure_section
        self.__config_parser: Final[ConfigParser] = self._load_project_ini_file()

        # - PROJECT section
        self.name: Final[str | None] = self.__config_parser.get(self.__project_section, 'name', fallback=None)
        self.version: Final[str | None] = self.__config_parser.get(self.__project_section, 'version', fallback=None)
        self.author: Final[str | None] = self.__config_parser.get(self.__project_section, 'author', fallback=None)
        self.url: Final[str | None] = self.__config_parser.get(self.__project_section, 'url', fallback=None)
        self.author_email: Final[str | None] = self.__config_parser.get(self.__project_section, 'email', fallback=None)
        self.description: Final[str | None] = self.__config_parser.get(
            self.__project_section, 'description', fallback=None
        )
        self.long_description_file: Final[str] = self.__config_parser.get(
            self.__project_section, 'long_description_file', fallback=DEFAULT_LONG_DESCRIPTION_FILE
        )
        self.long_description_content_type: Final[str] = self.__config_parser.get(
            self.__project_section, 'long_description_content_type', fallback=DEFAULT_LONG_DESCRIPTION_CONTENT_TYPE
        )
        self.license: Final[str | None] = self.__config_parser.get(self.__project_section, 'license', fallback=None)
        self.use_pipenv: Final[bool] = self.__config_parser.getboolean(
            self.__project_section, 'use_pipenv', fallback=DEFAULT_USE_PIPENV
        )
        self.install_requires: Final[list[str]] = self._get_deps()
        self.test_file_pattern: Final[str] = self.__config_parser.get(
            self.__project_section, 'test_file_pattern', fallback=DEFAULT_TEST_FILE_PATTERN
        )

        # - PROJECT.ENTRY_POINTS section
        self.entry_points: Final[dict[str, list[str]] | None] = self._load_entry_points()

        # - PROJECT.STRUCTURE section
        self.sources_path: Final[str] = self.__config_parser.get(
            self.__structure_section, 'sources_path', fallback=DEFAULT_SRC_PATH
        )
        self.resources_path: Final[str] = self.__config_parser.get(
            self.__structure_section, 'resources_path', fallback=DEFAULT_RESOURCES_PATH
        )
        self.test_sources_path: Final[str] = self.__config_parser.get(
            self.__structure_section, 'test_sources_path', fallback=DEFAULT_TEST_SRC_PATH
        )
        self.test_resources_path: Final[str] = self.__config_parser.get(
            self.__structure_section, 'test_resources_path', fallback=DEFAULT_TEST_RESOURCES_PATH
        )
        self.build_path: Final[str] = self.__config_parser.get(
            self.__structure_section, 'build_path', fallback=DEFAULT_BUILD_PATH
        )
        self.dist_path: Final[str] = self.__config_parser.get(
            self.__structure_section, 'dist_path', fallback=DEFAULT_DIST_PATH
        )

    def _load_project_ini_file(self) -> ConfigParser:
        esc_env_vars: Final[dict[str, str]] = {k: v.replace('$', '$$') for k, v in dict(os_environ).items()}
        config_parser: Final[ConfigParser] = ConfigParser(interpolation=ExtendedInterpolation())
        config_parser.read(self.__ini_file_path)
        if config_parser.has_section(self.__env_var_section):
            config_parser[self.__env_var_section] = dict(config_parser[self.__env_var_section], **esc_env_vars)
        else:
            config_parser[self.__env_var_section] = esc_env_vars
        return config_parser

    def _load_entry_points(self) -> dict[str, list[str]] | None:
        if not self.__config_parser.has_section(self.__entry_points_section):
            return None

        return {k: v.splitlines() for k, v in self.__config_parser.items(self.__entry_points_section)}

    @staticmethod
    def _get_deps_from_pipfile(section: str = "default", pipfile_path: str = "Pipfile.lock") -> list[str]:
        with open(pipfile_path) as pipfile:
            pipfile_content = json_load(pipfile)

        return [package + detail.get('version', "") for package, detail in pipfile_content.get(section, {}).items()]

    @staticmethod
    def _get_deps_from_requirements(requirements_path: str = "requirements.txt") -> list[str]:
        with open(requirements_path) as file:
            return file.read().splitlines()

    def _get_deps(self) -> list[str]:
        return self._get_deps_from_pipfile() if self.use_pipenv else self._get_deps_from_requirements()

    def get_sources_and_resources_paths(self) -> list[str]:
        return [
            PROJECT_PATH.joinpath(self.sources_path).as_posix(),
            PROJECT_PATH.joinpath(self.resources_path).as_posix(),
            PROJECT_PATH.joinpath(self.test_sources_path).as_posix(),
            PROJECT_PATH.joinpath(self.test_resources_path).as_posix()
        ]


# - Project commands abstract class
class ProjectCommand:
    """The ProjectCommand abstract class used to execute a new project command"""

    def __init__(self):
        pass

    def build_command_line(self, args: list[str] | None = None) -> list[str]:
        """
        Build the command line to execute
        :param args: the given argument list to use. Parse it with an ArgumentParser if necessary
        :return:
        """
        raise RuntimeError("abstract method -- subclass %s must override" % self.__class__)


# - Project command executor class
class CommandsRunner:
    def __init__(
            self,
            stdin: TextIOWrapper = sys_stdin,
            stdout: TextIOWrapper = sys_stdout,
            stderr: TextIOWrapper = sys_stderr
    ):
        self.__stdin: Final[TextIOWrapper] = stdin
        self.__stdout: Final[TextIOWrapper] = stdout
        self.__stderr: Final[TextIOWrapper] = stderr
        self.__command_dict: Final[dict[str, ProjectCommand]] = {}

    def add_command(self, cmd_name: str, cmd: ProjectCommand) -> None:
        self.__command_dict[cmd_name] = cmd

    def run(self) -> None:
        if sys_argv and len(sys_argv) > 1:
            argv: str = sys_argv[1]
            if argv == "--help" or argv == "-h":
                print(self._get_help_str(), file=self.__stdout)
                return

            current_cmd: ProjectCommand | None = self.__command_dict.get(argv)
            if not self.__command_dict.get(argv):
                print(f"Command unknown: '{argv}'", file=self.__stderr)
                return
            else:
                current_args: list[str] = []
                for argv in sys_argv[2:]:
                    cmd: ProjectCommand | None = self.__command_dict.get(argv)
                    if cmd:
                        self._run_process(current_cmd.build_command_line(current_args))
                        current_args.clear()
                        current_cmd = cmd
                    else:
                        current_args.append(argv)
                self._run_process(current_cmd.build_command_line(current_args))
        else:
            print("Project command missing use --help or -h for help", file=self.__stderr)

    def _run_process(self, args: list[str]) -> None:
        subprocess_run(args, stdin=self.__stdin, stdout=self.__stdout, stderr=self.__stderr, check=True)

    def _get_help_str(self):
        return "PROJECT COMMANDS WRAPPER:\n\n" \
               "Usage: python project.py <COMMAND_1> <arg1_1 ...> ... <COMMAND_N> <argN_1 ...>\n" \
               "\tNote: In order to get the wrapped command help, you can try python project.py <command> --help\n\n" \
               "Available commands are:\n" \
               + ''.join([f"  {cmd}    \t{cls.__doc__}\n" for cmd, cls in self.__command_dict.items()])


# -- Clean Command
class CleanCommand(ProjectCommand):
    """Remove directories generated by the "build" commands (like 'sdist' or 'wheel')"""

    def build_command_line(self, args: list[str] | None = None) -> list[str]:
        command_line: list[str] = [sys_executable, PROJECT_PATH.joinpath("setup.py").as_posix(), "clean"]
        if args:
            command_line.extend(args)
        return command_line


# -- Run Command
class RunCommand(ProjectCommand):
    """Run module which can be in the Maven Standard Directory Layout tree without having to configure the PYTHONPATH"""

    def build_command_line(self, args: list[str] | None = None) -> list[str]:
        command_line: list[str] = [sys_executable, PROJECT_PATH.joinpath("setup.py").as_posix(), "run"]
        if args:
            command_line.extend(args)
        return command_line


# -- Run Command
class TestCommand(ProjectCommand):
    """Run configured unit tests"""

    def build_command_line(self, args: list[str] | None = None) -> list[str]:
        command_line: list[str] = [sys_executable, PROJECT_PATH.joinpath("setup.py").as_posix(), "test"]
        if args:
            command_line.extend(args)
        return command_line


# -- Wheel Command
class WheelCommand(ProjectCommand):
    """Build Wheel archive into the configured 'dist_path' and using the configured 'build_path'"""

    def build_command_line(self, args: list[str] | None = None) -> list[str]:
        command_line: list[str] = [
            "pip",
            "wheel",
            f"--wheel-dir={project_properties.dist_path}",
            PROJECT_PATH.as_posix()
        ]
        if args:
            command_line.extend(args)
        return command_line


# -- Sdist Command
class SdistCommand(ProjectCommand):
    """Build sdist archive into the configured 'dist_path'"""

    def build_command_line(self, args: list[str] | None = None) -> list[str]:
        command_line: list[str] = [sys_executable, PROJECT_PATH.joinpath("setup.py").as_posix(), "sdist"]
        if args:
            command_line.extend(args)
        return command_line


# -- Upload Command
class UploadCommand(ProjectCommand):
    """Upload available deliveries from the configured 'dist_path'"""

    def build_command_line(self, args: list[str] | None = None) -> list[str]:
        command_line: list[str] = ["twine", "upload", f"{Path(project_properties.dist_path).as_posix()}/*"]
        if args:
            command_line.extend(args)
        return command_line


# FUNCTIONS
def run() -> None:
    """"Execute given commands (from sys.argv) with the configured project structure in the PYTHONPATH"""
    # Configure CommandsRunner
    command_runner: Final[CommandsRunner] = CommandsRunner()
    command_runner.add_command('clean', CleanCommand())
    command_runner.add_command('run', RunCommand())
    command_runner.add_command('test', TestCommand())
    command_runner.add_command('wheel', WheelCommand())
    command_runner.add_command('sdist', SdistCommand())
    command_runner.add_command('upload', UploadCommand())

    # Prepare PYTHONPATH
    project_paths: Final[list[str]] = project_properties.get_sources_and_resources_paths()
    pythonpath_env_var: Final[str] = 'PYTHONPATH'
    pythonpath: Final[str] = os_environ.get(pythonpath_env_var)
    if pythonpath:
        project_paths.append(pythonpath)

    # Run commands with project structure in the PYTHONPATH
    try:
        os_environ[pythonpath_env_var] = os_pathsep.join(project_paths)
        command_runner.run()
    finally:
        if pythonpath:
            os_environ[pythonpath_env_var] = pythonpath
        else:
            os_environ.pop(pythonpath_env_var, None)


# SHARED VARIABLES
project_properties = ProjectProperties()

# MAIN
if __name__ == '__main__':
    run()
