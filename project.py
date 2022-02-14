import subprocess
from configparser import ConfigParser, ExtendedInterpolation
from json import load as json_load
from os import environ as os_environ
from pathlib import Path
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
        self.__config_parser: Final[ConfigParser] = self._load_project_ini_file(ini_file_path, env_var_section)

        # - PROJECT section
        self.name: Final[str] = self.__config_parser.get(project_section, 'name', fallback=None)
        self.version: Final[str] = self.__config_parser.get(project_section, 'version', fallback=None)
        self.author: Final[str] = self.__config_parser.get(project_section, 'author', fallback=None)
        self.url: Final[str] = self.__config_parser.get(project_section, 'url', fallback=None)
        self.author_email: Final[str] = self.__config_parser.get(project_section, 'email', fallback=None)
        self.description: Final[str] = self.__config_parser.get(project_section, 'description', fallback=None)
        self.long_description_file: Final[str] = self.__config_parser.get(
            project_section, 'long_description_file', fallback=DEFAULT_LONG_DESCRIPTION_FILE
        )
        self.long_description_content_type: Final[str] = self.__config_parser.get(
            project_section, 'long_description_content_type', fallback=DEFAULT_LONG_DESCRIPTION_CONTENT_TYPE
        )
        self.license: Final[str] = self.__config_parser.get(project_section, 'license', fallback=None)
        self.use_pipenv: Final[bool] = self.__config_parser.getboolean(
            INI_PROJECT_SECTION, 'use_pipenv', fallback=DEFAULT_USE_PIPENV
        )
        self.install_requires: Final[list[str]] = self._get_deps(self.use_pipenv)
        self.test_file_pattern: Final[str] = self.__config_parser.get(
            INI_PROJECT_SECTION, 'test_file_pattern', fallback=DEFAULT_TEST_FILE_PATTERN
        )

        # - PROJECT.ENTRY_POINTS section
        self.entry_points: Final[dict[str, list[str]] | None] = self._load_entry_points(
            self.__config_parser, entry_points_section
        )

        # - PROJECT.STRUCTURE section
        self.sources_path: Final[str] = self.__config_parser.get(
            structure_section, 'sources_path', fallback=DEFAULT_SRC_PATH
        )
        self.resources_path: Final[str] = self.__config_parser.get(
            structure_section, 'resources_path', fallback=DEFAULT_RESOURCES_PATH
        )
        self.test_sources_path: Final[str] = self.__config_parser.get(
            structure_section, 'test_sources_path', fallback=DEFAULT_TEST_SRC_PATH
        )
        self.test_resources_path: Final[str] = self.__config_parser.get(
            structure_section, 'test_resources_path', fallback=DEFAULT_TEST_RESOURCES_PATH
        )
        self.build_path: Final[str] = self.__config_parser.get(
            structure_section, 'build_path', fallback=DEFAULT_BUILD_PATH
        )
        self.dist_path: Final[str] = self.__config_parser.get(
            structure_section, 'dist_path', fallback=DEFAULT_DIST_PATH
        )

    @staticmethod
    def _load_project_ini_file(project_ini_file_path: str, environment_section: str) -> ConfigParser:
        esc_env_vars: Final[dict[str, str]] = {k: v.replace('$', '$$') for k, v in dict(os_environ).items()}
        config_parser: Final[ConfigParser] = ConfigParser(interpolation=ExtendedInterpolation())
        config_parser.read(project_ini_file_path)
        if config_parser.has_section(environment_section):
            config_parser[environment_section] = dict(config_parser[environment_section], **esc_env_vars)
        else:
            config_parser[environment_section] = esc_env_vars
        return config_parser

    @staticmethod
    def _load_entry_points(config_parser: ConfigParser, entry_point_section: str) -> dict[str, list[str]] | None:
        if not config_parser.has_section(entry_point_section):
            return None

        return {k: v.splitlines() for k, v in config_parser.items(entry_point_section)}

    @staticmethod
    def _get_deps_from_pipfile(section: str = "default", pipfile_path: str = "Pipfile.lock") -> list[str]:
        with open(pipfile_path) as pipfile:
            pipfile_content = json_load(pipfile)

        return [package + detail.get('version', "") for package, detail in pipfile_content.get(section, {}).items()]

    @staticmethod
    def _get_deps_from_requirements(requirements_path: str = "requirements.txt") -> list[str]:
        with open(requirements_path) as file:
            return file.read().splitlines()

    @classmethod
    def _get_deps(cls, use_pipfile: bool = True) -> list[str]:
        return cls._get_deps_from_pipfile() if use_pipfile else cls._get_deps_from_requirements()


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
    def __init__(self):
        self.__command_dict: dict[str, ProjectCommand] = {}

    def add_command(self, cmd_name: str, cmd: ProjectCommand) -> None:
        self.__command_dict[cmd_name] = cmd

    def run(self) -> None:
        if sys_argv and len(sys_argv) > 1:
            argv: str = sys_argv[1]
            if argv == "--help" or argv == "-h":
                print(self._get_help_str())
                return

            current_cmd: ProjectCommand | None = self.__command_dict.get(argv)
            if not self.__command_dict.get(argv):
                print(f"Command unknown: '{argv}'", file=sys_stderr)
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
            print("Project command missing use --help or -h for help", file=sys_stderr)

    @staticmethod
    def _run_process(args: list[str]) -> None:
        subprocess.run(args, stdin=sys_stdin, stdout=sys_stdout, stderr=sys_stderr, check=True)

    def _get_help_str(self):
        return "Usage: python project.py <command_1> <args1...> ... <commmand_N> <args-N>\n" \
               + "\tNote: You can also try python project.py <command> --help\n\n" \
               + "Available commands are:\n" \
               + ''.join([f"  {cmd}\t\t{cls.__doc__}\n" for cmd, cls in self.__command_dict.items()])


# -- Clean Command
class CleanCommand(ProjectCommand):
    """Remove directories generated by the 'build' command"""

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
    """Build Wheel archive into the configured 'dist_path' and using the configured 'build_path"""

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


# SHARED VARIABLES
project_properties = ProjectProperties()

if __name__ == '__main__':
    command_runner: Final[CommandsRunner] = CommandsRunner()
    command_runner.add_command('clean', CleanCommand())
    command_runner.add_command('run', RunCommand())
    command_runner.add_command('test', TestCommand())
    command_runner.add_command('wheel', WheelCommand())
    command_runner.add_command('sdist', SdistCommand())
    command_runner.add_command('upload', UploadCommand())
    command_runner.run()
