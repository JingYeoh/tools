#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

HELP_INFO = "usage:\n\tpython extract_apk.py [apk_path] [output_dir]"


def unzip_apk(apk_path, outdir_path):
    """使用 apktool 解压 apk 并返回 dex list"""
    outdir = os.path.join(outdir_path, "apktool")
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    os.chdir(outdir)
    cmd = "unzip %s" % apk_path
    print("cmd = %s" % cmd)
    status = os.system(cmd)
    if not status == 0:
        print("execute apktool failed")
        sys.exit(0)
    # 获取所有的 dex 文件
    files = os.listdir(outdir)
    dex_list = []
    for file in files:
        if not os.path.isdir(file):
            if file.endswith("dex"):
                dex_list.append(os.path.abspath(file))
    return dex_list


def d2j_dex2jar(dex_list, outdir_path):
    """使用 d2j 转换 dex 为 jar"""
    print("----------- d2j_dex2jar -----------")
    print("dex_list : %s" % dex_list)
    outdir = os.path.join(outdir_path, "jars")
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    os.chdir(outdir)
    for dex in dex_list:
        cmd = "d2j-dex2jar %s" % dex
        print("cmd = %s" % cmd)
        status = os.system(cmd)
        if not status == 0:
            print("execute d2j failed")
            sys.exit(0)


def extract_apk(apk_path, outdir_path):
    apk_path = os.path.abspath(apk_path)
    outdir_path = os.path.abspath(outdir_path)
    print("outdir_path %s" % outdir_path)
    if not os.path.exists(apk_path):
        print("file %s does not exist" % apk_path)
        sys.exit(0)
    if not os.path.exists(outdir_path):
        os.mkdir(outdir_path)
        print("mkdir out_dir %s" % outdir_path)
    dex_list = unzip_apk(apk_path, outdir_path)
    print(dex_list)
    d2j_dex2jar(dex_list, outdir_path)


def main(args):
    """用于 apk 的反编译"""
    if len(args) == 0:
        print(HELP_INFO)
        sys.exit(0)
    apk_path = ""
    outdir_path = "."
    if len(args) == 2:
        if not args[1].endswith("apk"):
            print(HELP_INFO)
            sys.exit(0)
        apk_path = args[1]
    if len(args) == 3:
        apk_path = args[1]
        outdir_path = args[2]
    extract_apk(apk_path, outdir_path)


if __name__ == '__main__':
    main(sys.argv)
