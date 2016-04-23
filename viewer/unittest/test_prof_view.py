#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest


def adjust_path():
    pre_path_list = []
    import sys
    for path in sys.path:
        if "semile" in path:
            pre_path_list.append(path)
    for path in pre_path_list:
        sys.path.insert(0, path)


class ProfViewTest(unittest.TestCase):

    def setUp(self):
        print("==============")
        print("prof_view test")
        print("==============")

    def test_prof_view(self):
        adjust_path()
        from prof_view import ProfileParser, Tree
        parser = ProfileParser("case_test")
        execution_tree = Tree(parser.start_time)
        for prof_row in parser:
            execution_tree.add_row(prof_row)
        execution_tree.finalize()

        cycle_entries = execution_tree.traverse().splitlines()
        golden_file = "golden.txt"
        with open(golden_file) as f:
            golden_entries = f.read().splitlines()

        self.assertEqual(len(cycle_entries), len(golden_entries))
        for cycle, golden in zip(cycle_entries, golden_entries):
            self.assertEqual(cycle, golden)


if __name__ == '__main__':
    unittest.main()
