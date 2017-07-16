#!/usr/bin/env python
# -*- coding:utf-8 -*-
from backend.form import fields


class BaseForm:

    def __init__(self):
        self._value_dict = {}
        self._error_dict = {}
        self._valid_status = True

    def valid(self, handler):

        for field_name, field_obj in self.__dict__.items():    #将表单循环一遍，filed_name表单form中的fieled，field_obj为filed类的obj，handler为homehandler对象
            if field_name.startswith('_'):
                continue

            if type(field_obj) == fields.CheckBoxField:
                post_value = handler.get_arguments(field_name, None)  #获取表单中的filed值
            elif type(field_obj) == fields.FileField:
                post_value = []
                file_list = handler.request.files.get(field_name, [])
                for file_item in file_list:
                    post_value.append(file_item['filename'])
            else:
                post_value = handler.get_argument(field_name, None)

            field_obj.match(field_name, post_value)    #通过field类的match方法将post值与正则表达式匹配
            if field_obj.is_valid:     #经过匹配，得出is_valid值，将值放进dict
                self._value_dict[field_name] = field_obj.value
            else:     #未匹配成功
                self._error_dict[field_name] = field_obj.error
                self._valid_status = False
        return self._valid_status