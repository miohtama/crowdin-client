import json
import logging
import os
import sys

from optparse import OptionParser

from . import __version__
from .client import push, pull, pretranslate


def main():
    parser = OptionParser(usage='Usage: %prog [options] push|pull|pretranslate')
    parser.add_option('-v', '--version', dest="version", action="store_true",
                      help="Show the version number and exit")
    parser.add_option('-d', '--debug', dest="debug", action="store_true",
                      help="Be more verbose")
    parser.add_option(
        '-a', '--all', dest="include_source", action="store_true",
        help="Push all translation, not just the source translation."
    )
    parser.add_option(
        '-p', '--auto-approve-imported', dest="auto_approve_imported", action="store_true",
        help="Set CrowdIn state for uploaded translations to proof-read complete."
    )

    parser.add_option(
        '-x', '--exclude', dest="excluded_languages", action="store", type="string",
        help="Comma separated list for CrowdIn language codes which are not be pushed"
    )

    options, args = parser.parse_args()

    if options.version:
        sys.stdout.write("crowdin-client %s\n" % __version__)
        return

    if not args or len(args) != 1 or args[0] not in ('push', 'pull', 'pretranslate'):
        parser.print_help()
        return

    if options.debug:
        level = logging.DEBUG
        formatter = logging.Formatter('%(levelname)s: %(message)s')
    else:
        level = logging.INFO
        formatter = logging.Formatter('%(message)s')

    console = logging.StreamHandler()
    console.setLevel(level)
    console.setFormatter(formatter)
    logger = logging.getLogger('crowdin')
    logger.setLevel(level)
    logger.addHandler(console)

    action = args[0]

    config_file = os.path.join(os.path.abspath(os.getcwd()), '.crowdin')
    with open(config_file, 'r') as f:
        conf = json.loads(f.read())

    if action == 'push':
        if options.excluded_languages:
            excluded_languages = options.excluded_languages.split(",")
        else:
            excluded_languages = []

        push(conf, include_source=options.include_source, auto_approve_imported=options.auto_approve_imported, excluded_languages=excluded_languages)

    elif action == 'pull':
        pull(conf)

    elif action == 'pretranslate':
        pretranslate(conf)
