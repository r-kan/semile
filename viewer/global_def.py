#!/usr/bin/env python3
# -*- coding: utf-8 -*-


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


__MAX_MSG_LENGTH = 100


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
