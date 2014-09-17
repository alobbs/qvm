import os
import sys
import copy
import shlex
import logging
import subprocess

def run(cmd):
    import os
    print >> sys.stderr, "+ %s"%(cmd)
    return os.system(cmd)

def run_command(args, stdin=None, raiseonerr=True, env=None, cwd=None):
    """
    Execute a command and return stdin, stdout and the process return code.

    :param args: List of arguments for the command
    :param stdin: Optional input to the command
    :param raiseonerr: If True, raises an exception if the return code is
    :param env: Dictionary of environment variables passed to the command.
        When None, current environment is copied
    :param cwd: Current working directory
    """
    p_in = None
    p_out = None
    p_err = None

    if env is None:
        # copy default env
        env = copy.deepcopy(os.environ)
        env["PATH"] = "/bin:/sbin:/usr/bin:/usr/sbin"
    if stdin:
        p_in = subprocess.PIPE
    p_out = subprocess.PIPE
    p_err = subprocess.PIPE

    if type(args) == str:
        arg_string = args
        args = shlex.split(arg_string)
    else:
        arg_string = ' '.join(shell_quote(a) for a in args)

    print >> sys.stderr, "+ %s"%(arg_string)
    try:
        pid = subprocess.Popen(args, stdin=p_in, stdout=p_out, stderr=p_err,
                               close_fds=True, env=env, cwd=cwd)
        stdout, stderr = pid.communicate(stdin)
    except KeyboardInterrupt:
        logging.debug('Process interrupted')
        pid.wait()
        raise
    except:
        logging.debug('Process execution failed')
        raise

    logging.debug('Process finished, return code=%s', pid.returncode)

    if pid.returncode != 0 and raiseonerr:
        raise subprocess.CalledProcessError(pid.returncode, arg_string)

    return (stdout, stderr, pid.returncode)
