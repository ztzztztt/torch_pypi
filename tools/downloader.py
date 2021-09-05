#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  : zhoutao
@License : (C) Copyright 2013-2021, China University of Petroleum
@Contact : zhoutao@s.upc.edu.cn
@Software: PyCharm
@File    : downloader
@Time    : 2021/08/31 11:07
@Desc    : 自定义的多线程下载器
"""
from __future__ import annotations
import os
import requests
from tqdm import tqdm
from retry import retry
from typing import Union
import concurrent.futures as cf


# 请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 '
                  'Safari/537.36 QIHU 360SE '
}
MB = 1024 ** 2


def split(start: int, end: int, step: int) -> list:
    # 分块下载
    parts = [(item_start, min(item_start + step, end)) for item_start in range(start, end, step)]
    return parts
    pass


def get_file_size(url: str) -> Union[int, None]:
    response = requests.head(url)
    file_size = response.headers.get("Content-Length")
    if file_size is None:
        return file_size
    else:
        return int(file_size)
    pass


def download(url: str, file_name: str, retry_times: int = 3, each_size: int = 16 * MB, override: bool = False):
    """
    文件下载
    :param url: 文件下载的地址
    :param file_name: 文件下载保存的文件名
    :param retry_times: 出现错误重试次数，默认为重试3次
    :param each_size: 分块下载的块大小，默认为 16MB
    :param override: 如果文件存在，是否覆盖下载， 默认为False
    :return:
    """
    if os.path.exists(file_name):
        if override:
            os.remove(file_name)
        else:
            print(f"{file_name} File exists, please check 'override=True' to override it !!!")
            return

    file_size = get_file_size(url)
    f = open(file_name, "wb")
    # f.truncate(file_size)
    chunk_list = []

    @retry(tries=retry_times)
    def start_download(start: int, end: int):
        """
        根据文件的起始结束位置下载文件
        :param start: 开始位置
        :param end: 结束位置
        :return:
        """
        _headers = headers.copy()
        # 指定请求头中分段下载的字段
        _headers["Range"] = f"bytes={start}-{end}"
        response = session.get(url, headers=_headers, stream=True)
        chunks = []
        chunk_size = 128
        for chunk in response.iter_content(chunk_size=chunk_size):
            chunks.append(chunk)
            if len(chunk) == chunk_size:
                bar.update(chunk_size)
            else:
                bar.update(len(chunk))
        chunk_list.append(chunks)
        # 循环写入磁盘
        f.seek(start)
        for chunk in chunks:
            f.write(chunk)
        # 释放写入磁盘的资源
        del chunks
        pass

    session = requests.Session()
    # 设置每块的大小
    each_size = min(each_size, file_size)
    # 分块
    parts = split(0, file_size, each_size)
    with tqdm(total=file_size, desc=f'Downloading: {file_name}', unit="B", unit_scale=True, unit_divisor=1024) as bar:
        # 线程池
        futures = []
        with cf.ThreadPoolExecutor() as p:
            for (start, end) in parts:
                if end == file_size:
                    end = file_size - 1
                futures.append(p.submit(start_download, start, end))
                pass
        cf.wait(futures)
    session.close()
    f.close()
    return True
    pass


if __name__ == '__main__':
    # url = 'https://issuecdn.baidupcs.com/issue/netdisk/yunguanjia/BaiduNetdisk_7.2.8.9.exe'
    # file_name = 'BaiduNetDisk_7.2.8.9.exe'
    # download(url, file_name)

    # url2 = 'https://media.w3.org/2010/05/sintel/trailer.mp4'
    # file_name2 = 'trailer(1).mp4'
    # # # 开始下载文件
    # download(url2, file_name2)

    url2 = 'https://download.pytorch.org/whl/cpu/torchvision-0.8.2%2Bcpu-cp39-cp39-win_amd64.whl'
    file_name2 = 'torch/torchvision-0.8.2%2Bcpu-cp39-cp39-win_amd64.whl'
    # # 开始下载文件
    download(url2, file_name2)

    # url2 = 'https://download.pytorch.org/whl/cpu/torch-1.8.0%2Bcpu-cp39-cp39-win_amd64.whl'
    # file_name2 = 'torch/torch-1.8.0%2Bcpu-cp39-cp39-win_amd64.bak.whl'
    # # # 开始下载文件
    # download(url2, file_name2, override=True)
    # lists = [(url, file_name), (url2, file_name2)]
    # for item_url, item_name in lists:
    #     download(item_url, item_name)
