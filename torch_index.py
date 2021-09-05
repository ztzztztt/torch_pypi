#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  : zhoutao
@License : (C) Copyright 2013-2021, China University of Petroleum
@Contact : zhoutao@s.upc.edu.cn
@Software: PyCharm
@File    : refresh
@Time    : 2021/09/04 19:58
@Desc    : 生成索引文件
"""
import os
from argparse import ArgumentParser


class TorchIndex(object):
    def __init__(self,
                 root_pkg_path: str,
                 output_file: str,
                 pkg_url_prefix: str = "https://download.pytorch.org/whl/",
                 title: str = "Torch Mirror"):
        self._head_string = f"<html><head><title>{title}</title><meta name='api-version' value='2' /></head><body>\n"
        self._foot_string = "</body></html>\n"
        self._pkg_url_prefix = pkg_url_prefix
        self._root_pkg_path = root_pkg_path
        self._output_file = output_file
        pass

    def _get_pkg_index_list_from_pkg(self, sub_path: str = ""):
        body_string_list = []
        current_pkg_path = os.path.join(self._root_pkg_path, sub_path)
        if not os.path.exists(current_pkg_path):
            print(f"Input {current_pkg_path} Not Exists!!!")
        else:
            # 列出当前文件夹下的所有文件, 包含目录
            sub_file_or_dir_list = os.listdir(current_pkg_path)
            for file_or_dir in sub_file_or_dir_list:
                # 生成某一个文件或者文件夹的路径
                file_or_dir_path = os.path.join(current_pkg_path, file_or_dir)
                # 生成子路径
                current_sub_path = os.path.join(sub_path, file_or_dir)
                # 该路径是文件夹, 则递归执行
                if os.path.isdir(file_or_dir_path):
                    body_string_list += self._get_pkg_index_list_from_pkg(current_sub_path)
                # 如果该路径是文件，则获取索引
                elif os.path.isfile(file_or_dir_path):
                    # 去除路径头部的斜杠
                    file_name_ = file_or_dir_path.split(self._root_pkg_path)[-1]
                    file_name_path = file_name_[1:] if file_name_[0:1] == "/" else file_name_
                    body_string_list.append(f"<a href='{file_name_path}'>{file_name_path}</a><br />\n")
                else:
                    pass
                pass
        return body_string_list
        pass

    def _get_pkg_index_list_from_file(self):
        if os.path.exists(self._root_pkg_path):
            with open(self._root_pkg_path, "r") as f:
                requests_url_list = f.readlines()
            requests_url_list = [requests_url.split("\n")[0] for requests_url in requests_url_list]
        else:
            requests_url_list = []
        return requests_url_list

    def _index_from_pkg(self):
        index_string = self._get_pkg_index_list_from_pkg("")
        index_string = sorted(index_string)
        with open(self._output_file, "w") as f:
            f.write(self._head_string + "".join(index_string) + self._foot_string)
        pass

    def _index_from_file(self):
        body_string = ""
        requests_url_list = self._get_pkg_index_list_from_file()
        if len(requests_url_list) > 0:
            for url in requests_url_list:
                sub_file_from_url = url.split(self._pkg_url_prefix)[-1]
                body_string += f"<a href='{sub_file_from_url}'>{sub_file_from_url}</a><br />\n"
        with open(self._output_file, "w") as f:
            f.write(self._head_string + body_string + self._foot_string)
        pass

    def index(self):
        if os.path.isfile(self._root_pkg_path):
            self._index_from_file()
        else:
            self._index_from_pkg()
        pass


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-m", "--mirror", default="stable")
    args = parser.parse_args()
    mirror_type = args.mirror
    if mirror_type == "stable":
        torch_index = TorchIndex(
            root_pkg_path="tmp/torch_stable.txt",
            output_file="index.html",
            pkg_url_prefix="https://download.pytorch.org/whl/",
            title="Torch Mirror"
        )
    elif mirror_type == "lts":
        torch_index = TorchIndex(
            root_pkg_path="tmp/torch_lts.txt",
            output_file="index.html",
            pkg_url_prefix="https://download.pytorch.org/whl/lts/1.8/",
            title="Torch Mirror LTS"
        )
    else:
        torch_index = None
    if torch_index:
        torch_index.index()
    pass
