from argparse import ArgumentParser
from io import TextIOBase
import sys
import os
import tsunami
import traceback


class CommandError(Exception):

    pass


class CommandParser(ArgumentParser):

    def __init__(self, cmd, **kwargs):
        self.cmd = cmd
        super().__init__(**kwargs)

    def parse_args(self, args=None, namespace=None):
        if (hasattr(self.cmd, 'missing_args_message') and
                not (args or any(not arg.startswith('-') for arg in args))):
            self.error(self.cmd.missing_args_message)
        return super().parse_args(args, namespace)

    def error(self, message):
        if self.cmd._called_from_command_line:
            super().error(message)
        else:
            raise CommandError("Error: %s" % message)


class OutputWrapper(TextIOBase):
    """
    Wrapper around stdout/stderr
    """
    @property
    def style_func(self):
        return self._style_func

    @style_func.setter
    def style_func(self, style_func):
        if style_func and self.isatty():
            self._style_func = style_func
        else:
            self._style_func = lambda x: x

    def __init__(self, out, style_func=None, ending='\n'):
        self._out = out
        self.style_func = None
        self.ending = ending

    def __getattr__(self, name):
        return getattr(self._out, name)

    def isatty(self):
        return hasattr(self._out, 'isatty') and self._out.isatty()

    def write(self, msg, style_func=None, ending=None):
        ending = self.ending if ending is None else ending
        if ending and not msg.endswith(ending):
            msg += ending
        style_func = style_func or self.style_func
        self._out.write(style_func(msg))


class BaseCommand:

    help = ''

    def __init__(self, stdout=None, stderr=None):
        self.stdout = OutputWrapper(stdout or sys.stdout)
        self.stderr = OutputWrapper(stderr or sys.stderr)

    def get_version(self):

        return tsunami.VERSION

    def create_parser(self, prog_name, subcommand):

        parser = CommandParser(
            self, prog="%s %s" % (os.path.basename(prog_name), subcommand),
            description=self.help or None,
        )
        parser.add_argument(
            '--version', action='version', version=self.get_version())

        self.add_arguments(parser)
        return parser

    def add_arguments(self, parser):
        """
        Entry point for subclassed commands to add custom arguments.
        """
        pass

    def print_help(self, prog_name, subcommand):

        parser = self.create_parser(prog_name, subcommand)
        parser.print_help()

    def run_from_argv(self, argv):

        self._called_from_command_line = True
        parser = self.create_parser(argv[0], argv[1])
        options = parser.parse_args(argv[2:])
        cmd_options = vars(options)
        # Move positional args out of options to mimic legacy optparse
        args = cmd_options.pop('args', ())
        self.check()
        try:
            self.execute(*args, **cmd_options)
        except Exception as e:
            print(traceback.format_exc())
            self.stderr.write('%s: %s' % (e.__class__.__name__, e))

            sys.exit(1)

    def check(self):
        if not os.path.exists('.tsunami'):
            raise CommandError('Invalid tsunami project')

    def execute(self, *args, **options):

        raise NotImplementedError
