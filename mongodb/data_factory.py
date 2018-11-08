# -*- coding: UTF-8 -*-
'''
@project:mongodb
@author:wangfy
@time:2018/11/8 14:14
'''

class Datafactory:

    @staticmethod
    def create_tags(num):
        tags_list = []
        for i in range(num):
            tags_one = {'Id': i, 'TagName': 'Java', 'Count': 10000, 'ExcerptPostId': 3673183, 'WikiPostId': 3673182}
            tags_list.append(tags_one)
        return tags_list


    def create_tags_from_start(num_start,count):
        tags_list = []
        for i in range(num_start, num_start+count+1):
            tags_one = {'Id': i, 'TagName': 'Java', 'Count': 10000, 'ExcerptPostId': 3673183, 'WikiPostId': 3673182}
            tags_list.append(tags_one)
        return tags_list


