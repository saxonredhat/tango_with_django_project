# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def str_contain_chinese(str):
    for s in unicode(str):
        if s >= u'\u4e00' and s <= u'\u9fa5':
            return True
    return False