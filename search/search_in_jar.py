#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""在 jar 文件中查询字符串/文件信息"""

import sys
import os

HELP_INFO = "usage:\n\tpython search_in_jar.py [dir/jar_path] [-i/-name] [search_info]"


class Config:
    search_file = None
    search_info = None


def check_arguments():
    """检查输入参数"""
    args = sys.argv
    if len(args) < 3:
        print(HELP_INFO)
        sys.exit(0)
    config = Config()
    file = os.path.abspath(args[1])
    if not os.path.exists(file):
        print(HELP_INFO)
        sys.exit(0)
    config.search_file = file
    config.search_info = args[2]
    return config


def find_by_file_name(file, info):
    """查找目标文件中是否包含文件名称"""
    if os.path.isdir(file):
        files = os.listdir(file)
        for child_file in files:
            find_by_file_name(os.path.join(file, child_file), info)
    elif file.endswith(".jar"):
        cmd = "zgrep -i %s %s" % (info, file)
        os.system(cmd)


def find_target(config):
    """寻找目标文件"""
    find_by_file_name(config.search_file, config.search_info)


def main():
    config = check_arguments()
    find_target(config)


if __name__ == '__main__':
    main()
