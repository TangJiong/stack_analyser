# -*- coding:utf-8 -*-

__author__ = 'tangjiong'

import re


def parse_int(str_with_num):
    """从字符串中提取数字"""
    if str is None:
        return 0
    str_nums = re.findall(r"\d+", str_with_num)
    if len(str_nums) > 0:
        return int(str_nums[0])
    return 0



