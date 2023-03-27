import os
import sys
import os.path
from ntchat.wc import SUPPORT_VERSIONS


def get_exec_dir():
    return os.path.dirname(sys.argv[0])


def get_log_dir():
    log_dir = os.path.join(os.path.dirname(sys.argv[0]), 'log')
    if not os.path.isdir(log_dir):
        os.makedirs(log_dir)
    return log_dir


def get_root_dir():
    return os.path.dirname(os.path.dirname(__file__))


def get_wc_dir():
    return os.path.join(get_root_dir(), "wc")


def get_helper_file(version):
    return os.path.join(get_wc_dir(), f"helper_{version}.dat")


def has_helper_file():
    for name in os.listdir(get_wc_dir()):
        if name.startswith("helper_"):
            return True
    return False


def is_support_version(version):
    return version in SUPPORT_VERSIONS

