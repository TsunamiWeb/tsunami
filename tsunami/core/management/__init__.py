from collections import defaultdict
from contextlib import suppress
from importlib import import_module
from tsunami.core.management.base import (
    BaseCommand, CommandError, CommandParser
)
import functools
import os
import pkgutil
import sys
import tsunami


def find_commands(management_dir):
    """
    Given a path to a management directory, return a list of all the command
    names that are available.
    """
    command_dir = os.path.join(management_dir, 'commands')
    return [name for _, name, is_pkg in pkgutil.iter_modules([command_dir])
            if not is_pkg and not name.startswith('_')]


def load_command_class(app_name, name):
    """
    Given a command name and an application name, return the Command
    class instance. Allow all errors raised by the import process
    (ImportError, AttributeError) to propagate.
    """
    module = import_module('%s.management.commands.%s' % (app_name, name))
    return module.Command()


@functools.lru_cache(maxsize=None)
def get_commands():

    commands = {name: 'tsunami.core' for name in find_commands(
        __path__[0])}
    return commands


class ManagementUtility:

    def __init__(self, argv=None):
        self.argv = argv or sys.argv[:]
        self.prog_name = os.path.basename(self.argv[0])
        self.settings_exception = None

    def main_help_text(self, commands_only=False):
        """Return the script's main help text, as a string."""
        if commands_only:
            usage = sorted(get_commands())
        else:
            usage = [
                "",
                (
                    f"Type '{self.prog_name} help <subcommand>' "
                    "for help on a specific subcommand."),
                "",
                "Available subcommands:",
            ]
            commands_dict = defaultdict(lambda: ['version'])
            for name, app in get_commands().items():
                if app == 'tsunami.core':
                    app = 'tsunami'
                else:
                    app = app.rpartition('.')[-1]
                commands_dict[app].append(name)
            for app in sorted(commands_dict):
                usage.append("")
                usage.append("[%s]" % app)
                for name in sorted(commands_dict[app]):
                    usage.append("    %s" % name)

        return '\n'.join(usage)

    def fetch_command(self, subcommand):

        commands = get_commands()
        try:
            app_name = commands[subcommand]
        except KeyError:

            sys.stderr.write(
                "Unknown command: %r\nType '%s help' for usage.\n"
                % (subcommand, self.prog_name)
            )
            sys.exit(1)
        if isinstance(app_name, BaseCommand):
            # If the command is already loaded, use it directly.
            klass = app_name
        else:
            klass = load_command_class(app_name, subcommand)
        return klass

    def execute(self):
        """
        Given the command-line arguments, figure out which subcommand is being
        run, create a parser appropriate to that command, and run it.
        """
        try:
            subcommand = self.argv[1]
        except IndexError:
            subcommand = 'help'  # Display help if no arguments were given.

        # Preprocess options to extract --settings and --pythonpath.
        # These options could affect the commands that are available, so they
        # must be processed early.
        parser = CommandParser(
            None, usage="%(prog)s subcommand [options] [args]", add_help=False)
        parser.add_argument('args', nargs='*')  # catch-all
        with suppress(CommandError):  # Ignore any option errors at this point.
            options, args = parser.parse_known_args(self.argv[2:])

        if subcommand == 'help':
            if '--commands' in args:
                sys.stdout.write(
                    self.main_help_text(commands_only=True) + '\n')
            elif len(options.args) < 1:
                sys.stdout.write(self.main_help_text() + '\n')
            else:
                self.fetch_command(
                    options.args[0]).print_help(
                    self.prog_name, options.args[0])

        elif subcommand == 'version' or self.argv[1:] == ['--version']:
            sys.stdout.write(tsunami.VERSION + '\n')
        elif self.argv[1:] in (['--help'], ['-h']):
            sys.stdout.write(self.main_help_text() + '\n')
        else:
            self.fetch_command(subcommand).run_from_argv(self.argv)


def execute_from_command_line(argv=None):
    """Run a ManagementUtility."""
    utility = ManagementUtility(argv)
    utility.execute()
