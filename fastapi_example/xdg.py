import os
import sys
import os.path


def get_exec_dir():
    return os.path.dirname(sys.argv[0])


def get_download_dir():
    user_dir = os.path.join(get_exec_dir(), 'download')
    user_dir = os.path.abspath(user_dir)
    if not os.path.isdir(user_dir):
        os.makedirs(user_dir)
    return user_dir
