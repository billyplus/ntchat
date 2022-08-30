import os
import sys
import os.path


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


def get_support_download_url():
    return 'https://webcdn.m.qq.com/spcmgr/download/WeChat3.6.0.18.exe'


if __name__ == '__main__':
    print(get_helper_file('3.6.0.18'))
