#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  : zhoutao
@License : (C) Copyright 2013-2021, China University of Petroleum
@Contact : zhoutao@s.upc.edu.cn
@Software: PyCharm
@File    : torch_mirror
@Time    : 2021/09/02 11:12
@Desc    : torch镜像源文件下载
"""
import os
import sys
import requests
from lxml import etree
from urllib import parse
from wget import download
from argparse import ArgumentParser


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 '
                  'Safari/537.36 QIHU 360SE '
}


class TorchMirror(object):
    def __init__(self, dest: str,
                 torch_mirror: str = "https://download.pytorch.org/whl/torch_stable.html",
                 torch_prefix: str = "https://download.pytorch.org/whl/",
                 tmp_dir: str = "tmp", tmp_file_name: str = "torch_stable.txt"):
        self._dest_dir = dest
        self._tmp_dir = tmp_dir
        self._tmp_file_name = tmp_file_name
        self._tmp_file = os.path.join(self._tmp_dir, self._tmp_file_name)
        self._torch_prefix = torch_prefix
        self._torch_mirror_pkg = torch_mirror
        self._sub_file_name = ""
        self._total_pkg_num = 0
        self._finish_pkg_num = 0
        pass

    def _request_torch_url_list(self, torch_req_url: str):
        response = requests.get(torch_req_url, headers=headers)
        page = etree.HTML(response.text)
        hrefs = page.xpath("//a")
        requests_url_list = []
        for href in hrefs:
            if href.attrib.get("href"):
                requests_url = self._torch_prefix + href.attrib.get("href")
                requests_url_list.append(requests_url)
            else:
                continue
        return requests_url_list
        pass

    def _get_torch_url_list(self, torch_req_url: str):
        if not os.path.exists(self._tmp_dir):
            os.makedirs(self._tmp_dir)
        if os.path.exists(self._tmp_file):
            with open(self._tmp_file, "r") as f:
                requests_url_list = f.readlines()
            requests_url_list = [requests_url.split("\n")[0] for requests_url in requests_url_list]
        else:
            requests_url_list = self._request_torch_url_list(torch_req_url)
            with open(self._tmp_file, "w") as f:
                for requests_url in requests_url_list:
                    f.write(f"{requests_url}\n")
        return requests_url_list

    def _get_torch_pkg_name_from_url(self, torch_url):
        return torch_url.split("/")[-1]

    def _get_sub_folder_name_from_url(self, torch_url):
        sub_string = torch_url.split(self._torch_prefix)[-1]
        sub_folder_list = sub_string.split("/")
        if len(sub_folder_list) > 1:
            return sub_folder_list[0]
        else:
            return ""

    def _progress(self, current, total, width=80):
        width = 80
        mb = 1024 ** 2
        total_mb = total / mb
        current_mb = current / mb
        percent = current / total * 100
        bar = "=" * int(percent * width / 100) + (width - int(percent * width / 100)) * " "

        progress_message = f"Downloading: {self._sub_file_name:75}:" \
                           f" [{bar}] {percent:.2f}% [{current_mb:.2f}MB/{total_mb:.2f}MB]" \
                           f" [{self._finish_pkg_num}/{self._total_pkg_num}]"

        sys.stdout.write("\r" + progress_message)
        sys.stdout.flush()
        if current == total:
            sys.stdout.flush()
            print("\r")

    def download(self):
        if not os.path.exists(self._dest_dir):
            os.makedirs(self._dest_dir)
        requests_url_list = self._get_torch_url_list(self._torch_mirror_pkg)
        self._total_pkg_num = len(requests_url_list)
        print(f"Downloading package from {self._torch_mirror_pkg}")
        for index, torch_pkg_url in enumerate(requests_url_list):
            self._finish_pkg_num = index + 1
            # torch 包的文件名
            file_name = self._get_torch_pkg_name_from_url(torch_pkg_url)
            # 子文件夹路径
            sub_folder = self._get_sub_folder_name_from_url(torch_pkg_url)

            if not os.path.exists(os.path.join(self._dest_dir, sub_folder)):
                os.makedirs(os.path.join(self._dest_dir, sub_folder))
            # 生成子文件夹
            out_file_path = os.path.join(self._dest_dir, sub_folder, file_name)
            self._sub_file_name = os.path.join(sub_folder, file_name)
            # 特殊字符处理，例如%2B处理为+
            # 将下载连接变成url的格式
            # 将文件路径中特殊字符转换
            torch_pkg_url = parse.unquote(torch_pkg_url)
            out_file_path = parse.unquote(out_file_path)
            if not os.path.exists(out_file_path):
                download(torch_pkg_url, out_file_path, bar=self._progress)
                pass
            else:
                print(f"{self._sub_file_name:75} File Exists")
                pass
            pass
        pass


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-m", "--mirror", default="stable")
    args = parser.parse_args()

    mirror_type = args.mirror

    if mirror_type == "lts":
        mirror = TorchMirror(
            "lts/1.8",
            torch_mirror="https://download.pytorch.org/whl/lts/1.8/torch_lts.html",
            torch_prefix="https://download.pytorch.org/whl/lts/1.8/",
            tmp_file_name="torch_lts.txt"
        )
    elif mirror_type == "stable":
        mirror = TorchMirror(
            "packages",
            torch_mirror="https://download.pytorch.org/whl/torch_stable.html",
            torch_prefix="https://download.pytorch.org/whl/",
            tmp_file_name="torch_stable.txt"
        )
    else:
        mirror = None
    if mirror:
        mirror.download()
    pass
