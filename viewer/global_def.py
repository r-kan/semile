#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os


def get_delim():
    import platform
    system_name = platform.system()
    if "Darwin" in system_name:
        return "/"
    elif "Linux" in system_name:
        return "/"
    elif "Windows" in system_name:
        return "\\"
    return "/"  # default treats it an unix-like system


__USE_REDUCED_TIME = False


def set_use_reduced_time(use_reduced_time):
    assert type(use_reduced_time) is bool
    global __USE_REDUCED_TIME
    __USE_REDUCED_TIME = use_reduced_time


def get_use_reduced_time():
    return __USE_REDUCED_TIME


__LONGER_TIME_FIRST = False


def set_longer_time_first(longer_time_first):
    assert type(longer_time_first) is bool
    global __LONGER_TIME_FIRST
    __LONGER_TIME_FIRST = longer_time_first


def get_longer_time_first():
    return __LONGER_TIME_FIRST

__REMOVE_NO_MSG_ENTRY = False


def set_remove_no_msg_entry(remove_no_msg_entry):
    assert type(remove_no_msg_entry) is bool
    global __REMOVE_NO_MSG_ENTRY
    __REMOVE_NO_MSG_ENTRY = remove_no_msg_entry


def get_remove_no_msg_entry():
    return __REMOVE_NO_MSG_ENTRY


__MAX_BRANCH = 10


def set_max_branch(max_branch):
    assert type(max_branch) is int
    global __MAX_BRANCH
    __MAX_BRANCH = max_branch


def get_max_branch():
    return __MAX_BRANCH


__MAX_MSG_LENGTH = 40


def set_max_msg_length(msg_length):
    assert type(msg_length) is int
    global __MAX_MSG_LENGTH
    __MAX_MSG_LENGTH = msg_length


def get_max_msg_length():
    return __MAX_MSG_LENGTH


__TRAVERSE = False


def set_traverse(traverse):
    assert type(traverse) is bool
    global __TRAVERSE
    __TRAVERSE = traverse


def get_traverse():
    return __TRAVERSE


__DATA_HOME = (os.environ['HOME'] + get_delim() + 'semile' + get_delim()) if 'HOME' in os.environ else ''


def set_data_home(home):
    global __DATA_HOME
    __DATA_HOME = home


def get_data_home():
    return __DATA_HOME


def get_user_config_file():
    return __DATA_HOME + "config.ini"


def config_action():
    config_file = get_user_config_file()
    if config_file:
        from util.config import Config
        Config(config_file).set_general_setting()


class CustomPrint(object):

    def __init__(self, verbose):
        self.verbose = verbose

    def set_verbose(self, verbose):
        self.verbose = verbose

    def show(self, *msg):
        if self.verbose:
            print(*msg)

    # noinspection PyMethodMayBeStatic
    def info(self, *msg):
        print("[info]", *msg)

    # noinspection PyMethodMayBeStatic
    def error(self, *msg):
        print("[error]", *msg)


__OUT = CustomPrint(False)


def set_verbose(verbose):
    global __OUT
    __OUT.set_verbose(verbose)


def get_verbose():
    return __OUT.verbose


def show(*msg):
    __OUT.show(*msg)


def info(*msg):
    __OUT.info(*msg)


def error(*msg):
    __OUT.error(*msg)
