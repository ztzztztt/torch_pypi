#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  : zhoutao
@License : (C) Copyright 2013-2021, China University of Petroleum
@Contact : zhoutao@s.upc.edu.cn
@Software: PyCharm
@File    : move
@Time    : 2021/09/04 10:18
@Desc    :
"""
import os
import shutil


def get_torch_package_url(tmp_file: str = "./tmp/torch_stable.txt"):
    if not os.path.exists("../tmp"):
        os.makedirs("../tmp")
    if os.path.exists(tmp_file):
        with open(tmp_file, "r") as f:
            requests_url_array = f.readlines()
        requests_url_array = [requests_url.split("\n")[0] for requests_url in requests_url_array]
    else:
        requests_url_array = []
    return requests_url_array


def get_torch_package_name_from_url(torch_url):
    return torch_url.split("/")[-1]
    pass


def get_sub_torch_package_name_from_url(torch_url):
    sub_string = torch_url.split("https://download.pytorch.org/whl/")[-1]
    return sub_string.split("/")[0]
    pass


def sync_torch_package(dest: str):
    if not os.path.exists(dest):
        os.makedirs(dest)
    requests_url_array = get_torch_package_url()
    for index, torch_url in enumerate(requests_url_array):
        file_name = get_torch_package_name_from_url(torch_url)
        # 子文件夹
        sub_folder = get_sub_torch_package_name_from_url(torch_url)
        if not os.path.exists(os.path.join(dest, sub_folder)) and (sub_folder != file_name):
            os.makedirs(os.path.join(dest, sub_folder))
        int_file_path = os.path.join(dest, file_name)
        if sub_folder != file_name:
            out_file_path = os.path.join(dest, sub_folder, file_name)
        else:
            out_file_path = os.path.join(dest, file_name)
        if not os.path.exists(int_file_path):
            print(f"{file_name:60} File Not Exists")
            pass
        else:
            shutil.move(int_file_path, out_file_path)
            print(f"Moving {file_name:60} to {sub_folder:60}")
        pass


if __name__ == '__main__':
    sync_torch_package("torch")
