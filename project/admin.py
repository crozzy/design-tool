#!/usr/bin/python
import sys
import os
import subprocess
import logging
import glob

logger = logging.getLogger('admin')

# Helpers from utils
def normpath(path):
    """Normalize pathname, preserving ending slash and initial './'."""
    new_path = os.path.normpath(path)
    if path.startswith('./'):
        # Preserve starting './' as this is necessary if the path is an
        # executable to be passed to subprocess.call().
        new_path = './' + new_path
    if path.endswith('/'):
        # Preserve trailing slash, as it has semantic value in some contexts
        # (e.g., as rsync source).
        new_path += '/'
    return new_path

def dirpath(path, *args):
    """Return the directory name of pathname PATH, joining with ARGS. """
    new_path = normpath(os.path.join(os.path.dirname(path), *args))
    return new_path if new_path else '.'

here = lambda *args: dirpath(__file__, *args)

def proccall(*cmd, **kw):
    logger.debug('proc.call: %r, kw=%r', cmd, kw)
    if 'stdin' in kw and isinstance(kw['stdin'], str):
        data = kw.pop('stdin')
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, **kw)
        p.stdin.write(data)
        p.stdin.close()
    subprocess.check_call(cmd, **kw)

# Get virtualenv(or potential) virtualenv dir 
VENVDIR = os.environ.get('ADMIN_VENV', os.path.dirname('../.virtualenv/jobdesign'))

def make_virtualenv(venv_dir):
    if not os.path.exists(venv_dir):
        proccall('/usr/bin/virtualenv', VENVDIR)
        path = glob.glob('./distribute-*.tar.gz')[0]
        try:
            os.remove(path)
        except Exception as e:
            print e

def virtualenv_activate(venv_dir, ignore_errors=False):
    activate = os.path.join(venv_dir, 'bin/activate_this.py')
    execfile(activate, dict(__file__=activate))

def pip_install(venv, *args):
    return proccall(os.path.join(venv, 'bin/pip'), 'install',
        '--no-index', '-f', 'http://labs.careesma.lan/archive/pip/',
        *args,
        env=dict(PIP_DOWNLOAD_CACHE='~/.local/share/pip-cache'))

# COMMANDS
def cmd_install_deps():
    make_virtualenv(VENVDIR)
    virtualenv_activate(VENVDIR, ignore_errors=True)
    pip_install(VENVDIR, '-r', here('../requirements.txt'))

# TODO(jcrosland): Make more generic/moveable
def cmd_runserver():
    proccall(os.path.join(VENVDIR, 'bin/python'), 'runserver.py')

def main(cmd, *args):
    cmd_func = globals()['cmd_' + cmd.replace('-', '_')]
    return cmd_func(*args)

if __name__ == '__main__':
    sys.exit(main(*sys.argv[1:]))
