#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  : zhoutao
@License : (C) Copyright 2013-2021, China University of Petroleum
@Contact : zhoutao@s.upc.edu.cn
@Software: PyCharm
@File    : pip_dep_file
@Time    : 2021/08/30 20:54
@Desc    :
"""
import os
import sys
import requests
from lxml import etree
from urllib import parse
from wget import download


torch_packages_url = "https://download.pytorch.org/whl/torch_stable.html"
torch_prefix = "https://download.pytorch.org/whl/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 '
                  'Safari/537.36 QIHU 360SE '
}

sub_file_name = ""
total_items_num = 0
finish_items_num = 0


def request_torch_url_list(pip_req_url: str):
    response = requests.get(pip_req_url, headers=headers)
    page = etree.HTML(response.text)
    hrefs = page.xpath("//a")
    requests_url_array = []
    for href in hrefs:
        if href.attrib.get("href"):
            requests_url = torch_prefix + href.attrib.get("href")
            requests_url_array.append(requests_url)
        else:
            continue
    return requests_url_array
    pass


def get_torch_url_list(pip_req_url: str, tmp_file: str = "./tmp/torch_stable.txt"):
    if not os.path.exists("../tmp"):
        os.makedirs("../tmp")
    if os.path.exists(tmp_file):
        with open(tmp_file, "r") as f:
            requests_url_array = f.readlines()
        requests_url_array = [requests_url.split("\n")[0] for requests_url in requests_url_array]
    else:
        requests_url_array = request_torch_url_list(pip_req_url)
        with open(tmp_file, "w") as f:
            for requests_url in requests_url_array:
                f.write(f"{requests_url}\n")
    return requests_url_array


def set_1_sub_set_2(set_1: set, set_2: set):
    difference_set = set_1.difference(set_2)
    return difference_set


def get_torch_package_name_from_url(torch_url):
    return torch_url.split("/")[-1]
    pass


def get_sub_torch_package_name_from_url(torch_url):
    sub_string = torch_url.split(torch_prefix)[-1]
    sub_folder_list = sub_string.split("/")
    if len(sub_folder_list) > 1:
        return sub_folder_list[0]
    else:
        return ""
    pass


def download_torch_package(dest: str, items: int = 10):
    if not os.path.exists(dest):
        os.makedirs(dest)
    requests_url_array = get_torch_url_list(torch_packages_url)
    if items == -1:
        items = len(requests_url_array)
    global total_items_num
    total_items_num = items
    for index, torch_url in enumerate(requests_url_array):
        if index >= items:
            break
        global sub_file_name, finish_items_num
        finish_items_num = index + 1
        # 文件名
        file_name = get_torch_package_name_from_url(torch_url)
        # 子文件夹路径
        sub_folder = get_sub_torch_package_name_from_url(torch_url)
        if not os.path.exists(os.path.join(dest, sub_folder)):
            os.makedirs(os.path.join(dest, sub_folder))
        # 生成子文件夹
        out_file_path = os.path.join(dest, sub_folder, file_name)
        sub_file_name = os.path.join(sub_folder, file_name)
        # 特殊字符处理，例如%2B处理为+
        # 将下载连接变成url的格式
        torch_url = parse.unquote(torch_url)
        # 将文件路径中特殊字符转换
        out_file_path = parse.unquote(out_file_path)
        if not os.path.exists(out_file_path):
            # print(out_file_path)
            download(torch_url, out_file_path, bar=bar_progress)
            pass
        else:
            print(f"{sub_file_name:75} File Exists")
            pass
        pass
    pass


def bar_progress(current, total, width=80):
    width = 80
    mb = 1024**2
    total_mb = total / mb
    current_mb = current / mb
    percent = current / total * 100
    left = "=" * int(percent * width / 100)
    bar = left + (width - int(percent * width / 100)) * " "
    progress_message = f"Downloading: {sub_file_name:75}: [{bar}] {percent:.2f}% [{current_mb:.2f}MB/{total_mb:.2f}MB]" \
                       f" [{finish_items_num}/{total_items_num}]"
    sys.stdout.write("\r" + progress_message)
    sys.stdout.flush()
    if current == total:
        sys.stdout.flush()
        print("\r")


if __name__ == '__main__':
    download_torch_package("packages", items=-1)
    pass
