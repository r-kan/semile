#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import sys
from global_def import get_use_reduced_time, get_longer_time_first, get_max_branch, get_user_config_file, \
    get_max_msg_length, get_traverse

# Ref. http://www.graphviz.org/doc/info/colors.html
__ROOT_COLOR = "plum1"
__GT_10_COLOR = "powderblue"
__GT_50_COLOR = "deepskyblue"


def refine_dot_str(input_str):
    if "\\n" in input_str:  # a mul-line string
        output_str = (input_str.replace("\"", "\\\"").replace("\\n", "\\l")) + "\\l"  # \l at rhs to be left-aligned
    else:
        output_str = input_str.replace("\"", "\\\"")
    return output_str


def get_dot_str(parent, parent_time, parent_no, child, child_time, child_no, child_msg, parent_msg, child_is_group):
    max_msg_length = get_max_msg_length()
    child_msg = refine_dot_str(child_msg)
    parent_msg = refine_dot_str(parent_msg)

    child_msg_str = child_msg if len(child_msg) <= max_msg_length else child_msg[0:max_msg_length - 3] + "..."
    parent_msg_str = parent_msg if len(parent_msg) <= max_msg_length else parent_msg[0:max_msg_length - 3] + "..."

    parent_no_str = ("#%s" % parent_no) if parent_no > 0 else ""
    parent_str = "\"%s%s%s\"" % (parent, parent_no_str, (("\\n" + parent_msg_str) if "" != parent_msg_str else ""))
    child_str = "\"%s#%s%s\"" % (child, child_no, (("\\n" + child_msg_str) if "" != child_msg_str else ""))

    edge_attr = ""
    child_attr = child_str + " [style=filled]" if child_is_group else ""
    time_ratio = 100 * child_time / parent_time
    if time_ratio >= 50:
        edge_attr = ", color=%s, " % __GT_50_COLOR
        child_attr = "%s [color=%s%s]\n" % (child_str, __GT_50_COLOR, (", style=filled" if child_is_group else ""))
    elif time_ratio >= 10:
        edge_attr = ", color=%s, " % __GT_10_COLOR
        child_attr = "%s [color=%s%s]\n" % (child_str, __GT_10_COLOR, (", style=filled" if child_is_group else ""))

    edge_str = " [label=\"%.4f\n(%.4f%%)\"%s];" % (child_time, time_ratio, edge_attr)
    is_root = 0 == parent_no
    parent_attr_str = ("%s [color=%s, style=filled]\n" % (parent_str, __ROOT_COLOR)) if is_root else ""

    return child_attr + parent_attr_str + parent_str + " -> " + child_str + edge_str + "\n"


def get_xml_str(child, child_time, child_no, child_msg, parent_is_group):
    pre_xml_tag = child.xml_str() + "_" if not parent_is_group else "_"
    xml_tag = "%s%s_%.4f" % (pre_xml_tag, str(child_no), child_time)  # TODO: add '#' before str(child_no)
    xml_tag_str = "<%s>\n" % xml_tag
    if child_msg:
        xml_tag_str += "<![CDATA[%s]]>\n" % child_msg
    return xml_tag_str, "</%s>\n" % xml_tag


class Node(object):
    _INDENTATION = " " * 4
    __serial_no = 0

    def __init__(self, position, elapsed_time, message):
        self.position = position
        self.elapsed_time = elapsed_time  # elapsed time on this 'single' execution (not consider 'nodes')
        self.message = message
        self.serial_no = Node.__serial_no
        Node.__serial_no += 1

    def build_view_inner(self, fd, cnt, is_dot, sorted_tuple, parent_is_group):
        self_is_group = isinstance(self, GroupNode)
        build_cnt = 0
        for node_tuple in sorted_tuple:
            if -1 != cnt and build_cnt >= cnt:
                break
            [pos, node, elapsed_time, _] = node_tuple
            logging.debug("%s %s => %s" % (pos, elapsed_time, node.message))
            if is_dot:
                self_to_child_str = get_dot_str(self.position if not parent_is_group else "",
                                                self.elapsed_time, self.serial_no,
                                                pos if not self_is_group else "",
                                                elapsed_time, node.serial_no,
                                                node.message, self.message,
                                                isinstance(node, GroupNode))
            else:
                self_to_child_str, end_xml_tag_str = get_xml_str(pos, elapsed_time, node.serial_no, node.message,
                                                                 self_is_group)
            fd.write(self_to_child_str)
            node.build_view(fd, cnt, is_dot, self_is_group)
            if not is_dot:
                fd.write(end_xml_tag_str)
            build_cnt += 1


class UnitNode(Node):
    def __init__(self, position, elapsed_time, message):
        super(UnitNode, self).__init__(position, elapsed_time, message)
        self.__nodes = {}  # key: position, value: Node
        self.last_pos = None  # keep position of the 'disclosed' node

    def finalize(self):
        for pos in self.__nodes:
            self.__nodes[pos].finalize()
            self.elapsed_time += self.__nodes[pos].elapsed_time

    def enclose_last_pos(self, elapsed_time):
        self.last_pos = None
        self.elapsed_time += elapsed_time

    def add_row(self, row, serial_no):
        assert type(row) is ProfRow
        positions = row.positions
        assert positions
        current_pos = positions[0]
        if current_pos in self.__nodes:
            match_node = self.__nodes[current_pos]
            if self.last_pos == current_pos:  # has available disclosed node
                if 1 == len(positions):  # the disclosed node has popped off => enclose it
                    match_node.enclose_last_pos(row.current_time)  # consider the 'popped-off' interval between nodes
                else:
                    inner_row = ProfRow(positions[1:], row.current_time, row.message)
                    match_node.add_row(inner_row, serial_no)
            else:  # find_or_create a GroupNode
                new_node = UnitNode(current_pos, row.current_time, row.message)
                self.last_pos = current_pos
                if type(match_node) is UnitNode:  # need create GroupNode
                    # TODO: pick up the whole thing why Position need copy here (they are mutable like lists?)
                    import copy
                    group_node = GroupNode(copy.copy(current_pos))
                    group_node.add_node(match_node)
                    group_node.add_node(new_node)
                    self.__nodes[current_pos] = group_node
                else:  # use current GroupNode
                    assert type(match_node) is GroupNode
                    match_node.add_node(new_node)
        else:
            node = UnitNode(current_pos, row.current_time, row.message)
            if 1 == len(positions):
                if self.last_pos:
                    assert False  # may happen in bash(?) but not in current c++ implementation
            else:
                inner_row = ProfRow(positions[1:], row.current_time, row.message)
                node.add_row(inner_row, serial_no)
            self.__nodes[current_pos] = node
            self.last_pos = current_pos

    def traverse(self, indent_cnt=0):
        ret = ""
        for pos in self.__nodes:
            node = self.__nodes[pos]
            assert type(pos) is Position and isinstance(node, Node)
            type_str = "g-" if type(node) is GroupNode else "u-"
            ret += "%s %s%s ==> %.4f\n" % (self._INDENTATION * indent_cnt, type_str, node.position, node.elapsed_time)
            ret += node.traverse(indent_cnt + 1)
        return ret

    def build_view(self, fd, cnt, is_dot, parent_is_group):
        node_tuples = []
        for pos in self.__nodes:
            node = self.__nodes[pos]
            node_tuples.append([node.position, node, node.elapsed_time, node.serial_no])
        if get_longer_time_first():
            sorted_tuple = sorted(node_tuples, key=lambda x: x[2], reverse=True)
        else:
            sorted_tuple = sorted(node_tuples, key=lambda x: x[3], reverse=False)
        self.build_view_inner(fd, cnt, is_dot, sorted_tuple, parent_is_group)


class GroupNode(Node):
    def __init__(self, position):
        super(GroupNode, self).__init__(position, 0, "")
        self.__nodes = []  # UnitNode

    def enclose_last_pos(self, elapsed_time):
        assert self.__nodes
        self.__nodes[-1].elapsed_time += elapsed_time
        self.__nodes[-1].last_pos = None

    def finalize(self):
        for node in self.__nodes:
            node.finalize()
            self.elapsed_time += node.elapsed_time

    def add_node(self, node):
        assert type(node) is UnitNode
        line_order = 1  # start from 1
        if len(self.__nodes) > 0:
            line_order = self.__nodes[-1].position.line_order + 1
        node.position.line_order = line_order
        self.__nodes.append(node)

    def add_row(self, row, serial_no):
        assert self.__nodes
        self.__nodes[-1].add_row(row, serial_no)

    def traverse(self, indent_cnt=0):
        ret = ""
        for node in self.__nodes:
            assert type(node) is UnitNode
            ret += "%s u-%s ==> %.4f\n" % (self._INDENTATION * indent_cnt, node.position, node.elapsed_time)
            ret += node.traverse(indent_cnt + 1)
        return ret

    def build_view(self, fd, cnt, is_dot, _):
        node_tuples = []
        for node in self.__nodes:
            node_tuples.append([node.position, node, node.elapsed_time, node.position.line_order])
        if get_longer_time_first():
            sorted_tuple = sorted(node_tuples, key=lambda x: x[2], reverse=True)
        else:
            sorted_tuple = sorted(node_tuples, key=lambda x: x[3], reverse=False)
        self.build_view_inner(fd, cnt, is_dot, sorted_tuple, False)


class Tree(object):
    def __init__(self, init_time):
        self._current_time = init_time
        self.total_time = 0
        self.__root = UnitNode(root_position, 0, "root")
        self.__serial_no = 1

    def add_row(self, row):
        # print(str(row))
        elapsed_time = row.current_time - self._current_time
        elapsed_time -= ProfileParser.__reduce_time__  # reduce time, to simulate the profiling overhead, e.g., bash -x
        if elapsed_time <= 0:
            elapsed_time = 0.0001
        self.total_time += elapsed_time
        self._current_time = row.current_time
        positions = row.positions
        if not positions:
            self.__root.last_pos = None
            self.__root.elapsed_time += elapsed_time  # consider the 'popped-off' interval between nodes
            return
        prof_row = ProfRow(positions, elapsed_time, row.message)
        self.__root.add_row(prof_row, self.__serial_no)
        self.__serial_no += 1

    def finalize(self):
        self.__root.finalize()

    def traverse(self):
        return self.__root.traverse()

    def build_view(self, fd, cnt, is_dot):  # dot or xml output
        self.__root.build_view(fd, cnt, is_dot, False)


class Position(object):

    def __init__(self, filename, func, line_no):
        self.filename = filename
        self.func = func
        self.line_no = line_no
        self.line_order = None  # order appear in the same filename same line

    def __hash__(self):  # need to be hashable for UnitNode use it as dict key
        return hash((self.filename, self.func, self.line_no))

    def __eq__(self, other):
        if isinstance(other, Position):
            return self.filename == other.filename and \
                self.func == other.func and \
                self.line_no == other.line_no
        return False

    def __str__(self):
        line_no_str = ("," + str(self.line_no)) if self.line_no > 0 else ""
        line_order_str = ("@" + str(self.line_order)) if self.line_order else ""
        return "(" + os.path.basename(self.filename) + "," + self.func + line_no_str + line_order_str + ")"

    def xml_str(self):
        # line_no_str = ("_" + str(self.line_no)) if self.line_no > 0 else ""
        # line_order_str = ("@" + str(self.line_order)) if self.line_order else ""
        # return "(" + os.path.basename(self.filename) + "_" + self.func + line_no_str + line_order_str + ")"
        return self.func


root_position = Position("program", "main", -1)


class ProfRow(object):

    def __init__(self, positions, current_time, message):
        self.positions = positions
        self.current_time = current_time
        self.message = message

    def __str__(self):
        position_str = ""
        for position in self.positions:
            position_str += str(position)
        if "" == position_str:
            position_str = "EMPTY_POS"
        return position_str + " " + str(self.current_time) + " " + str(self.message)


class ProfileParser(object):
    __reduce_time__ = 0  # TODO: find out why remove tailed '__' in naming will cause unresolved reference

    def __init__(self, prof_file):
        self.start_time, self.__rows = ProfileParser.parse(prof_file)

    def __iter__(self):
        return self

    def __next__(self):
        return self.__rows.__next__()

    @staticmethod
    def parse(profile):
        rows = []
        positions_pattern = "+{"
        positions_end_pattern = "}+"
        with open(profile, 'r') as fd:
            for line in fd.readlines():
                pos_positions_begin = line.find(positions_pattern)
                pos_positions_end = line.find(positions_end_pattern)
                if -1 == pos_positions_begin or -1 == pos_positions_end:  # not a recognized line
                    continue
                positions_segment = line[pos_positions_begin + len(positions_pattern):pos_positions_end]
                positions = ProfileParser.parse_positions(positions_segment)
                last_half_segment = line[pos_positions_end + len(positions_end_pattern):]
                pos_message_begin = last_half_segment.find(" ")
                assert -1 != pos_message_begin, last_half_segment
                current_time = float(last_half_segment[0: pos_message_begin])
                message = last_half_segment[pos_message_begin:].replace('\n', "").lstrip()
                rows.append(ProfRow(positions, current_time, message))
        ProfileParser.compute_reduced_time(rows)
        # time adjustment: to let 'time' in each row represents time 'after' execution the same row
        # (instead of 'before' the execution)
        start_time = 0
        row_size = len(rows)
        for i in range(row_size):
            current_time = rows[i].current_time
            if 0 == i:
                start_time = current_time
            if row_size - 1 == i:
                # Note: for the last row, its current_time is then not meaningful...
                # (bcoz no one after it to reveal its actual elapsed time)
                break
            else:
                rows[i].current_time = rows[i + 1].current_time
        return start_time, iter(rows)

    @staticmethod
    def parse_positions(segment):
        positions = segment.split(",")
        if [''] == positions:
            return []
        position_objects = []
        for position in positions:
            items = position.split()
            assert 3 == len(items), len(items)
            position_objects.append(Position(items[0], items[1], int(items[2])))
        return position_objects

    @staticmethod
    def compute_reduced_time(rows):
        if not get_use_reduced_time():
            return
        elapsed_times = []
        last_time = rows[0].current_time
        row_size = len(rows)
        for i in range(row_size - 1):
            elapsed_time = rows[i + 1].current_time - last_time
            elapsed_times.append(elapsed_time)
            last_time = rows[i + 1].current_time
        elapsed_times.sort()
        if elapsed_times:
            ProfileParser.__reduce_time__ = elapsed_times[int(len(elapsed_times) / 2)]  # use median as reduced time
            print("use reduced time:", ProfileParser.__reduce_time__)


def flush_print(msg, new_line=False):
    if new_line:
        print(msg)
    else:
        print(msg, end="")
    sys.stdout.flush()


def locate_abs_exec(program):  # 'program' can be an absolute path name, or just a basename
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None


DEFAULT_CONFIG_FILE = "config.ini"


class ProfileViewer(object):

    def __init__(self):
        self.__has_error = False
        import argparse
        arg_parser = argparse.ArgumentParser(description="The Semile Viewer")
        arg_parser.add_argument('profile')
        arg_parser.add_argument("-c", "--config",
                                dest="config_file", default=DEFAULT_CONFIG_FILE,
                                help="config file name (default: '" + DEFAULT_CONFIG_FILE + "')")
        args = arg_parser.parse_args()
        config_file = get_user_config_file() if os.path.exists(get_user_config_file()) else args.config_file
        if not os.path.exists(config_file):
            print("config file not found, use default setting")
        else:
            print("use config file:", config_file)
            ProfileViewer.__parse_config(config_file)

        self.__profile = args.profile
        if not os.path.exists(self.__profile):
            print("[ERROR]", self.__profile, "not available")
            sys.exit()

        print("profile:", self.__profile)
        flush_print("Parsing profile data...")
        parser = ProfileParser(self.__profile)
        self.__execution_tree = Tree(parser.start_time)
        for prof_row in parser:
            self.__execution_tree.add_row(prof_row)
        self.__execution_tree.finalize()
        flush_print("done", True)

    @staticmethod
    def __parse_config(config_file):
        from config import Config
        config = Config(config_file)
        config.set_general_setting()

    def traverse(self):
        return self.__execution_tree.traverse()

    def build_prof_view(self):
        _, file_extname = os.path.splitext(self.__profile)
        adopt_name = os.path.basename(self.__profile).replace(file_extname, '')
        dot_file = adopt_name + ".dot"
        pic_file = adopt_name + ".png"
        flush_print("Generate prof view [" + pic_file + "] ...")
        dot_fd = ProfileViewer.__begin_dot(dot_file)
        self.__execution_tree.build_view(dot_fd, get_max_branch(), True)
        ProfileViewer.__end_dot(dot_fd, dot_file, pic_file)
        flush_print("done", True)

        xml_file = adopt_name + ".xml"
        flush_print("Generate command view [" + xml_file + "] ...")
        xml_fd = open(xml_file, 'w')
        xml_fd.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
        main_tag_str = "program_" + "%.4f" % self.__execution_tree.total_time
        xml_fd.write("<" + main_tag_str + ">\n")
        self.__execution_tree.build_view(xml_fd, -1, False)
        xml_fd.write("</" + main_tag_str + ">")
        xml_fd.close()
        flush_print("done", True)

    @staticmethod
    def __begin_dot(dot_file):
        write_fd = open(dot_file, 'w')
        write_fd.write("digraph cmdView {\n")
        write_fd.write("node [shape=box]\n")
        write_fd.write("rankdir=LR;\n")
        return write_fd

    @staticmethod
    def __end_dot(write_fd, dot_file, pic_file):
        write_fd.write("}\n")
        write_fd.close()
        dot_path = locate_abs_exec("dot")
        if not dot_path:
            print("[WARNING] \"dot\" not available, skip generating PNG file")
        else:
            os.system(dot_path + " " + dot_file + " -T png -o " + pic_file)
        os.remove(dot_file)


if __name__ == '__main__':
    viewer = ProfileViewer()
    if get_traverse():
        print(viewer.traverse())  # this only print node info. (irrelevant to profile construction)
    viewer.build_prof_view()
