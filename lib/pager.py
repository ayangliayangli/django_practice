#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
@version:
@author: leo Yang
@license: none
@contact: yangliw3@foxmail.com
@site:
@software:PyCharm
@file:pager.py
@time(UTC+8):16/10/25-20:35
'''


def get_pager(item_total, item_per_page=10, cur_page=1, cur_page_start=1, cur_page_step=5):
    '''

    :param item_total:       总共有多少项需要显示的
    :param item_per_page:    每页显示多少项, 默认 10
    :param cur_page:         当前页号, 默认1
    :param cur_page_start:   在尾部,当前开始的页号
    :param cur_page_step:    显示多少页
    :return:
    '''

    ret_data_dict = {"start":None, "end":None, "cur_page":None, "cur_page_start":None,
                     "cur_page_stop":None}

    page_total, last_page_item_count = divmod(item_total, item_per_page)
    if last_page_item_count:
        page_total += 1

    # 修正当前选中的页面
    if cur_page < 1:
        cur_page = 1
    if cur_page > page_total:
        cur_page = page_total

    start = (cur_page - 1) * item_per_page
    end = cur_page * item_per_page
    if last_page_item_count and cur_page == page_total:
        # 当最后一页没有充满整个页面,且当前页面就是最后一页的时候
        end = start + last_page_item_count + 1

    if cur_page < cur_page_start:
        # 向前挪一个窗口 cur_page_step
        cur_page_start -= cur_page_step

    if cur_page > cur_page_start + cur_page_step - 1:
        # 向后移动一个窗口 cur_page_step
        cur_page_start += cur_page_step

    # 调整显示起始页面
    if cur_page_start < 1:
        cur_page_start = 1

    cur_page_stop = cur_page_start + cur_page_step - 1

    # 调整显示结束页面
    if cur_page_stop > page_total:
        cur_page_stop = page_total

    cur_page_range = range(cur_page_start, cur_page_stop + 1)
    pre_page = cur_page_start - 1
    post_page = cur_page_stop + 1
    # 修正上一页,下一页
    if pre_page < 1:
        pre_page = None
    if post_page > page_total:
        post_page = None

    ret_data_dict["start"] = start  # 切片开始
    ret_data_dict["end"] = end  # 切片借宿
    ret_data_dict["cur_page"] = cur_page  # 当前页面
    ret_data_dict["cur_page_start"] = cur_page_start  # 显示页开始
    ret_data_dict["cur_page_stop"] = cur_page_stop  # 显示页结束
    ret_data_dict["page_total"] = page_total  # 总页数
    ret_data_dict["cur_page_range"] = cur_page_range  # 当前显示页范围
    ret_data_dict["pre_page"] = pre_page  # 上一页
    ret_data_dict["post_page"] = post_page  # 下一页

    # handle special env which data is null
    if page_total == 0:
        ret_data_dict["cur_page_range"] = None
        ret_data_dict["start"] = 0

    return ret_data_dict


if __name__ == '__main__':
    print(get_pager(88,item_per_page=10, cur_page=3, cur_page_start=5, cur_page_step=5))