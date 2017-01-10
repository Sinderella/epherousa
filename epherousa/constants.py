# coding=utf-8

from os import path

# defile configuration file paths
CONFIG_FILE_NAME = 'ephe.yml'
DEFAULT_SYSTEM_CONFIG = path.join('/etc/', CONFIG_FILE_NAME)
DEFAULT_USER_CONFIG = path.join(path.expanduser('~'), CONFIG_FILE_NAME)

# default configurations
DEFAULT_ENABLE = None
DEFAULT_DISABLE = None
DEFAULT_VERBOSE = False
DEFAULT_QUIET = False
DEFAULT_PHRASE = False
DEFAULT_LIMIT = 5
