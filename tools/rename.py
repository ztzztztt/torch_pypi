#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  : zhoutao
@License : (C) Copyright 2013-2021, China University of Petroleum
@Contact : zhoutao@s.upc.edu.cn
@Software: PyCharm
@File    : rename
@Time    : 2021/09/04 21:32
@Desc    :
"""
import os
import shutil


def rename_package_name(root_package_path: str):
    if not os.path.exists(root_package_path):
        print(f"Input {root_package_path} Not Exists!!!")
        pass
    else:
        # 列出当前文件夹下的所有文件, 包含目录
        sub_file_or_dir_list = os.listdir(root_package_path)
        for file_or_dir in sub_file_or_dir_list:
            # 生成某一个文件或者文件夹的路径
            file_or_dir_path = os.path.join(root_package_path, file_or_dir)
            # 该路径时文件夹
            if os.path.isdir(file_or_dir_path):
                # 递归执行
                rename_package_name(file_or_dir_path)
            elif os.path.isfile(file_or_dir_path):
                if len(file_or_dir_path.split("%2B")) > 1:
                    out_file_path = file_or_dir_path.replace("%2B", "+")
                    shutil.move(file_or_dir_path, out_file_path)
                    print(f"Rename {file_or_dir_path} to {out_file_path}")
                pass
            else:
                pass
            pass
    pass


if __name__ == '__main__':
    rename_package_name("packages")
