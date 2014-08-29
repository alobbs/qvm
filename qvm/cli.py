import sys

ANSI_ERROR   = '\033[91m'
ANSI_WARNING = '\033[93m'
ANSI_END     = '\033[0m'

def _error_pre():
    return '[%sERROR%s]'%(ANSI_ERROR, ANSI_END)

def _warning_pre():
    return '[%sWARNING%s]'%(ANSI_WARNING, ANSI_END)

def FATAL_ERROR(msg):
    ERROR(msg)
    raise SystemExit

def ERROR(msg):
    print >> sys.stderr, '%s %s'%(_error_pre(), msg)

def WARNING(msg):
    print >> sys.stderr, '%s %s'%(_warning_pre(), msg)
