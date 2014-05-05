#!/usr/bin/env python

# Python 2/3 compatibility
from __future__ import division, absolute_import, print_function, unicode_literals

import argparse
import os

import core
import settings
import view
from daemon import Daemon


def app_run(debug=False):
    view.app.run(host=settings.HOST, port=settings.PORT, debug=debug)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--daemon",
        help="Run as a daemon, keeping pid in FILE.", metavar="FILE")
    parser.add_argument("--log", default="/dev/null",
        help="Write log output to FILE. Only in daemon mode.", metavar="FILE")
    parser.add_argument("--debug", action="store_true",
        help="Run in debug mode. Cannot be used with --daemon.")
    parser.add_argument("root_dir", nargs="?",
        help="Directory to serve music from. Overrides settings.ROOT_DIR. " \
            "Falls back to current directory if neither is set.")
    args = parser.parse_args()
    if not args.root_dir:
        args.root_dir = settings.__dict__.get("ROOT_DIR", ".")
    return args


def process_path(path):
    return os.path.abspath(os.path.expanduser(path))


def main():
    args = parse_args()
    core.set_root_dir(args.root_dir)
    if args.daemon:
        pidfile = process_path(args.daemon)
        logfile = process_path(args.log)
        daemon = Daemon(run=app_run, pidfile=pidfile, stderr=logfile)
        daemon.start()
    else:
        app_run(debug=args.debug)


if __name__ == "__main__":
    main()
