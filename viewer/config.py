#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from configparser import ConfigParser
from global_def import get_use_reduced_time, set_use_reduced_time, \
    get_longer_time_first, set_longer_time_first, \
    get_remove_no_msg_entry, set_remove_no_msg_entry, \
    get_max_branch, set_max_branch, \
    get_max_msg_length, set_max_msg_length, \
    get_traverse, set_traverse


class Config(object):

    def __init__(self, config_file):
        import os
        assert os.path.exists(config_file)
        self.__config = ConfigParser()
        self.__config.read(config_file)

    def set_general_setting(self):
        reduced_time = get_use_reduced_time() if not self.__config.has_option("profile", "use_reduced_time") else \
            "True" == self.__config.get("profile", "use_reduced_time")
        longer_time_first = get_longer_time_first() if not self.__config.has_option("view", "longer_time_first") else \
            "True" == self.__config.get("view", "longer_time_first")
        remove_no_msg_entry = get_remove_no_msg_entry() if not self.__config.has_option("view", "remove_no_msg_entry") else \
            "True" == self.__config.get("view", "remove_no_msg_entry")
        max_branch = get_max_branch() if not self.__config.has_option("view", "max_branch") else \
            int(self.__config.get("view", "max_branch"))
        max_msg_length = get_max_msg_length() if not self.__config.has_option("view", "max_msg_length") else \
            int(self.__config.get("view", "max_msg_length"))
        traverse = get_traverse() if not self.__config.has_option("debug", "traverse") else \
            "True" == self.__config.get("debug", "traverse")
        set_use_reduced_time(reduced_time)
        set_longer_time_first(longer_time_first)
        set_remove_no_msg_entry(remove_no_msg_entry)
        set_max_branch(max_branch)
        set_max_msg_length(max_msg_length)
        set_traverse(traverse)
        print("====  smview setting  =======")
        print("use reduced time: ", reduced_time)
        print("longer time first:", longer_time_first)
        print("remove no msg entry:", remove_no_msg_entry)
        print("max branch:       ", max_branch)
        print("max msg length:   ", max_msg_length)
        print("=============================")

    def get_setting(self, section, option):
        if self.__config.has_option(section, option):
            return self.__config.get(section, option)
        else:
            return None
